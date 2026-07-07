
import os
import glob
import json
import re
import time
from typing import List, Dict, Tuple, Any, Optional
from bs4 import BeautifulSoup, NavigableString, Tag
from dataclasses import dataclass, field
import html


GENERIC_LABELS = {"PARAMETER", "VALUE", "MIN", "MAX", "TYP", "UNIT", "CONDITION", "SYMBOL"}

RELATION_TYPES = {
    "has_value":     "has_value",
    "has_unit":      "has_unit",
    "has_min":       "has_min",
    "has_max":       "has_max",
    "has_typ":       "has_typ",
    "has_condition": "has_condition",
}


@dataclass
class Span:
    start: int
    end:   int
    label: str
    text:  str


@dataclass
class Token:
    text:       str
    start:      int
    end:        int
    span_label: str = "O"

def pre_process_text(text: str) -> Tuple[str, List[int]]:
    """
    מחזיר (processed_text, offset_map)
    offset_map[i] = מיקום ב-processed_text של תו i ב-raw_text
    """
    # החלפות שלא משנות אורך
    text = re.sub(r'(\w)-\s*\n\s*(\w)', r'\1\2', text)  # hyphen join - מקצר, נשאר ראשון

    result = []
    offset_map = []
    i = 0
    while i < len(text):
        c = text[i]
        pos = len(result)
        next_c = text[i+1] if i+1 < len(text) else ''

        # bA → b A
        if c.islower() and next_c.isupper():
            result.append(c); offset_map.append(pos)
            result.append(' ')  # רווח מוסף - לא ממופה
            i += 1; continue

        # AABb → AA Bb
        if c.isupper() and next_c.isupper() and i+2 < len(text) and text[i+2].islower():
            result.append(c); offset_map.append(pos)
            i += 1; continue

        # 5V → 5 V
        if c.isdigit() and (next_c.isalpha() or next_c in 'µΩ°'):
            result.append(c); offset_map.append(pos)
            result.append(' ')
            i += 1; continue

        # V5 → V 5
        if c.isalpha() and next_c.isdigit():
            result.append(c); offset_map.append(pos)
            result.append(' ')
            i += 1; continue

        result.append(c); offset_map.append(pos)
        i += 1

    return ''.join(result), offset_map
    
