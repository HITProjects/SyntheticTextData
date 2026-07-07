"""
Validates that all GeneratedParameter objects satisfy the 3 data-quality rules:
  1. value_min/typ/max are scalar numbers (never list or list-string)
  2. condition is a real measurement condition, not a structural column header
  3. label is a clean Title Case string (no merged lowercase, no newlines)

Usage:
    from synthetic_pipeline.strategies_validator import run_validation
    ok = run_validation(all_results)   # returns True if 0 errors
"""

from typing import List

STRUCTURAL_CONDITIONS = {
    "Max", "Min", "Typ", "Nominal", "Nom", "Typical", "Value",
    "Guaranteed", "Absolute Max", "Rating", "Limit", "Average",
    "Maximum", "Minimum",
}


def validate_param(param) -> List[str]:
    errors = []

    for field in ("value_min", "value_typ", "value_max"):
        v = getattr(param, field, None)
        if isinstance(v, list):
            errors.append(f"{field} is a list: {v}")
        if isinstance(v, str) and v.strip().startswith("["):
            errors.append(f"{field} is list-string: {v}")
        if isinstance(v, str) and "to" in v:
            core = v.replace(" ", "").replace("to", "").replace(".", "")
            if core.lstrip("-").isdigit():
                errors.append(f"{field} is range-string: '{v}'")
        if isinstance(v, dict):
            errors.append(f"{field} is dict (unresolved limits): {list(v.keys())[:3]}")

    cond = getattr(param, "condition", "") or ""
    if cond.strip() in STRUCTURAL_CONDITIONS:
        errors.append(f"condition is structural: '{cond}'")

    label = getattr(param, "label", "") or ""
    if "\n" in label:
        errors.append(f"label has newline: '{label}'")
    if label == label.lower() and " " not in label and len(label) > 5:
        errors.append(f"label is merged lowercase: '{label}'")
    BAD_PREFIXES = ("from", "to", "at", "for", "with", "by")
    if label.lower().split(" ")[0] in BAD_PREFIXES:
        errors.append(f"label starts with preposition: '{label}'")

    return errors


def run_validation(all_results) -> bool:
    total_params = 0
    total_errors = 0

    for result in all_results:
        comp = getattr(result.context, "component_type", "?")
        for param in result.parameters:
            total_params += 1
            errs = validate_param(param)
            if errs:
                total_errors += 1
                print(f"  [{comp}] {param.key}:")
                for e in errs:
                    print(f"    [ERR] {e}")

    print(f"\n{'='*50}")
    print(f"Validated {total_params} params: "
          f"{total_params - total_errors} OK, {total_errors} errors")
    return total_errors == 0
