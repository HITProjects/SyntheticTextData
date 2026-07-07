import random
import re
import math
from typing import Optional, Any, List, Tuple, Dict


# ==========================================
# 1. PHYSICAL CORRELATION ENGINE AND HELPER FUNCTIONS
# ==========================================

class PhysicalCorrelationEngine:
    """
    Ensures physically realistic relationships between parameters.
    Example: High VDS → High RDS(on), Low Capacitance → High SRF
    """
    
    @staticmethod
    def adjust_rds_based_on_vds(vds_value: float, base_rds: float) -> float:
        """MOSFETs: Higher voltage rating → Higher on-resistance"""
        if vds_value > 500:
            return base_rds * random.uniform(2.0, 5.0)
        elif vds_value > 200:
            return base_rds * random.uniform(1.5, 3.0)
        elif vds_value > 100:
            return base_rds * random.uniform(1.0, 2.0)
        else:
            return base_rds * random.uniform(0.5, 1.2)
    
    @staticmethod
    def adjust_forward_current_based_on_package(package: str, base_current: float) -> float:
        """Diodes: Larger packages → Higher current capability"""
        if any(p in package for p in ["TO-220", "TO-247", "D2PAK"]):
            return base_current * random.uniform(1.5, 3.0)
        elif any(p in package for p in ["SMC", "DO-214"]):
            return base_current * random.uniform(1.0, 1.5)
        else:
            return base_current * random.uniform(0.5, 1.0)
            
    @staticmethod        
    def adjust_capacitance_vs_voltage(cap_base, voltage_rating, archetype):
        if "Electrolytic" in archetype and voltage_rating > 50:
            return cap_base * random.uniform(0.8, 0.95)
        return cap_base
    
    @staticmethod
    def adjust_esr_based_on_capacitance(cap_value: float, base_esr: float) -> float:
        """Capacitors: Higher capacitance → Lower ESR (usually)"""
        if cap_value > 100e6:  # >100µF
            return base_esr * random.uniform(0.3, 0.7)
        elif cap_value > 10e6:  # >10µF
            return base_esr * random.uniform(0.6, 1.0)
        else:
            return base_esr * random.uniform(1.0, 2.0)
    
    @staticmethod
    def adjust_power_dissipation_based_on_package(package: str, base_power: float) -> float:
        """Larger packages → Better thermal performance"""
        thermal_map = {
            "TO-220": 2.5, "TO-247": 3.5, "TO-264": 4.0,
            "DPAK": 1.5, "D2PAK": 2.0,
            "SOT-23": 0.3, "SOT-223": 0.8,
            "0805": 0.2, "1206": 0.4, "2512": 1.0
        }
        for pkg, factor in thermal_map.items():
            if pkg in package:
                return base_power * factor
        return base_power


    # E-series standards
E24_SERIES = [
    1.0, 1.1, 1.2, 1.3, 1.5, 1.6, 1.8, 2.0, 2.2, 2.4, 2.7, 3.0,
    3.3, 3.6, 3.9, 4.3, 4.7, 5.1, 5.6, 6.2, 6.8, 7.5, 8.2, 9.1
    ]
    
E96_SERIES = [
    1.00, 1.02, 1.05, 1.07, 1.10, 1.13, 1.15, 1.18, 1.21, 1.24,
    1.27, 1.30, 1.33, 1.37, 1.40, 1.43, 1.47, 1.50, 1.54, 1.58,
    1.62, 1.65, 1.69, 1.74, 1.78, 1.82, 1.87, 1.91, 1.96, 2.00,
    2.05, 2.10, 2.15, 2.21, 2.26, 2.32, 2.37, 2.43, 2.49, 2.55,
    2.61, 2.67, 2.74, 2.80, 2.87, 2.94, 3.01, 3.09, 3.16, 3.24,
    3.32, 3.40, 3.48, 3.57, 3.65, 3.74, 3.83, 3.92, 4.02, 4.12,
    4.22, 4.32, 4.42, 4.53, 4.64, 4.75, 4.87, 4.99, 5.11, 5.23,
    5.36, 5.49, 5.62, 5.76, 5.90, 6.04, 6.19, 6.34, 6.49, 6.65,
    6.81, 6.98, 7.15, 7.32, 7.50, 7.68, 7.87, 8.06, 8.25, 8.45,
    8.66, 8.87, 9.09, 9.31, 9.53, 9.76
    ]
    
