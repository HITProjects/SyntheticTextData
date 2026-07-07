import uuid
import datetime
from enum import Enum
from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional
from threading import Lock


# ============================================================================
# UNIFIED ENUMS (MASTER)
# ============================================================================
class SpecType(Enum):
    """Specification type classification"""
    NOMINAL = "nominal"
    TYPICAL = "typical"
    
    # Limits
    MAX_RATING = "max_rating"   # Absolute Maximum (נזק אם עוברים)
    MAX_LIMIT = "max_limit"     # Performance Max (מובטח שלא יעבור את זה)
    MIN_LIMIT = "min_limit"     # Performance Min
    MIN_RATING = "min_rating"   # Absolute Minimum
    
    # Ranges
    OPERATIONAL_RANGE = "operational_range" # טווח עבודה מומלץ

class EngineeringClass(Enum):
    """Engineering classification"""
    SAFETY_LIMIT = "SAFETY_LIMIT"           # גבול בטיחות (Absolute Max)
    
    # Performance
    PERFORMANCE = "PERFORMANCE"             # ביצועים (ברירת מחדל)
    PERFORMANCE_LIMIT = "PERFORMANCE_LIMIT" # גבול ביצועים (אותו דבר, לתאימות)
    
    # Operation
    OPERATING_CONDITION = "OPERATING_CONDITION" # תנאי סביבה/עבודה
    NOMINAL_PARAMETER = "NOMINAL_PARAMETER"     # ערך נקוב
    
    # Others
    RELIABILITY = "RELIABILITY" # אמינות
    MECHANICAL = "MECHANICAL"   # מכאני
    THERMAL = "THERMAL"         # תרמי
    GENERIC = "GENERIC"         # כללי
    
class RoundingMode(Enum):
    ADAPTIVE = "adaptive"
    HIGH = "high"
    MINIMAL = "minimal"

# ==========================================
# 2. Data Models (Immutable Context & Results)
# ==========================================

@dataclass()
class GenerationContext:
    """מחזיק את כל המצב של הדגימה הנוכחית. Immutable."""
    sample_id: str
    component_type: str
    package: str
    archetype: str
    tolerance: float
    process_corner: str = "TYPICAL"
    temp_c: int = 25
    package_index: Optional[int] = None 
    extras: Dict[str, Any] = field(default_factory=dict)
    _lock: Any = field(default=None, repr=False, compare=False)

    def __post_init__(self):  
        """Initialize thread lock for parallel processing"""
        if self._lock is None:
            object.__setattr__(self, '_lock', Lock())


@dataclass
class GeneratedParameter:
    """תוצאה של חישוב פרמטר בודד (לפני פירמוט לתצוגה)"""
    # שדות חובה (חייבים לתת להם ערך ביצירה)
    key: str
    label: str
    symbol: str
    section: str
    value_min: Optional[float] = None
    value_typ: Optional[float] = None
    value_max: Optional[float] = None
    unit: str = ""
    condition: str = ""
    spec_type: SpecType = SpecType.NOMINAL
    engineering_class: EngineeringClass = EngineeringClass.PERFORMANCE

@dataclass
class DatasheetResult:
    """האובייקט המלא שמוחזר מהגנרטור"""
    context: GenerationContext
    parameters: List[GeneratedParameter]
    # ניתן להוסיף כאן לוגיקה של קורלציות גלובליות בעתיד
