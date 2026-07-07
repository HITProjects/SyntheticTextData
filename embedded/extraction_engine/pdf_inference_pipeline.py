
"""
pdf_inference_pipeline.py  (v3 — all fixes applied)
=====================================================

Pipeline מלא:
    PDF → HTML גולמי → סינון עמודים → ניקוי טקסט → Preprocessor → Aligner → מודל → JSON

תיקונים בגרסה זו (על בסיס ביקורת על IRF740A / 91051):
  תיקון 1 — סינון עמודים: רק עמודים עם טבלאות חשמליות עוברים לשלבים הבאים
  תיקון 2 — הרחבת ELECTRICAL_HEADER_KEYWORDS: זיהוי THERMAL ו-SYMBOL
  תיקון 3 — הסרת טקסט הפוך מגרפים: "ecruo", "S-ot-niar" וכד'
  תיקון 4 — הסרת עמודי disclaimer משפטי אוטומטית
  תיקון 5 — Aligner עם tables_only=True: רק טוקנים מטבלאות
  תיקון 6 — סינון פרמטרים לא-תקינים מהפלט הסופי
"""

from __future__ import annotations

import json
import logging
import re
import shutil
import sys
import html as html_module
import traceback
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from bs4 import BeautifulSoup, Tag

logging.basicConfig(
    format="%(asctime)s | %(levelname)-8s | %(message)s",
    datefmt="%H:%M:%S",
    level=logging.INFO,
)
log = logging.getLogger(__name__)


# =============================================================================
# נתיבים — שנה כאן בלבד
# =============================================================================

BASE        = r"C:\Users\nivsa\Generation of Synthetic Training Data\embedded"
INPUT_DIR   = Path(BASE) / "example_datasheets"
OUTPUT_DIR  = Path(BASE) / "output_results"
ALIGNER_DIR = Path(BASE) / "extraction_engine"
MODEL_PATH  = Path(BASE) / "models" / "checkpoints"

# "auto" | "trained" | "base" | "dummy"
NER_MODE = "auto"


# =============================================================================
# שלב 1 — PDF → HTML גולמי  (pdfplumber)
# =============================================================================

class PDFConverter:
    """ממיר PDF ל-HTML עם <table> מדויק לכל טבלה בעמוד."""

    _TABLE_SETTINGS = {
        "vertical_strategy":   "lines",
        "horizontal_strategy": "lines",
        "snap_tolerance":      5,
        "join_tolerance":      3,
        "edge_min_length":     10,
    }
    _TABLE_SETTINGS_FALLBACK = {
        "vertical_strategy":   "text",
        "horizontal_strategy": "text",
        "snap_tolerance":      3,
    }

    def convert(self, pdf_path: Path) -> str:
        try:
            import pdfplumber
        except ImportError:
            raise ImportError("pip install pdfplumber")

        html_parts = [
            "<!DOCTYPE html>",
            "<html><head><meta charset='UTF-8'></head><body>",
        ]

        with pdfplumber.open(str(pdf_path)) as pdf:
            for page_num, page in enumerate(pdf.pages, start=1):
                html_parts.append(f"<div class='page' data-page='{page_num}'>")

                table_objs = page.find_tables(self._TABLE_SETTINGS)
                if not table_objs:
                    table_objs = page.find_tables(self._TABLE_SETTINGS_FALLBACK)

                table_bboxes = [t.bbox for t in table_objs]

                for tbl in table_objs:
                    data = tbl.extract()
                    if not data:
                        continue
                    html_parts.append("<table>")
                    for row_idx, row in enumerate(data):
                        tag = "th" if row_idx == 0 else "td"
                        html_parts.append("<tr>")
                        for cell in row:
                            html_parts.append(f"<{tag}>{self._clean(cell)}</{tag}>")
                        html_parts.append("</tr>")
                    html_parts.append("</table>")

                words = page.extract_words(x_tolerance=3, y_tolerance=3)
                non_tbl_words = [
                    w for w in words if not self._in_any_bbox(w, table_bboxes)
                ]
                if non_tbl_words:
                    for line in self._group_lines(non_tbl_words):
                        text = " ".join(self._clean(w["text"]) for w in line)
                        if text.strip():
                            html_parts.append(f"<p>{text}</p>")

                html_parts.append("</div>")

        html_parts.append("</body></html>")
        return "\n".join(html_parts)

    @staticmethod
    def _clean(text: Optional[str]) -> str:
        if text is None:
            return ""
        return html_module.escape(" ".join(str(text).split()))

    @staticmethod
    def _in_any_bbox(word: dict, bboxes: list) -> bool:
        cx = (word["x0"] + word["x1"]) / 2
        cy = (word["top"] + word["bottom"]) / 2
        return any(x0 <= cx <= x1 and top <= cy <= bot
                   for x0, top, x1, bot in bboxes)

    @staticmethod
    def _group_lines(words: list, y_tol: float = 5) -> list:
        if not words:
            return []
        words = sorted(words, key=lambda w: (w["top"], w["x0"]))
        lines, cur_line, cur_y = [], [words[0]], words[0]["top"]
        for w in words[1:]:
            if abs(w["top"] - cur_y) <= y_tol:
                cur_line.append(w)
            else:
                lines.append(sorted(cur_line, key=lambda x: x["x0"]))
                cur_line, cur_y = [w], w["top"]
        if cur_line:
            lines.append(sorted(cur_line, key=lambda x: x["x0"]))
        return lines


# =============================================================================
# תיקון 1 — סינון עמודים: רק עמודים עם טבלאות חשמליות
# תיקון 4 — הסרת עמודי disclaimer משפטי
# תיקון 3 — הסרת טקסט הפוך מגרפים
# =============================================================================

# מילות מפתח המעידות שעמוד מכיל טבלת מפרטים
# B1: removed generic "voltage","current","resistance" — appear on any page and cause FP
_ELECTRICAL_PAGE_SIGNALS = {
    "min", "max", "typ", "unit", "units",
    "min.", "max.", "typ.",
    "parameter", "symbol",
    "specifications", "electrical", "thermal",
    "absolute maximum", "absolute max",
    "static", "dynamic",
    "drain", "gate", "source",
}

# ביטויים המעידים שעמוד הוא disclaimer משפטי — תיקון 4
_LEGAL_SIGNALS = [
    "legal disclaimer",
    "all product, product specifications",
    "subject to change without notice",
    "not designed for use in life-saving",
    "all rights reserved",
    "without limitation special",
    "warranties of fitness",
]

# רגקס לזיהוי מילה הפוכה: 4+ תווים אלפביתיים שנקראים כמילה אנגלית הפוכה — תיקון 3
# הקריטריון: המילה מכילה רק אותיות, אין בה ספרות, ואינה מילה אנגלית נפוצה
_ROTATED_WORD_RE = re.compile(r"^[a-z]{4,}$")

# מילים אנגליות נפוצות שלא נסנן אותן (False Positive guard)
_COMMON_WORDS = {
    "that", "this", "with", "from", "have", "been", "will", "they",
    "their", "when", "also", "more", "over", "than", "then", "some",
    "each", "such", "into", "only", "most", "both", "time", "very",
    "much", "well", "even", "back", "just", "data", "case", "gate",
    "test", "note", "peak", "rise", "fall", "turn", "body", "open",
    "area", "safe", "flat",
}

# B5: electrical measurement words for catalog/key-value table format detection
_ELEC_MEAS_WORDS = {
    "voltage", "current", "resistance", "capacitance", "inductance",
    "temperature", "power", "frequency", "impedance", "dissipation",
    "coefficient", "tolerance", "rating", "leakage",
}

# B10: ABS MAX table detection — matches section-title strings, not column headers
_ABS_MAX_RE = re.compile(
    r'absolute\s+max(?:imum)?\s*rating|maximum\s+ratings?\b|stresses\s+(?:above|beyond)',
    re.IGNORECASE
)


def _is_abs_max_table(table: Tag) -> bool:
    """
    B10: Returns True if this table is an Absolute Maximum Ratings table.

    Strategy: only flag single-cell rows (section-title / colspan super-headers),
    not multi-column header rows that happen to contain 'Maximum Rating' as a
    column label.  This mirrors the existing colspan rendering logic in _TableCleaner.

    Also checks the immediately preceding non-empty sibling element, which is where
    pdfplumber places section titles that sit above a table as free text.
    """
    rows = table.find_all("tr")
    for row in rows[:3]:
        cells = row.find_all(["th", "td"])
        if not cells:
            continue
        # Match only single-cell (colspan) rows — section title pattern
        if len(cells) == 1 or all(c.get_text(strip=True) == "" for c in cells[1:]):
            txt = cells[0].get_text(" ", strip=True)
            if _ABS_MAX_RE.search(txt):
                return True

    # Check the immediately preceding non-empty sibling (free-text section title)
    for sib in table.previous_siblings:
        if hasattr(sib, "get_text"):
            txt = sib.get_text(" ", strip=True)
        elif isinstance(sib, str):
            txt = sib.strip()
        else:
            continue
        if not txt:
            continue
        if _ABS_MAX_RE.search(txt):
            return True
        break  # stop at first non-empty sibling

    return False


def _is_legal_page(page_div: Tag) -> bool:
    """
    תיקון 4: מזהה עמוד disclaimer משפטי לפי צבירת ביטויים אופייניים.
    דורש לפחות 2 ביטויים — מניעת False Positives.
    """
    text  = page_div.get_text().lower()
    count = sum(1 for sig in _LEGAL_SIGNALS if sig in text)
    return count >= 2


