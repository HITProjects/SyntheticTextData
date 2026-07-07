import random
import math
import uuid
import re
from typing import Dict, Any, Optional, List, Tuple
from dataclasses import dataclass

# ==========================================
# 1. PIPELINE IMPORTS
# ==========================================
from synthetic_pipeline.data_types import (
    GenerationContext, 
    DatasheetResult, 
    GeneratedParameter,
    SpecType, 
    EngineeringClass,
)

from synthetic_pipeline.strategy_base import ComponentStrategy

# ============================================================================
# CONSTANTS CLASS
# ============================================================================
class VoltageRegulatorConstants:
    """Constants and lookup tables for voltage regulator generation"""
    
    # ========================================================================
    # MASTER PACKAGE SPECIFICATIONS - SINGLE SOURCE OF TRUTH
    # ========================================================================
    PACKAGE_SPECS = {
        # --- SMALL SIGNAL ---
        "SOT-23-3": {
            "dimensions": [2.9, 1.3, 1.0, 0.015], 
            "limits": { "max_power_watts": 0.4, "max_current_a": 0.5, "max_voltage_v": 30, "rth_ja": 357, "rth_jc": 100 }
        },
        "SOT-23-5": {
            "dimensions": [2.9, 1.6, 1.0, 0.02],
            "limits": { "max_power_watts": 0.5, "max_current_a": 0.6, "max_voltage_v": 30, "rth_ja": 280, "rth_jc": 90 }
        },
        "SOT-223": {
            "dimensions": [6.5, 3.5, 1.6, 0.1],
            "limits": { "max_power_watts": 1.5, "max_current_a": 1.5, "max_voltage_v": 45, "rth_ja": 130, "rth_jc": 30 }
        },
        
        # --- POWER SMD ---
        "DPAK": {
            "dimensions": [6.6, 6.1, 2.3, 0.3],
            "limits": { "max_power_watts": 2.5, "max_current_a": 5.0, "max_voltage_v": 60, "rth_ja": 80, "rth_jc": 5 }
        },
        "D2PAK": {
            "dimensions": [10.2, 9.0, 4.5, 1.5],
            "limits": { "max_power_watts": 5.0, "max_current_a": 8.0, "max_voltage_v": 60, "rth_ja": 50, "rth_jc": 3 }
        },
        
        # --- ADVANCED / ULTRA SMALL ---
        "DFN_1x1": {
            "dimensions": [1.0, 1.0, 0.4, 0.002],
            "limits": { "max_power_watts": 0.3, "max_current_a": 0.3, "max_voltage_v": 5.5, "rth_ja": 200, "rth_jc": 50 }
        },
        "DFN_2x2": {
            "dimensions": [2.0, 2.0, 0.75, 0.015],
            "limits": { "max_power_watts": 0.8, "max_current_a": 1.0, "max_voltage_v": 25, "rth_ja": 150, "rth_jc": 20 }
        },
        "DFN_3x3": {
            "dimensions": [3.0, 3.0, 0.75, 0.03],
            "limits": { "max_power_watts": 1.5, "max_current_a": 3.0, "max_voltage_v": 30, "rth_ja": 60, "rth_jc": 8 }
        },
        
        # --- THROUGH HOLE ---
        "TO-220": {
            "dimensions": [10.0, 4.5, 9.0, 2.0],
            "limits": { "max_power_watts": 20.0, "max_current_a": 10.0, "max_voltage_v": 60, "rth_ja": 60, "rth_jc": 3 }
        },
        "TO-263": {
            "dimensions": [10.2, 9.0, 4.5, 1.0],
            "limits": { "max_power_watts": 5.0, "max_current_a": 5.0, "max_voltage_v": 60, "rth_ja": 50, "rth_jc": 5 }
        }
    }
    
    TOLERANCE_MAP = {
        "LDO_Low_Voltage_CMOS": 0.02,
        "LDO_High_Voltage_Bipolar": 0.04
    }
    
    # SI Units (Amperes)
    IQ_BASE = {
        "LDO_Low_Voltage_CMOS": 5e-6,      # 5 µA
        "LDO_High_Voltage_Bipolar": 1e-3   # 1 mA
    }
    
    DROPOUT_CURRENT_FACTOR = 0.4 # Vdo increases with current
    
    # Ohm * Ampere product (to estimate pass element resistance)
    RDS_SCALING = {
        "LDO_Low_Voltage_CMOS": 0.2, 
        "LDO_High_Voltage_Bipolar": 0.5
    }
    
    # Loop bandwidth vs quiescent current ratio (Hz/A)
    BW_IQ_RATIO = 50e6  # 50 MHz/A -> 1mA Iq = 50kHz BW
    
    # Output capacitor-bandwidth product (F·Hz)
    COUT_BW_PRODUCT = 1e-4  # 100 µF·kHz

    R_PASS_FACTOR = {
        # CMOS LDOs (PMOS Pass Element)
        "LDO_Low_Voltage_CMOS": 0.25,      # ~250mV drop at 1A
        "LDO_Ultra_Low_Drop": 0.15,        # ~150mV drop at 1A
        "LDO_CMOS_Tiny": 0.5,              # Higher resistance
        
        # Bipolar LDOs (PNP Pass Element)
        "LDO_High_Voltage_Bipolar": 0.6,   # ~600mV drop at 1A
        "LDO_Automotive_Bipolar": 0.8,
        
        # Standard Linear Regulators (NPN Darlington)
        "Standard_Linear_78xx": 2.0,       # ~2V drop at 1A
        "High_Current_Linear": 1.2,
        
        # Specialized
        "LDO_Ultra_Low_Noise": 0.35,
        "LDO_Wide_Input": 0.5
    }


