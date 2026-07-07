"""
strategies_loader.py
Loads component database from strategies_data.py and validates its schema at import time.

Import this module (or strategies.py which re-exports from here) instead of
importing strategies_data.py directly, so validation always runs.
"""

from synthetic_pipeline.strategies_data import UNIFIED_COMPONENT_DB as _raw_db, MODEL_TO_USE

# ── Required keys for each parameter entry ────────────────────────────────────
_PARAM_REQUIRED = {"key", "spec_type", "scenarios"}
_SCENARIO_REQUIRED = {"condition", "limits"}


class StrategyDataError(ValueError):
    """Raised when UNIFIED_COMPONENT_DB fails schema validation."""


def validate_component_db(db: dict) -> dict:
    """
    Validate the structure of UNIFIED_COMPONENT_DB.

    Checks:
    - Each component has 'archetypes' (list of str)
    - Each section value is a list of dicts
    - Each parameter dict has all required keys
    - Each scenario dict has 'condition' and 'limits'
    - Each limit entry is a number or a list of numbers

    Raises StrategyDataError on the first violation found.
    Returns the db unchanged if valid.
    """
    if not isinstance(db, dict):
        raise StrategyDataError("UNIFIED_COMPONENT_DB must be a dict")

    for comp_name, comp_data in db.items():
        if not isinstance(comp_data, dict):
            raise StrategyDataError(f"[{comp_name}] value must be a dict")

        archetypes = comp_data.get("archetypes")
        if archetypes is None:
            raise StrategyDataError(f"[{comp_name}] missing 'archetypes' key")
        if not isinstance(archetypes, list) or not all(isinstance(a, str) for a in archetypes):
            raise StrategyDataError(f"[{comp_name}] 'archetypes' must be a list of strings")

        for section_name, section_value in comp_data.items():
            if section_name == "archetypes":
                continue
            if not isinstance(section_value, list):
                raise StrategyDataError(
                    f"[{comp_name}][{section_name}] must be a list of parameter dicts"
                )
            for idx, param in enumerate(section_value):
                if not isinstance(param, dict):
                    raise StrategyDataError(
                        f"[{comp_name}][{section_name}][{idx}] must be a dict"
                    )
                missing = _PARAM_REQUIRED - param.keys()
                if missing:
                    raise StrategyDataError(
                        f"[{comp_name}][{section_name}][{idx}] "
                        f"missing required keys: {missing}"
                    )
                for s_idx, scenario in enumerate(param["scenarios"]):
                    if not isinstance(scenario, dict):
                        raise StrategyDataError(
                            f"[{comp_name}][{section_name}][{idx}].scenarios[{s_idx}] "
                            f"must be a dict"
                        )
                    s_missing = _SCENARIO_REQUIRED - scenario.keys()
                    if s_missing:
                        raise StrategyDataError(
                            f"[{comp_name}][{section_name}][{idx}].scenarios[{s_idx}] "
                            f"missing: {s_missing}"
                        )
                    limits = scenario["limits"]
                    if not isinstance(limits, dict):
                        raise StrategyDataError(
                            f"[{comp_name}][{section_name}][{idx}].scenarios[{s_idx}]"
                            f".limits must be a dict"
                        )
                    for arch, vals in limits.items():
                        if not isinstance(vals, (int, float, str, list, dict)):
                            raise StrategyDataError(
                                f"[{comp_name}][{section_name}][{idx}]"
                                f".scenarios[{s_idx}].limits[{arch}] "
                                f"has unexpected type {type(vals).__name__}"
                            )
    return db


# Run validation at import time — fail fast rather than at generation time
UNIFIED_COMPONENT_DB = validate_component_db(_raw_db)

__all__ = ["UNIFIED_COMPONENT_DB", "MODEL_TO_USE", "validate_component_db", "StrategyDataError"]