E192_SERIES = E96_SERIES  # Simplified for now
    
E_SERIES = {
    "E24": E24_SERIES,
    "E96": E96_SERIES,
    "E192": E192_SERIES
    }

def snap_to_e_series(value: float, series: str = "E24") -> float:
    """Snap a value to nearest E-series standard value"""
    if value <= 0:
        return value
     
    # Get mantissa and exponent
    exponent = 0
    mantissa = value
     
    # נרמול לטווח [1, 10)
    while mantissa >= 10:
        mantissa /= 10.0  # הוספתי .0 ליתר ביטחון
        exponent += 1
     
    while mantissa < 1:
        mantissa *= 10.0
        exponent -= 1
     
    # Find nearest E-series value
    e_values = E_SERIES.get(series, E_SERIES["E24"])
    nearest = min(e_values, key=lambda x: abs(x - mantissa))
    
    # Reconstruct value
    result = nearest * (10 ** exponent)
    
    # --- התיקון: עיגול כדי להעיף שגיאות דיוק ---
    # אם זה נגד ב-Ohm, בדרך כלל 2-3 ספרות אחרי הנקודה זה די והותר,
    # או 10 ספרות משמעותיות כדי לנקות את ה"זבל" הבינארי.
    if exponent >= 0:
        # למשל: 4700.0 במקום 4700.0000004
        return round(result, 2) 
    else:
        # למשל: 0.047 (מספרים קטנים דורשים יותר ספרות)
        return round(result, abs(exponent) + 2)
    
    
def extract_temperature_from_condition(condition_str: str) -> Optional[int]:
    """Extract temperature value from condition string"""
    import re
    match = re.search(r'(\d+)\s*°C', condition_str)
    if match:
        return int(match.group(1))
    match = re.search(r'T[acj]\s*=\s*(\d+)', condition_str, re.IGNORECASE)
    if match:
        return int(match.group(1))
    return None

def apply_temperature_derating(base_value: float, temp: int) -> float:
    """Apply derating based on temperature"""
    closest_temp = min(TEMP_DERATING.keys(), key=lambda x: abs(x - temp))
    factor = TEMP_DERATING[closest_temp]
    return base_value * factor



def snap_to_standard_tolerance(value: float) -> float:
    """Snap tolerance value to standard values"""
    return min(ResistorConstants.STANDARD_TOLERANCES, key=lambda x: abs(x - value))

def apply_final_rounding(value: Any, precision_level: str = "adaptive", 
                        unit: str = "", param_key: str = "") -> Any:
    """
    FIXED VERSION: Human-like rounding logic.
    Enforces "Datasheet Style" numbers:
    - > 100: No decimals (e.g., 350, not 349.9)
    - 10-100: Max 1 decimal (e.g., 12.5)
    - 1-10: Max 2 decimals (e.g., 3.3, 1.25)
    - < 1: 2 significant digits (e.g., 0.05, 0.0012)
    """
    if not isinstance(value, (int, float)):
        return value
    if value == 0:
        return 0
    
    # 1. Rounding Logic helper
    def human_round(val):
        abs_v = abs(val)
        
        # Large numbers (>100) -> Integer
        if abs_v >= 100:
            return int(round(val))
            
        # Medium numbers (10-100) -> Max 1 decimal
        if abs_v >= 10:
            return round(val, 1)
            
        # Small numbers (1-10) -> Max 2 decimals
        if abs_v >= 1:
            return round(val, 2)
            
        # Tiny numbers (<1) -> 2 Significant digits (e.g., 0.0047)
        return float(f"{val:.2g}")

    # 2. Force Integers for specific types
    if unit in ["°C", "K"] or "temp" in param_key.lower():
        return int(round(value))
        
    if unit == "ppm/°C" or unit == "ppm/V":
        # Snap to nearest 5
        return int(round(value / 5) * 5)

    # 3. Special handling for E-Series (Resistors/Capacitors)
    if param_key in ["resistance", "capacitance", "inductance"]:
        # First, snap to standard value if close enough
        if precision_level != "high":
            series = "E24" if precision_level == "adaptive" else "E12"
            snapped = snap_to_e_series(value, series)
            # Only use snapped if it's reasonably close (within 5%)
            if abs(value - snapped) / value < 0.05:
                # But adhere to human formatting for the snapped value too!
                return human_round(snapped)
    
    # 4. Apply generic human rounding
    return human_round(value)
    
