"""
Real-World Benchmark Evaluation
================================
Compares model extraction output (JSON) against gold annotations.

Three evaluation tiers:
  Tier 1 — Discovery:  Was the parameter found at all? (name match)
  Tier 2 — Values:     Was the numeric value correct? (±5% tolerance)
  Tier 3 — Complete:   Name + value + unit all correct

Usage:
  python evaluate_benchmark.py
"""
import sys, json, re, os
sys.stdout.reconfigure(encoding='utf-8')
from pathlib import Path

BASE       = Path(r'C:\Users\nivsa\Generation of Synthetic Training Data\embedded')
GOLD_FILE  = BASE / 'benchmark' / 'benchmark_gold.json'
PRED_DIR   = BASE / 'output_results_benchmark'

VALUE_TOL  = 0.10   # 10% tolerance for numeric comparison


# ---------------------------------------------------------------------------
# Text normalisation helpers
# ---------------------------------------------------------------------------

_EVAL_KNOWN_WORDS = {
    "supply", "voltage", "current", "power", "input", "output", "offset",
    "bias", "noise", "gain", "bandwidth", "common", "mode", "rejection",
    "ratio", "slew", "rate", "quiescent", "thermal", "resistance", "drain",
    "gate", "source", "base", "collector", "emitter", "forward", "reverse",
    "breakdown", "saturation", "cutoff", "leakage", "storage", "junction",
    "ambient", "case", "dissipation", "frequency", "response", "settling",
    "time", "delay", "rise", "fall", "turn", "short", "circuit", "open",
    "loop", "closed", "unity", "phase", "margin", "ripple", "regulation",
    "dropout", "inhibit", "enable", "adjust", "reference", "sense",
    "duration", "consumption", "characteristic", "range", "swing",
    "transient", "average", "drift", "temperature", "operating",
    "differential", "large", "signal", "continuous", "pulsed", "peak",
    "recovery", "propagation", "voltage", "static", "dynamic",
}

def _expand_runon(word: str) -> str:
    """Greedily split a lowercase concatenated word into known subwords."""
    if not word or re.search(r"[^a-z]", word):
        return word
    parts, pos = [], 0
    while pos < len(word):
        matched = False
        for wlen in range(min(15, len(word) - pos), 2, -1):
            if word[pos:pos + wlen] in _EVAL_KNOWN_WORDS:
                parts.append(word[pos:pos + wlen])
                pos += wlen
                matched = True
                break
        if not matched:
            if parts:
                parts[-1] += word[pos]
            else:
                parts.append(word[pos])
            pos += 1
    return " ".join(parts)

def _norm_text(s: str) -> str:
    """Lowercase, collapse whitespace, strip punctuation edges; expand runon words."""
    if not s:
        return ''
    s = s.lower().strip()
    s = re.sub(r'[^\w\s]', ' ', s)
    s = re.sub(r'\s+', ' ', s).strip()
    # Expand single-token runon words (e.g. "moderejectionratio" → "mode rejection ratio")
    tokens = s.split()
    expanded = [_expand_runon(t) if len(t) > 8 else t for t in tokens]
    s = re.sub(r'\s+', ' ', ' '.join(expanded)).strip()
    return s

def _norm_unit(u: str) -> str:
    if not u:
        return ''
    u = u.strip()
    replacements = [
        ('°c/w', 'degc/w'), ('°c / w', 'degc/w'), ('c/w', 'degc/w'),
        ('°c', 'degc'), ('degc', 'degc'),
        ('µ', 'u'), ('μ', 'u'), ('ω', 'ohm'), ('ω', 'ohm'),
        ('mohm', 'mohm'), ('mω', 'mohm'), ('kohm', 'kohm'),
        ('v/µs', 'v/us'), ('v/μs', 'v/us'),
    ]
    u_low = u.lower()
    for src, dst in replacements:
        u_low = u_low.replace(src, dst)
    return u_low.strip()

def _parse_number(s: str):
    """Extract a single float from a string. Returns None if not parseable."""
    if not s:
        return None
    s = str(s).strip()
    # Handle ± prefix (use absolute value for comparison)
    s = s.replace('±', '').replace('+/-', '').strip()
    # Handle ranges like "0.5 to 1.0" — take first number
    s = re.split(r'\s+to\s+', s)[0].strip()
    # Extract first numeric token
    m = re.search(r'[+-]?\d+\.?\d*(?:[eE][+-]?\d+)?', s)
    if m:
        try:
            return float(m.group())
        except ValueError:
            return None
    return None