class PreprocessingEngine:

    def __init__(self, tokenizer=None):
        self.custom_tokenizer = tokenizer
        self._reset()

    def _reset(self):
        """Reset all mutable state so the same instance can be reused safely."""
        self.spans:      List[Span]  = []
        self.clean_text: str         = ""
        self.tokens:     List[Token] = []

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def process(self, html_content: str, jsonl_relations: List[Dict] = None) -> List[Dict]:
        self._reset()                                   # FIX #2: safe reuse
        html_content = html.unescape(html_content)

        self.clean_text, self.spans = self._extract_text_and_spans(html_content)
        self.tokens = self._tokenize(self.clean_text)
        self._assign_bio_tags()
        samples = self._sliding_window(max_tokens=512, overlap=50)

        if jsonl_relations:
            samples = self._add_relations(samples, jsonl_relations)

        return samples

    # ------------------------------------------------------------------
    # DOM → clean text + spans
    # ------------------------------------------------------------------

    def _extract_text_and_spans(self, html_content: str) -> Tuple[str, List[Span]]:
        soup = BeautifulSoup(html_content, 'html.parser')

        segments: List[Tuple[str, Optional[str]]] = []
        self._walk_dom(soup, segments)

        raw_text_parts: List[str] = []
        pending_spans:  List[Tuple[int, int, str]] = []
        cursor = 0

        for text_frag, label in segments:
            text_frag = self._clean_artifacts(text_frag)
            if not text_frag:
                continue
            raw_start = cursor
            raw_text_parts.append(text_frag)
            cursor += len(text_frag)
            if label is not None:
                pending_spans.append((raw_start, cursor, label))

        raw_text = "".join(raw_text_parts)
        preprocessed, pre_map = pre_process_text(raw_text)                    # שורה 108
        clean_text, ws_map = self._normalize_whitespace_with_map(preprocessed) # שורה 109

        def combined_map(raw_idx: int) -> int:                                 # שורות 111-113
            pre_idx = pre_map[min(raw_idx, len(pre_map) - 1)]
            return ws_map[min(pre_idx, len(ws_map) - 1)]

        spans: List[Span] = []
        for raw_start, raw_end, label in pending_spans:
            norm_start = combined_map(raw_start)                               # שורה 114
            norm_end   = combined_map(raw_end - 1) + 1   

            surface = clean_text[norm_start:norm_end]
            if surface.strip():
                spans.append(Span(
                    start=norm_start,
                    end=norm_end,
                    label=self._normalize_label(label),
                    text=surface,
                ))

        return clean_text, spans

    def _walk_dom(self, node, segments: List[Tuple[str, Optional[str]]], in_table: bool = False):
        if isinstance(node, NavigableString):
            text = str(node)
            if text:
                segments.append((text, None))
            return

        tag_name = node.name if hasattr(node, 'name') else None

        if tag_name in ('style', 'script', 'head'):
            return

        # Labeled span — emit as a single tagged segment
        if tag_name == 'span' and node.get('data-label'):
            label = node.get('data-label')
            sub_segments: List[Tuple[str, Optional[str]]] = []
            for child in node.children:
                self._walk_dom(child, sub_segments, in_table)
            span_text = "".join(s for s, _ in sub_segments)
            # FIX: clean newlines inside span content
            span_text = re.sub(r'\s+', ' ', span_text).strip()
            if span_text:
                # FIX Bug 6: use a single space separator between adjacent spans
                # (instead of \n) so that spans within the same table cell do not
                # generate 2-4 consecutive \n tokens each.  Row boundaries are
                # already provided by the <tr> block-tag handler below.
                if segments and segments[-1] not in ((' ', None), ('\n', None)):
                    segments.append((' ', None))
                segments.append((span_text, label))
                segments.append((' ', None))
            return

        # -----------------------------------------------------------------
        # FIX (data-leakage): Tables are treated like plain PDF text.
        # Cells are separated by a space; rows by a newline.
        # NO header injection — the model must learn from structure alone.
        # -----------------------------------------------------------------
        BLOCK_TAGS  = {'p', 'div', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
                       'li', 'br', 'thead', 'tbody', 'tfoot', 'tr', 'table'}
        SPACE_TAGS  = {'td', 'th'}

        is_block = tag_name in BLOCK_TAGS if tag_name else False
        is_space  = tag_name in SPACE_TAGS if tag_name else False

        if is_block and tag_name != 'br':
            segments.append(('\n', None))
        elif is_space:
            segments.append((' ', None))

        for child in node.children:
            self._walk_dom(child, segments, in_table=True if tag_name == 'table' else in_table)

        if is_block and tag_name != 'br':
            segments.append(('\n', None))
        elif is_space:
            segments.append((' ', None))

    # ------------------------------------------------------------------
    # Text Normalization
    # ------------------------------------------------------------------

    @staticmethod
    def _clean_artifacts(text: str) -> str:
        # 1. Normalize special characters to prevent [UNK] tokens.
        #    Order matters: longer/compound patterns before single-char ones.
        replacements = [
            # Compound patterns first (avoid partial replacement)
            ("V/µs",  "V/us"),
            ("V/μs",  "V/us"),
            ("µV",    "uV"),
            ("µA",    "uA"),
            ("µF",    "uF"),
            ("µs",    "us"),
            ("µH",    "uH"),
            # Greek / special single chars
            ("µ",     "u"),
            ("μ",     "u"),
            ("√",     "sqrt"),
            ("Ω",     "Ohm"),
            ("≤",     "<="),
            ("≥",     ">="),
            ("°C",    "degC"),
            ("° C",   "degC"),
            ("±",     "+/-"),
        ]
        for old, new in replacements:
            text = text.replace(old, new)

        # 2. Remove Python list notation: ['-65 to 150'] → -65 to 150
        text = re.sub(r"\[(['\"])(.*?)\1\]", r'\2', text)

        # FIX #4: safer deduplication — only collapse exact full-word repetitions
        # like "nHnH" but not numeric sequences like "1010" or short tokens.
        # Require at least 3 chars to avoid false positives on short tokens.
        text = re.sub(r'\b([A-Za-z])\1\b', r'\1', text)   # ← חדש: VV→V
        text = re.sub(r'\b(\S{3,20})\1\b', r'\1', text)

        # FIX (unit splitting): pre_process_text מפצל digit→alpha ו-alpha→digit,
        # מה שגורם ל-mW → m W, pF → p F, nA → n A וכו'.
        # מגן על יחידות SI compound על ידי החלפתן בצורה שלא תיפצל.
        # הסדר חשוב: ארוך לפני קצר (mOhm לפני Ohm, MHz לפני Hz).
        _SI_UNITS = [
            # התנגדות תרמית
            (r'\bdegC/W\b',   'degCperW'),
            # תדר
            (r'\bGHz\b',      'GHz'),
            (r'\bMHz\b',      'MHz'),
            (r'\bkHz\b',      'kHz'),
            # מתח
            (r'\bmV\b',       'mV'),
            (r'\buV\b',       'uV'),
            (r'\bnV\b',       'nV'),
            # זרם
            (r'\bmA\b',       'mA'),
            (r'\buA\b',       'uA'),
            (r'\bnA\b',       'nA'),
            (r'\bpA\b',       'pA'),
            # הספק
            (r'\bmW\b',       'mW'),
            (r'\buW\b',       'uW'),
            # קיבול
            (r'\bpF\b',       'pF'),
            (r'\bnF\b',       'nF'),
            (r'\buF\b',       'uF'),
            # השראות
            (r'\bnH\b',       'nH'),
            (r'\buH\b',       'uH'),
            (r'\bmH\b',       'mH'),
            # זמן
            (r'\bns\b',       'ns'),
            (r'\bus\b',       'us'),
            (r'\bms\b',       'ms'),
            # התנגדות
            (r'\bmOhm\b',     'mOhm'),
            (r'\bkOhm\b',     'kOhm'),
            (r'\bMOhm\b',     'MOhm'),
        ]
        for pattern, replacement in _SI_UNITS:
            text = re.sub(pattern, replacement, text)

        return text

    # ------------------------------------------------------------------
    # Whitespace normalization with offset map
    # ------------------------------------------------------------------

    def _normalize_whitespace_with_map(self, raw: str) -> Tuple[str, List[int]]:
        """
        Collapse runs of plain spaces to one space.
        Collapse runs of newlines to at most 2 (structural row boundary).
        Preserve \\t (structural separator).

        FIX #1: offset_map is built *after* accounting for leading whitespace
        removal so that every raw-index maps correctly to the final string.
        FIX Bug 6: cap consecutive \\n at 2 to prevent O-token flooding between
        value spans.  With the old code, 4-6 \\n tokens between every tagged value
        pushed the O-ratio to ~92%, making NER training unstable.
        """
        norm_chars:  List[str] = []
        raw_to_norm: List[int] = []   # raw index → norm index (pre-strip)
        norm_idx = 0
        i = 0

        while i < len(raw):
            ch = raw[i]
            if ch == ' ':
                raw_to_norm.append(norm_idx)
                # Collapse: skip if previous emitted char was whitespace
                if not norm_chars or norm_chars[-1] in (' ', '\t', '\n'):
                    pass
                else:
                    norm_chars.append(' ')
                    norm_idx += 1
            elif ch == '\n':
                raw_to_norm.append(norm_idx)
                # FIX Bug 6: allow at most 2 consecutive \n characters so that
                # row boundaries remain visible but value spans are not separated
                # by long runs of blank-line tokens.
                recent_newlines = sum(1 for c in norm_chars[-2:] if c == '\n')
                if recent_newlines < 2:
                    norm_chars.append('\n')
                    norm_idx += 1
            else:
                norm_chars.append(ch)
                raw_to_norm.append(norm_idx)
                norm_idx += 1
            i += 1

        joined = "".join(norm_chars)
        result = joined.strip()

        # How many characters were removed from the left by strip()
        leading_removed = len(joined) - len(joined.lstrip())

        # Shift every entry so index 0 in `result` is the first real char
        offset_map = [max(0, v - leading_removed) for v in raw_to_norm]

        return result, offset_map

    # ------------------------------------------------------------------
    # Label normalization
    # ------------------------------------------------------------------

    def _normalize_label(self, data_label: str) -> str:
        """
        Maps a data-label attribute to one of the GENERIC_LABELS.

        FIX: The original code mapped any `_value` suffix to VALUE.
        But the HTML renderer uses `_value` for ABS_MAX single-column params
        whose ground truth is actually MAX_ONLY.  We therefore map `_value`
        to MAX (same semantics: the one permitted value is the upper limit).

        Additional suffixes added: _rating, _limit (also ABS_MAX conventions).
        """
        label = data_label.upper().strip()

        if label in GENERIC_LABELS:
            return label

        for suffix, canon in [('_MIN', 'MIN'), ('_MINIMUM', 'MIN'),
                               ('_MAX', 'MAX'), ('_MAXIMUM', 'MAX'),
                               ('_TYP', 'TYP'), ('_TYPICAL', 'TYP'),
                               # FIX: _value / _val / _rating / _limit → MAX
                               # (abs-max params use a single "Value" column
                               #  which semantically is the maximum rating)
                               ('_VALUE', 'MAX'), ('_VAL', 'MAX'),
                               ('_RATING', 'MAX'), ('_LIMIT', 'MAX')]:
            if label.endswith(suffix):
                return canon

        if 'UNIT'      in label:                             return 'UNIT'
        if 'CONDITION' in label or label.endswith('_COND'): return 'CONDITION'
        if 'SYMBOL'    in label or label.endswith('_SYM'):  return 'SYMBOL'
        if any(kw in label for kw in ('PARAM', 'NAME', 'PIN')):
            return 'PARAMETER'

        return 'VALUE'

    # ------------------------------------------------------------------
    # Tokenization
    # ------------------------------------------------------------------

    def _tokenize(self, text: str) -> List[Token]:
        if self.custom_tokenizer:
            return self._tokenize_custom(text)
        return self._tokenize_simple(text)

    def _tokenize_simple(self, text: str) -> List[Token]:
        tokens: List[Token] = []
        pattern = re.compile(
            r'(\t|\n)'
            # Scientific notation
            r'|([+-]?(?:\d+\.?\d*|\.\d+)[eE][+-]?\d+)'
            # Plain numbers (including sign)
            r'|([+-]?(?:\d+\.?\d*|\.\d+))'
            # Compound units with slash and sqrt: V/us, nV/sqrtHz, mV/us, A/us
            r'|([a-zA-ZÀ-ÿµ°Ωθ]+/(?:sqrt|√)?[a-zA-ZÀ-ÿµ°Ωθ]+)'
            # Words (possibly hyphenated or with slash between pure-alpha parts)
            r'|([a-zA-ZÀ-ÿµ°Ω±%θ~]+(?:[-/][a-zA-ZÀ-ÿθ~]+)*)'
            # Any other non-whitespace single character
            r'|([^\w\s])'
        )
        for m in pattern.finditer(text):
            tok_text = m.group(0)
            if tok_text.strip() == '' and tok_text not in ('\t', '\n'):
                continue
            tokens.append(Token(text=tok_text, start=m.start(), end=m.end()))
        return tokens

    def _tokenize_custom(self, text: str) -> List[Token]:
        tok    = self.custom_tokenizer
        tokens: List[Token] = []

        if hasattr(tok, 'tokenize'):
            cursor = 0
            for rt in tok.tokenize(text):
                clean = rt.replace('##', '')
                pos   = text.find(clean, cursor)
                if pos == -1:
                    continue
                tokens.append(Token(text=rt, start=pos, end=pos + len(clean)))
                cursor = pos + len(clean)
        elif callable(tok):
            cursor = 0
            for rt in tok(text):
                pos = text.find(rt, cursor)
                if pos == -1:
                    continue
                tokens.append(Token(text=rt, start=pos, end=pos + len(rt)))
                cursor = pos + len(rt)

        return tokens

    # ------------------------------------------------------------------
    # BIO tag assignment
    # ------------------------------------------------------------------

    def _assign_bio_tags(self):
        """
        FIX: Complete rewrite of BIO assignment.

        Problems fixed vs. original:
        1. Post-hoc B→I fixup loop was inside the per-token loop — it ran on
           every O token and could corrupt already-set labels.  Removed entirely;
           the invariant is maintained inline.
        2. span_idx was never rewound when a token fell *before* the current span
           (possible after whitespace normalisation shifts boundaries). Added a
           backward scan guard.
        3. A token whose char-range overlaps with a span that starts strictly
           after the token's start was incorrectly tagged.  Now we only tag when
           token.start >= sp.start AND token.end <= sp.end (already correct) but
           the span_idx advancement logic could skip spans.  Rewritten to be
           unambiguous.
        4. current_span_id was never reset when moving to a new non-overlapping
           span, causing the *first* token of a new span to get I- instead of B-.
           Fixed by resetting inside the O branch AND before advancing span_idx.
        """
        span_list = sorted(self.spans, key=lambda s: s.start)
        n_spans   = len(span_list)

        # Build a fast lookup: for each token position find the active span (or None)
        # This avoids all the cursor-drift issues with the original single scan.
        span_idx = 0
        current_span_id: Optional[int] = None

        for token in self.tokens:
            # Advance past spans that end before this token starts
            while span_idx < n_spans and span_list[span_idx].end <= token.start:
                span_idx += 1

            if span_idx < n_spans:
                sp = span_list[span_idx]
                # Token is fully inside the span
                if token.start >= sp.start and token.end <= sp.end:
                    span_id = id(sp)
                    if span_id != current_span_id:
                        # New span: always B-
                        token.span_label = f"B-{sp.label}"
                        current_span_id  = span_id
                    else:
                        # Continuation of same span: I-
                        token.span_label = f"I-{sp.label}"
                    continue

            # Token does not belong to any span
            token.span_label    = "O"
            current_span_id     = None  # FIX: reset so next span starts with B-
    # ------------------------------------------------------------------
    # Sliding window  (stride = max_tokens − overlap)
    # ------------------------------------------------------------------

    def _sliding_window(self, max_tokens: int = 512, overlap: int = 50) -> List[Dict]:
        if not self.tokens:
            return []

        stride  = max_tokens - overlap
        samples = []
        n       = len(self.tokens)
        start   = 0

        while start < n:
            end    = min(start + max_tokens, n)
            window = self.tokens[start:end]

            ner_tags = [t.span_label for t in window]

            # FIX: Any I- tag that appears without a preceding B- of the same
            # type within THIS window must be promoted to B-.  The original code
            # only fixed the very first token; tags at positions > 0 could still
            # carry a dangling I- from the overlap region.
            active_label: Optional[str] = None
            for idx, tag in enumerate(ner_tags):
                if tag == 'O':
                    active_label = None
                elif tag.startswith('B-'):
                    active_label = tag[2:]
                elif tag.startswith('I-'):
                    entity = tag[2:]
                    if active_label != entity:
                        # Promote to B-: this is the first token of a new entity
                        # in this window even though globally it was a continuation
                        ner_tags[idx] = f'B-{entity}'
                        active_label  = entity

            # FIX #3: store only the text slice for this window, not the full doc
            window_text = self.clean_text[window[0].start: window[-1].end]

            # Quality filter: skip windows with extreme label density or
            # orphaned-condition windows (no PARAMETER anchor).
            total_w  = len(ner_tags)
            labeled  = sum(1 for t in ner_tags if t != 'O')
            density  = labeled / total_w if total_w else 0
            b_cond   = sum(1 for t in ner_tags if t == 'B-CONDITION')
            b_param  = sum(1 for t in ner_tags if t == 'B-PARAMETER')

            if density > 0.60:
                # Window is almost all labels — would bias model toward over-tagging
                if end >= n: break
                start += stride
                continue
            if b_cond > 4 and b_param == 0:
                # Notes-only window: many conditions but no parameter anchors
                if end >= n: break
                start += stride
                continue

            samples.append({
                'id':              f'sample_{len(samples)}',
                'text':            window_text,
                'tokens':          [t.text for t in window],
                'ner_tags':        ner_tags,
                'token_start_idx': start,
                'token_end_idx':   end - 1,
                'relations':       [],
            })

            if end >= n:
                break
            start += stride

        return samples

    # ------------------------------------------------------------------
    # Relation extraction
    # ------------------------------------------------------------------

    def _add_relations(self, samples: List[Dict], jsonl_relations: List[Dict]) -> List[Dict]:
        if not jsonl_relations:
            return samples

        processed: List[Dict] = []
        for rel in jsonl_relations:
            subj = rel.get('subject', '')
            pred = rel.get('predicate', '')
            obj  = rel.get('object', '')

            if isinstance(subj, list): subj = ' '.join(str(x) for x in subj)
            if isinstance(obj,  list): obj  = ' '.join(str(x) for x in obj)

            subj, obj = str(subj).strip(), str(obj).strip()

            # Skip self-referential relations
            if subj and obj and subj != obj:
                processed.append({
                    'subject':   subj,
                    'predicate': self._map_predicate(pred),
                    'object':    obj,
                })

        if not processed:
            return samples

        def normalize(s: str) -> str:
            """
            Canonical form for phrase matching.
            Applies the same character substitutions as _clean_artifacts
            (µ→u, Ω→Ohm, etc.) BEFORE stripping non-alphanumeric characters
            so that "V/µs" in the GT and "V/us" in the token text both
            normalise to "vus" instead of "vs" vs "vus".
            """
            s = self._clean_artifacts(s)
            return re.sub(r'[^a-z0-9]', '', s.lower())

        # Tokens we never want as part of a head or tail span
        _NOISE_TOKENS = {'\n', '\t', '—', '-', '–', '', ' '}

        def is_clean_span(token_list: List[str]) -> bool:
            """True if the span contains at least one real content token."""
            return any(t not in _NOISE_TOKENS for t in token_list)

        def trim_span(indices: List[int], toks: List[str]) -> List[int]:
            """
            Remove leading/trailing noise tokens (newlines, em-dashes) from a
            span's index list so that e.g. [\\n, \\n, Supply, Voltage, Range]
            becomes [Supply, Voltage, Range] and ['—', '1.61'] becomes ['1.61'].
            """
            # trim leading noise
            start = 0
            while start < len(indices) and toks[indices[start]] in _NOISE_TOKENS:
                start += 1
            # trim trailing noise
            end = len(indices)
            while end > start and toks[indices[end - 1]] in _NOISE_TOKENS:
                end -= 1
            return indices[start:end] if start < end else indices

        # Build phrase index: norm_phrase → [(sample_idx, [token_indices])]
        # Index ALL tokens so injected-param (NLG) subjects can be found.
        #
        # FIX New Bug A+B: trim tokens that contribute NOTHING to the normalized
        # form before indexing.
        #
        # Root cause: normalize() strips ALL non-alphanumeric chars, so
        #   normalize(') 11.7 mOhm') == normalize('11.7 mOhm')
        # Any n-gram starting/ending with a pure-punctuation token (like the ')'
        # at the end of Symbol "R_DS(on)") gets indexed under the same key as the
        # clean phrase.  At match time these extra tokens end up in the relation
        # tail/head — e.g. tail=[')','11.7','m','Ohm'] instead of ['11.7','m','Ohm'].
        #
        # Fix: trim leading/trailing tokens whose normalized form is empty (i.e. they
        # contain no alphanumeric characters) before indexing.  Store only the trimmed
        # indices so duplicates collapse to a single canonical entry.
        _ALPHA_RE = re.compile(r'[a-zA-Z0-9]')

        def alphanum_trim(indices: List[int], toks: List[str]) -> List[int]:
            """Remove leading/trailing tokens with no alphanumeric content."""
            start = 0
            while start < len(indices) and not _ALPHA_RE.search(str(toks[indices[start]])):
                start += 1
            end = len(indices)
            while end > start and not _ALPHA_RE.search(str(toks[indices[end - 1]])):
                end -= 1
            return indices[start:end] if start < end else []

        phrase_index: Dict[str, List[Tuple[int, List[int]]]] = {}

        for si, sample in enumerate(samples):
            toks      = sample['tokens']
            max_ngram = min(10, len(toks))
            for n in range(1, max_ngram + 1):
                for i in range(len(toks) - n + 1):
                    raw_indices  = list(range(i, i + n))
                    # Trim tokens with no alphanumeric content from edges
                    trim_indices = alphanum_trim(raw_indices, toks)
                    if not trim_indices:
                        continue
                    trim_toks = [toks[j] for j in trim_indices]
                    if not is_clean_span(trim_toks):
                        continue
                    phrase_norm = normalize(' '.join(trim_toks))
                    if not phrase_norm:
                        continue
                    # Store trimmed indices — ')11.7mOhm' and '11.7mOhm' now
                    # produce identical entries and deduplicate naturally
                    entry = (si, trim_indices)
                    if entry not in phrase_index.get(phrase_norm, []):
                        phrase_index.setdefault(phrase_norm, []).append(entry)

        for rel in processed:
            subj_norm = normalize(rel['subject'])
            obj_norm  = normalize(rel['object'])

            # Guard: subject == object at the normalised level
            if subj_norm == obj_norm:
                continue

            for sample_idx, raw_subj_indices in phrase_index.get(subj_norm, []):
                toks = samples[sample_idx]['tokens']

                # Trim noise from subject span
                subj_indices = trim_span(raw_subj_indices, toks)
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
                _, raw_obj_indices = min(
                    obj_matches, key=lambda x: abs(x[1][0] - subj_end)
                )

                # Trim noise from object span
                obj_indices = trim_span(raw_obj_indices, toks)
                if not obj_indices:
                    continue

                # Guard: index-level self-reference (after trimming)
                if subj_indices == obj_indices:
                    continue

                # Guard: subject span must contain a tagged token
                # (prevents metadata triples like OPAMP→QFN matching random text)
                sample_tags = samples[sample_idx]['ner_tags']
                if not any(sample_tags[i] != 'O' for i in subj_indices):
                    continue

                new_rel = {
                    'head': subj_indices,
                    'type': rel['predicate'],
                    'tail': obj_indices,
                }
                if new_rel not in samples[sample_idx]['relations']:
                    samples[sample_idx]['relations'].append(new_rel)

        return samples

    def _map_predicate(self, raw_pred: str) -> str:
        p = raw_pred.lower().strip()
        if 'unit' in p: return 'has_unit'
        if 'min'  in p: return 'has_min'
        if 'max'  in p: return 'has_max'
        if 'typ'  in p: return 'has_typ'
        if 'cond' in p: return 'has_condition'
        return 'has_value'


