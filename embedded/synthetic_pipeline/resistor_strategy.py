
import random
import math
import uuid
from typing import Dict, Any, Optional, Tuple
from synthetic_pipeline.data_types import (
    GenerationContext,
    DatasheetResult,
    GeneratedParameter,
    SpecType,
    EngineeringClass,
)
from synthetic_pipeline.strategy_base import ComponentStrategy
# מניח שרשימות ה-E-Series נמצאות ב-utils, אם לא - צריך להחזיר אותן לקבועים
from synthetic_pipeline.strategy_utils import snap_to_e_series, apply_final_rounding

# ============================================================================
# CONSTANTS – PHYSICAL & INDUSTRIAL TRUTH
# ============================================================================

class ResistorConstants:
    """
    All constants here represent realistic manufacturer envelopes
    """
    # רשימות ערכים סטנדרטיים (אם חסר ב-utils, נגדיר כאן)
    E24_SERIES = [1.0, 1.1, 1.2, 1.3, 1.5, 1.6, 1.8, 2.0, 2.2, 2.4, 2.7, 3.0, 3.3, 3.6, 3.9, 4.3, 4.7, 5.1, 5.6, 6.2, 6.8, 7.5, 8.2, 9.1]

    PACKAGE_SPECS = {
        # ✅ תוקן: נתונים מדויקים לפי תקני IPC-7351 ו-IEC 60115
        # dims: L, W, H במילימטרים
        # weight: גרם (מבוסס על נפח × צפיפות קרמיקה)
        # P_max: וואט @ 70°C (derating curve)
        
        "01005": { 
            "dims": {"L": 0.4, "W": 0.2, "H": 0.13}, 
            "tol_mm": 0.02, 
            "weight_mg": 0.08,  # ✅ 0.08 מ"ג (80 מיקרוגרם)
            "limits": {"P_70C": 0.031, "V_max": 15, "V_over": 30, "I_max": 0.05}, 
            "R_range": {"min": 10, "max": 100_000} 
        },
        "0201":  { 
            "dims": {"L": 0.6, "W": 0.3, "H": 0.23}, 
            "tol_mm": 0.03, 
            "weight_mg": 0.2,   # ✅ 0.2 מ"ג
            "limits": {"P_70C": 0.05, "V_max": 25, "V_over": 50, "I_max": 0.1}, 
            "R_range": {"min": 10, "max": 200_000} 
        },
        "0402":  { 
            "dims": {"L": 1.0, "W": 0.5, "H": 0.35}, 
            "tol_mm": 0.05, 
            "weight_mg": 0.6,   # ✅ 0.6 מ"ג (המציאות!)
            "limits": {"P_70C": 0.063, "V_max": 50, "V_over": 100, "I_max": 0.15}, 
            "R_range": {"min": 1, "max": 1_000_000} 
        },
        "0603":  { 
            "dims": {"L": 1.6, "W": 0.8, "H": 0.45}, 
            "tol_mm": 0.1, 
            "weight_mg": 1.5,   # ✅ 1.5 מ"ג
            "limits": {"P_70C": 0.1, "V_max": 75, "V_over": 150, "I_max": 0.2}, 
            "R_range": {"min": 0.1, "max": 2_000_000} 
        },
        "0805":  { 
            "dims": {"L": 2.0, "W": 1.25, "H": 0.5}, 
            "tol_mm": 0.1, 
            "weight_mg": 3.2,   # ✅ 3.2 מ"ג
            "limits": {"P_70C": 0.125, "V_max": 150, "V_over": 300, "I_max": 0.3}, 
            "R_range": {"min": 0.05, "max": 10_000_000} 
        },
        "1206":  { 
            "dims": {"L": 3.2, "W": 1.6, "H": 0.55}, 
            "tol_mm": 0.2, 
            "weight_mg": 7.0,   # ✅ 7 מ"ג
            "limits": {"P_70C": 0.25, "V_max": 200, "V_over": 400, "I_max": 0.5}, 
            "R_range": {"min": 0.01, "max": 10_000_000} 
        },
        "1210":  { 
            "dims": {"L": 3.2, "W": 2.5, "H": 0.55}, 
            "tol_mm": 0.2, 
            "weight_mg": 11.0,  # ✅ 11 מ"ג
            "limits": {"P_70C": 0.5, "V_max": 200, "V_over": 400, "I_max": 1.0}, 
            "R_range": {"min": 0.01, "max": 10_000_000} 
        },
        "2512":  { 
            "dims": {"L": 6.4, "W": 3.2, "H": 0.55}, 
            "tol_mm": 0.2, 
            "weight_mg": 28.0,  # ✅ 28 מ"ג
            "limits": {"P_70C": 1.0, "V_max": 200, "V_over": 400, "I_max": 2.0}, 
            "R_range": {"min": 0.001, "max": 1_000_000} 
        },
        # THT Packages
        "Axial_1/4W": { 
            "dims": {"L": 6.5, "W": 2.3, "H": 2.3}, 
            "tol_mm": 0.3, 
            "weight_mg": 120.0,  # ✅ 120 מ"ג (גוף קרמי + חוטים)
            "limits": {"P_70C": 0.25, "V_max": 250, "V_over": 500, "I_max": 0.5}, 
            "R_range": {"min": 0.1, "max": 10_000_000} 
        },
    }

    # ✅ תוקן: Tolerance mapping מדויק יותר
    TOLERANCE_MAP = {
        "Standard_SMD": 5.0,           # ±5% (E24)
        "Precision_Thin_Film": 0.1,    # ±0.1% (E96/E192)
        "Thick_Film": 1.0,             # ±1% (E96)
        "Current_Sense": 1.0,          # ±1% (Low ohm, tight tolerance)
        "JUMPER": 0.0,                 # ✅ Zero-ohm has no tolerance
        "Standard_THT": 5.0,           # ±5% (E24)
        "High_Power": 5.0,             # ±5% (Wire-wound)
        "Metal_Film": 1.0,             # ±1% (E96)
    }

    # ✅ תוקן: TCR (Temperature Coefficient of Resistance) in ppm/°C
    TCR_MAP = {
        "Standard_SMD": 100,           # ±100 ppm/°C (Thick Film)
        "Precision_Thin_Film": 25,     # ±25 ppm/°C (Thin Film)
        "Thick_Film": 100,             # ±100 ppm/°C
        "Current_Sense": 50,           # ±50 ppm/°C (Metal alloy)
        "JUMPER": 0,                   # No TCR for jumpers
        "Standard_THT": 250,           # ±250 ppm/°C (Carbon Film)
        "High_Power": 50,              # ±50 ppm/°C (Wire-wound)
        "Metal_Film": 50,              # ±50 ppm/°C
    }

    # ✅ חדש: Maximum Operating Temperature
    MAX_TEMP_MAP = {
        "Standard_SMD": 125,
        "Precision_Thin_Film": 125,
        "Thick_Film": 125,
        "Current_Sense": 170,         # Higher for automotive
        "JUMPER": 125,
        "Standard_THT": 155,          # THT can handle more
        "High_Power": 275,            # Wire-wound high temp
        "Metal_Film": 155,
    }