def _values_match(pred_val: str, gold_val: str, tol=VALUE_TOL) -> bool:
    """Numeric match within tolerance, or exact string match."""
    if pred_val is None and gold_val is None:
        return True
    if pred_val is None or gold_val is None:
        return False
    p = _parse_number(pred_val)
    g = _parse_number(gold_val)
    if p is not None and g is not None:
        if g == 0:
            return abs(p) < 1e-9
        return abs(p - g) / abs(g) <= tol
    # Fall back to normalised string comparison
    return _norm_text(str(pred_val)) == _norm_text(str(gold_val))


def _value_in_gold_range(pred_vals: dict, gold_vals: dict, margin: float = 0.05) -> bool:
    """B4 — Range-aware check (general).

    When gold specifies at least two of {min, typ, max}, any predicted value
    that falls within the implied range counts as correct.  This handles the
    common case where extraction picks a valid operating point that differs
    from the canonical value but is still in-spec.

    Implied ranges:
      min + max  → [min, max]
      min + typ  → [min, typ]
      typ + max  → [typ, max]

    Works for any component/parameter type — no hardcoded tolerances.
    """
    g_min = _parse_number(gold_vals.get('min'))
    g_typ = _parse_number(gold_vals.get('typ'))
    g_max = _parse_number(gold_vals.get('max'))

    # Build the tightest range from whichever two bounds are available
    candidates = [v for v in (g_min, g_typ, g_max) if v is not None]
    if len(candidates) < 2:
        return False   # only one point — _values_match already handles it
    lo, hi = min(candidates), max(candidates)
    if lo == hi:
        return False   # degenerate
    lo_m = lo - abs(lo) * margin
    hi_m = hi + abs(hi) * margin
    for pv in (pred_vals.get('min'), pred_vals.get('typ'), pred_vals.get('max')):
        p = _parse_number(pv)
        if p is not None and lo_m <= p <= hi_m:
            return True
    return False

def _units_match(pred_unit: str, gold_aliases: list) -> bool:
    p = _norm_unit(pred_unit or '')
    return p in [_norm_unit(a) for a in gold_aliases] or p == ''

_TERMINAL_WORDS = {
    "drain", "gate", "source", "emitter", "base", "collector",
    "anode", "cathode", "input", "output", "junction", "case", "ambient",
}

def _name_match(pred_name: str, gold_aliases: list) -> bool:
    """Word-overlap match: ≥60% of gold alias words found in prediction.

    Terminal-word guard: if a gold alias contains terminal words (drain/gate/
    emitter/etc.), all such words must also appear in the prediction.
    This prevents 'Gate-Source Voltage' from matching 'Drain-Source Voltage'.
    """
    pred_n = _norm_text(pred_name)
    pred_words = set(pred_n.split())

    for alias in gold_aliases:
        alias_n = _norm_text(alias)
        if not alias_n:
            continue
        alias_words = set(alias_n.split())

        # Terminal-word guard: required terminal words from alias must be in pred
        required_terminals = alias_words & _TERMINAL_WORDS
        if required_terminals and not required_terminals.issubset(pred_words):
            continue  # alias's terminal words absent from prediction — not a match

        # Substring match — only valid when both strings are substantial (>3 chars).
        # Short aliases like "tr", "tf", "VSD" must appear as whole words, not substrings,
        # to avoid "tr" matching inside "transconductance".
        if len(alias_n) > 3 and (alias_n in pred_n or pred_n in alias_n):
            return True
        elif len(alias_n) <= 3:
            # Whole-word match for short aliases
            if re.search(r"(?<![a-z])" + re.escape(alias_n) + r"(?![a-z])", pred_n):
                return True
        # Word overlap
        if not alias_words:
            continue
        overlap = alias_words & pred_words
        if len(overlap) / len(alias_words) >= 0.6:
            return True
    return False


def _name_score(pred_name: str, gold_aliases: list) -> float:
    """Return the best word-overlap score for this prediction against the gold aliases."""
    pred_n = _norm_text(pred_name)
    pred_words = set(pred_n.split())
    best = 0.0
    for alias in gold_aliases:
        alias_n = _norm_text(alias)
        if not alias_n:
            continue
        alias_words = set(alias_n.split())
        if not alias_words:
            continue
        overlap = alias_words & pred_words
        score = len(overlap) / len(alias_words)
        if score > best:
            best = score
    return best


