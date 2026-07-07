"""
strategies.py  —  backward-compatibility re-export.

The raw data now lives in  strategies_data.py.
Schema validation runs in  strategies_loader.py at import time.

All existing code that does:
    from synthetic_pipeline.strategies import UNIFIED_COMPONENT_DB, MODEL_TO_USE
continues to work unchanged.
"""
from synthetic_pipeline.strategies_loader import (   # noqa: F401
    UNIFIED_COMPONENT_DB,
    MODEL_TO_USE,
    validate_component_db,
    StrategyDataError,
)

__all__ = ["UNIFIED_COMPONENT_DB", "MODEL_TO_USE", "validate_component_db", "StrategyDataError"]