def validate_min_typ_max_spacing(
    min_val: Optional[float], 
    typ_val: Optional[float], 
    max_val: Optional[float],
    tolerance_pct: float,  # שים לב: מצפים פה לאחוז (למשל 1 או 0.5)
    decimals: int = 2      # ברירת מחדל 2, אבל אפשר לשנות לכל רכיב
) -> Tuple[Optional[float], Optional[float], Optional[float]]:
    """
    Ensure min/max values respect the tolerance relative to typ_val.
    Recalculates min/max if they deviate too much (e.g. due to bad rounding elsewhere).
    """
    # 1. בדיקות תקינות בסיסיות
    if typ_val is None:
        return min_val, typ_val, max_val
        
    if min_val is None and max_val is None:
        return min_val, typ_val, max_val

    # המרה מאחוזים (0.5) לשבר עשרוני (0.005)
    tol_fraction = tolerance_pct / 100.0

    # 2. טיפול ב-Min (Low Side)
    if min_val is not None:
        # חישוב הטולרנס בפועל
        actual_tol_low = abs(typ_val - min_val) / typ_val
        
        # אם יש סטייה של יותר מ-10% מהטולרנס המוגדר (למשל טולרנס 1% יצא 0.8%)
        # או שהערך "התנגש" (min == typ) בגלל עיגול אגרסיבי
        if abs(actual_tol_low - tol_fraction) > (tol_fraction * 0.1) or min_val == typ_val:
            # מחשבים מחדש בצורה מדויקת
            new_min = typ_val * (1 - tol_fraction)
            min_val = round(new_min, decimals)

    # 3. טיפול ב-Max (High Side)
    if max_val is not None:
        actual_tol_high = abs(max_val - typ_val) / typ_val
        
        if abs(actual_tol_high - tol_fraction) > (tol_fraction * 0.1) or max_val == typ_val:
            new_max = typ_val * (1 + tol_fraction)
            max_val = round(new_max, decimals)

    return min_val, typ_val, max_val

def select_best_display_unit(value: float, base_unit: str, possible_units: List[str]) -> str:
    """Select best unit for display based on value magnitude"""
    if not isinstance(value, (int, float)):
        return base_unit
    
    abs_val = abs(value)
    
    # Voltage
    if base_unit == "V":
        if abs_val < 0.1 and "mV" in possible_units:
            return "mV"
        if abs_val < 0.0001 and "µV" in possible_units:
            return "µV"
    
    # Current
    if base_unit == "A":
        if abs_val < 0.001 and "µA" in possible_units:
            return "µA"
        elif abs_val < 1 and "mA" in possible_units:
            return "mA"
    
    # Resistance
    if base_unit == "Ω":
        if abs_val >= 1e6 and "MΩ" in possible_units:
            return "MΩ"
        elif abs_val >= 1000 and "kΩ" in possible_units:
            return "kΩ"
        elif abs_val < 1 and "mΩ" in possible_units:
            return "mΩ"
    
    # Capacitance
    if base_unit in ["pF", "F"]:
        if abs_val >= 1e6 and "µF" in possible_units:
            return "µF"
        elif abs_val >= 1000 and "nF" in possible_units:
            return "nF"
        elif base_unit == "F" and abs_val < 1e-6 and "pF" in possible_units:
            return "pF"
    
    # Inductance
    if base_unit == "µH":
        if abs_val >= 1000 and "mH" in possible_units:
            return "mH"
        elif abs_val < 1 and "nH" in possible_units:
            return "nH"
    
    # Frequency
    if base_unit == "MHz":
        if abs_val >= 1000 and "GHz" in possible_units:
            return "GHz"
        elif abs_val < 1 and "kHz" in possible_units:
            return "kHz"
    
    return base_unit