def _has_electrical_content(page_div: Tag) -> bool:
    """
    תיקון 1 / B1: בודק אם עמוד מכיל לפחות טבלה אחת עם כותרות חשמליות.

    B1 fix: checks only the first 3 rows (headers) of each table, not the
    entire table text — prevents ToC, application notes, and feature lists
    from passing because they contain words like "voltage" or "current"
    somewhere in data cells.

    Requires BOTH a value column (min/max/typ/unit) AND a parameter column
    (parameter/characteristic/symbol) to be present in the header.
    """
    _value_signals  = {"min", "max", "typ", "typical", "unit", "units", "value", "nom", "nominal"}
    _param_signals  = {"parameter", "param", "characteristic", "characteristics",
                       "symbol", "description", "item", "specification"}

    for table in page_div.find_all("table"):
        rows = table.find_all("tr")
        for hdr_row in rows[:3]:
            cells = [c.get_text(strip=True).lower() for c in hdr_row.find_all(["th", "td"])]
            cell_text = " ".join(cells)
            # Require both a param-type column and a value-type column in the same header row
            has_value = any(sig in cell_text for sig in _value_signals)
            has_param = any(sig in cell_text for sig in _param_signals)
            if has_value and has_param:
                return True
            # Also accept if ANY cell exactly equals one of the strong signals
            if any(c in {"min", "max", "typ", "unit", "parameter", "symbol"} for c in cells):
                strong_count = sum(1 for c in cells
                                   if c in {"min", "max", "typ", "unit", "parameter", "symbol",
                                            "typical", "minimum", "maximum"})
                if strong_count >= 2:
                    return True

        # B5: Catalog table — ≥2 column headers contain electrical measurement words
        if rows:
            hdr_cells = [c.get_text(strip=True).lower() for c in rows[0].find_all(["th", "td"])]
            elec_hdr_count = sum(1 for h in hdr_cells if any(w in h for w in _ELEC_MEAS_WORDS))
            if elec_hdr_count >= 2:
                return True

        # B5: Key-value table — ≥2 data rows have electrical word in col[0] AND digit in col[1]
        if len(rows) >= 3:
            kv_signals = 0
            for kv_row in rows[1:6]:
                kv_cells = kv_row.find_all(["td", "th"])
                if len(kv_cells) >= 2:
                    c0 = kv_cells[0].get_text(strip=True).lower()
                    c1 = kv_cells[1].get_text(strip=True)
                    if any(w in c0 for w in _ELEC_MEAS_WORDS) and re.search(r'\d', c1):
                        kv_signals += 1
            if kv_signals >= 2:
                return True

    return False


def _is_rotated_word(word: str) -> bool:
    """
    תיקון 3: מזהה מילה בודדת כטקסט הפוך מגרף.
    קריטריונים: 4+ אותיות, לא מילה נפוצה, ולא מכילה ספרות.
    """
    w = word.lower().strip()
    if not _ROTATED_WORD_RE.match(w):
        return False
    if w in _COMMON_WORDS:
        return False
    return True


def _remove_rotated_text_from_page(page_div: Tag) -> None:
    """
    תיקון 3: מסיר פסקאות <p> שמרביתן מילים הפוכות מגרפים.
    קריטריון: >40% מהמילים בפסקה נראות כמילים הפוכות.
    """
    for p_tag in page_div.find_all("p"):
        text  = p_tag.get_text()
        words = [w for w in text.split() if len(w) >= 2]
        if not words:
            continue
        rotated_count = sum(1 for w in words if _is_rotated_word(w))
        ratio = rotated_count / len(words)
        if ratio > 0.4:
            p_tag.decompose()


def filter_html_pages(raw_html: str) -> Tuple[str, Dict]:
    """
    תיקון 1 + 3 + 4: מקבל HTML גולמי מ-pdfplumber ומחזיר HTML מסונן.

    מה שמוסר:
      - עמודי disclaimer משפטי (תיקון 4)
      - עמודים ללא תוכן חשמלי (תיקון 1)
      - פסקאות של טקסט הפוך מגרפים (תיקון 3)

    מחזיר (filtered_html, stats_dict).
    """
    soup  = BeautifulSoup(raw_html, "html.parser")
    pages = soup.find_all("div", class_="page")

    stats = {
        "total_pages":    len(pages),
        "legal_removed":  0,
        "no_elec_removed": 0,
        "kept_pages":     0,
        "rotated_paras_removed": 0,
    }

    kept_pages: List[Tag] = []

    for page in pages:
        # תיקון 4: הסר עמודי disclaimer
        if _is_legal_page(page):
            stats["legal_removed"] += 1
            log.debug(f"  דילוג עמוד {page.get('data-page','?')} — disclaimer משפטי")
            continue

        # תיקון 1: הסר עמודים ללא תוכן חשמלי
        if not _has_electrical_content(page):
            stats["no_elec_removed"] += 1
            log.debug(f"  דילוג עמוד {page.get('data-page','?')} — אין תוכן חשמלי")
            continue

        # תיקון 3: הסר פסקאות טקסט הפוך בתוך העמוד שנשמר
        paras_before = len(page.find_all("p"))
        _remove_rotated_text_from_page(page)
        paras_after  = len(page.find_all("p"))
        stats["rotated_paras_removed"] += paras_before - paras_after

        kept_pages.append(page)
        stats["kept_pages"] += 1

    if not kept_pages:
        log.warning("לא נשמר אף עמוד אחרי הסינון — מחזיר HTML מקורי")
        return raw_html, stats

    filtered_html = (
        "<!DOCTYPE html>\n"
        "<html><head><meta charset='UTF-8'></head><body>\n"
        + "\n".join(str(p) for p in kept_pages)
        + "\n</body></html>"
    )
    return filtered_html, stats


# =============================================================================
# תיקון 2 — Preprocessor עם ELECTRICAL_HEADER_KEYWORDS מורחב
# =============================================================================

# תיקון 2: הוסף "symbol", "sym", "thermal", "parameter", "param"
# כדי שטבלת THERMAL RESISTANCE תזוהה נכון
ELECTRICAL_HEADER_KEYWORDS = {
    # קיים
    "min", "max", "typ", "typical", "minimum", "maximum",
    "nom", "nominal", "unit", "units",
    "min.", "max.", "typ.", "nom.",
    "value", "rating", "limit",
    # תיקון 2 — חדש:
    "symbol", "sym", "sym.",
    "parameter", "param",
    "thermal",
    "testconditions", "conditions", "condition",
    "spec", "specs",
}

HEADER_ROLE_MAP: Dict[str, str] = {
    "parameter":      "PARAMETER",
    "param":          "PARAMETER",
    "testconditions": "CONDITION",
    "testcon":        "CONDITION",
    "conditions":     "CONDITION",
    "condition":      "CONDITION",
    "notes":          "CONDITION",
    "min":            "MIN",      "minimum":  "MIN",
    "max":            "MAX",      "maximum":  "MAX",
    "typ":            "TYP",      "typical":  "TYP",
    "nom":            "TYP",      "nominal":  "TYP",
    "value":          "MAX",      "rating":   "MAX",   "limit": "MAX",
    "unit":           "UNIT",     "units":    "UNIT",  "uom":   "UNIT",
    # תיקון 2 — חדש:
    "symbol":         "SYMBOL",   "sym":      "SYMBOL", "sym.": "SYMBOL",
}

_CID_RE      = re.compile(r"\(cid:\d+\)", re.IGNORECASE)
_SIGNED_NUM  = re.compile(
    r"[+-]?(?:\d+\.?\d*|\.\d+)(?:[eE][+-]?\d+)?(?:\s*%)?|±\s*(?:\d+\.?\d*|\.\d+)"
)
_SUB_TAIL_RE = re.compile(
    r"\b([A-Z]{1,3})\s*([=<>]+|[≤≥]+)\s*([^\s,;]+)\s+([A-Z]{1,3})\b"
)
# Fix 2: שורות הערות/footnotes בתוך טבלאות (Note 1, (1), †, ‡)
_NOTE_ROW_RE = re.compile(
    r'^\s*(?:notes?[\s:*\d]|\(\s*\d+\s*\)|†|‡|\*\s)',
    re.IGNORECASE
)


def _pp_clean(text: str) -> str:
    text = _CID_RE.sub("", text).replace("\u2581", " ")
    # B2: normalize Unicode minus/dash variants to ASCII minus so _SIGNED_NUM captures them
    text = text.replace("\u2212", "-").replace("\u2013", "-")  # \u2212 and \u2013
    return re.sub(r"[ \t]+", " ", text).strip()

_RUNON_KNOWN_WORDS = {
    "supply", "voltage", "current", "power", "input", "output", "offset",
    "bias", "noise", "gain", "bandwidth", "common", "mode", "rejection",
    "ratio", "slew", "rate", "quiescent", "thermal", "resistance", "drain",
    "gate", "source", "base", "collector", "emitter", "forward", "reverse",
    "breakdown", "saturation", "cutoff", "leakage", "storage", "junction",
    "ambient", "case", "dissipation", "frequency", "response", "settling",
    "time", "delay", "rise", "fall", "turn", "short", "circuit", "open",
    "loop", "closed", "unity", "phase", "margin", "ripple", "regulation",
    "dropout", "inhibit", "enable", "adjust", "reference", "sense",
    # B1 additions:
    "duration", "consumption", "characteristic", "characteristics",
    "range", "swing", "transient", "average", "drift", "temperature",
    "operating", "junction", "differential", "large", "signal",
    "continuous", "pulsed", "peak", "recovery", "propagation",
}

def _split_runon_token(token: str) -> str:
    """Split a single all-lowercase runon token into known words (greedy left-to-right)."""
    lower = token.lower()
    if re.search(r"[^a-z]", lower):
        return token  # contains digits/symbols — don't mangle
    result_parts, pos = [], 0
    while pos < len(lower):
        matched = False
        for wlen in range(min(15, len(lower) - pos), 2, -1):
            candidate = lower[pos:pos + wlen]
            if candidate in _RUNON_KNOWN_WORDS:
                result_parts.append(token[pos:pos + wlen])
                pos += wlen
                matched = True
                break
        if not matched:
            if result_parts:
                result_parts[-1] += token[pos]
            else:
                result_parts.append(token[pos])
            pos += 1
    rejoined = " ".join(result_parts).strip()
    return rejoined if rejoined != token else token


