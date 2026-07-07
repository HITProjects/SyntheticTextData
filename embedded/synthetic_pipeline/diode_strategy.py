
import random
import math
import uuid
from typing import Dict, Any, Optional

# ==========================================
# PIPELINE IMPORTS
# ==========================================
from synthetic_pipeline.data_types import (
    GenerationContext,
    DatasheetResult,
    GeneratedParameter,
    SpecType,
)

from synthetic_pipeline.strategy_base import ComponentStrategy


# ============================================================================
# CONSTANTS CLASS
# ============================================================================
class DiodeConstants:
    """Constants and lookup tables for diode generation"""

    PACKAGE_SPECS = {
        # SMD Packages - ערכים מדויקים לפי תקני IPC
        "SOD-323": { "dims": [1.7, 1.25, 0.95, 0.004], "limits": { "max_p": 0.2, "max_i": 0.25, "rth_ja": 650 } },
        "SOD-123": { "dims": [2.7, 1.6, 1.15, 0.010], "limits": { "max_p": 0.4, "max_i": 1.0,  "rth_ja": 350 } },
        "SOT-23":  { "dims": [2.9, 1.3, 1.0, 0.008],  "limits": { "max_p": 0.35,"max_i": 0.6,  "rth_ja": 400 } },

        # Through-Hole Packages
        "DO-35":   { "dims": [3.8, 1.7, 1.7, 0.13],   "limits": { "max_p": 0.5, "max_i": 0.5,  "rth_ja": 250 } },
        "DO-41":   { "dims": [5.2, 2.7, 2.7, 0.35],   "limits": { "max_p": 1.0, "max_i": 1.5,  "rth_ja": 100 } },
        "DO-201":  { "dims": [9.5, 5.3, 5.3, 1.20],   "limits": { "max_p": 5.0, "max_i": 5.0,  "rth_ja": 40  } },

        # Power Packages
        "TO-220":  { "dims": [10.0, 4.5, 15.0, 2.0],  "limits": { "max_p": 50,  "max_i": 20,   "rth_ja": 60  } },
        "TO-247":  { "dims": [16.0, 5.0, 21.0, 6.0],  "limits": { "max_p": 150, "max_i": 60,   "rth_ja": 40  } },

        # Surface Mount Power
        "SMA":     { "dims": [4.6, 2.6, 2.1, 0.06],   "limits": { "max_p": 1.0, "max_i": 1.5,  "rth_ja": 120 } },
        "SMB":     { "dims": [5.4, 3.6, 2.3, 0.10],   "limits": { "max_p": 3.0, "max_i": 3.0,  "rth_ja": 90  } },
        "SMC":     { "dims": [7.9, 5.9, 2.3, 0.21],   "limits": { "max_p": 5.0, "max_i": 5.0,  "rth_ja": 75  } }
    }

    ARCHETYPE_PHYSICS = {
        # ✅ תוקן: ערכי Vf ו-Ir מבוססים על פיזיקה אמיתית של חצי-מוליכים
        "Power_Rectifier":     { "vf_base": 0.95, "ir_factor": 1.0,   "trr_base": 2000, "is_schottky": False, "is_zener": False },
        "Schottky_Barrier":    { "vf_base": 0.45, "ir_factor": 100.0, "trr_base": 0,    "is_schottky": True,  "is_zener": False },
        "Fast_Recovery":       { "vf_base": 1.1,  "ir_factor": 5.0,   "trr_base": 150,  "is_schottky": False, "is_zener": False },
        "Ultra_Fast_Recovery": { "vf_base": 1.3,  "ir_factor": 10.0,  "trr_base": 50,   "is_schottky": False, "is_zener": False },
        "Zener":               { "vf_base": 1.0,  "ir_factor": 2.0,   "trr_base": None, "is_schottky": False, "is_zener": True  },
        "TVS_Transient":       { "vf_base": 3.3,  "ir_factor": 5.0,   "trr_base": None, "is_schottky": False, "is_zener": False },
        "Signal_Small_Signal": { "vf_base": 0.7,  "ir_factor": 0.1,   "trr_base": 4,    "is_schottky": False, "is_zener": False },
        "Switching":           { "vf_base": 0.85, "ir_factor": 0.5,   "trr_base": 4,    "is_schottky": False, "is_zener": False },
        "PIN_Diode":           { "vf_base": 0.95, "ir_factor": 0.01,  "trr_base": 1000, "is_schottky": False, "is_zener": False },
        "Avalanche":           { "vf_base": 0.9,  "ir_factor": 1.0,   "trr_base": 1500, "is_schottky": False, "is_zener": False }
    }

    # ✅ חדש: ערכי Zener סטנדרטיים לפי סדרת E24
    STANDARD_ZENER_VOLTAGES = [
        2.4, 2.7, 3.0, 3.3, 3.6, 3.9, 4.3, 4.7, 5.1, 5.6, 6.2, 6.8, 7.5, 
        8.2, 9.1, 10, 11, 12, 13, 15, 16, 18, 20, 22, 24, 27, 30, 33, 36, 
        39, 43, 47, 51, 56, 62, 68, 75, 82, 91, 100
    ]

    # ✅ חדש: ערכי מתח נדחפים סטנדרטיים
    STANDARD_REVERSE_VOLTAGES = [
        20, 30, 40, 50, 60, 75, 100, 150, 200, 300, 400, 600, 800, 1000, 
        1200, 1400, 1600, 2000
    ]

    # ✅ חדש: מקדמי טמפרטורה לזרם דליפה (Ir @ 125°C / Ir @ 25°C)
    TEMP_COEFFICIENT_IR = {
        "Power_Rectifier": 50,      # Si PN junction: x50 @ 125°C
        "Schottky_Barrier": 200,    # Schottky: x100-300 @ 125°C
        "Fast_Recovery": 40,
        "Ultra_Fast_Recovery": 35,
        "Zener": 30,
        "TVS_Transient": 25,
        "Signal_Small_Signal": 60,
        "Switching": 50,
        "PIN_Diode": 80,           # PIN very sensitive
        "Avalanche": 45
    }