def convert_for_display(value: Any, base_unit: str, target_unit: str, 
                       precision: str = "adaptive", param_key: str = "") -> Any:
    """Convert value to target unit and round for display"""
    if value == "-" or value is None:
        return "-"
    if not isinstance(value, (int, float)):
        return value
    
    # Get conversion factor
    factor = UnitConverters.get_factor(base_unit, target_unit)
    converted = value * factor
    
    # Round the converted value
    rounded = apply_final_rounding(converted, precision, target_unit, param_key)
    
    return rounded

def validate_min_typ_max(min_val: Optional[float], typ_val: Optional[float], 
                        max_val: Optional[float]) -> Tuple[Optional[float], 
                                                            Optional[float], 
                                                            Optional[float]]:
    """Ensure min <= typ <= max constraint"""
    values = [v for v in [min_val, typ_val, max_val] if isinstance(v, (int, float))]
    
    if len(values) < 2:
        return min_val, typ_val, max_val
    
    values_sorted = sorted(values)
    
    result = [None, None, None]
    idx = 0
    if min_val is not None and isinstance(min_val, (int, float)):
        result[0] = values_sorted[idx]
        idx += 1
    if typ_val is not None and isinstance(typ_val, (int, float)):
        result[1] = values_sorted[idx]
        idx += 1
    if max_val is not None and isinstance(max_val, (int, float)):
        result[2] = values_sorted[idx]
    
    return tuple(result)


class UnitConverters:
    """מילון המרות אוניברסלי לכל סוגי הרכיבים"""
    
    # המרה מיחידת בסיס ליחידת יעד (המכפיל)
    CONVERSION_MAP = {
        # Voltage
        ("V", "mV"): 1000, ("V", "µV"): 1e6,
        ("mV", "V"): 0.001, ("µV", "V"): 1e-6,
        
        # Current
        ("A", "mA"): 1000, ("A", "µA"): 1e6, ("mA", "µA"): 1000,
        ("mA", "A"): 0.001, ("µA", "A"): 1e-6, ("µA", "mA"): 0.001,
        
        # Resistance
        ("Ω", "mΩ"): 1000, ("Ω", "kΩ"): 0.001, ("Ω", "MΩ"): 1e-6,
        ("mΩ", "Ω"): 0.001, ("kΩ", "Ω"): 1000, ("MΩ", "Ω"): 1e6,
        
        # Capacitance
        ("F", "mF"): 1000, ("F", "µF"): 1e6, ("F", "nF"): 1e9, ("F", "pF"): 1e12,
        ("µF", "nF"): 1000, ("µF", "pF"): 1e6, ("nF", "pF"): 1000,
        ("pF", "nF"): 0.001, ("nF", "µF"): 0.001, ("µF", "F"): 1e-6,
        
        # Frequency
        ("Hz", "kHz"): 0.001, ("Hz", "MHz"): 1e-6, ("Hz", "GHz"): 1e-9,
        ("kHz", "Hz"): 1000, ("kHz", "MHz"): 0.001,
        ("MHz", "kHz"): 1000, ("MHz", "Hz"): 1e6, ("MHz", "GHz"): 0.001,
        
        # Time
        ("s", "ms"): 1000, ("s", "µs"): 1e6, ("s", "ns"): 1e9,
        ("ms", "s"): 0.001, ("ms", "µs"): 1000,
        ("µs", "ms"): 0.001, ("µs", "ns"): 1000, ("ns", "µs"): 0.001
    }

    @staticmethod
    def get_factor(from_unit, to_unit):
        if from_unit == to_unit: return 1.0
        return UnitConverters.CONVERSION_MAP.get((from_unit, to_unit), 1.0)