# ---------------------------------------------------------------------------
# File-level helpers
# ---------------------------------------------------------------------------

def process_file(
    html_path:   str,
    jsonl_path:  str = None,
    output_path: str = None,
) -> List[Dict]:
    with open(html_path, 'r', encoding='utf-8') as f:
        html_content = f.read()

    relations: List[Dict] = []
    if jsonl_path and os.path.exists(jsonl_path):
        with open(jsonl_path, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    relations.append(json.loads(line))

    engine  = PreprocessingEngine()
    samples = engine.process(html_content, relations)

    if output_path:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(samples, f, indent=2, ensure_ascii=False)

    return samples


def run_batch_processing(
    input_html_dir:     str,
    input_jsonl_dir:    str,
    output_dataset_dir: str,
    debug_interval:     int = 100,
):
    print(f"\n{'='*70}\nBATCH PROCESSING START\n{'='*70}")
    os.makedirs(output_dataset_dir, exist_ok=True)

    print("\n[PHASE 1] Loading JSONL relations...")
    relations_map: Dict[str, List[Dict]] = {}
    for jsonl_file in glob.glob(os.path.join(input_jsonl_dir, "*.jsonl")):
        with open(jsonl_file, 'r', encoding='utf-8') as f:
            for line in f:
                if not line.strip():
                    continue
                data = json.loads(line)
                # FIX Bug 3: generators.py writes "id" but older code read "sample_id".
                # Accept both so that no relations are silently dropped.
                sid  = data.get('sample_id') or data.get('id')
                rels = data.get('relation_ground_truth', [])
                if sid:
                    relations_map[sid] = rels
    print(f"  [OK] {len(relations_map)} samples with relations loaded.")

    html_files = glob.glob(os.path.join(input_html_dir, "*.html"))
    print(f"\n[PHASE 2] Found {len(html_files)} HTML files.")
    print(f"\n[PHASE 3] Processing...")

    success = errors = 0
    phase_start = time.time()

    for idx, html_path in enumerate(html_files, 1):
        fname      = os.path.basename(html_path)
        sample_id  = fname.replace('datasheet_', '').replace('.html', '')
        sample_relations = relations_map.get(sample_id, [])

        if idx % debug_interval == 0 or idx == 1:
            elapsed = time.time() - phase_start
            avg = elapsed / idx
            eta = (len(html_files) - idx) * avg
            print(f"\n  [{idx}/{len(html_files)}] {idx/len(html_files)*100:.1f}% | "
                  f"elapsed={elapsed:.1f}s avg={avg:.3f}s/file ETA={eta:.1f}s "
                  f"ok={success} err={errors}")

        try:
            with open(html_path, 'r', encoding='utf-8') as f:
                html_content = f.read()

            engine  = PreprocessingEngine()
            samples = engine.process(html_content, sample_relations)

            out_path = os.path.join(output_dataset_dir, f"{sample_id}.json")
            with open(out_path, 'w', encoding='utf-8') as f:
                json.dump(samples, f, indent=2, ensure_ascii=False)

            success += 1
        except Exception as exc:
            errors += 1
            print(f"  [ERROR] {fname}: {exc}")

    total = time.time() - phase_start
    print(f"\n{'='*70}")
    print(f"DONE — {success}/{len(html_files)} files OK | {errors} errors")
    print(f"Total: {total:.1f}s  avg: {total/max(len(html_files),1):.3f}s/file")
    print(f"Output: {output_dataset_dir}\n{'='*70}\n")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def generate_val_split(
    data_dir: str,
    val_save: str,
    val_split: float = 0.2,
    seed: int = 42,
):
    import torch
    files = sorted(glob.glob(os.path.join(data_dir, "*.json")))
    if not files:
        print(f"[WARN] No JSON files found in {data_dir} — skipping val split.")
        return

    samples = []
    for path in files:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, list):
            samples.extend(data)
        else:
            samples.append(data)

    n        = len(samples)
    val_size = max(1, int(n * val_split))
    perm     = torch.randperm(n, generator=torch.Generator().manual_seed(seed)).tolist()
    val_samples = [samples[i] for i in perm[:val_size]]

    os.makedirs(os.path.dirname(val_save), exist_ok=True)
    with open(val_save, "w", encoding="utf-8") as f:
        json.dump(val_samples, f, ensure_ascii=False, indent=2)

    print(f"val.json saved: {len(val_samples)} samples -> {val_save}")


if __name__ == "__main__":
    INPUT_HTML_DIR  = r"C:\Users\nivsa\Generation of Synthetic Training Data\embedded\data\raw\html"
    INPUT_JSONL_DIR = r"C:\Users\nivsa\Generation of Synthetic Training Data\embedded\data\raw"
    OUTPUT_DIR      = r"C:\Users\nivsa\Generation of Synthetic Training Data\embedded\data\processed"
    VAL_SAVE        = r"C:\Users\nivsa\Generation of Synthetic Training Data\embedded\data\splits\val.json"

    run_batch_processing(INPUT_HTML_DIR, INPUT_JSONL_DIR, OUTPUT_DIR, debug_interval=100)
    generate_val_split(OUTPUT_DIR, VAL_SAVE)