# ============================================================================
# STRATEGY
# ============================================================================
class DiodeStrategy(ComponentStrategy):

    def __init__(self):
        self.constants = DiodeConstants()

    # ------------------------------------------------------------------
    # CONTEXT
    # ------------------------------------------------------------------
    def create_context(self, schema: Dict, requested_corner: Optional[str]) -> GenerationContext:
        archetype = random.choice(schema.get("archetypes", ["Power_Rectifier"]))

        valid_packages = list(self.constants.PACKAGE_SPECS.keys())
        if "valid_packages" in schema:
            valid_packages = [p for p in valid_packages if p in schema["valid_packages"]]

        package = random.choice(valid_packages)
        ratings = self._generate_physics_compliant_ratings(archetype, package)

        return GenerationContext(
            sample_id=str(uuid.uuid4())[:8],
            component_type="DIODE",
            package=package,
            archetype=archetype,
            tolerance=0.05,
            process_corner=requested_corner or "TYPICAL",
            extras={
                "rated_current": ratings["if_rated"],
                "rated_voltage": ratings["vr_rated"],
                "power_rating": ratings["p_max"],
                "physics_meta": self.constants.ARCHETYPE_PHYSICS[archetype],
            }
        )

    # ------------------------------------------------------------------
    # RATINGS ENGINE (✅ שופר)
    # ------------------------------------------------------------------
    def _generate_physics_compliant_ratings(self, archetype: str, package: str) -> Dict[str, float]:
        pkg = self.constants.PACKAGE_SPECS[package]["limits"]
        meta = self.constants.ARCHETYPE_PHYSICS[archetype]

        # ✅ תוקן: חישוב תרמי מדויק יותר
        # P = Vf × If → If_max = P_max / Vf
        vf_typical = meta["vf_base"]
        thermal_limit_current = pkg["max_p"] / vf_typical
        
        # גם מגבלת זרם של האריזה
        max_i = min(pkg["max_i"], thermal_limit_current * 0.8)  # Safety margin
        
        # ✅ תוקן: ערכי זרם סטנדרטיים E6/E12
        std_i = [0.05, 0.1, 0.15, 0.2, 0.3, 0.5, 0.75, 1.0, 1.5, 2.0, 3.0, 5.0, 10.0, 15.0, 20.0, 30.0, 60.0]
        
        valid_i = [i for i in std_i if i <= max_i]
        if not valid_i: 
            valid_i = [round(max_i * 0.7, 2)]  # Derating
        
        if_rated = random.choice(valid_i)

        # ✅ תוקן: בחירת מתחים סטנדרטיים
        if meta["is_zener"]:
            # Zener מוגבל לפי הספק
            max_zener = min(100, pkg["max_p"] * 20)  # Rough estimate
            vr = random.choice([v for v in self.constants.STANDARD_ZENER_VOLTAGES if v <= max_zener])
        else:
            # Schottky מוגבל ל-200V בדרך כלל
            max_v = 200 if meta["is_schottky"] else 2000
            vr = random.choice([v for v in self.constants.STANDARD_REVERSE_VOLTAGES if v <= max_v])

        return {"if_rated": if_rated, "vr_rated": vr, "p_max": pkg["max_p"]}

    # ------------------------------------------------------------------
    # PARAMETERS
    # ------------------------------------------------------------------
    def create_custom_parameter(self, key: str, context: GenerationContext, param_def: Dict):

        meta = context.extras["physics_meta"]
        if_rated = context.extras["rated_current"]
        vr_rated = context.extras["rated_voltage"]

        if key == "forward_current":
            return GeneratedParameter(
                key=key, label="Average Forward Current", symbol="I_F(AV)",
                section="ABS_MAX", value_typ=if_rated, unit="A",
                spec_type=SpecType.MAX_RATING
            )

        if key in ("reverse_voltage", "zener_voltage"):
            if ("zener" in key) != meta["is_zener"]:
                return None
            return GeneratedParameter(
                key=key,
                label="Rated Voltage",
                symbol="V_Z" if meta["is_zener"] else "V_RRM",
                section="ABS_MAX",
                value_typ=vr_rated,
                unit="V",
                spec_type=SpecType.MAX_RATING
            )

        if key == "forward_voltage":
            # ✅ תוקן: Vf עולה עם זרם (לוגריתמית)
            # Vf @ If = Vf_base + n*Vt*ln(If/If_ref)
            # n ≈ 1-2 (ideality factor), Vt ≈ 26mV @ 25°C
            vf_base = meta["vf_base"]
            current_factor = math.log10(max(if_rated, 0.1)) * 0.05  # Simplified
            vf_at_rated = vf_base + current_factor
            
            # Variation ±5%
            vf = vf_at_rated * random.uniform(0.97, 1.03)
            
            return GeneratedParameter(
                key=key, label="Forward Voltage", symbol="V_F",
                section="ELEC_CHAR",
                value_typ=round(vf, 2),
                value_max=round(vf * 1.15, 2),  # Spec tolerance
                unit="V",
                condition=f"I_F={if_rated}A, T_A=25°C"
            )

        if key == "reverse_current":
            return GeneratedParameter(
                key=key, label="Reverse Leakage Current", symbol="I_R",
                section="ELEC_CHAR",
                value_max=0.0,  # filled in correlations
                unit="µA"
            )

        if key == "reverse_current_hot":
            # ✅ חדש: זרם דליפה בטמפרטורה גבוהה
            return GeneratedParameter(
                key=key, label="Reverse Leakage Current (Hot)", symbol="I_R",
                section="ELEC_CHAR",
                value_max=0.0,  # filled in correlations
                unit="µA"
            )

        if key == "surge_current":
            # ✅ חדש: זרם הלם (קריטי לדיודות כוח)
            return GeneratedParameter(
                key=key, label="Non-Repetitive Peak Forward Surge Current", symbol="I_FSM",
                section="ABS_MAX",
                value_typ=0.0,  # filled in correlations
                unit="A",
                spec_type=SpecType.MAX_RATING
            )

        if key == "zener_impedance":
            # ✅ חדש: עכבת זנר (קריטי עבור Zener diodes)
            if not meta["is_zener"]:
                return None
            return GeneratedParameter(
                key=key, label="Zener Impedance", symbol="Z_z",
                section="ELEC_CHAR",
                value_typ=0.0,  # filled in correlations
                unit="Ω"
            )

        if key == "zener_test_current":
            # ✅ חדש: זרם בדיקה לזנר
            if not meta["is_zener"]:
                return None
            return GeneratedParameter(
                key=key, label="Zener Test Current", symbol="I_ZT",
                section="ELEC_CHAR",
                value_typ=0.0,  # filled in correlations
                unit="mA"
            )

        if key == "junction_capacitance":
            return GeneratedParameter(
                key=key, label="Junction Capacitance", symbol="C_j",
                section="ELEC_CHAR",
                value_typ=0.0,
                unit="pF"
            )

        if key == "reverse_recovery_time":
            if meta["is_schottky"]:
                return None
            return GeneratedParameter(
                key=key, label="Reverse Recovery Time", symbol="t_rr",
                section="ELEC_CHAR",
                value_typ=0,
                unit="ns"
            )

        return None

    # ------------------------------------------------------------------
    # DIMS
    # ------------------------------------------------------------------
    def calculate_base_value(self, key: str, limits: Any, context: GenerationContext):
        dims = self.constants.PACKAGE_SPECS[context.package]["dims"]
        noise = random.uniform(0.98, 1.02)  # Manufacturing tolerance
        
        mapping = {"length": dims[0], "width": dims[1], "height": dims[2], "weight": dims[3]}
        if key in mapping:
            return mapping[key] * noise
        return None

    # ------------------------------------------------------------------
    # CORRELATIONS (✅ שופר משמעותית)
    # ------------------------------------------------------------------
    def apply_correlations(self, result: DatasheetResult):
        ctx = result.context
        meta = ctx.extras.get("physics_meta", {})
        if_rated = ctx.extras.get("rated_current")
        vr_rated = ctx.extras.get("rated_voltage")
        p_max = ctx.extras.get("power_rating")
        
        if if_rated is None or vr_rated is None:
            print(f"   ⚠️  Skipping correlations for {ctx.sample_id}: missing rated_current or rated_voltage")
            return
        
        for p in result.parameters:
            if p.key == "reverse_current":
                # ✅ פיזיקה מדויקת של זרם דליפה @ 25°C
                ir_factor = meta.get("ir_factor", 1.0)
                
                if ir_factor is not None:
                    area_factor = math.sqrt(if_rated)
                    
                    if meta.get("is_schottky"):
                        base_leakage_uA = 5.0 * area_factor * ir_factor
                    else:
                        base_leakage_uA = 0.1 * area_factor * ir_factor
                    
                    # Auto-scale units
                    if base_leakage_uA < 1.0:
                        p.value_max = round(base_leakage_uA * 1000, 1)
                        p.unit = "nA"
                    elif base_leakage_uA >= 1000:
                        p.value_max = round(base_leakage_uA / 1000, 3)
                        p.unit = "mA"
                    else:
                        p.value_max = round(base_leakage_uA, 2)
                        p.unit = "µA"
                        
                    p.condition = f"V_R={vr_rated}V, T_A=25°C"
            
            elif p.key == "reverse_current_hot":
                # ✅ חדש: זרם דליפה @ 125°C (קריטי לשוטקי!)
                ir_factor = meta.get("ir_factor", 1.0)
                archetype = ctx.archetype
                temp_mult = self.constants.TEMP_COEFFICIENT_IR.get(archetype, 50)
                
                if ir_factor is not None:
                    area_factor = math.sqrt(if_rated)
                    
                    if meta.get("is_schottky"):
                        base_leakage_uA = 5.0 * area_factor * ir_factor
                    else:
                        base_leakage_uA = 0.1 * area_factor * ir_factor
                    
                    # Apply temperature multiplication
                    hot_leakage_uA = base_leakage_uA * temp_mult
                    
                    # Auto-scale units
                    if hot_leakage_uA < 1.0:
                        p.value_max = round(hot_leakage_uA * 1000, 1)
                        p.unit = "nA"
                    elif hot_leakage_uA >= 1000:
                        p.value_max = round(hot_leakage_uA / 1000, 3)
                        p.unit = "mA"
                    else:
                        p.value_max = round(hot_leakage_uA, 2)
                        p.unit = "µA"
                        
                    p.condition = f"V_R={vr_rated}V, T_A=125°C"
            
            elif p.key == "surge_current":
                # ✅ חדש: זרם הלם I_FSM ≈ 10-30× If_rated
                # Smaller diodes: higher ratio, Power diodes: lower ratio
                if if_rated < 1.0:
                    surge_ratio = random.uniform(25, 35)  # Signal/small
                elif if_rated < 5.0:
                    surge_ratio = random.uniform(15, 25)  # Medium
                else:
                    surge_ratio = random.uniform(10, 15)  # Power
                
                i_fsm = if_rated * surge_ratio
                p.value_typ = round(i_fsm, 1)
                p.condition = "t=8.3ms (1/2 cycle @ 60Hz), T_A=25°C"
            
            elif p.key == "zener_impedance":
                # ✅ חדש: עכבת זנר Z_z @ I_ZT
                # Z_z inversely proportional to power rating
                # Low voltage zeners: higher impedance
                if p_max is not None and vr_rated is not None:
                    # Empirical formula from datasheets:
                    # Z_z ≈ Vz / (10 × P_max) for medium power zeners
                    base_z = vr_rated / (10 * p_max)
                    
                    # Low voltage zeners have higher Z_z
                    if vr_rated < 5.0:
                        base_z *= 3.0
                    elif vr_rated < 10.0:
                        base_z *= 1.5
                    
                    # Add variation ±30%
                    zz = base_z * random.uniform(0.7, 1.3)
                    
                    # Auto-scale units
                    if zz < 1.0:
                        p.value_typ = round(zz * 1000, 1)
                        p.unit = "mΩ"
                    elif zz >= 1000:
                        p.value_typ = round(zz / 1000, 2)
                        p.unit = "kΩ"
                    else:
                        p.value_typ = round(zz, 1)
                        p.unit = "Ω"
                    
                    p.condition = f"I_ZT (see below)"
            
            elif p.key == "zener_test_current":
                # ✅ חדש: I_ZT - זרם הבדיקה של הזנר
                # Typically I_ZT ≈ 0.1 × P_max / V_z (10% of max power)
                if p_max is not None and vr_rated is not None:
                    izt_mA = (0.1 * p_max / vr_rated) * 1000  # Convert to mA
                    
                    # Round to standard values
                    standard_izt = [0.25, 0.5, 1, 2, 5, 10, 20, 50, 100, 200, 500]
                    p.value_typ = min(standard_izt, key=lambda x: abs(x - izt_mA))
                    p.condition = f"V_Z={vr_rated}V ±5%"
            
            elif p.key == "junction_capacitance":
                # ✅ Cj ∝ Area / sqrt(Vr)
                if if_rated is not None:
                    cj_base = 20 * math.sqrt(if_rated)
                    
                    vr_test = 4.0
                    vbi = 0.7
                    cj_at_vr = cj_base / math.sqrt(1 + vr_test / vbi)
                    
                    p.value_typ = round(cj_at_vr, 1)
                    p.condition = "V_R=4V, f=1MHz"
            
            elif p.key == "reverse_recovery_time":
                trr_base = meta.get("trr_base")
                
                if trr_base is not None and if_rated is not None:
                    size_factor = math.sqrt(if_rated) if if_rated > 0.1 else 1.0
                    trr_calculated = trr_base * size_factor
                    
                    trr_final = trr_calculated * random.uniform(0.8, 1.2)
                    
                    p.value_typ = int(trr_final)
                    p.condition = f"I_F={if_rated}A, di/dt=100A/µs"