def _split_runon(text: str) -> str:
    """B1: split CamelCase and all-lowercase concatenated parameter names.
    Also handles hyphen-separated runon words like 'Common-moderejectionratio'.
    """
    if not text:
        return text
    # CamelCase split
    spaced = re.sub(r"([a-z])([A-Z])", r"\1 \2", text)
    if spaced != text:
        return spaced.strip()
    # If text has spaces, apply per-token runon splitting
    if " " in text:
        parts = text.split()
        split_parts = []
        for p in parts:
            # Handle hyphen-joined tokens by splitting on hyphens first
            sub = re.split(r"[-]", p)
            split_sub = [_split_runon_token(s) for s in sub]
            split_parts.append("-".join(split_sub))
        return " ".join(split_parts)
    # Single token without spaces — try runon split directly
    # Handle hyphen as word boundary
    sub = re.split(r"[-]", text)
    split_sub = [_split_runon_token(s) for s in sub]
    result = " ".join(split_sub).replace("  ", " ").strip()
    return result if result != text else text

# =============================================================================
# B5 — Generic table format detection + parsing
# =============================================================================

_KV_UNIT_RE = re.compile(
    r'\d\s*([µμuμmkMGnpf]?(?:F\b|H\b|Ω|ohm\b|V\b|A\b|W\b|Hz\b|°C|˚C|%|ppm\b))',
    re.IGNORECASE,
)
_HDR_UNIT_RE = re.compile(r'\(([^)]{1,25})\)\s*$')
_STD_ELEC_KEYWORDS = frozenset({
    "min", "max", "typ", "typical", "minimum", "maximum", "unit", "units",
})


def _extract_unit_from_value_str(text: str) -> Optional[str]:
    """Extract unit from value strings like '6.3 to 50V' or '–40 to +105˚C'."""
    m = _KV_UNIT_RE.search(text)
    return m.group(1).strip() if m else None


def _extract_unit_from_header(header: str) -> Optional[str]:
    """Extract unit from parenthesized suffix in column headers like 'Power Rating (watts)'."""
    m = _HDR_UNIT_RE.search(header)
    return m.group(1).strip() if m else None


def _is_key_value_table(rows: list) -> bool:
    """Detect 2-column key-value tables: col[0]=param name, col[1]=value, cols 2+≈empty.

    Pattern is common in capacitor/component specification sheets that list
    a single overall spec per line rather than min/typ/max columns.
    """
    if len(rows) < 3:
        return False
    # Standard electrical tables (which have min/max/typ headers) are handled elsewhere
    hdr_cells = [c.get_text(strip=True).lower() for c in rows[0].find_all(["th", "td"])]
    if any(h in _STD_ELEC_KEYWORDS for h in hdr_cells):
        return False
    # Count rows matching key-value structure: non-empty col[0]+col[1], rest empty
    total = kv_count = 0
    for row in rows[1:11]:
        cells = row.find_all(["td", "th"])
        if len(cells) < 2:
            continue
        c0 = cells[0].get_text(strip=True)
        c1 = cells[1].get_text(strip=True)
        total += 1
        if c0 and c1:
            rest_empty = len(cells) <= 2 or all(
                not cells[i].get_text(strip=True) for i in range(2, len(cells))
            )
            if rest_empty:
                kv_count += 1
    if total < 2 or kv_count / total < 0.5:
        return False
    # Confirm col[0] contains electrical parameter names
    all_col0 = " ".join(
        row.find_all(["td", "th"])[0].get_text(strip=True).lower()
        for row in rows[1:11]
        if row.find_all(["td", "th"])
    )
    return any(w in all_col0 for w in _ELEC_MEAS_WORDS)


def _parse_key_value_table(rows: list) -> List[Dict]:
    """Parse key-value format table into parameter dicts."""
    params: List[Dict] = []
    for row in rows[1:]:
        cells = row.find_all(["td", "th"])
        if len(cells) < 2:
            continue
        param = _pp_clean(cells[0].get_text(strip=True))
        value_raw = _pp_clean(cells[1].get_text(strip=True))
        if not param or not value_raw:
            continue
        param = _split_runon(param)
        unit = _extract_unit_from_value_str(value_raw)
        nums = _split_vals(value_raw)
        if len(nums) == 0:
            min_v, typ_v, max_v = None, value_raw, None
        elif len(nums) == 1:
            min_v, typ_v, max_v = None, nums[0], None
        elif len(nums) == 2:
            min_v, typ_v, max_v = nums[0], None, nums[1]
        else:
            min_v, typ_v, max_v = nums[0], nums[1], nums[-1]
        params.append({
            "parameter": param,
            "min":       min_v,
            "typ":       typ_v,
            "max":       max_v,
            "unit":      unit,
            "condition": None,
        })
    return params


def _is_catalog_table(rows: list) -> bool:
    """Detect catalog-format tables: rows=device variants, columns=electrical specs.

    Criteria: first row has ≥3 non-empty headers, ≥2 of which contain electrical
    measurement words, and none of the standard min/max/typ/unit keywords are present
    (those are handled by the standard parser).
    """
    if len(rows) < 3:
        return False
    hdr_cells = [c.get_text(strip=True) for c in rows[0].find_all(["th", "td"])]
    non_empty = [h for h in hdr_cells if h]
    if len(non_empty) < 3:
        return False
    hdr_lower = [h.lower() for h in hdr_cells]
    if any(h in _STD_ELEC_KEYWORDS for h in hdr_lower):
        return False
    elec_count = sum(1 for h in hdr_lower if any(w in h for w in _ELEC_MEAS_WORDS))
    return elec_count >= 2


def _parse_catalog_table(rows: list) -> List[Dict]:
    """Parse catalog-format table into parameter dicts.

    One parameter per electrical spec column; range derived from all data-row values.
    """
    if not rows:
        return []
    # Find first row with ≥3 non-empty cells as the header row
    hdr_idx = 0
    headers: List[str] = []
    for i, row in enumerate(rows[:3]):
        cells = [c.get_text(strip=True) for c in row.find_all(["th", "td"])]
        if sum(1 for c in cells if c) >= 3:
            headers = cells
            hdr_idx = i
            break
    if not headers:
        return []

    # Data rows = rows after header where col[0] is non-empty (skip sub-headers)
    data_rows = []
    for row in rows[hdr_idx + 1:]:
        cells = row.find_all(["td", "th"])
        if cells and cells[0].get_text(strip=True):
            data_rows.append(row)
    if not data_rows:
        return []

    elec_cols = [
        (i, h) for i, h in enumerate(headers)
        if h and any(w in h.lower() for w in _ELEC_MEAS_WORDS)
    ]
    if not elec_cols:
        return []

    params: List[Dict] = []
    for col_idx, col_header in elec_cols:
        col_values = []
        for row in data_rows:
            cells = row.find_all(["td", "th"])
            if col_idx < len(cells):
                v = _pp_clean(cells[col_idx].get_text(strip=True))
                if v:
                    col_values.append(v)
        if not col_values:
            continue

        # Collect all numeric tokens from this column's values
        all_nums: List[str] = []
        for v in col_values:
            all_nums.extend(
                n for n in _split_vals(v)
                if re.match(r'^[+-]?\d+\.?\d*$', n)
            )
        try:
            float_vals = sorted(set(float(n) for n in all_nums))
        except (ValueError, TypeError):
            float_vals = []

        unit = _extract_unit_from_header(col_header)
        # Remove parenthetical unit from the parameter name
        param_name = re.sub(r'\s*\([^)]+\)\s*$', '', col_header).strip()
        param_name = _split_runon(_pp_clean(param_name))

        if float_vals:
            if len(float_vals) == 1:
                min_v, typ_v, max_v = None, str(float_vals[0]), None
            else:
                min_v = str(float_vals[0])
                max_v = str(float_vals[-1])
                typ_v = None
        else:
            min_v, typ_v, max_v = None, col_values[0], None

        params.append({
            "parameter": param_name,
            "min":       min_v,
            "typ":       typ_v,
            "max":       max_v,
            "unit":      unit,
            "condition": None,
        })
    return params


def _reassemble_sub(text: str) -> str:
    return _SUB_TAIL_RE.sub(
        lambda m: f"{m.group(1)}_{m.group(4)} {m.group(2)} {m.group(3)}", text
    )

def _norm_hdr(h: str) -> str:
    return h.lower().replace(" ", "").replace(".", "").strip()

def _is_part_number(h: str) -> bool:
    """Fix 1: כותרת עמודה שנראית כמספר חלק (1N5817, BC546) ולא כתווית כמות (MIN/MAX)."""
    h = h.strip()
    return (
        4 <= len(h) <= 15
        and " " not in h
        and bool(re.search(r"[A-Za-z]", h))
        and bool(re.search(r"[0-9]", h))
        and not re.search(r"[^A-Za-z0-9\-.]", h)
    )


_NUMERIC_COND_HDR_RE = re.compile(
    r'^[+-]?\d+(?:\.\d+)?'
    r'(?:\s*(?:V|kV|mV|A|mA|µA|μA|uA|kHz|MHz|Hz|°C|℃|K|kΩ|Ω|Ohm|pF|nF|µF|uF|W|mW|%|ns|ms|µs|us))?$',
    re.IGNORECASE,
)

def _is_numeric_condition_header(h: str) -> bool:
    """Return True when a column header is a bare number or physical-value label
    (e.g. '6.3', '10V', '25°C', '1kHz') — meaning the column represents a
    measurement condition, NOT a Min/Typ/Max role.

    Capacitor and characteristic tables often use rated-voltage or frequency
    values as column headings; assigning them as MIN/TYP/MAX roles causes
    incorrect value extraction.
    """
    h = h.strip()
    if not h or len(h) > 12:
        return False
    return bool(_NUMERIC_COND_HDR_RE.match(h))

def _split_symbol(sym: str) -> Optional[Tuple[str, str]]:
    """Fix 3: מפצל סימבול מורכב לשני תת-סימבולים (למשל 'Rθ JA Rθ JC' → ('Rθ JA','Rθ JC'))."""
    parts = sym.split()
    if len(parts) == 2:
        return parts[0], parts[1]
    if len(parts) == 4:
        return f"{parts[0]} {parts[1]}", f"{parts[2]} {parts[3]}"
    return None