# ============================================================================
# STRATEGY CLASS
# ============================================================================
class VoltageRegulatorStrategy(ComponentStrategy):
    """Hermetic Voltage Regulator Strategy - FIXED VERSION"""

    # Keys excluded to keep document under 512 tokens (aligner window limit)
    EXCLUDED_KEYS = {
        # ABS_MAX — niche
        'vout_max', 'esd_hbm', 'reverse_current', 'lead_temp',
        # DYNAMIC_CHAR — advanced, rarely in basic datasheets
        'phase_margin', 'gain_margin',
        # PACKAGE — thermal_jc rarely specified separately
        'thermal_resistance_jc',
        # ELEC_CHAR — keep only 16 core parameters
        'iout_min', 'efficiency', 'vin_to_vout_differential',
        'shutdown_current', 'input_supply_current', 'reverse_leakage_current',
        'output_noise_density', 'enable_input_current',
        'uvlo_threshold', 'uvlo_hysteresis',
        'short_circuit_current', 'current_limit_foldback', 'current_limit_response_time',
        'thermal_shutdown_hysteresis',
        'startup_time', 'settling_time',
        'load_transient_response', 'load_transient_recovery_time',
        'output_voltage_overshoot', 'output_voltage_undershoot',
        'slew_rate', 'monotonic_startup',
        'pgood_threshold_high', 'pgood_output_low', 'pgood_leakage', 'pgood_delay',
        'open_loop_gain', 'pass_element_resistance', 'output_discharge_resistance',
        'power_on_reset_threshold', 'tracking_accuracy',
        'reference_voltage', 'reference_tempco',
        'feedback_pin_voltage', 'feedback_pin_current',
        'adj_pin_voltage', 'adj_pin_current',
        'output_capacitor_min', 'output_capacitor_esr', 'input_capacitor_min',
    }

    def __init__(self):
        self.C = VoltageRegulatorConstants()

    # ------------------------------------------------------------------
    # 1. CONTEXT - The Lock-in Phase (FIXED)
    # ------------------------------------------------------------------
    def create_context(self, schema: Dict, requested_corner: Optional[str]) -> GenerationContext:
        archetype = random.choice(schema.get("archetypes", ["LDO_Low_Voltage_CMOS"]))
        
        # Filter valid packages based on archetype hints
        valid_packages = list(self.C.PACKAGE_SPECS.keys())
        if "Power" in archetype or "Bipolar" in archetype:
            valid_packages = [p for p in valid_packages if "TO" in p or "DPAK" in p or "SOT-223" in p]
        
        package = random.choice(valid_packages)

        # Hermetic Lock: Determine Vout and Iout constraints NOW
        primary = self._generate_primary(schema, archetype, package)

        # 🔧 FIX: Calculate vdrop and iq IMMEDIATELY in context
        r_pass = self.C.R_PASS_FACTOR.get(archetype, 0.4)
        vdrop = primary["iout"] * r_pass
        
        base_iq = self.C.IQ_BASE.get(archetype, 50e-6)
        iq = base_iq * random.uniform(0.8, 1.3)

        extras = dict(
            vout=primary["vout"],
            iout=primary["iout"],
            vdrop=vdrop,      # ✅ NOW CALCULATED
            iq=iq,            # ✅ NOW CALCULATED
            loop_bw=None,     # Will be calculated in apply_correlations
            is_cmos="CMOS" in archetype,
        )

        return GenerationContext(
            sample_id=f"LDO_{uuid.uuid4().hex[:6]}",
            component_type="VOLTAGE_REGULATOR",
            package=package,
            archetype=archetype,
            tolerance=0.02 if "CMOS" in archetype else 0.04,
            process_corner=requested_corner or "TYPICAL",
            extras=extras,
        )

    # ------------------------------------------------------------------
    # 2. PRIMARY LOCK (IMPROVED PHYSICS)
    # ------------------------------------------------------------------
    def _generate_primary(self, schema, archetype, package):
        pkg_limits = self.C.PACKAGE_SPECS[package]["limits"]

        # Extract options from schema limits or use defaults
        vouts = self._extract_numeric_list(self._get_schema_limits(schema, "output_voltage", archetype))
        iouts = self._extract_numeric_list(self._get_schema_limits(schema, "iout_max", archetype))

        # Try to find a valid combination within package physics limits
        for _ in range(100):  # More iterations
            vout = random.choice(vouts or [1.2, 1.8, 2.5, 3.3, 5.0])
            iout = random.choice(iouts or [0.1, 0.3, 0.5])

            # Estimate dropout for this archetype
            r_pass = self.C.R_PASS_FACTOR.get(archetype, 0.4)
            vdrop_est = iout * r_pass
            
            # Worst-case Vin (max input from package rating)
            vin_max = min(pkg_limits["max_voltage_v"], vout + 10)
            
            # Worst-case power dissipation
            p_worst = (vin_max - vout) * iout + vout * 1e-3  # Assume 1mA Iq
            
            # Thermal check: P < (Tj_max - Ta) / Rth_ja
            t_junction_max = 125.0
            t_ambient = 85.0  # Worst case ambient
            p_thermal_limit = (t_junction_max - t_ambient) / pkg_limits["rth_ja"]
            
            # Physics Check - ALL CONDITIONS
            if (iout <= pkg_limits["max_current_a"] and 
                p_worst <= pkg_limits["max_power_watts"] and
                p_worst <= p_thermal_limit and
                vout <= pkg_limits["max_voltage_v"]):
                return dict(vout=vout, iout=iout)

        # Aggressive fallback if solver fails
        return dict(
            vout=min(vouts or [3.3]), 
            iout=pkg_limits["max_current_a"] * 0.3
        )

    # ------------------------------------------------------------------
    # 3. PARAMETERS GENERATION (SIMPLIFIED - values pre-calculated)
    # ------------------------------------------------------------------
    def create_custom_parameter(self, key, ctx, pd):
        if key in self.EXCLUDED_KEYS:
            return None

        if key == "output_voltage":
            v = ctx.extras["vout"]
            return self._nominal(pd, v, "V", ctx)

        if key == "iout_max":
            i = ctx.extras["iout"]
            val_disp, unit = self._auto_scale(i, "A")
            return GeneratedParameter(
                key=key,
                label=pd["llm_context"]["formal_name"],
                symbol=pd["symbol"],
                section="ELEC_CHAR",
                value_typ=val_disp,
                value_max=val_disp,
                unit=unit,
                condition=pd["scenarios"][0]["condition"],
                spec_type=SpecType.MAX_RATING,
                engineering_class=EngineeringClass.PERFORMANCE,
            )

        if key == "quiescent_current":
            # ✅ Already calculated in context
            val_disp, unit = self._auto_scale(ctx.extras["iq"], "A")
            return self._typ_max_obj(pd, val_disp, unit)

        if key == "dropout_voltage":
            # ✅ Already calculated in context
            val_disp, unit = self._auto_scale(ctx.extras["vdrop"], "V")
            return self._typ_max_obj(pd, val_disp, unit)
        
        # 🆕 NEW PARAMETERS
        if key == "line_regulation":
            # ΔVout / ΔVin (better with higher loop gain ~ Iq)
            reg_pct = 0.05 / (ctx.extras["iq"] * 1e6 + 1)  # Prevent div by zero
            return self._typ_max_obj(pd, round(reg_pct, 4), "%/V")
        
        if key == "load_regulation":
            # ΔVout / ΔIout (mV/mA) - output resistance effect
            rout = ctx.extras["vdrop"] / (ctx.extras["iout"] + 1e-6) * 0.01
            reg_mv_ma = rout * 1000
            return self._typ_max_obj(pd, round(reg_mv_ma, 2), "mV/mA")

        # General handler: extract archetype-specific limits and build proper min/typ/max
        for scenario in pd.get("scenarios", []):
            arch_limits = scenario.get("limits", {}).get(ctx.archetype)
            if arch_limits is None:
                continue

            # Handle list of strings (range like "5 to 500" or categorical "Yes")
            if isinstance(arch_limits, list) and all(isinstance(v, str) for v in arch_limits):
                if not arch_limits:
                    return None
                m = re.match(r'^(-?[\d.]+)\s+to\s+(-?[\d.]+)$', arch_limits[0].strip())
                if m:
                    return self._make_param(pd, float(m.group(1)), None, float(m.group(2)), scenario)
                return None  # Non-numeric (e.g., "Yes")

            # Handle numeric list: [min, typ, max] semantics
            if isinstance(arch_limits, list):
                numeric = [float(v) for v in arch_limits if isinstance(v, (int, float))]
                if not numeric:
                    return None
                if len(numeric) == 1:
                    v_min, v_typ, v_max = None, numeric[0], None
                elif len(numeric) == 2:
                    v_min, v_typ, v_max = numeric[0], None, numeric[1]
                else:
                    mid = len(numeric) // 2
                    v_min, v_typ, v_max = numeric[0], numeric[mid], numeric[-1]
                return self._make_param(pd, v_min, v_typ, v_max, scenario)

        return None

    # ------------------------------------------------------------------
    # 4. CORRELATIONS (IMPROVED PHYSICS)
    # ------------------------------------------------------------------
    def apply_correlations(self, result: DatasheetResult):
        ctx = result.context

        # Physics: Bandwidth is proportional to quiescent current (g_m stage)
        if ctx.extras["loop_bw"] is None and ctx.extras["iq"]:
            ctx.extras["loop_bw"] = ctx.extras["iq"] * self.C.BW_IQ_RATIO

        for p in result.parameters:
            # 🔧 IMPROVED: Noise Correlation with architecture dependency
            if p.key == "output_noise" and p.value_typ and ctx.extras["loop_bw"]:
                # Base noise density depends on architecture
                noise_density_base = {
                    "LDO_Low_Voltage_CMOS": 20,      # µV/√Hz
                    "LDO_High_Voltage_Bipolar": 60,
                    "LDO_Ultra_Low_Noise": 10,
                }.get(ctx.archetype, 40)
                
                # Integrated noise: Vnoise_rms = noise_density * sqrt(BW)
                bw_effective = ctx.extras["loop_bw"]
                integrated_noise = noise_density_base * math.sqrt(bw_effective / 1e3)  # Normalize
                
                p.value_typ = round(integrated_noise, 1)
            
            # 🔧 IMPROVED: PSRR with frequency rolloff
            if p.key == "psrr" and ctx.extras["loop_bw"]:
                # Extract test frequency from condition
                freq_match = re.search(r'(\d+)\s*(Hz|kHz|MHz)', p.condition or "")
                if freq_match:
                    freq_val = float(freq_match.group(1))
                    freq_unit = freq_match.group(2)
                    test_freq = freq_val * {"Hz": 1, "kHz": 1e3, "MHz": 1e6}[freq_unit]
                    
                    f_pole = ctx.extras["loop_bw"] / 10
                    
                    if test_freq > f_pole:
                        # --- התיקון שלך נכנס כאן ---
                        base_val = p.value_typ
                        
                        # טיפול במקרה שהערך הגיע מהסכמה כמילון
                        if isinstance(base_val, dict):
                            # לוקחים את הערך המינימלי כנקודת מוצא
                            base_val = min(base_val.values()) if base_val else 60.0
                        
                        # ביצוע החישוב המתמטי רק אם יש לנו מספר
                        if isinstance(base_val, (int, float)):
                            rolloff_db = 20 * math.log10(test_freq / f_pole)
                            p.value_typ = max(base_val - rolloff_db, 20)  # Floor at 20dB

            self._round(p)

    # ------------------------------------------------------------------
    # 5. BASE VALUES & HELPERS (FIXED)
    # ------------------------------------------------------------------
    def calculate_base_value(self, key, limits, ctx):
        if key in self.EXCLUDED_KEYS:
            return None

        pkg_data = self.C.PACKAGE_SPECS[ctx.package]
        pkg_limits = pkg_data["limits"]

        if key == "package_code": return ctx.package
        if key == "dimensions_lxwxh": return pkg_data["dimensions"]

        if key == "power_dissipation":
            # 🔧 FIXED: Actual power dissipation at max load
            # Assume typical Vin = Vout + 2*Vdrop (reasonable operating point)
            vin_typ = ctx.extras["vout"] + 2 * ctx.extras["vdrop"]
            p_load = (vin_typ - ctx.extras["vout"]) * ctx.extras["iout"]
            p_quiescent = ctx.extras["vout"] * ctx.extras["iq"]
            p_actual = p_load + p_quiescent
            
            return round(p_actual * 1.2, 2)  # 20% margin

        if key == "thermal_resistance_ja": 
            return pkg_limits["rth_ja"]

        if key == "minimum_input_voltage":
            # 🔧 FIXED: Vin_min must provide AT LEAST the specified dropout
            # Add 10% margin to ensure spec compliance
            return ctx.extras["vout"] + ctx.extras["vdrop"] * 1.1

        if key == "output_voltage": return ctx.extras["vout"]
        if key == "iout_max": return ctx.extras["iout"]

        # Extract archetype-specific numeric value; return None for non-numeric/missing
        if isinstance(limits, dict):
            arch_list = limits.get(ctx.archetype, [])
            if isinstance(arch_list, list):
                numeric = [v for v in arch_list if isinstance(v, (int, float))]
                return random.choice(numeric) if numeric else None
            return None

        return self._pick_generic(limits)

    # ------------------------------------------------------------------
    # UTILS
    # ------------------------------------------------------------------
    def _nominal(self, pd, val, unit, ctx):
        tol = ctx.tolerance
        return GeneratedParameter(
            key=pd["key"], label=pd["llm_context"]["formal_name"], symbol=pd["symbol"],
            section="ELEC_CHAR",
            value_min=val * (1 - tol), value_typ=val, value_max=val * (1 + tol),
            unit=unit, condition=pd["scenarios"][0]["condition"],
            spec_type=SpecType.NOMINAL, engineering_class=EngineeringClass.PERFORMANCE,
        )

    def _typ_max_obj(self, pd, val, unit):
        return GeneratedParameter(
            key=pd["key"], label=pd["llm_context"]["formal_name"], symbol=pd["symbol"],
            section="ELEC_CHAR",
            value_typ=val, value_max=val * 1.5,
            unit=unit, condition=pd["scenarios"][0]["condition"],
            spec_type=SpecType.NOMINAL, engineering_class=EngineeringClass.PERFORMANCE,
        )

    def _auto_scale(self, val, unit):
        if val is None: return 0, unit
        if val < 1e-6: return val * 1e9, "n" + unit
        if val < 1e-3: return val * 1e6, "µ" + unit
        if val < 1: return val * 1e3, "m" + unit
        return val, unit

    def _round(self, p):
        for f in ("value_typ", "value_min", "value_max"):
            v = getattr(p, f)
            if isinstance(v, float): setattr(p, f, round(v, 3))

    def _get_schema_limits(self, schema, key, archetype):
        p = next((x for x in schema.get("ELEC_CHAR", []) if x["key"] == key), None)
        if not p: return []
        return p["scenarios"][0]["limits"].get(archetype, [])

    def _extract_numeric_list(self, limits):
        out = []
        for x in limits if isinstance(limits, list) else [limits]:
            if isinstance(x, (int, float)): out.append(float(x))
            elif isinstance(x, str):
                m = re.search(r"[\d.]+", x)
                if m: out.append(float(m.group()))
        return out

    def _pick_generic(self, limits):
        if isinstance(limits, list) and limits: return random.choice(limits)
        return limits

    def _make_param(self, pd, v_min, v_typ, v_max, scenario):
        """Build GeneratedParameter from explicit min/typ/max values."""
        try:
            s_type = SpecType(pd.get("spec_type", "nominal"))
        except ValueError:
            s_type = SpecType.NOMINAL
        try:
            e_class = EngineeringClass(pd.get("engineering_class", "PERFORMANCE"))
        except ValueError:
            e_class = EngineeringClass.PERFORMANCE

        section = "ABS_MAX" if s_type in (SpecType.MAX_RATING, SpecType.MIN_RATING) else "ELEC_CHAR"

        return GeneratedParameter(
            key=pd["key"],
            label=pd["llm_context"]["formal_name"],
            symbol=pd.get("symbol", ""),
            section=section,
            value_min=v_min,
            value_typ=v_typ,
            value_max=v_max,
            unit=pd["std_unit"],
            condition=scenario.get("condition", ""),
            spec_type=s_type,
            engineering_class=e_class,
        )