# ============================================================================
# STRATEGY
# ============================================================================

class ResistorStrategy(ComponentStrategy):
    """
    Hermetic physics-based resistor generation.
    ✅ Improved Version: Accurate physics, realistic values, industry standards.
    """

    def create_context(self, schema: Dict, requested_corner: Optional[str]) -> GenerationContext:
        archetypes = schema.get("archetypes", ["Standard_SMD"])
        archetype = random.choice(archetypes)

        packages = list(ResistorConstants.PACKAGE_SPECS.keys())
        if "valid_packages" in schema:
            packages = [p for p in packages if p in schema["valid_packages"]]

        package = random.choice(packages)
        tolerance = ResistorConstants.TOLERANCE_MAP.get(archetype, 5.0)

        return GenerationContext(
            sample_id=str(uuid.uuid4())[:8],
            component_type="RESISTOR",
            package=package,
            archetype=archetype,
            tolerance=tolerance,
            process_corner=requested_corner or "TYPICAL",
            extras={}
        )

    # ----------------------------------------------------------------------
    # SINGLE SOURCE OF TRUTH – RESISTANCE
    # ----------------------------------------------------------------------
    def _get_or_create_resistance(self, context: GenerationContext) -> float:
        """
        Thread-safe resistance generation with E-series snapping.
        ✅ Improved: Better handling of jumpers and current sense resistors.
        """
        with context._lock:
            if "R" in context.extras:
                return context.extras["R"]

            pkg = ResistorConstants.PACKAGE_SPECS[context.package]

            # ✅ Zero-ohm jumper handling
            if context.archetype == "JUMPER":
                context.extras["R"] = 0.0
                return 0.0

            r_min = pkg["R_range"]["min"]
            r_max = pkg["R_range"]["max"]

            # ✅ Current sense resistors: favor low values (0.001Ω - 0.1Ω)
            if context.archetype == "Current_Sense":
                r_min = max(r_min, 0.001)
                r_max = min(r_max, 1.0)  # Limit to 1Ω max

            # Log-uniform distribution for realistic inventory spread
            exponent = random.uniform(math.log10(r_min), math.log10(r_max))
            raw = 10 ** exponent

            # ✅ E-series selection based on tolerance
            if context.tolerance <= 0.5:
                series = "E192"  # ±0.1% - ±0.5%
            elif context.tolerance <= 1.0:
                series = "E96"   # ±1%
            else:
                series = "E24"   # ±5%

            R = snap_to_e_series(raw, series)

            context.extras["R"] = R
            return R

    # ----------------------------------------------------------------------
    # REQUIRED IMPLEMENTATION: Create Custom Parameter
    # ----------------------------------------------------------------------
    def create_custom_parameter(self, key: str, context: GenerationContext, param_def: Dict) -> Optional[GeneratedParameter]:
        """
        ✅ Improved: Added more parameters and better handling.
        """
        if key == "resistance":
            # 1. Get the authoritative resistance value
            typ_v = self._get_or_create_resistance(context)
            
            # 2. Calculate min/max based on tolerance
            tol_dec = context.tolerance / 100.0
            min_v = typ_v * (1 - tol_dec) if typ_v > 0 else 0
            max_v = typ_v * (1 + tol_dec) if typ_v > 0 else 0

            # 3. Rounding for display
            def _clean(val): return float(f"{val:.4g}")
            
            # ✅ Special handling for jumpers
            if context.archetype == "JUMPER":
                return GeneratedParameter(
                    key="resistance",
                    label="Resistance (Jumper)",
                    symbol="R",
                    section="ELEC_CHAR",
                    value_typ=0.0,
                    value_max=0.05,  # Max 50mΩ for jumper
                    unit="Ω",
                    condition="Zero-ohm link",
                    spec_type=SpecType.NOMINAL,
                    engineering_class=EngineeringClass.PERFORMANCE
                )
            
            return GeneratedParameter(
                key="resistance",
                label="Resistance",
                symbol="R",
                section="ELEC_CHAR",
                value_min=_clean(min_v),
                value_typ=typ_v,
                value_max=_clean(max_v),
                unit="Ω",
                condition=f"T=25°C",
                spec_type=SpecType.NOMINAL,
                engineering_class=EngineeringClass.PERFORMANCE
            )

        if key == "tolerance":
            return GeneratedParameter(
                key="tolerance", 
                label="Resistance Tolerance", 
                symbol="Tol", 
                section="ELEC_CHAR",
                value_typ=context.tolerance, 
                unit="%",
                spec_type=SpecType.NOMINAL, 
                engineering_class=EngineeringClass.PERFORMANCE
            )

        if key == "max_operating_temp":
            # ✅ חדש: טמפרטורת הפעלה מקסימלית
            max_temp = ResistorConstants.MAX_TEMP_MAP.get(context.archetype, 125)
            return GeneratedParameter(
                key="max_operating_temp",
                label="Maximum Operating Temperature",
                symbol="T_max",
                section="ABS_MAX",
                value_typ=max_temp,
                unit="°C",
                spec_type=SpecType.MAX_RATING,
                engineering_class=EngineeringClass.RELIABILITY
            )
        
        return None

    # ----------------------------------------------------------------------
    # PHYSICS ENGINE
    # ----------------------------------------------------------------------
    def calculate_base_value(self, key: str, limits: Any, context: GenerationContext) -> Optional[float]:
        """
        ✅ Fixed: Corrected weight calculation (was off by 1000×)
        ✅ Improved: Added derating and realistic voltage limits
        """
        pkg = ResistorConstants.PACKAGE_SPECS[context.package]
        dims = pkg["dims"]
        lim = pkg["limits"]
        tol = pkg["tol_mm"]

        # ---- MECHANICAL ----
        if key == "length": 
            return dims["L"] + random.uniform(-tol, tol)
        
        if key == "width": 
            return dims["W"] + random.uniform(-tol, tol)
        
        if key == "height": 
            return dims["H"] + random.uniform(-tol / 2, tol / 2)
        
        if key == "weight":
            # ✅ CRITICAL FIX: Use pre-calculated weight from specs
            # Previous bug: calculated weight was off by 1000× (used wrong density units)
            base_weight_mg = pkg["weight_mg"]
            
            # Add ±5% manufacturing variation
            return base_weight_mg * random.uniform(0.95, 1.05)

        # ---- ELECTRICAL ----
        # Always get R first (Thread-safe)
        R = self._get_or_create_resistance(context)

        if key in ("rated_power", "power_rating"):
            # ✅ Power rating @ 70°C (standard derating point)
            return lim["P_70C"]

        if key == "max_power_25C":
            # ✅ חדש: הספק מקסימלי @ 25°C (before derating)
            # Typically 1.5-2× the 70°C rating
            return lim["P_70C"] * 1.6

        if key in ("rated_voltage", "max_working_voltage"):
            # ✅ Voltage limited by BOTH thermal (√PR) and package max
            # V = √(P×R), but cannot exceed V_max
            if R <= 0.001:  # Jumper or very low resistance
                return lim["V_max"] * 0.1  # Jumpers rated very low voltage
            
            v_thermal = math.sqrt(lim["P_70C"] * R)
            return min(v_thermal, lim["V_max"])

        if key == "max_overload_voltage":
            # ✅ Overload voltage (short-term, non-operating)
            # Typically 2-2.5× working voltage, limited by package
            v_work = self.calculate_base_value("rated_voltage", limits, context)
            if v_work is None:
                v_work = lim["V_max"]
            return min(v_work * 2.5, lim["V_over"])

        if key in ("rated_current", "max_current"):
            # ✅ I = √(P/R), limited by package max
            if R <= 0.001:  
                return lim["I_max"]  # Jumper: use package limit
            
            i_thermal = math.sqrt(lim["P_70C"] / R)
            return min(i_thermal, lim["I_max"])

        if key == "tcr":
            # Temperature Coefficient of Resistance (ppm/°C)
            return ResistorConstants.TCR_MAP.get(context.archetype, 100)

        if key == "max_element_temp":
            # ✅ חדש: טמפרטורת אלמנט מקסימלית (בדרך כלל +20-30°C ממקסימום הפעלה)
            max_op = ResistorConstants.MAX_TEMP_MAP.get(context.archetype, 125)
            return max_op + 25  # Element can be hotter than ambient

        return None

    # ----------------------------------------------------------------------
    # FINAL CONSISTENCY GUARDS
    # ----------------------------------------------------------------------
    # ----------------------------------------------------------------------
    # FINAL CONSISTENCY GUARDS
    # ----------------------------------------------------------------------
    def apply_correlations(self, result: DatasheetResult) -> None:
        """
        ✅ Improved: Better physics validation and warnings
        """
        # המרה למילון כדי שנוכל לשלוף לפי מפתח
        params_map = {p.key: p for p in result.parameters}
        
        try:
            # --- התיקון: שימוש ב-params_map במקום ב-result ---
            
            # בדיקה אם הפרמטר קיים לפני שניגשים ל-value_typ
            r_param = params_map.get("resistance")
            p_param = params_map.get("rated_power")
            
            if not r_param or not p_param:
                return

            R = r_param.value_typ
            P = p_param.value_typ
            
            # Get voltage and current
            V_param = params_map.get("rated_voltage") # תיקון כאן
            I_param = params_map.get("rated_current") # תיקון כאן
            
            if V_param is None or I_param is None:
                return
            
            V = V_param.value_typ
            I = I_param.value_typ
            
            # ✅ Physics Check (Skip for Jumpers)
            if R > 0.01:  # Skip very low resistances
                # Ohm's law: V = I × R
                expected_I = V / R if R > 0 else 0
                
                # הגנה מפני חלוקה ב-0 או מספרים אפסיים
                denom_i = max(expected_I, 1e-9)
                i_error = abs(expected_I - I) / denom_i
                
                if i_error > 0.05:  # 5% tolerance
                    print(f"⚠️  Physics mismatch in {result.context.sample_id}:")
                    print(f"    R={R}Ω, V={V}V, I={I}A")
                    print(f"    Expected I={expected_I:.3f}A (error: {i_error*100:.1f}%)")
                
                # Power check: P = V × I = V² / R = I² × R
                expected_P_from_V = V * V / R
                expected_P_from_I = I * I * R
                
                denom_p = max(P, 1e-9)
                p_error = abs(expected_P_from_V - P) / denom_p
                
                if p_error > 0.1:  # 10% tolerance
                    print(f"⚠️  Power rating issue in {result.context.sample_id}:")
                    print(f"    P_rated={P}W, P_from_V²/R={expected_P_from_V:.3f}W")
                    print(f"    (This is expected due to derating)")
            
            # ✅ Current sense resistor validation
            if result.context.archetype == "Current_Sense":
                if R > 0.1:
                    print(f"⚠️  Current sense resistor too high: {R}Ω (should be <0.1Ω)")
            
        except Exception as e:
            print(f"⚠️  Correlation check failed: {e}")