def _build_roles(raw_headers: List[str]) -> List[Optional[str]]:
    n = len(raw_headers)
    roles: List[Optional[str]] = [None] * n
    i = 0
    while i < n:
        if i + 1 < n:
            combined = _norm_hdr(raw_headers[i] + raw_headers[i + 1])
            if combined in HEADER_ROLE_MAP:
                roles[i] = roles[i + 1] = HEADER_ROLE_MAP[combined]
                i += 2
                continue
        single = _norm_hdr(raw_headers[i])
        if single in HEADER_ROLE_MAP:
            roles[i] = HEADER_ROLE_MAP[single]
        i += 1
    return roles

def _is_electrical(raw_headers: List[str]) -> bool:
    return bool({_norm_hdr(h) for h in raw_headers} & ELECTRICAL_HEADER_KEYWORDS)


def _find_header_row_idx(rows: list) -> int:
    """
    מאתר את אינדקס שורת הכותרות האמיתית בטבלה.

    דפוסים נתמכים:
      1. Super-header: row[0] = כותרת סקציה ממוזגת, row[1] = עמודות אמיתיות
         (Vishay, Infineon, TI Abs Max)
      2. רגיל: row[0] הוא כבר שורת הכותרות
         (ON Semi, רוב הטבלאות)

    סורק עד 3 שורות. מחזיר 0 כ-fallback.
    """
    for i, row in enumerate(rows[:3]):
        cells = [c.get_text(strip=True) for c in row.find_all(["th", "td"])]
        if _is_electrical(cells):
            return i
    return 0


def _merge_header_table(
    header_table: Tag,
    data_tables:  List[Tag],
) -> Optional[Tag]:
    """
    דפוס ON Semi / Fairchild: טבלת כותרות נפרדת + טבלאות נתונים ללא כותרות.

    מזהה את הדפוס כאשר:
      - header_table מכילה בדיוק שורה אחת עם מילות מפתח חשמליות
      - data_tables[0] מכילה שורות נתונים שמספר עמודותיהן תואם לכותרות

    מחזיר Tag חדש עם הכותרות + כל שורות הנתונים,
    או None אם הדפוס לא מתאים.
    """
    hdr_rows = header_table.find_all("tr")
    if len(hdr_rows) != 1:
        return None

    hdr_cells = [c.get_text(strip=True) for c in hdr_rows[0].find_all(["th", "td"])]
    if not _is_electrical(hdr_cells):
        return None

    n_cols = len(hdr_cells)
    if n_cols < 3:
        return None

    # בדוק שהטבלה הבאה תואמת במספר עמודות (±1 כי לפעמים יש עמודת condition כפולה)
    if not data_tables:
        return None
    first_data_rows = data_tables[0].find_all("tr")
    if not first_data_rows:
        return None
    first_data_cols = len(first_data_rows[0].find_all(["th", "td"]))
    if abs(first_data_cols - n_cols) > 2:
        return None

    # בנה soup חדש: כותרת + כל שורות הנתונים מכל הטבלאות
    combined_html = "<table>\n<tr>" + "".join(
        f"<th>{html_module.escape(c)}</th>" for c in hdr_cells
    ) + "</tr>\n"

    for data_tbl in data_tables:
        for row in data_tbl.find_all("tr"):
            combined_html += str(row) + "\n"

    combined_html += "</table>"
    return BeautifulSoup(combined_html, "html.parser").find("table")


def _infer_roles_from_data(rows: List, n_cols: int) -> List[Optional[str]]:
    """
    דפוס TI / אחרים: שורת כותרות קיימת אבל col[0] ריק בכל שורות הנתונים.
    במקרה זה col[0] הוא בפועל עמודת SYMBOL/PARAMETER משנית שחסרה כותרת.

    בודק: האם col[0] ריק ב-80%+ משורות הנתונים?
    אם כן — מסיק שcol[0] הוא SYMBOL (לא נצטרך להגדיר role מפורש,
    אלא פשוט לא לתת לו role כדי שלא יפריע לPARAMETER בcol[1]).

    מחזיר dict עם correction שיש להחיל על roles הקיים.
    לא משנה את _build_roles, רק מסיר role שגוי מcol[0].
    """
    if not rows or n_cols < 2:
        return []

    col0_empty = 0
    total = 0
    for row in rows[:10]:
        cells = row.find_all(["td", "th"])
        if not cells:
            continue
        total += 1
        val = cells[0].get_text(strip=True) if cells else ""
        if len(val) < 12:   # קצר מאוד = likely symbol fragment or empty
            col0_empty += 1

    if total > 0 and col0_empty / total >= 0.7:
        return [0]   # רשימת אינדקסים של עמודות שצריך לשנות ל-SYMBOL
    return []


def _split_vals(cell: str) -> List[str]:
    """
    מפצל תא לרשימת ערכים מספריים.

    תומך ב:
      "3.0"          → ['3.0']            (ערך יחיד)
      "-1 1"         → ['-1', '1']        (min/max סימטרי)
      "240 450 750"  → ['240','450','750'] (min/typ/max)
      "−55 to +175"  → ['-55', '175']     (טווח)
    """
    cell = cell.strip()
    if not cell:
        return []
    tokens = [m.group().strip() for m in _SIGNED_NUM.finditer(cell)
              if re.search(r"\d", m.group())]
    return tokens if tokens else [cell]


def _assign_vals(
    nums:  List[str],
    role:  str,
) -> Tuple[Optional[str], Optional[str], Optional[str]]:
    """
    ממפה רשימת ערכים מספריים ל-(min, typ, max) לפי ה-role וכמות הערכים.

    1 ערך  → לפי role (MIN/TYP/MAX)
    2 ערכים → min=ראשון, max=אחרון  (ספציפיקציות סימטריות כמו -1 / +1)
    3 ערכים → min, typ, max          (TI: 240 450 750 mA)
    4+ ערכים → min=ראשון, max=אחרון (טווחים מורכבים)
    """
    n = len(nums)
    if n == 0:
        return None, None, None
    if n == 1:
        v = nums[0]
        if role == "MIN":  return v,    None, None
        if role == "MAX":  return None, None, v
        if role == "TYP":  return None, v,    None
        return None, v, None       # fallback → typ
    if n == 2:
        return nums[0], None, nums[1]
    if n == 3:
        return nums[0], nums[1], nums[2]
    # 4+: min/max בלבד
    return nums[0], None, nums[-1]


