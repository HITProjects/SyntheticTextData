from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, Tuple, List
import math

from synthetic_pipeline.data_types import (
    GenerationContext,
    DatasheetResult,
    GeneratedParameter,
)

from synthetic_pipeline.strategy_utils import apply_final_rounding

class ComponentStrategy(ABC):
    """
    המוח ההנדסי. כל רכיב (נגד, מוספט) חייב לממש את זה.
    הגנרטור מדבר רק עם הממשק הזה.
    """
    
    @abstractmethod
    def create_context(self, schema: Dict, requested_corner: Optional[str]) -> GenerationContext:
        """חישוב ראשוני של נתוני הדגימה (Package, Archetype)"""
        pass

    @abstractmethod
    def calculate_base_value(self, key: str, limits: Any, context: GenerationContext) -> Optional[float]:
        """שליפת הערך הגולמי (לוגיקה פיזיקלית)"""
        pass

    @abstractmethod
    def apply_correlations(self, result: DatasheetResult) -> None:
        """
        הזדמנות לתקן ערכים על סמך ערכים אחרים.
        למשל: עדכון RDSon על בסיס VDS שחושב כבר.
        """
        pass
   

    def create_custom_parameter(self, key: str, context: GenerationContext, param_def: Dict) -> Optional[GeneratedParameter]:
        """
        Hook method: מאפשרת לאסטרטגיה לייצר פרמטר שלם בעצמה, 
        ובכך לעקוף את הלוגיקה הגנרית של הגנרטור.
        אם מחזיר None - הגנרטור ימשיך בלוגיקה הרגילה.
        """
        return None

    from typing import Tuple, Optional

    def apply_final_rounding_atomic(
        self, 
        values_triple: Tuple[Optional[float], Optional[float], Optional[float]], 
        tolerance: float,
        unit: str,
        param_key: str = "",
        auto_calculate_bounds: bool = True  # פרמטר חדש לשליטה
    ) -> Tuple[Optional[float], Optional[float], Optional[float]]:
      
        
        raw_min, raw_typ, raw_max = values_triple
        
        # ============================================================
        # 1. פונקציית עיגול מרכזית
        # ============================================================
        def _smart_round(val: Optional[float]) -> Optional[float]:
            """
            עיגול חכם המשתמש ב-apply_final_rounding אם קיים,
            אחרת חוזר ל-fallback פשוט
            """
            if val is None:
                return None
            
            # נסה להשתמש בפונקציה המתקדמת אם קיימת
            try:
                return apply_final_rounding(val, "adaptive", unit, param_key)
            except (NameError, AttributeError):
                # Fallback: עיגול פשוט אבל חכם
                if abs(val) >= 10:
                    return round(float(val), 2)  # מספרים גדולים: 2 ספרות
                elif abs(val) >= 1:
                    return round(float(val), 3)  # בינוניים: 3 ספרות
                else:
                    return round(float(val), 4)  # קטנים: 4 ספרות
        
        # ============================================================
        # 2. עיגול הערכים הקיימים
        # ============================================================
        rounded_min = _smart_round(raw_min)
        rounded_typ = _smart_round(raw_typ)
        rounded_max = _smart_round(raw_max)
        
        # ============================================================
        # 3. חישוב אוטומטי של גבולות (רק אם מבוקש)
        # ============================================================
        if auto_calculate_bounds and rounded_typ is not None and tolerance is not None and tolerance > 0:
            # חישוב Min אם חסר
            if rounded_min is None:
                calculated_min = raw_typ * (1 - tolerance)
                rounded_min = _smart_round(calculated_min)
            
            # חישוב Max אם חסר
            if rounded_max is None:
                calculated_max = raw_typ * (1 + tolerance)
                rounded_max = _smart_round(calculated_max)
        
        return (rounded_min, rounded_typ, rounded_max)
    
    