# ---------------------------------------------------------------------------
# Per-component evaluation
# ---------------------------------------------------------------------------

def evaluate_component(gold_comp: dict, pred_params: list) -> dict:
    gold_params = gold_comp['parameters']

    t1_tp = t1_fp = t1_fn = 0
    t2_tp = t2_fp = t2_fn = 0
    t3_tp = t3_fp = t3_fn = 0

    details = []

    # --- For each gold parameter, find best matching prediction ---
    matched_pred_indices = set()

    for gp in gold_params:
        aliases    = gp['aliases'] + [gp['canonical']]
        gold_vals  = {k: gp.get(k) for k in ('min', 'typ', 'max')}
        gold_unit  = gp.get('unit_aliases', [gp.get('unit', '')])

        best_match = None
        best_score = 0.0
        for i, pp in enumerate(pred_params):
            if i in matched_pred_indices:
                continue
            if _name_match(pp.get('parameter', ''), aliases):
                score = _name_score(pp.get('parameter', ''), aliases)
                if score > best_score:
                    best_score = score
                    best_match = (i, pp)

        if best_match is None:
            # MISS
            t1_fn += 1
            t2_fn += 1
            t3_fn += 1
            details.append({
                'gold':   gp['canonical'],
                'pred':   None,
                'tier1':  'MISS',
                'tier2':  'MISS',
                'tier3':  'MISS',
            })
            continue

        idx, pp = best_match
        matched_pred_indices.add(idx)

        # Tier 1 — found
        t1_tp += 1

        # Tier 2 — value check (any of min/typ/max must match)
        pred_vals = {k: pp.get(k) for k in ('min', 'typ', 'max')}
        val_ok = False
        for field in ('min', 'typ', 'max'):
            gv = gold_vals[field]
            pv = pred_vals[field]
            if gv is not None and _values_match(pv, gv):
                val_ok = True
                break
            # Also check if gold has a value and model put it in wrong field
            if gv is not None:
                for pf in ('min', 'typ', 'max'):
                    if _values_match(pred_vals[pf], gv):
                        val_ok = True
                        break

        # B4 — range-aware fallback: if gold defines a range [min, max],
        # accept any predicted value that falls within that range.
        if not val_ok:
            val_ok = _value_in_gold_range(pred_vals, gold_vals)

        if val_ok:
            t2_tp += 1
        else:
            t2_fn += 1

        # Tier 3 — value + unit
        unit_ok = _units_match(pp.get('unit', ''), gold_unit)
        if val_ok and unit_ok:
            t3_tp += 1
        else:
            t3_fn += 1

        details.append({
            'gold':        gp['canonical'],
            'pred':        pp.get('parameter', ''),
            'gold_values': gold_vals,
            'pred_values': pred_vals,
            'gold_unit':   gp.get('unit', ''),
            'pred_unit':   pp.get('unit', ''),
            'tier1':  'HIT',
            'tier2':  'HIT' if val_ok else 'WRONG_VALUE',
            'tier3':  'HIT' if (val_ok and unit_ok) else ('WRONG_UNIT' if val_ok else 'WRONG_VALUE'),
        })

    # FP — predictions that matched nothing
    for i, pp in enumerate(pred_params):
        if i not in matched_pred_indices:
            t1_fp += 1

    def f1(tp, fp, fn):
        p = tp / (tp + fp) if (tp + fp) > 0 else 0.0
        r = tp / (tp + fn) if (tp + fn) > 0 else 0.0
        f = 2 * p * r / (p + r) if (p + r) > 0 else 0.0
        return round(p, 3), round(r, 3), round(f, 3)

    p1, r1, f1_ = f1(t1_tp, t1_fp, t1_fn)
    p2, r2, f2_ = f1(t2_tp, t1_fp, t2_fn)
    p3, r3, f3_ = f1(t3_tp, t1_fp, t3_fn)

    return {
        'component':    gold_comp['id'],
        'type':         gold_comp['type'],
        'gold_count':   len(gold_params),
        'pred_count':   len(pred_params),
        'tier1': {'precision': p1, 'recall': r1, 'f1': f1_,
                  'tp': t1_tp, 'fp': t1_fp, 'fn': t1_fn},
        'tier2': {'precision': p2, 'recall': r2, 'f1': f2_},
        'tier3': {'precision': p3, 'recall': r3, 'f1': f3_},
        'details': details,
    }


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    gold_data = json.loads(GOLD_FILE.read_text(encoding='utf-8'))
    all_results = []

    for gold_comp in gold_data['components']:
        comp_id  = gold_comp['id']
        pred_dir = PRED_DIR / comp_id
        pred_file = pred_dir / f"{comp_id}.json"

        if not pred_file.exists():
            print(f"[SKIP] {comp_id} — prediction file not found")
            continue

        pred_data   = json.loads(pred_file.read_text(encoding='utf-8'))
        pred_params = pred_data.get('parameters', [])

        result = evaluate_component(gold_comp, pred_params)
        all_results.append(result)

    # --- Print report ---
    print('\n' + '=' * 72)
    print('  REAL-WORLD BENCHMARK RESULTS')
    print('=' * 72)
    print(f"  {'Component':<35} {'Type':<8} {'T1-F1':>6} {'T2-F1':>6} {'T3-F1':>6}  {'Gold':>4} {'Pred':>4}")
    print('-' * 72)

    t1_all = t2_all = t3_all = []
    t1_scores = []
    t2_scores = []
    t3_scores = []

    for r in all_results:
        t1_scores.append(r['tier1']['f1'])
        t2_scores.append(r['tier2']['f1'])
        t3_scores.append(r['tier3']['f1'])
        print(f"  {r['component']:<35} {r['type']:<8} "
              f"{r['tier1']['f1']:>6.3f} {r['tier2']['f1']:>6.3f} {r['tier3']['f1']:>6.3f}  "
              f"{r['gold_count']:>4} {r['pred_count']:>4}")

    if t1_scores:
        print('-' * 72)
        avg1 = sum(t1_scores) / len(t1_scores)
        avg2 = sum(t2_scores) / len(t2_scores)
        avg3 = sum(t3_scores) / len(t3_scores)
        print(f"  {'AVERAGE':<44} {avg1:>6.3f} {avg2:>6.3f} {avg3:>6.3f}")

    print('\n' + '=' * 72)
    print('  LEGEND')
    print('  Tier 1 — Discovery:  parameter name found (word-overlap ≥60%)')
    print('  Tier 2 — Values:     name found + numeric value correct (±10%)')
    print('  Tier 3 — Complete:   name + value + unit all correct')
    print('=' * 72)

    # --- Per-component miss report ---
    print('\n--- MISSES & ERRORS PER COMPONENT ---')
    for r in all_results:
        misses  = [d for d in r['details'] if d['tier1'] == 'MISS']
        errors  = [d for d in r['details'] if d['tier1'] == 'HIT' and d['tier3'] != 'HIT']
        if not misses and not errors:
            print(f"\n[{r['type']}] {r['component']} — all OK ✓")
            continue
        print(f"\n[{r['type']}] {r['component']}")
        for d in misses:
            print(f"  MISS        {d['gold']}")
        for d in errors:
            gv = d.get('gold_values', {})
            pv = d.get('pred_values', {})
            gu = d.get('gold_unit', '')
            pu = d.get('pred_unit', '')
            print(f"  {d['tier3']:<12} {d['gold']}")
            print(f"             gold: min={gv.get('min')} typ={gv.get('typ')} max={gv.get('max')} unit={gu}")
            print(f"             pred: min={pv.get('min')} typ={pv.get('typ')} max={pv.get('max')} unit={pu}")

    # --- Save JSON report ---
    out_file = BASE / 'benchmark' / 'evaluation_report.json'
    out_file.parent.mkdir(exist_ok=True)
    report = {
        'summary': {
            'avg_tier1_f1': round(sum(t1_scores)/len(t1_scores), 3) if t1_scores else 0,
            'avg_tier2_f1': round(sum(t2_scores)/len(t2_scores), 3) if t2_scores else 0,
            'avg_tier3_f1': round(sum(t3_scores)/len(t3_scores), 3) if t3_scores else 0,
            'components_evaluated': len(all_results),
        },
        'per_component': all_results,
    }
    out_file.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f'\n[OK] Report saved → {out_file}')


if __name__ == '__main__':
    main()
