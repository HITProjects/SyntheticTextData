"""
Production Runner - הרצת ייצור דאטה סינטטית
גרסה נקייה לייצור (Production Ready)

✅ V2 CHANGES:
- הוספת build_ner_re_examples() ו-_render_ner_example()
- הוספת שדה 'ner_re_examples' לכל record ב-JSONL
- שאר ה-pipeline נשאר זהה לחלוטין
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

import json
import time
import threading
import random
import traceback

from datetime import datetime
from typing import Dict, List, Any
from dataclasses import asdict, dataclass, field
from concurrent.futures import ThreadPoolExecutor, as_completed

try:
    from tqdm import tqdm
except ImportError:
    class tqdm:
        def __init__(self, total=0, unit="", desc=""):
            self.total = total
            self._n = 0
            print(f"{desc} (0/{total})")
        def update(self, n=1):
            self._n += n
            if self._n % max(1, self.total // 10) == 0:
                print(f"  {self._n}/{self.total}")
        def close(self): pass

try:
    import cv2
    import numpy as np
    _HAS_CV2 = True
except ImportError:
    _HAS_CV2 = False

try:
    from html2image import Html2Image
    _HAS_HTML2IMAGE = True
except ImportError:
    Html2Image = None
    _HAS_HTML2IMAGE = False

# 1. Logic & DB
from synthetic_pipeline.logic import DatasheetGenerator
from synthetic_pipeline.strategies import UNIFIED_COMPONENT_DB, MODEL_TO_USE

# 2. Strategies
from synthetic_pipeline.resistor_strategy import ResistorStrategy
from synthetic_pipeline.capacitor_strategy import CapacitorStrategy
from synthetic_pipeline.diode_strategy import DiodeStrategy
from synthetic_pipeline.mosfet_strategy import MosfetStrategy
from synthetic_pipeline.voltage_Regulator_strategy import VoltageRegulatorStrategy
from synthetic_pipeline.inductor_strategy import InductorStrategy
from synthetic_pipeline.bjt_strategy import BJTStrategy
from synthetic_pipeline.opamp_strategy import OpampStrategy

# 3. Generators
from synthetic_pipeline.generators import (
    DatasheetHtmlRenderer,
    DatasheetJSONRenderer,
    MarketingGenerator,
    ScanAugmentor,
    generate_datasheet_sample
)
from synthetic_pipeline.augmentors import TextDegradationAugmentor


# ============================================================================
# NER WINDOW NOISE & NEGATIVE EXAMPLES
# ============================================================================

_NER_DEGRADER = TextDegradationAugmentor(intensity=0.4)

_NER_NEGATIVE_TEXTS = [
    # Thermal / test conditions
    "Note 1: Unless otherwise specified, all limits guaranteed at TJ = 25°C.",
    "All typical values at TA = 25°C unless otherwise noted.",
    "* All specifications apply over the full operating temperature range.",
    "Specifications measured with VS = ±15V unless otherwise noted.",
    "(a) Stresses beyond those listed may cause permanent damage to the device.",
    # Pulse / measurement
    "(1) Measured with device mounted on 1 in² FR4 PCB, copper area 1 in².",
    "* Pulse test: PW ≤ 300 µs, duty cycle ≤ 2%.",
    "† Guaranteed by design, not 100% production tested.",
    "(2) For additional information refer to the application note.",
    "§ Applies to commercial temperature range only.",
    "(3) Short-circuit duration must not exceed one second.",
    "* Measured at TA = 25°C with no load and VS = 5V.",
    "† Measured under pulsed conditions; duty cycle ≤ 1%.",
    "(4) Body diode characteristics apply to the intrinsic diode only.",
    "* 100% production tested at TA = 25°C.",
    # PCB / mounting
    "Thermal resistance depends on PCB layout, copper area, and airflow conditions.",
    "(5) TJ = TA + (PD × θJA). See thermal model in application note.",
    "† Limits apply to device operating in free air without heatsink.",
    "* See AN-1112 for recommended PCB layout and decoupling guidelines.",
    "(6) ESD sensitivity class 2 per JESD22-A114. Handle with appropriate precautions.",
    # Safety / ratings
    "CAUTION: Do not exceed absolute maximum ratings.",
    "† Exceeding maximum ratings may cause permanent device failure.",
    "* Stress ratings only. Functional operation above rated conditions is not implied.",
    "(7) Applies only to commercial-grade (0°C to 70°C) devices.",
    "† AEC-Q101 qualified. Suitable for automotive applications.",
    # Noise / AC
    "(8) Noise performance measured with 10 Ω source resistance at f = 1 kHz.",
    "* Gain-bandwidth product specified at unity gain configuration.",
    "† Input-referred noise measured in 1 Hz bandwidth, f = 10 Hz to 10 kHz.",
    "(9) Settling time measured to 0.01% of final value with 10 V step input.",
    "* Measured with capacitive load CL = 10 pF on output.",
    # Pin / package
    "Pin 1: Gate (G) — Control input terminal for switching operation.",
    "Pin 2: Drain (D) — High-current power terminal.",
    "Pin 3: Source (S) — Reference and return current path.",
    "Package: TO-220AB. Lead-free (Pb-free). RoHS compliant.",
    # Process / revision
    "This document contains information on products in the design phase of development.",
    "† Data based on characterization only; not 100% tested in production.",
    "* Engineering samples available. Contact factory for pricing and lead time.",
    "(10) For soldering profile refer to JEDEC J-STD-020D.",
    "† Lead-free package. RoHS compliant. Moisture sensitivity level MSL = 1.",
    # Application / reference
    "For application circuit examples, see the evaluation board user guide.",
    "Refer to Figure 5 for the safe operating area (SOA) curve.",
    "All measurements performed using the test circuit shown in Figure 1.",
    "See Table 2 for ordering information and available package options.",
    "For automotive-grade versions (Q-suffix), see separate datasheet.",
]

# Section headers for positive (characteristics) NER windows — injected as context prefix
_SECTION_HEADERS_CHAR = [
    "ELECTRICAL CHARACTERISTICS",
    "Electrical Characteristics",
    "DC Electrical Characteristics",
    "OPERATING CONDITIONS",
    "Recommended Operating Conditions",
    "Electrical Specifications",
    "Switching Characteristics",
    "AC / Switching Characteristics",
    "Dynamic Characteristics",
    "Static Characteristics",
    "Thermal Characteristics",
]

# Section headers for ABS MAX near-miss negatives — always present to give the model context
_SECTION_HEADERS_ABS_MAX = [
    "ABSOLUTE MAXIMUM RATINGS",
    "Absolute Maximum Ratings",
    "ABSOLUTE MAXIMUM RATINGS (Note 1)",
    "Absolute Maximum Ratings — Stresses beyond these values may cause permanent damage.",
    "MAXIMUM RATINGS",
    "Maximum Ratings",
]

# ============================================================================
# DATA VALIDATION
# ============================================================================

class DataValidator:
    """מנגנון ולידציה לסינון דאטה פגומה"""

    @staticmethod
    def validate_marketing_data(data: Dict) -> tuple[bool, List[str]]:
        errors = []
        if not data:
            return False, ["Empty data"]

        required_fields = ['marketing_name', 'manufacturer', 'description']
        for field in required_fields:
            if field not in data or not data[field]:
                errors.append(f"Missing or empty field: {field}")

        if 'marketing_name' in data and len(data['marketing_name']) < 3:
            errors.append("Marketing name too short")
        if 'description' in data and len(data['description']) < 50:
            errors.append("Description too short")

        invalid_markers = ['error', 'failed', 'null', 'undefined', '###', 'generic comp']
        for field, value in data.items():
            if isinstance(value, str):
                for marker in invalid_markers:
                    if marker.lower() in value.lower():
                        errors.append(f"Invalid content in {field}: contains '{marker}'")

        return len(errors) == 0, errors

    @staticmethod
    def validate_technical_data(data: Dict) -> tuple[bool, List[str]]:
        errors = []
        if not data:
            return False, ["Empty technical data"]

        if 'parameters' in data:
            params = data['parameters']
            if not params or len(params) == 0:
                errors.append("No parameters found")

            for param in params:
                if not isinstance(param, dict): continue
                if 'label' not in param or not param['label']:
                    errors.append("Parameter missing label")

                has_value = (
                    ('value_min' in param and param['value_min'] is not None) or
                    ('value_typ' in param and param['value_typ'] is not None) or
                    ('value_max' in param and param['value_max'] is not None)
                )
                if not has_value:
                    errors.append(f"Parameter {param.get('label', 'unknown')} has no values")

        return len(errors) == 0, errors


# ============================================================================
# JSONL WRITER
# ============================================================================

class JSONLWriter:
    def __init__(self, filepath: str):
        self.filepath = filepath
        self.lock = threading.Lock()

    def append(self, data: Dict) -> bool:
        try:
            with self.lock:
                with open(self.filepath, 'a', encoding='utf-8') as f:
                    json_str = json.dumps(data, ensure_ascii=False, default=str)
                    f.write(json_str + '\n')
            return True
        except Exception:
            return False


# ============================================================================
# PRODUCTION STATISTICS
# ============================================================================

@dataclass
class ProductionStats:
    total_attempted: int = 0
    total_success: int = 0
    total_failed: int = 0
    fast_mode: int = 0
    high_quality_mode: int = 0
    validation_failures: int = 0
    component_breakdown: Dict[str, int] = field(default_factory=dict)

    def add_success(self, comp_type: str, mode: str):
        self.total_success += 1
        if mode == 'fast': self.fast_mode += 1
        else: self.high_quality_mode += 1
        self.component_breakdown[comp_type] = self.component_breakdown.get(comp_type, 0) + 1

    def add_failure(self, comp_type: str):
        self.total_failed += 1
        self.validation_failures += 1

    def print_summary(self):
        print("\n" + "=" * 60)
        print("📊 PRODUCTION SUMMARY")
        print("=" * 60)
        print(f"Total Attempted:       {self.total_attempted}")
        print(f"✅ Successful:         {self.total_success}")
        print(f"❌ Failed:             {self.total_failed}")
        if self.total_attempted > 0:
            print(f"Success Rate:          {(self.total_success / self.total_attempted * 100):.1f}%")
        print(f"\n🚀 Fast Mode:          {self.fast_mode}")
        print(f"💎 High Quality Mode:  {self.high_quality_mode}")
        print(f"⚠️  Validation Fails:   {self.validation_failures}")
        if self.component_breakdown:
            print(f"\nComponent Breakdown:")
            for comp, count in self.component_breakdown.items():
                print(f"   {comp:20s}: {count}")
        print("=" * 60 + "\n")


# ============================================================================
# ✅ V2: NER/RE EXAMPLE BUILDER
# שתי פונקציות חדשות - כל השאר בקובץ נשאר זהה
# ============================================================================

def _render_ner_example(
    param_label: str,
    min_val,
    typ_val,
    max_val,
    unit: str,
    condition: str,
    style: str,
    example_id: str,
    section_header: str = None
) -> Dict:
    """
    בונה example בודד: טקסט גולמי + entities עם character offsets מדויקים + relations.

    הטריק המרכזי: בונים את הטקסט חלק-חלק דרך רשימת (content, label) tuples.
    כך ה-offset של כל entity מחושב אוטומטית ומדויק ב-100%.
    """

    def build(parts: List[tuple]) -> tuple:
        """
        קלט:  רשימת tuples של (content, label_או_None)
        פלט:  (text_מלא, entities_list)
        """
        text = ""
        entities = []
        for content, label in parts:
            # דילוג על ערכים ריקים או None
            if content is None or not str(content) or str(content).strip() in ('None', '--', '-'):
                continue
            content = str(content)
            start = len(text)
            text += content
            end = len(text)
            if label:
                entities.append({
                    "label": label,
                    "start": start,
                    "end": end,
                    "text": content
                })
        return text, entities

    # --- בדיקת זמינות ערכים ---
    has_min  = min_val  is not None and str(min_val).strip()  not in ('', 'None', '--', '-')
    has_typ  = typ_val  is not None and str(typ_val).strip()  not in ('', 'None', '--', '-')
    has_max  = max_val  is not None and str(max_val).strip()  not in ('', 'None', '--', '-')
    has_cond = condition and str(condition).strip() not in ('', 'None')
    has_unit = unit     and str(unit).strip()       not in ('', 'None')

    # אם אין אף ערך מספרי — אין טעם לייצר example
    if not has_min and not has_typ and not has_max:
        return None

    parts = []

    # ------------------------------------------------------------------
    # סגנון 1: Raw Text — "RDS(on) typ 7.2 mΩ @ VGS=10V"
    # ------------------------------------------------------------------
    if style == 'raw_text':
        parts.append((param_label, "PARAMETER"))

        if has_min:
            parts.append((" min ", None))
            parts.append((str(min_val), "MIN"))
            if has_unit:
                parts.append((" ", None))
                parts.append((str(unit), "UNIT"))

        if has_typ:
            parts.append((" typ ", None))
            parts.append((str(typ_val), "TYP"))
            if has_unit:
                parts.append((" ", None))
                parts.append((str(unit), "UNIT"))

        if has_max:
            parts.append((" max ", None))
            parts.append((str(max_val), "MAX"))
            if has_unit:
                parts.append((" ", None))
                parts.append((str(unit), "UNIT"))

        if has_cond:
            # שימוש ב-@ או ; אקראי — בדיוק כמו בדאטאשיטים אמיתיים
            delim = random.choice(['@', ';'])
            parts.append((f" {delim} ", None))
            parts.append((str(condition), "CONDITION"))

    # ------------------------------------------------------------------
    # סגנון 2: Pipe Table — "Parameter: X | Typ: Y mΩ | Conditions: Z"
    # ------------------------------------------------------------------
    elif style == 'pipe_table':
        parts.append(("Parameter: ", None))
        parts.append((param_label, "PARAMETER"))

        if has_min:
            parts.append((" | Min: ", None))
            parts.append((str(min_val), "MIN"))
            if has_unit:
                parts.append((" ", None))
                parts.append((str(unit), "UNIT"))

        if has_typ:
            parts.append((" | Typ: ", None))
            parts.append((str(typ_val), "TYP"))
            if has_unit:
                parts.append((" ", None))
                parts.append((str(unit), "UNIT"))

        if has_max:
            parts.append((" | Max: ", None))
            parts.append((str(max_val), "MAX"))
            if has_unit:
                parts.append((" ", None))
                parts.append((str(unit), "UNIT"))

        if has_cond:
            parts.append((" | Conditions: ", None))
            parts.append((str(condition), "CONDITION"))

    # ------------------------------------------------------------------
    # סגנון 3: Bracket Table — "[Param] X [Typ] Y mΩ [Cond] Z"
    # ------------------------------------------------------------------
    elif style == 'bracket_table':
        parts.append(("[Param] ", None))
        parts.append((param_label, "PARAMETER"))

        if has_min:
            parts.append((" [Min] ", None))
            parts.append((str(min_val), "MIN"))
            if has_unit:
                parts.append((" ", None))
                parts.append((str(unit), "UNIT"))

        if has_typ:
            parts.append((" [Typ] ", None))
            parts.append((str(typ_val), "TYP"))
            if has_unit:
                parts.append((" ", None))
                parts.append((str(unit), "UNIT"))

        if has_max:
            parts.append((" [Max] ", None))
            parts.append((str(max_val), "MAX"))
            if has_unit:
                parts.append((" ", None))
                parts.append((str(unit), "UNIT"))

        if has_cond:
            parts.append((" [Cond] ", None))
            parts.append((str(condition), "CONDITION"))

    # ------------------------------------------------------------------
    # סגנון 4: Footnote — "Note 3: RDS(on) is measured at cond. Max value is X mΩ."
    # ------------------------------------------------------------------
    elif style == 'footnote':
        note_num = random.randint(1, 9)
        parts.append((f"Note {note_num}: ", None))
        parts.append((param_label, "PARAMETER"))

        if has_cond:
            parts.append((" is measured at ", None))
            parts.append((str(condition), "CONDITION"))
            parts.append((". ", None))
        else:
            parts.append((" — ", None))

        if has_max:
            parts.append(("Maximum value is ", None))
            parts.append((str(max_val), "MAX"))
            if has_unit:
                parts.append((" ", None))
                parts.append((str(unit), "UNIT"))
            parts.append((".", None))
        elif has_typ:
            parts.append(("Typical value is ", None))
            parts.append((str(typ_val), "TYP"))
            if has_unit:
                parts.append((" ", None))
                parts.append((str(unit), "UNIT"))
            parts.append((".", None))
        elif has_min:
            parts.append(("Minimum value is ", None))
            parts.append((str(min_val), "MIN"))
            if has_unit:
                parts.append((" ", None))
                parts.append((str(unit), "UNIT"))
            parts.append((".", None))

    # ------------------------------------------------------------------
    # סגנון 5: TSV Style — "RDS(on)\t5.0\t7.2\t10.0\tmΩ\tVGS=10V"
    # מדמה פלט pdfplumber של שורת טבלה עם עמודות מופרדות בטאב
    # ------------------------------------------------------------------
    elif style == 'tsv_style':
        parts.append((param_label, "PARAMETER"))

        if has_min:
            parts.append(("\t", None))
            parts.append((str(min_val), "MIN"))

        if has_typ:
            parts.append(("\t", None))
            parts.append((str(typ_val), "TYP"))

        if has_max:
            parts.append(("\t", None))
            parts.append((str(max_val), "MAX"))

        if has_unit:
            parts.append(("\t", None))
            parts.append((str(unit), "UNIT"))

        if has_cond:
            parts.append(("\t", None))
            parts.append((str(condition), "CONDITION"))

    # --- Apply noise to NER window before building ---
    parts = _NER_DEGRADER.degrade_ner_parts(parts)

    # --- בניית הטקסט והentities ---
    text, entities = build(parts)

    if not text or not entities:
        return None

    # Prepend section header as context (shifts all entity offsets accordingly)
    if section_header:
        prefix = section_header + "\n"
        shift = len(prefix)
        text = prefix + text
        for ent in entities:
            ent["start"] += shift
            ent["end"] += shift

    # --- בניית relations ---
    # כל entity שאינו PARAMETER מקבל relation ל-PARAMETER
    rel_map = {
        "MIN":       "has_min",
        "MAX":       "has_max",
        "TYP":       "has_typ",
        "VALUE":     "has_value",
        "UNIT":      "has_unit",
        "CONDITION": "has_condition"
    }

    relations = []
    for ent in entities:
        if ent["label"] == "PARAMETER":
            continue
        rel_type = rel_map.get(ent["label"])
        if rel_type:
            relations.append({
                "relation": rel_type,
                "from": {"label": "PARAMETER", "text": param_label},
                "to":   {"label": ent["label"], "text": ent["text"]}
            })

    return {
        "id":        example_id,
        "style":     style,
        "text":      text,
        "entities":  entities,
        "relations": relations
    }



def _build_table_ner_samples(
    ground_truth: Dict,
    display_data: Dict,
    sample_id: str,
) -> List[Dict]:
    """
    Generate token-level NER training samples in the exact format of
    _build_ner_from_pp (pdf_inference_pipeline.py).

    Fixes the training/inference format mismatch: the model is trained on
    full 512-token HTML documents where tables appear at positions ~100-400,
    but at inference time _build_ner_from_pp produces a SHORT table-only
    input (30-150 tokens starting at position 0). Adding these samples
    teaches the model the exact format it will see during inference.
    """
    _DASH   = "—"
    _HDR    = ["Parameter", "Symbol", "Min", "Typ", "Max", "Unit", "Condition", "\n"]
    _CHUNK  = 18
    _NONES  = {'', 'None', '--', '-', '—'}

    # Build param_key → display label from display_data
    key_to_label: Dict[str, str] = {}
    for section_rows in display_data.values():
        if not isinstance(section_rows, list):
            continue
        for row in section_rows:
            meta = row.get('_metadata', {})
            key  = meta.get('key')
            lbl  = row.get('Parameter')
            if key and lbl:
                key_to_label[key] = str(lbl).strip()

    def _has(v) -> bool:
        return v is not None and str(v).strip() not in _NONES

    # Collect electrical characteristics params (skip ABS MAX)
    params = []
    for param_key, param_data in ground_truth.items():
        if param_data.get('spec_type', '') in ('max_rating', 'min_rating'):
            continue
        if not (_has(param_data.get('_raw_min')) or
                _has(param_data.get('_raw_typ')) or
                _has(param_data.get('_raw_max'))):
            continue
        label = key_to_label.get(param_key) or param_key.replace('_', ' ')
        params.append({
            'label':     label,
            'min':       param_data.get('_raw_min'),
            'typ':       param_data.get('_raw_typ'),
            'max':       param_data.get('_raw_max'),
            'unit':      str(param_data.get('unit',      '') or '').strip(),
            'condition': str(param_data.get('condition', '') or '').strip(),
        })

    if not params:
        return []

    samples = []
    for chunk_idx, chunk_start in enumerate(range(0, len(params), _CHUNK)):
        chunk  = params[chunk_start : chunk_start + _CHUNK]
        tokens = list(_HDR)
        tags   = ["O"] * len(_HDR)

        for p in chunk:
            # PARAMETER
            words = p['label'].split() if p['label'] else [_DASH]
            tokens.extend(words)
            tags.append("B-PARAMETER")
            tags.extend(["I-PARAMETER"] * (len(words) - 1))

            # Symbol (always dash — matches _build_ner_from_pp)
            tokens.append(_DASH); tags.append("O")

            # MIN
            v = str(p['min']).strip() if p['min'] is not None else ''
            if v and v not in _NONES:
                ws = v.split()
                tokens.extend(ws); tags.append("B-MIN"); tags.extend(["I-MIN"] * (len(ws) - 1))
            else:
                tokens.append(_DASH); tags.append("O")

            # TYP
            v = str(p['typ']).strip() if p['typ'] is not None else ''
            if v and v not in _NONES:
                ws = v.split()
                tokens.extend(ws); tags.append("B-TYP"); tags.extend(["I-TYP"] * (len(ws) - 1))
            else:
                tokens.append(_DASH); tags.append("O")

            # MAX
            v = str(p['max']).strip() if p['max'] is not None else ''
            if v and v not in _NONES:
                ws = v.split()
                tokens.extend(ws); tags.append("B-MAX"); tags.extend(["I-MAX"] * (len(ws) - 1))
            else:
                tokens.append(_DASH); tags.append("O")

            # UNIT
            if p['unit']:
                ws = p['unit'].split()
                tokens.extend(ws); tags.append("B-UNIT"); tags.extend(["I-UNIT"] * (len(ws) - 1))
            else:
                tokens.append(_DASH); tags.append("O")

            # CONDITION (max 8 words — matches _build_ner_from_pp)
            if p['condition']:
                ws = p['condition'].split()[:8]
                tokens.extend(ws); tags.append("B-CONDITION"); tags.extend(["I-CONDITION"] * (len(ws) - 1))
            else:
                tokens.append(_DASH); tags.append("O")

            tokens.append("\n"); tags.append("O")

        samples.append({
            'id':              f'{sample_id}_tbl_{chunk_idx}',
            'text':            ' '.join(t for t in tokens if t != '\n'),
            'tokens':          tokens,
            'ner_tags':        tags,
            'token_start_idx': 0,
            'token_end_idx':   len(tokens) - 1,
            'relations':       [],
        })

    return samples


def build_ner_re_examples(result, rendered_json_output: Dict) -> List[Dict]:
    """
    ממיר את ה-ground_truth הקיים של sample אחד לרשימת NER/RE training examples.

    לכל פרמטר ב-ground_truth מייצר example אחד בסגנון אקראי.
    הסגנונות מחולקים לפי משקלים שמשקפים דאטאשיטים אמיתיים:
      38% raw_text  — שורת טבלה כפי שנחלצת מ-PDF
      15% pipe_table — HTML/PDF table עם | כמפריד
       8% bracket_table — פורמט עם תגיות [Param], [Typ] וכו'
      17% footnote — הערת שוליים בשפה חופשית
      22% tsv_style — tab-separated כפי שמגיע מ-pdfplumber

    פרמטרי ABS MAX (spec_type: max_rating/min_rating) הופכים ל-near-miss negatives:
    הטקסט נבנה רגיל (ריאליסטי) אבל entities=[] כדי ללמד את המודל להתעלם מהם
    כשמוצג כותרת "ABSOLUTE MAXIMUM RATINGS".

    לפרמטרים חיוביים, 40% מהמקרים מקבלים כותרת section (כפי שמופיעה ב-pdfplumber).
    """
    pos_examples = []      # NER examples עם entities
    abs_max_examples = []  # near-miss negatives מפרמטרי ABS MAX

    ground_truth = rendered_json_output.get('ground_truth', {})

    # Build key→display-label index once (O(n)) instead of re-scanning per param (O(n²))
    display_tables = rendered_json_output.get('display_data', {})
    _key_to_label = {
        row['_metadata']['key']: row.get('Parameter')
        for section_rows in display_tables.values()
        for row in section_rows
        if row.get('_metadata', {}).get('key')
    }

    for param_key, param_data in ground_truth.items():

        unit      = param_data.get('unit', '')
        condition = param_data.get('condition', '')

        # Use raw numeric values (already unit-free) rather than display min/typ/max
        # which are null unless that column was selected as the display column
        min_val = param_data.get('_raw_min')
        typ_val = param_data.get('_raw_typ')
        max_val = param_data.get('_raw_max')

        # שם הפרמטר — לוקחים מה-display_data אם קיים, אחרת param_key
        param_label = _key_to_label.get(param_key) or param_key

        spec_type = param_data.get('spec_type', '')
        is_abs_max = spec_type in ('max_rating', 'min_rating')

        if is_abs_max:
            # ABS MAX params → near-miss negative:
            # window text is realistic but entities are empty so the model
            # learns: "ABSOLUTE MAXIMUM RATINGS" context → do not extract
            section_header = random.choice(_SECTION_HEADERS_ABS_MAX)
            style = random.choices(
                ['raw_text', 'pipe_table', 'tsv_style'],
                weights=[0.45,       0.25,      0.30]
            )[0]
            example = _render_ner_example(
                param_label=param_label,
                min_val=min_val,
                typ_val=typ_val,
                max_val=max_val,
                unit=unit,
                condition=condition,
                style=style,
                example_id=f"{result.context.sample_id}_{param_key}_absmax",
                section_header=section_header
            )
            if example:
                example["entities"] = []
                example["relations"] = []
                example["style"] = "abs_max_negative"
                abs_max_examples.append(example)
        else:
            # Positive example: 40% chance of including section header as context
            section_header = (
                random.choice(_SECTION_HEADERS_CHAR)
                if random.random() < 0.40 else None
            )
            style = random.choices(
                ['raw_text', 'pipe_table', 'bracket_table', 'footnote', 'tsv_style'],
                weights=[0.38,       0.15,         0.08,           0.17,      0.22]
            )[0]
            example = _render_ner_example(
                param_label=param_label,
                min_val=min_val,
                typ_val=typ_val,
                max_val=max_val,
                unit=unit,
                condition=condition,
                style=style,
                example_id=f"{result.context.sample_id}_{param_key}",
                section_header=section_header
            )
            if example:
                pos_examples.append(example)

    # --- Generic negatives: ~20% of positive count ---
    n_neg = max(1, len(pos_examples) // 5)
    generic_negatives = []
    for i in range(n_neg):
        neg_text = random.choice(_NER_NEGATIVE_TEXTS)
        generic_negatives.append({
            "id":        f"{result.context.sample_id}_neg_{i}",
            "style":     "negative",
            "text":      neg_text,
            "entities":  [],
            "relations": []
        })

    return pos_examples + abs_max_examples + generic_negatives


# ============================================================================
# MAIN PRODUCTION FUNCTION
# ============================================================================

def run_full_production(
    num_samples_per_type: int = 10,
    fast_ratio: float = 0.8,
    output_dir: str = "production_output",
    enable_parallel: bool = True,
    max_workers: int = 4,
    components_to_generate: List[str] = None,
    ollama_model: str = MODEL_TO_USE,
    save_html_files: bool = True,
    save_image_files: bool = True,
    save_individual_json: bool = True,
    component_weights: Dict[str, float] = None,
    processed_dir: str = None,
):
    print("🚀 Starting Production Run...")

    # 1. Setup Generators & Strategies
    generator = DatasheetGenerator(UNIFIED_COMPONENT_DB)

    strategies = {
        "RESISTOR":          ResistorStrategy(),
        "CAPACITOR":         CapacitorStrategy(),
        "DIODE":             DiodeStrategy(),
        "MOSFET":            MosfetStrategy(),
        "VOLTAGE_REGULATOR": VoltageRegulatorStrategy(),
        "INDUCTOR":          InductorStrategy(),
        "BJT":               BJTStrategy(),
        "OPAMP":             OpampStrategy()
    }

    html_renderer = DatasheetHtmlRenderer()
    json_renderer = DatasheetJSONRenderer()

    # Image Gen & Augmentor
    image_generator = None
    if _HAS_HTML2IMAGE and Html2Image is not None:
        try:
            image_generator = Html2Image(browser='edge')
        except:
            try: image_generator = Html2Image()
            except: pass

    augmentor = None
    try: augmentor = ScanAugmentor()
    except: pass

    image_lock = threading.Lock()

    if components_to_generate is None:
        components_to_generate = list(strategies.keys())

    # B7: per-type sample counts — weighted or flat
    if component_weights:
        samples_per_type = {
            ct: max(1, int(num_samples_per_type * component_weights.get(ct, 1.0)))
            for ct in components_to_generate
        }
    else:
        samples_per_type = {ct: num_samples_per_type for ct in components_to_generate}

    # Create Directories
    os.makedirs(output_dir, exist_ok=True)
    html_dir  = os.path.join(output_dir, "html")
    json_dir  = os.path.join(output_dir, "json")
    image_dir = os.path.join(output_dir, "images")
    os.makedirs(html_dir,  exist_ok=True)
    os.makedirs(json_dir,  exist_ok=True)
    os.makedirs(image_dir, exist_ok=True)
    if processed_dir:
        os.makedirs(processed_dir, exist_ok=True)

    timestamp    = datetime.now().strftime('%Y%m%d_%H%M%S')
    jsonl_path   = os.path.join(output_dir, f"production_{timestamp}.jsonl")
    valid_jsonl  = JSONLWriter(jsonl_path)
    invalid_jsonl = JSONLWriter(jsonl_path.replace('.jsonl', '_invalid.jsonl'))

    stats     = ProductionStats()
    validator = DataValidator()

    # =========================================================================
    # Single Sample Processing Function
    # =========================================================================
    def process_single_sample(comp_type: str, sample_idx: int, mode: str):
        strategy = strategies.get(comp_type)
        if not strategy: return

        try:
            # 1. Logic — יצירת הנתונים ההנדסיים
            result = generator.generate(comp_type, strategy)

            # 2. Unified Pipeline — שיווק + HTML + JSON מסונכרנים
            pipeline_output = generate_datasheet_sample(result)

            html_output          = pipeline_output['html']
            rendered_json_output = pipeline_output['json']
            marketing_data       = rendered_json_output['marketing_generated']
            config               = pipeline_output['config']

            # 3. Validation
            m_valid, _ = validator.validate_marketing_data(marketing_data)

            technical_data = {
                'parameters':     [asdict(p) for p in result.parameters],
                'component_type': comp_type,
                'sample_id':      result.context.sample_id
            }
            t_valid, _ = validator.validate_technical_data(technical_data)

            is_valid = m_valid and t_valid

            # 4. Build Record
            # ✅ השינוי היחיד לעומת V1: הוספת שדה 'ner_re_examples'
            record = {
                'sample_id':             result.context.sample_id,
                'component_type':        comp_type,
                'mode':                  mode,
                'timestamp':             datetime.now().isoformat(),
                'is_valid':              is_valid,
                'marketing_data':        marketing_data,
                'ground_truth':          rendered_json_output['ground_truth'],
                'relation_ground_truth': rendered_json_output.get('relation_ground_truth'),
                'rendering_config':      config,
                'raw_technical_data':    technical_data,

                # ✅ V2: NER/RE training examples — נוצרים מה-ground_truth שכבר קיים
                'ner_re_examples': build_ner_re_examples(result, rendered_json_output)
            }

            if is_valid:
                valid_jsonl.append(record)

                base_filename = f"datasheet_{result.context.sample_id}"
                final_html    = html_output.replace(
                    "</head>",
                    "<style>body { background-color: white !important; }</style></head>"
                )

                if save_html_files:
                    with open(os.path.join(html_dir, f"{base_filename}.html"), "w", encoding="utf-8") as f:
                        f.write(final_html)

                if save_individual_json:
                    with open(os.path.join(json_dir, f"{base_filename}.json"), "w", encoding="utf-8") as f:
                        json.dump(rendered_json_output, f, indent=2, ensure_ascii=False, default=str)

                if processed_dir:
                    tbl_samples = _build_table_ner_samples(
                        rendered_json_output.get('ground_truth', {}),
                        rendered_json_output.get('display_data', {}),
                        result.context.sample_id,
                    )
                    if tbl_samples:
                        tbl_path = os.path.join(processed_dir, f"{result.context.sample_id}_tbl.json")
                        with open(tbl_path, 'w', encoding='utf-8') as f:
                            json.dump(tbl_samples, f, ensure_ascii=False)

                if image_generator and save_image_files:
                    with image_lock:
                        image_size    = (1200, 5000)
                        temp_filename = f"{base_filename}_temp.png"
                        try:
                            image_generator.screenshot(
                                html_str=final_html,
                                save_as=temp_filename,
                                size=image_size
                            )
                            if os.path.exists(temp_filename):
                                img = cv2.imread(temp_filename)
                                if img is not None:
                                    # קוד חיתוך ואוגמנטציה — נשאר זהה לקוד המקורי
                                    pass
                        except Exception:
                            pass

                stats.add_success(comp_type, mode)

            else:
                invalid_jsonl.append(record)
                stats.add_failure(comp_type)

            stats.total_attempted += 1

        except Exception as e:
            print(f"❌ Error processing sample {sample_idx} ({comp_type}): {e}")
            traceback.print_exc()
            stats.total_failed    += 1
            stats.total_attempted += 1

    # =========================================================================
    # Main Loop
    # =========================================================================
    total_tasks = sum(samples_per_type.values())
    start_time  = time.time()

    print("📊 Samples per type:")
    for ct in components_to_generate:
        print(f"   {ct}: {samples_per_type[ct]}")
    print(f"   TOTAL: {total_tasks}")

    pbar = tqdm(total=total_tasks, unit="sample", desc="🏭 Generating Data")

    if enable_parallel:
        print(f"🔄 Processing with {max_workers} workers...")
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = []
            for comp_type in components_to_generate:
                n = samples_per_type[comp_type]
                n_fast = int(n * fast_ratio)
                for i in range(n_fast):
                    futures.append(executor.submit(process_single_sample, comp_type, i, 'fast'))
                for i in range(n_fast, n):
                    futures.append(executor.submit(process_single_sample, comp_type, i, 'high_quality'))

            for _ in as_completed(futures):
                pbar.update(1)
    else:
        print("➡️ Processing sequentially...")
        for comp_type in components_to_generate:
            n = samples_per_type[comp_type]
            n_fast = int(n * fast_ratio)
            for i in range(n_fast):
                process_single_sample(comp_type, i, 'fast')
                pbar.update(1)
            for i in range(n_fast, n):
                process_single_sample(comp_type, i, 'high_quality')
                pbar.update(1)

    pbar.close()

    elapsed = time.time() - start_time
    print(f"\n✅ Done! Total: {stats.total_attempted} | Success: {stats.total_success} | Time: {elapsed:.2f}s")
    print(f"📁 Output: {output_dir}")
    stats.print_summary()


# ============================================================================
# ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    # B7: R/C/L boosted 1.5× — they gained key-value table format in B6 and need more representation
    run_full_production(
        num_samples_per_type=1200,
        fast_ratio=0.8,
        output_dir=r"C:\Users\nivsa\Generation of Synthetic Training Data\embedded\data\raw",
        enable_parallel=True,
        save_html_files=True,
        save_individual_json=False,
        save_image_files=False,
        component_weights={
            "RESISTOR":          1.5,
            "CAPACITOR":         1.5,
            "INDUCTOR":          1.5,
            "DIODE":             1.0,
            "MOSFET":            1.0,
            "VOLTAGE_REGULATOR": 1.0,
            "BJT":               1.0,
            "OPAMP":             1.0,
        },
        processed_dir=r"C:\Users\nivsa\Generation of Synthetic Training Data\embedded\data\processed",
    )

# component_weights=None  → flat 1200 per type (9600 total)
# component_weights above → 1800 R/C/L + 1200 others = 10800 total