def _pick(nums: List[str], role: str) -> Optional[str]:
    """Legacy helper — משמש עדיין לCONDITION / SYMBOL."""
    if not nums:        return None
    if len(nums) == 1:  return nums[0]
    if role == "MIN":   return nums[0]
    if role == "MAX":   return nums[-1]
    return nums[len(nums) // 2]


class _TableCleaner:
    """מנקה טבלה אחת ומחזיר HTML + רשימת פרמטרים."""

    def __init__(self, table: Tag):
        self.table = table
        self.rows  = table.find_all("tr")

    def process(self) -> Tuple[str, List[Dict]]:
        if not self.rows:
            return str(self.table), []

        # B5: dispatch to specialized parsers before standard processing
        if _is_key_value_table(self.rows):
            return str(self.table), _parse_key_value_table(self.rows)
        if _is_catalog_table(self.rows):
            return str(self.table), _parse_catalog_table(self.rows)

        hdr_idx = _find_header_row_idx(self.rows)

        raw_headers = [
            c.get_text(strip=True)
            for c in self.rows[hdr_idx].find_all(["th", "td"])
        ]

        if not _is_electrical(raw_headers):
            for node in self.table.find_all(string=True):
                node.replace_with(_pp_clean(str(node)))
            return str(self.table), []

        n_cols = len(raw_headers)
        roles  = _build_roles(raw_headers)

        # ── כוללני: זיהוי עמודה שחסרה כותרת אבל מכילה symbol/fragment ──
        data_rows = self.rows[hdr_idx + 1:]
        empty_col_indices = _infer_roles_from_data(data_rows, n_cols)
        for col_idx in empty_col_indices:
            if col_idx < len(roles) and roles[col_idx] is None:
                roles[col_idx] = "SYMBOL"

        # ── Fallback 1: PARAMETER role חסר (דפוס TI/National Semi) ───
        # בטבלאות AMR ו-DC של TI הכותרת היא ['', '', 'MIN', 'MAX', 'UNIT'].
        # העמודה הראשונה מכילה שמות פרמטרים אבל אין לה כותרת מזוהה.
        # נסרוק את 3 העמודות הראשונות ונקצה PARAMETER לעמודה עם תוכן טקסטואלי.
        if "PARAMETER" not in roles:
            for col_idx in range(min(3, n_cols)):
                if roles[col_idx] not in (None, "SYMBOL"):
                    continue
                text_n = total_n = 0
                for row in data_rows[:10]:
                    cells = row.find_all(["td", "th"])
                    if col_idx >= len(cells):
                        continue
                    val = cells[col_idx].get_text(strip=True)
                    if val and val not in ("—", "-", "–", ""):
                        total_n += 1
                        if not re.match(r'^[±\-\+\d\.\s%°/kmunpfM]+$', val):
                            text_n += 1
                if total_n > 0 and text_n / total_n >= 0.3:
                    roles[col_idx] = "PARAMETER"
                    break

        # ── Fallback 2: עמודות ערך ללא כותרת (דפוס split-header של pdfplumber) ──
        # pdfplumber מפצל תא ממוזג לשתי עמודות, מה שדוחף עמודות ערך לאין-תפקיד.
        # נסרוק עמודות ללא תפקיד עם תוכן מספרי ונקצה להן MIN/TYP/MAX לפי הסדר.
        # Fix 1: עמודות שכותרתן נראית כמספר חלק (1N5817, BC546) לא מקבלות MIN/TYP/MAX
        #        אלא מסומנות כ-VARIANT ונאסף מהן הערך הנציג.
        _missing_vals = [r for r in ("MIN", "TYP", "MAX") if r not in roles]
        if _missing_vals:
            for col_idx in range(n_cols):
                if not _missing_vals:
                    break
                if roles[col_idx] is not None:
                    continue
                hdr = raw_headers[col_idx] if col_idx < len(raw_headers) else ""
                if _is_part_number(hdr):
                    roles[col_idx] = "VARIANT"
                    continue
                if _is_numeric_condition_header(hdr):
                    roles[col_idx] = "VARIANT"
                    continue
                num_n = total_n = 0
                for row in data_rows[:10]:
                    cells = row.find_all(["td", "th"])
                    if col_idx >= len(cells):
                        continue
                    val = cells[col_idx].get_text(strip=True)
                    if val and val not in ("—", "-", "–", ""):
                        total_n += 1
                        if re.match(r'^[±\-\+]?\d+\.?\d*(?:[eE][+-]?\d+)?(?:\s*[kmunpfM%])?$', val):
                            num_n += 1
                if total_n > 0 and num_n / total_n >= 0.5:
                    roles[col_idx] = _missing_vals.pop(0)

        # Fix 1: pre-compute variant column indices for use in data row loop
        variant_col_indices = [i for i, r in enumerate(roles) if r == "VARIANT"]

        # שורות super-header לפני הכותרות
        out_rows = []
        for i in range(hdr_idx):
            cells = [c.get_text(strip=True)
                     for c in self.rows[i].find_all(["th", "td"])]
            out_rows.append(
                "<tr>" + "".join(
                    f"<th colspan='{n_cols}'>{html_module.escape(_pp_clean(cells[0]))}</th>"
                    if len(cells) == 1 or all(c == "" for c in cells[1:])
                    else f"<th>{html_module.escape(_pp_clean(c))}</th>"
                    for c in cells
                ) + "</tr>"
            )

        out_rows.append("<tr>" + "".join(
            f"<th>{html_module.escape(_pp_clean(h))}</th>" for h in raw_headers
        ) + "</tr>")

        parameters      = []
        last_param: str = ""
        last_unit:  str = ""

        for row in data_rows:
            cells      = row.find_all(["td", "th"])
            cell_texts = [
                _pp_clean(cells[i].get_text(strip=True)) if i < len(cells) else ""
                for i in range(n_cols)
            ]

            role_text: Dict[str, str] = {}
            # Fix 1: collect variant column values separately
            variant_vals: List[str] = [
                cell_texts[i] if i < len(cell_texts) else ""
                for i in variant_col_indices
            ]
            for idx, role in enumerate(roles):
                if not role or role == "VARIANT" or not cell_texts[idx]:
                    continue
                if role == "SYMBOL" and role in role_text:
                    continue
                role_text[role] = (
                    (role_text[role] + " " + cell_texts[idx]).strip()
                    if role in role_text else cell_texts[idx]
                )

            param_raw = role_text.get("PARAMETER", "")
            param     = _split_runon(param_raw) if param_raw else ""

            # B2: skip rows where the parameter cell IS a column header word
            # (happens when pdfplumber emits the header row twice as a data row)
            _HEADER_WORDS = {"min", "max", "typ", "typical", "parameter", "symbol",
                             "unit", "units", "condition", "value", "minimum", "maximum"}
            if param and param.strip().lower() in _HEADER_WORDS:
                continue

            if param:
                last_param = param
            effective = last_param

            cond = _reassemble_sub(role_text.get("CONDITION", ""))

            # ── כוללני: _assign_vals מטפל ב-1/2/3+ ערכים בתא ──────────
            min_v = typ_v = max_v = None

            for value_role in ("MIN", "TYP", "MAX"):
                raw = role_text.get(value_role, "")
                if not raw:
                    continue
                nums = _split_vals(raw)
                mn, tp, mx = _assign_vals(nums, value_role)
                if mn is not None and min_v is None: min_v = mn
                if tp is not None and typ_v is None: typ_v = tp
                if mx is not None and max_v is None: max_v = mx

            unit_raw = role_text.get("UNIT", "")
            if unit_raw:
                last_unit = unit_raw
            unit = last_unit

            # Fix 1+3: use variant column data when no regular value roles produced results
            _split_params: Optional[List[Dict]] = None
            if not any([min_v, typ_v, max_v]) and variant_vals:
                first = next((v for v in variant_vals if v.strip()), None)
                if first:
                    nums = _split_vals(first)
                    if len(nums) == 2:
                        # Fix 3: merged sub-parameter rows — try to split by symbol
                        sym_pair = _split_symbol(role_text.get("SYMBOL", ""))
                        if sym_pair:
                            _split_params = [
                                {"parameter": effective, "min": None, "typ": None,
                                 "max": nums[0], "unit": unit or None,
                                 "condition": sym_pair[0]},
                                {"parameter": effective, "min": None, "typ": None,
                                 "max": nums[1], "unit": unit or None,
                                 "condition": sym_pair[1]},
                            ]
                        else:
                            min_v, max_v = nums[0], nums[-1]
                    elif len(nums) == 1:
                        max_v = nums[0]
                    elif len(nums) >= 3:
                        min_v, typ_v, max_v = nums[0], nums[1], nums[2]

            td_parts, emitted = [], set()
            for idx, role in enumerate(roles):
                if role is None or role == "VARIANT":
                    td_parts.append(f"<td>{html_module.escape(cell_texts[idx])}</td>")
                    continue
                if role in emitted:
                    td_parts.append("<td></td>")
                    continue
                emitted.add(role)
                val_map = {
                    "PARAMETER": param,   "CONDITION": cond,
                    "MIN":       min_v,   "TYP":       typ_v,
                    "MAX":       max_v,   "UNIT":      unit,
                    "SYMBOL":    role_text.get("SYMBOL", ""),
                }
                v = val_map.get(role, cell_texts[idx])
                td_parts.append(
                    f"<td>{html_module.escape(v)}</td>" if v else "<td>—</td>"
                )
            out_rows.append("<tr>" + "".join(td_parts) + "</tr>")

            # Fix 2: דלג על שורות הערות / footnotes
            if _NOTE_ROW_RE.match(effective or ""):
                out_rows.append("<tr>" + "".join(td_parts) + "</tr>")
                continue

            # Fix 3: שורות מפוצלות (שני תת-פרמטרים בשורה אחת)
            if _split_params is not None:
                out_rows.append("<tr>" + "".join(td_parts) + "</tr>")
                parameters.extend(_split_params)
                continue

            has_values = any([min_v, typ_v, max_v])
            if not effective and not has_values and not cond:
                continue
            parameters.append({
                "parameter": effective,
                "min":       min_v,
                "typ":       typ_v,
                "max":       max_v,
                "unit":      unit or None,
                "condition": cond or None,
            })

        return "<table>\n" + "\n".join(out_rows) + "\n</table>", parameters


class DatasheetHTMLPreprocessor:
    """שלב 2 — מנקה HTML מסונן ומחזיר HTML נקי."""

    def process(self, filtered_html: str) -> Tuple[str, List[Dict], Dict]:
        n_cid        = len(_CID_RE.findall(filtered_html))
        filtered_html = _CID_RE.sub("", filtered_html).replace("\u2581", " ")

        soup       = BeautifulSoup(filtered_html, "html.parser")
        all_params = []

        # ── כוללני: מיזוג header-table + data-tables (דפוס ON Semi/Fairchild) ──
        # מזהה טבלת כותרות בודדת (שורה אחת עם מילות מפתח) שאחריה
        # מספר טבלאות נתונים ללא כותרות, ומאחד אותן לטבלה אחת.
        all_tables = soup.find_all("table")
        merged_tables: set = set()   # id() של טבלאות שכבר עובדו

        for i, table in enumerate(all_tables):
            if id(table) in merged_tables:
                continue
            rows = table.find_all("tr")
            if len(rows) != 1:
                continue
            hdr_cells = [c.get_text(strip=True) for c in rows[0].find_all(["th","td"])]
            if not _is_electrical(hdr_cells):
                continue

            # נסה לאסוף טבלאות נתונים עוקבות (עד 8) שאין להן כותרות
            subsequent: List[Tag] = []
            for j in range(i + 1, min(i + 9, len(all_tables))):
                nxt = all_tables[j]
                if id(nxt) in merged_tables:
                    break
                nxt_rows = nxt.find_all("tr")
                if not nxt_rows:
                    break
                nxt_r0 = [c.get_text(strip=True) for c in nxt_rows[0].find_all(["th","td"])]
                # עצור אם הטבלה הבאה מכילה כותרות בעצמה
                if _is_electrical(nxt_r0):
                    break
                subsequent.append(nxt)

            if not subsequent:
                continue

            merged = _merge_header_table(table, subsequent)
            if merged is None:
                continue

            # החלף את טבלת הכותרות ב-merged, הסר את הנתונים המקוריים
            table.replace_with(merged)
            for s in subsequent:
                merged_tables.add(id(s))
                s.decompose()

        for table in soup.find_all("table"):
            cleaner = _TableCleaner(table)
            clean_html, params = cleaner.process()
            if params:
                all_params.extend(params)
                table.replace_with(BeautifulSoup(clean_html, "html.parser"))

        for node in soup.find_all(string=True):
            orig = str(node)
            c    = _pp_clean(orig)
            if c != orig:
                node.replace_with(c)

        # B1: deduplicate — step 1: remove exact (name+values) duplicates
        seen_keys: set = set()
        deduped: List[Dict] = []
        for p in all_params:
            key = (
                (p.get("parameter") or "").strip().lower(),
                str(p.get("min") or ""),
                str(p.get("typ") or ""),
                str(p.get("max") or ""),
            )
            if key not in seen_keys:
                seen_keys.add(key)
                deduped.append(p)

        # B1: deduplicate — step 2: collapse multi-variant tables by parameter name.
        # Datasheets with multiple device variants (e.g., LM741/LM741C) repeat the same
        # parameter rows with slightly different values for each variant. The gold standard
        # keeps one canonical entry. We keep the entry with the most non-null value fields.
        name_best: Dict[str, Dict] = {}
        for p in deduped:
            name = (p.get("parameter") or "").strip().lower()
            if not name:
                continue
            def _value_count(x: Dict) -> int:
                return sum(1 for k in ("min", "typ", "max") if x.get(k) is not None)
            if name not in name_best or _value_count(p) > _value_count(name_best[name]):
                name_best[name] = p
        # Preserve original order while collapsing to one-per-name (drop empty-name entries)
        seen_names: set = set()
        collapsed: List[Dict] = []
        for p in deduped:
            name = (p.get("parameter") or "").strip().lower()
            if name and name not in seen_names:
                seen_names.add(name)
                collapsed.append(name_best[name])
            # empty-name entries are dropped (will also be caught by _is_valid_parameter)
        all_params = collapsed

        diag = {"cid_removed": n_cid, "params_found": len(all_params)}
        return str(soup), all_params, diag


# =============================================================================
# תיקון 5 — Aligner עם tables_only=True
# =============================================================================

def _parameters_to_relations(parameters: List[Dict]) -> List[Dict]:
    """
    ממיר פרמטרים שחולצו ע"י ה-Preprocessor ל-relation triples.
    הפורמט זהה לפורמט שה-aligner._add_relations() מצפה לקבל —
    כך ניתן להשתמש בתשתית הקיימת ל-alignment לטוקנים.

    לכל פרמטר נוצרות עד 5 triples:
      has_min / has_typ / has_max / has_unit / has_condition
    """
    predicate_map = {
        "min":       "has_min",
        "typ":       "has_typ",
        "max":       "has_max",
        "unit":      "has_unit",
        "condition": "has_condition",
    }
    triples: List[Dict] = []
    for p in parameters:
        subject = (p.get("parameter") or "").strip()
        if not subject:
            continue
        for key, predicate in predicate_map.items():
            obj = p.get(key)
            if not obj:
                continue
            obj_str = str(obj).strip()
            # דלג על ערכי placeholder ("-", "—") וערכים ריקים
            if not obj_str or obj_str in ("-", "—", "–"):
                continue
            # דלג על self-referential (subject == object)
            if obj_str.lower() == subject.lower():
                continue
            triples.append({
                "subject":   subject,
                "predicate": predicate,
                "object":    obj_str,
            })
    return triples


def run_aligner(clean_html: str, aligner_dir: Path) -> List[Dict]:
    """
    תיקון 5: מריץ את PreprocessingEngine עם קלט מצומצם לטבלאות בלבד.
    מחלץ את תגיות <table> מה-HTML ומעביר רק אותן ל-Aligner.

    הערה: לא מעביר relations כאן — ה-guard ב-_add_relations של ה-aligner
    דורש ner_tags != O, וב-inference הכל O. ה-alignment מתבצע בנפרד
    אחרי הרצת המודל, דרך _align_relations_inference().
    """
    aligner_str = str(aligner_dir)
    if aligner_str not in sys.path:
        sys.path.insert(0, aligner_str)

    from aligner import PreprocessingEngine  # noqa: E402

    soup   = BeautifulSoup(clean_html, "html.parser")
    tables = soup.find_all("table")

    if tables:
        tables_only_html = (
            "<html><head><meta charset='UTF-8'></head><body>\n"
            + "\n".join(str(t) for t in tables)
            + "\n</body></html>"
        )
    else:
        log.warning("        לא נמצאו טבלאות ב-HTML הנקי — מעביר HTML מלא ל-Aligner")
        tables_only_html = clean_html

    engine  = PreprocessingEngine(tokenizer=None)
    samples = engine.process(tables_only_html, jsonl_relations=None)
    return samples


def _align_relations_inference(
    samples:   List[Dict],
    relations: List[Dict],
) -> List[Dict]:
    """
    מיישר relation triples לטוקנים — גרסת inference בלבד.

    ההבדל מ-aligner._add_relations():
      - ה-guard שבודק ner_tags != O הוסר.
        ב-inference ner_tags הם תמיד O (אין data-label spans),
        אז הguard היה חוסם את כל ה-relations.
      - כל שאר הלוגיקה (phrase matching, trim_span, dedup) זהה.

    לא נוגעים ב-aligner.py — ה-guard שם נכון לאימון ולא ישונה.
    """
    import re as _re

    if not relations:
        return samples

    # ── normalize: זהה ל-aligner._add_relations ──────────────────────
    from aligner import PreprocessingEngine as _PE
    _eng = _PE.__new__(_PE)  # instance ללא __init__ לגישה ל-methods

    def _normalize(s: str) -> str:
        s = _eng._clean_artifacts(s)
        return _re.sub(r'[^a-z0-9]', '', s.lower())

    _NOISE = {'\n', '\t', '—', '-', '–', '', ' '}

    def _trim(indices: List[int], toks: List[str]) -> List[int]:
        start = 0
        while start < len(indices) and toks[indices[start]] in _NOISE:
            start += 1
        end = len(indices)
        while end > start and toks[indices[end - 1]] in _NOISE:
            end -= 1
        return indices[start:end] if start < end else indices

    # ── בנה phrase index על כל ה-samples ────────────────────────────
    phrase_index: Dict[str, List[Tuple[int, List[int]]]] = {}

    for si, sample in enumerate(samples):
        toks      = sample['tokens']
        max_ngram = min(10, len(toks))
        for n in range(1, max_ngram + 1):
            for i in range(len(toks) - n + 1):
                span_toks = toks[i:i + n]
                if not any(t not in _NOISE for t in span_toks):
                    continue
                phrase_norm = _normalize(' '.join(span_toks))
                if not phrase_norm:
                    continue
                phrase_index.setdefault(phrase_norm, []).append(
                    (si, list(range(i, i + n)))
                )

    # ── יישור כל triple ──────────────────────────────────────────────
    for rel in relations:
        subj = str(rel.get('subject', '')).strip()
        pred = rel.get('predicate', '')
        obj  = str(rel.get('object',  '')).strip()

        if not subj or not obj or subj == obj:
            continue

        subj_norm = _normalize(subj)
        obj_norm  = _normalize(obj)

        if subj_norm == obj_norm:
            continue

        for sample_idx, raw_subj_idx in phrase_index.get(subj_norm, []):
            toks = samples[sample_idx]['tokens']

            subj_indices = _trim(raw_subj_idx, toks)
            if not subj_indices:
                continue

            obj_matches = [
                (idx, idxs)
                for idx, idxs in phrase_index.get(obj_norm, [])
                if idx == sample_idx
            ]
            if not obj_matches:
                continue

            subj_end = subj_indices[-1]
            _, raw_obj_idx = min(
                obj_matches, key=lambda x: abs(x[1][0] - subj_end)
            )
            obj_indices = _trim(raw_obj_idx, toks)
            if not obj_indices or subj_indices == obj_indices:
                continue

            new_rel = {
                'head': subj_indices,
                'type': pred,
                'tail': obj_indices,
            }
            if new_rel not in samples[sample_idx]['relations']:
                samples[sample_idx]['relations'].append(new_rel)

    return samples


# =============================================================================
# שלב 4 — Tokens → NER predictions  (Model)
# =============================================================================

class NERModel:
    # Must match the order used during training in train_joint_model.py NER_LABELS.
    # B-VALUE/I-VALUE are at index 3/4 — do NOT reorder.
    LABEL_LIST = [
        "O",
        "B-PARAMETER", "I-PARAMETER",
        "B-MIN",       "I-MIN",
        "B-MAX",       "I-MAX",
        "B-TYP",       "I-TYP",
        "B-UNIT",      "I-UNIT",
        "B-CONDITION", "I-CONDITION",
    ]
    # 7 relation types — must match REL_LABELS in train_joint_model.py
    _NUM_REL_LABELS = 7
    BASE_MODEL = "microsoft/deberta-v3-base"

    def __init__(self, model_path: Path, mode: str = "auto"):
        self.model_path = model_path
        self.mode       = mode
        self.tokenizer  = None
        self.model      = None
        self.id2label: Dict[int, str] = {i: l for i, l in enumerate(self.LABEL_LIST)}
        self.device     = None
        self._load()

    def _load(self):
        if self.mode == "dummy":
            log.warning("Dummy mode — ללא מודל.")
            return

        try:
            import torch
            import torch.nn as nn
            from transformers import AutoTokenizer
        except ImportError:
            raise ImportError("pip install transformers torch")

        log.info(f"טוען tokenizer מ-{self.BASE_MODEL}…")
        self.tokenizer = AutoTokenizer.from_pretrained(self.BASE_MODEL, use_fast=False)

        pt_path = self.model_path / "best_model.pt"
        use_pt  = self.mode != "base" and pt_path.exists()

        if use_pt:
            self._load_pt_checkpoint(pt_path, torch, nn)
        else:
            self._load_hf_checkpoint(torch, nn)

        self.model.eval()
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model.to(self.device)
        log.info(f"device={self.device}")

    def _load_pt_checkpoint(self, pt_path: Path, torch, nn):
        """Load the JointNERRE .pt state dict into a matching architecture."""
        from transformers import DebertaV2Config, DebertaV2Model

        num_ner = len(self.LABEL_LIST)
        num_re  = self._NUM_REL_LABELS

        # Build the same architecture as JointNERRE in train_joint_model.py.
        # DebertaV2Model(cfg) initialises randomly; weights are overwritten below.
        cfg     = DebertaV2Config.from_pretrained(self.BASE_MODEL)
        encoder = DebertaV2Model(cfg)
        ner_head = nn.Linear(cfg.hidden_size, num_ner)
        re_head  = nn.Linear(cfg.hidden_size * 2, num_re)

        class _JointNER(nn.Module):
            def __init__(self, enc, ner, re):
                super().__init__()
                self.encoder  = enc
                self.ner_head = ner
                self.re_head  = re  # kept so state_dict keys match exactly

            def forward(self, input_ids, attention_mask, **_):
                out = self.encoder(input_ids=input_ids, attention_mask=attention_mask)
                return self.ner_head(out.last_hidden_state)

        model = _JointNER(encoder, ner_head, re_head)

        log.info(f"טוען checkpoint מ-{pt_path}…")
        state_dict = torch.load(str(pt_path), map_location="cpu", weights_only=False)
        # ner_weights is a class-weight tensor saved alongside the model — not a parameter
        state_dict.pop("ner_weights", None)
        missing, unexpected = model.load_state_dict(state_dict, strict=True)
        if missing:
            log.warning(f"checkpoint: {len(missing)} מפתחות חסרים: {missing[:5]}")
        if unexpected:
            log.warning(f"checkpoint: {len(unexpected)} מפתחות לא צפויים: {unexpected[:5]}")
        log.info("checkpoint JointNERRE (.pt) נטען בהצלחה.")
        self.model = model

    def _load_hf_checkpoint(self, torch, nn):
        """Fallback: load a HuggingFace AutoModelForTokenClassification checkpoint."""
        from transformers import AutoModelForTokenClassification, DebertaV2Config, DebertaV2ForTokenClassification

        cfg_path = self.model_path / "config.json"
        if self.model_path.exists() and cfg_path.exists():
            try:
                cfg_data = json.loads(cfg_path.read_text(encoding="utf-8"))
                if "model_type" in cfg_data:
                    self.model = AutoModelForTokenClassification.from_pretrained(str(self.model_path))
                    if self.model.config.id2label:
                        self.id2label = self.model.config.id2label
                    log.info("HuggingFace checkpoint נטען.")
                    return
            except Exception as e:
                if self.mode == "trained":
                    raise
                log.warning(f"config.json לא תקין ({e}) — fallback.")

        if self.mode == "trained":
            raise FileNotFoundError(f"לא נמצא checkpoint ב-{self.model_path}")

        log.warning("לא נמצא checkpoint — fallback למודל בסיסי (לא מאומן).")
        label2id = {l: i for i, l in enumerate(self.LABEL_LIST)}
        cfg = DebertaV2Config.from_pretrained(
            self.BASE_MODEL,
            num_labels=len(self.LABEL_LIST),
            id2label=self.id2label, label2id=label2id,
        )
        self.model = DebertaV2ForTokenClassification.from_pretrained(
            self.BASE_MODEL, config=cfg, ignore_mismatched_sizes=True,
        )
        log.warning("מודל בסיסי (לא מאומן) — predictions אינן אמינות.")

    def predict(self, samples: List[Dict]) -> List[Dict]:
        if self.mode == "dummy" or self.model is None:
            for s in samples:
                s["pred_tags"] = ["O"] * len(s["tokens"])
            return samples

        import torch

        for sample in samples:
            tokens = sample["tokens"]
            if not tokens:
                sample["pred_tags"] = []
                continue

            enc = self.tokenizer(
                tokens,
                is_split_into_words=True,
                return_tensors="pt",
                truncation=True,
                max_length=512,
            )
            enc_gpu = {k: v.to(self.device) for k, v in enc.items()}

            with torch.no_grad():
                out = self.model(**enc_gpu)
                # _JointNER returns logits tensor directly;
                # HuggingFace models return an object with .logits
                logits = out if isinstance(out, torch.Tensor) else out.logits

            pred_ids = logits.argmax(-1)[0].tolist()
            word_ids = enc.word_ids()   # CPU encoding — לא tensor

            # Build word_id → tag dict (first subword wins).
            # Tokens that produce zero subwords (e.g. '\n' in DeBERTa SentencePiece)
            # are absent from word_ids entirely, so we default them to 'O'.
            word_tag: Dict[int, str] = {}
            prev_wid = None
            for pid, wid in zip(pred_ids, word_ids):
                if wid is None or wid == prev_wid:
                    continue
                word_tag[wid] = self.id2label.get(pid, "O")
                prev_wid = wid

            pred_tags = [word_tag.get(i, "O") for i in range(len(tokens))]
            sample["pred_tags"] = pred_tags

        return samples


# =============================================================================
# שלב 5 — pred_tags → JSON מובנה
# תיקון 6 — סינון פרמטרים לא-תקינים
# =============================================================================

# תיקון 6: תבניות של parameter לא-תקין
_INVALID_PARAM_RE = re.compile(
    r"^[\s\n\t\r.,;:!?(){}[\]<>|/\\\"'`~@#$%^&*+=]+$"  # רק סימני פיסוק
)

# תיקון 6: אורך מינימלי/מקסימלי לפרמטר תקין
_PARAM_MIN_LEN = 2
_PARAM_MAX_LEN = 120

# B1: non-electrical categories that appear in datasheet tables but are not parameters
_NON_ELECTRICAL_PREFIXES = (
    "soldering", "solder", "storage", "shipping", "package", "marking",
    "ordering", "part number", "device marking", "moisture", "msl",
    "esd", "electrostatic", "latch", "latch-up", "human body",
    "machine model", "reflow", "wave solder", "hand solder",
    "assembly", "mounting", "weight", "dimension", "outline",
    "lead finish", "lead-free", "rohs", "halogen",
)

# B1: values that look like part numbers / page numbers rather than measurements
_BOGUS_VALUE_RE = re.compile(
    r"^(?:\d{3,}[a-zA-Z]|[a-zA-Z]{2,}\d{3,}|"   # part-number patterns
    r"(?:rev|pg|page|fig|table|section)\s*\.?\d+)$",  # document references
    re.IGNORECASE,
)


def _is_valid_parameter(param: Dict) -> bool:
    """
    תיקון 6 / B1: פילטר פרמטרים לא-תקינים מהפלט.

    פרמטר לא-תקין הוא אחד מהבאים:
      - שם ריק, רק whitespace, או רק סימני פיסוק
      - שם קצר מ-2 תווים או ארוך מ-120 (סבירות גבוהה שזה טקסט שגוי)
      - אין אף ערך (min/typ/max כולם None)
      - הערך מכיל newlines (סימן לטקסט גולמי שנכנס בטעות)
      - B1: שם שייך לקטגוריה לא-חשמלית (soldering, storage, ESD, ordering...)
      - B1: ערך שנראה כמספר חלק או מספר עמוד ולא כמדידה פיזיקלית
    """
    name = param.get("parameter", "")

    # שם ריק או רק whitespace
    if not name or not name.strip():
        return False

    # רק סימני פיסוק
    if _INVALID_PARAM_RE.match(name.strip()):
        return False

    # אורך לא סביר
    if len(name.strip()) < _PARAM_MIN_LEN or len(name.strip()) > _PARAM_MAX_LEN:
        return False

    # newline בשם (סימן לטקסט גולמי)
    if "\n" in name or "\r" in name:
        return False

    # B1: non-electrical categories
    name_lower = name.strip().lower()
    if any(name_lower.startswith(pfx) or pfx in name_lower for pfx in _NON_ELECTRICAL_PREFIXES):
        return False

    # אין אף ערך
    has_value = any(
        param.get(k) and str(param[k]).strip()
        for k in ("min", "typ", "max")
    )
    if not has_value:
        return False

    # ערך מכיל newline (טקסט גולמי)
    for key in ("min", "typ", "max", "unit"):
        v = param.get(key)
        if v and ("\n" in str(v) or len(str(v)) > 50):
            return False

    # B1: reject parameters whose ONLY values look like part numbers / doc refs
    all_vals = [str(param.get(k, "")).strip() for k in ("min", "typ", "max")
                if param.get(k) and str(param[k]).strip()]
    if all_vals and all(_BOGUS_VALUE_RE.match(v) for v in all_vals):
        return False

    # B2: reject if unit looks like a package type or pin-count descriptor
    unit_str = str(param.get("unit") or "").strip().upper()
    _PACKAGE_UNIT_RE = re.compile(
        r"(?:DIP|SOIC|TSSOP|QFN|SOT|TO-\d|SOP|PDIP|PLCC|\d+PINS?$|LEADS?$|WETTABLE)", re.I
    )
    if unit_str and _PACKAGE_UNIT_RE.search(unit_str):
        return False
    # B2: if unit is purely numeric, clear it (a value leaked into the unit column)
    # Don't reject the whole param — just let it through with no unit
    if unit_str and re.match(r"^[+-]?\d+\.?\d*$", unit_str):
        param["unit"] = None

    # B2: reject if any value field is pure text with no digits AND is not a dash/placeholder
    _DASH_PLACEHOLDER = re.compile(r"^[-–—/]+$")
    for key in ("min", "typ", "max"):
        v = str(param.get(key) or "").strip()
        if v and not re.search(r"\d", v) and not _DASH_PLACEHOLDER.match(v):
            # Contains words but no numbers — likely a label/text, not a measurement
            # Allow short strings (symbols like "±", single letters) but reject multi-word text
            if len(v.split()) >= 2:
                return False

    return True


def _label_to_key(label: str) -> Optional[str]:
    return {
        "PARAMETER": "parameter",
        "MIN":       "min",
        "TYP":       "typ",
        "MAX":       "max",
        "UNIT":      "unit",
        "CONDITION": "condition",
        "VALUE":     "max",
    }.get(label)


def _fill(current: Dict, label: str, tok: str):
    key = _label_to_key(label)
    if key and current.get(key) is None:
        current[key] = tok


def samples_to_parameters(samples: List[Dict]) -> List[Dict]:
    """
    ממיר samples (tokens + pred_tags) לרשימת פרמטרים.
    תיקון 6: מסנן פרמטרים לא-תקינים בסוף.
    """
    parameters: List[Dict] = []
    current: Optional[Dict] = None

    for sample in samples:
        tokens    = sample["tokens"]
        pred_tags = sample.get("pred_tags", ["O"] * len(tokens))

        for tok, tag in zip(tokens, pred_tags):
            if tag == "O":
                continue

            bio, label = tag.split("-", 1) if "-" in tag else ("O", "O")

            if bio == "B":
                if label == "PARAMETER":
                    if current and any(current.get(k) for k in ("min","typ","max")):
                        parameters.append(current)
                    current = {"parameter": tok, "min": None, "typ": None,
                               "max": None, "unit": None, "condition": None}
                elif current:
                    _fill(current, label, tok)

            elif bio == "I" and current:
                key = _label_to_key(label)
                if key == "parameter":
                    current["parameter"] = current["parameter"] + " " + tok
                elif key and current.get(key) is not None:
                    current[key] = current[key] + " " + tok

    if current and any(current.get(k) for k in ("min","typ","max")):
        parameters.append(current)

    # תיקון 6: סנן פרמטרים לא-תקינים
    before_filter = len(parameters)
    parameters    = [p for p in parameters if _is_valid_parameter(p)]
    after_filter  = len(parameters)

    if before_filter != after_filter:
        log.info(f"        סינון פלט: {before_filter} → {after_filter} פרמטרים "
                 f"(הוסרו {before_filter - after_filter} לא-תקינים)")

    return parameters


# =============================================================================
# Re-tokenization: preprocessor_params → NER input סינתטי
# =============================================================================

def _build_ner_from_pp(params_pp: List[Dict]) -> List[Dict]:
    """
    ממיר preprocessor_params לחלונות טוקנים שנראים כמו נתוני האימון הסינתטיים.

    NER is used as a pure filter: after prediction, only preprocessor params whose
    row contains a B-PARAMETER or I-PARAMETER tag are kept; their original
    preprocessor values (min/typ/max/unit/cond) are preserved unchanged.

    Each sample carries two extra fields:
      _param_base_idx  — index of the first param in this chunk
      _row_starts      — list of token indices where each param's row begins
      _row_ends        — list of exclusive token indices where each param's row ends

    כל חלון מכיל עד _CHUNK פרמטרים כדי להישאר מתחת ל-512 טוקנים.
    """
    _DASH  = "—"
    _HDR   = ["Parameter", "Symbol", "Min", "Typ", "Max", "Unit", "Condition", "\n"]
    _CHUNK = 18

    samples: List[Dict] = []

    for start in range(0, max(1, len(params_pp)), _CHUNK):
        chunk      = params_pp[start : start + _CHUNK]
        tokens     = list(_HDR)
        row_starts = []
        row_ends   = []

        for p in chunk:
            row_starts.append(len(tokens))

            param = (p.get("parameter") or "").strip()
            tokens.extend(param.split() if param else [_DASH])
            tokens.append(_DASH)                    # Symbol placeholder

            for key in ("min", "typ", "max"):
                val = str(p.get(key) or "").strip()
                if val and val not in (_DASH, "-", "–", ""):
                    tokens.extend(val.split())
                else:
                    tokens.append(_DASH)

            unit = str(p.get("unit") or "").strip()
            tokens.extend(unit.split() if unit else [_DASH])

            cond = str(p.get("condition") or "").strip()
            tokens.extend(cond.split()[:8] if cond else [_DASH])

            tokens.append("\n")
            row_ends.append(len(tokens))

        samples.append({
            "id":              f"pp_{start}",
            "tokens":          tokens,
            "ner_tags":        ["O"] * len(tokens),
            "relations":       [],
            "_param_base_idx": start,
            "_row_starts":     row_starts,
            "_row_ends":       row_ends,
        })

    return samples


# =============================================================================
# Deduplication helper
# =============================================================================

def _dedup_params(params: List[Dict]) -> List[Dict]:
    """Deduplicate extracted parameters by normalised name.

    The same parameter can appear in multiple tables (e.g. in both the
    Absolute Maximum Ratings table and the Electrical Characteristics table).
    We keep the first-seen entry by default, but promote a later entry if it
    has more non-null value fields (min/typ/max/unit/condition).
    """
    _STRIP_PUNCT = re.compile(r'[^\w\s]')
    seen: Dict[str, int] = {}
    out:  List[Dict]     = []

    for p in params:
        raw = (p.get("parameter") or "").strip()
        key = _STRIP_PUNCT.sub('', re.sub(r'\s+', ' ', raw.lower())).strip()
        if not key:
            out.append(p)
            continue
        if key not in seen:
            seen[key] = len(out)
            out.append(p)
        else:
            idx           = seen[key]
            existing_score = sum(1 for k in ("min", "typ", "max", "unit", "condition")
                                 if out[idx].get(k))
            new_score      = sum(1 for k in ("min", "typ", "max", "unit", "condition")
                                 if p.get(k))
            if new_score > existing_score:
                out[idx] = p

    return out


# =============================================================================
# Pipeline מלא — מחבר את כל השלבים
# =============================================================================

class PDFInferencePipeline:

    def __init__(
        self,
        input_dir:   Path,
        output_dir:  Path,
        aligner_dir: Path,
        model_path:  Path,
        ner_mode:    str = "auto",
    ):
        self.input_dir   = input_dir
        self.output_dir  = output_dir
        self.aligner_dir = aligner_dir

        log.info("מאתחל PDFConverter…")
        self.converter = PDFConverter()

        log.info("מאתחל DatasheetHTMLPreprocessor…")
        self.preprocessor = DatasheetHTMLPreprocessor()

        log.info("מאתחל NERModel…")
        self.ner = NERModel(model_path=model_path, mode=ner_mode)

    def run(self):
        self.output_dir.mkdir(parents=True, exist_ok=True)
        pdf_files = sorted(self.input_dir.glob("*.pdf"))
        if not pdf_files:
            log.warning(f"לא נמצאו PDFs ב-{self.input_dir}")
            return

        log.info(f"\n{'='*60}")
        log.info(f"מעבד {len(pdf_files)} PDFs → {self.output_dir}")
        log.info(f"{'='*60}\n")

        summary = {"ok": 0, "failed": 0, "files": []}
        for i, pdf_path in enumerate(pdf_files, 1):
            log.info(f"[{i}/{len(pdf_files)}] {pdf_path.name}")
            try:
                out_json = self._process_one(pdf_path)
                summary["ok"] += 1
                summary["files"].append(str(out_json))
            except Exception:
                log.error(traceback.format_exc())
                summary["failed"] += 1

        log.info(f"\n{'='*60}")
        log.info(f"הושלם: {summary['ok']} הצליחו | {summary['failed']} נכשלו")
        (self.output_dir / "_summary.json").write_text(
            json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8"
        )

    def _process_one(self, pdf_path: Path) -> Path:
        stem     = pdf_path.stem
        file_dir = self.output_dir / stem
        file_dir.mkdir(exist_ok=True)

        shutil.copy2(str(pdf_path), str(file_dir / pdf_path.name))

        # ── שלב 1: PDF → HTML גולמי ───────────────────────────────────
        log.info(f"  [1/5] PDF → HTML גולמי…")
        raw_html = self.converter.convert(pdf_path)
        (file_dir / f"{stem}.raw.html").write_text(raw_html, encoding="utf-8")
        log.info(f"        {len(raw_html)//1024}KB")

        # ── תיקונים 1+3+4: סינון עמודים ──────────────────────────────
        log.info(f"  [2/5] סינון עמודים…")
        filtered_html, filter_stats = filter_html_pages(raw_html)
        (file_dir / f"{stem}.filtered.html").write_text(filtered_html, encoding="utf-8")
        log.info(f"        נשמרו {filter_stats['kept_pages']}/{filter_stats['total_pages']} עמודים "
                 f"| legal={filter_stats['legal_removed']} "
                 f"| no_elec={filter_stats['no_elec_removed']} "
                 f"| rotated_paras={filter_stats['rotated_paras_removed']}")

        # ── תיקון 2: Preprocessor עם keywords מורחב ──────────────────
        log.info(f"  [3/5] Preprocessor…")
        clean_html, params_pp, diag = self.preprocessor.process(filtered_html)
        (file_dir / f"{stem}.clean.html").write_text(clean_html, encoding="utf-8")
        log.info(f"        cid={diag['cid_removed']}  params_preprocessor={diag['params_found']}")

        # ── שלב 4: validity filter + dedup ───────────────────────
        log.info(f"  [4/5] validity filter…")
        params_pp = [p for p in params_pp if _is_valid_parameter(p)]
        before_dedup = len(params_pp)
        params_pp = _dedup_params(params_pp)
        if len(params_pp) < before_dedup:
            log.info(f"        dedup: {before_dedup} → {len(params_pp)} params "
                     f"(הוסרו {before_dedup - len(params_pp)} כפולים)")
        log.info(f"        preprocessor: {len(params_pp)} params")

        # ── שלב 5: NER filter ────────────────────────────────────
        # NER acts as a pure inclusion filter: preprocessor params whose row contains
        # a PARAMETER tag are kept with their original values intact.
        # Rows where NER predicts only O (non-electrical content) are dropped.
        # Fallback to full preprocessor output if NER keeps fewer than ⅓ of params.
        log.info(f"  [5/5] NER filter…")
        if params_pp and self.ner.model is not None:
            ner_samples = _build_ner_from_pp(params_pp)
            ner_samples = self.ner.predict(ner_samples)

            ner_params: List[Dict] = []
            _PARAM_TAGS = {"B-PARAMETER", "I-PARAMETER"}
            for sample in ner_samples:
                pred   = sample["pred_tags"]
                base   = sample["_param_base_idx"]
                starts = sample["_row_starts"]
                ends   = sample["_row_ends"]
                for j, (rs, re) in enumerate(zip(starts, ends)):
                    # Keep param if any token in its row carries a PARAMETER tag
                    if any(pred[k] in _PARAM_TAGS for k in range(rs, min(re, len(pred)))):
                        ner_params.append(params_pp[base + j])

            fallback_threshold = max(1, len(params_pp) // 3)
            if len(ner_params) >= fallback_threshold:
                parameters = ner_params
                log.info(f"        NER: {len(params_pp)} → {len(parameters)} params")
            else:
                log.warning(f"        NER: {len(ner_params)}/{len(params_pp)} — below threshold, fallback to preprocessor")
                parameters = params_pp
        else:
            parameters = params_pp

        pp_relations = _parameters_to_relations(parameters)
        log.info(f"        final: {len(parameters)} params | {len(pp_relations)} relations")

        result = {
            "source_pdf":          pdf_path.name,
            "parameters":          parameters,
            "total_found":         len(parameters),
            "preprocessor_params": params_pp,
            "relations":           pp_relations,
            "filter_stats":        filter_stats,
            "diagnostics":         diag,
        }
        json_path = file_dir / f"{stem}.json"
        json_path.write_text(
            json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        log.info(f"  → {file_dir}\n")
        return json_path


# =============================================================================
# Entry point
# =============================================================================

if __name__ == "__main__":
    pipeline = PDFInferencePipeline(
        input_dir   = INPUT_DIR,
        output_dir  = OUTPUT_DIR,
        aligner_dir = ALIGNER_DIR,
        model_path  = MODEL_PATH,
        ner_mode    = NER_MODE,
    )
    pipeline.run()
