
import random
import math
import uuid
import re
from typing import Dict, Any, Optional, List, Tuple

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

from synthetic_pipeline.strategy_utils import snap_to_e_series
from synthetic_pipeline.strategy_base import ComponentStrategy

# ============================================================================
# CONSTANTS & PHYSICS SPECS
# ============================================================================
class CapacitorConstants:
    """Constants and lookup tables for capacitor generation"""

    # Valid packages per archetype — prevents physically impossible combos
    ARCHETYPE_PACKAGES = {
        "Ceramic_MLCC":         ["0201", "0402", "0603", "0805", "1206", "1210"],
        "Ceramic_C0G":          ["0201", "0402", "0603", "0805", "1206"],
        "Electrolytic_Alum":    ["Radial_5mm", "Radial_6.3mm", "Radial_8mm", "Radial_10mm"],
        "Electrolytic_Polymer": ["Case_A", "Case_B", "Case_C", "Case_D"],
        "Tantalum_Solid":       ["Case_A", "Case_B", "Case_C", "Case_D"],
        "Tantalum_Polymer":     ["Case_A", "Case_B", "Case_C", "Case_D"],
        "Film_Polyester":       ["Radial_5mm", "Radial_6.3mm", "Radial_8mm", "Radial_10mm"],
        "Film_Polypropylene":   ["Radial_5mm", "Radial_6.3mm", "Radial_8mm", "Radial_10mm"],
        "Supercapacitor":       ["Coin_Type"],
    }

    # ------------------------------------------------------------------------
    # MASTER PACKAGE SPECIFICATIONS
    # dims: [Length, Width, Height, Weight(g)]
    # limits: {max_v: Volt, cv: uF*V product}
    # esl: Equivalent Series Inductance (nH) - Critical for SRF calculation
    # ------------------------------------------------------------------------
    PACKAGE_SPECS = {
        # --- CERAMIC MLCC ---
        "0201": { "dims": [0.6, 0.3, 0.3, 0.0003], "limits": { "max_v": 25,  "cv": 100 },  "esl": 0.2 },
        "0402": { "dims": [1.0, 0.5, 0.5, 0.001],  "limits": { "max_v": 50,  "cv": 500 },  "esl": 0.4 },
        "0603": { "dims": [1.6, 0.8, 0.8, 0.002],  "limits": { "max_v": 100, "cv": 2200 }, "esl": 0.6 },
        "0805": { "dims": [2.0, 1.25, 1.25, 0.005],"limits": { "max_v": 100, "cv": 10000 },"esl": 0.8 },
        "1206": { "dims": [3.2, 1.6, 1.6, 0.010],  "limits": { "max_v": 200, "cv": 22000 },"esl": 1.0 },
        "1210": { "dims": [3.2, 2.5, 2.5, 0.015],  "limits": { "max_v": 250, "cv": 47000 },"esl": 1.2 },
        
        # --- ELECTROLYTIC / POLYMER (RADIAL) ---
        "Radial_5mm":   { "dims": [5.0, 5.0, 11.0, 0.4], "limits": { "max_v": 50, "cv": 22000 },  "esl": 3.0 },
        "Radial_6.3mm": { "dims": [6.3, 6.3, 11.0, 0.6], "limits": { "max_v": 63, "cv": 50000 },  "esl": 4.0 },
        "Radial_8mm":   { "dims": [8.0, 8.0, 12.0, 1.2], "limits": { "max_v": 100,"cv": 100000 }, "esl": 5.0 },
        "Radial_10mm":  { "dims": [10.0, 10.0, 16.0, 2.0],"limits": { "max_v": 100,"cv": 200000 }, "esl": 6.0 },

        # --- TANTALUM / SMD MOLDED ---
        "Case_A": { "dims": [3.2, 1.6, 1.6, 0.02], "limits": { "max_v": 25, "cv": 2200 }, "esl": 1.2 },
        "Case_B": { "dims": [3.5, 2.8, 1.9, 0.05], "limits": { "max_v": 35, "cv": 4700 }, "esl": 1.5 },
        "Case_C": { "dims": [6.0, 3.2, 2.6, 0.10], "limits": { "max_v": 50, "cv": 10000 },"esl": 1.8 },
        "Case_D": { "dims": [7.3, 4.3, 2.9, 0.15], "limits": { "max_v": 50, "cv": 22000 },"esl": 2.2 },
        
        # --- SUPERCAPACITOR ---
        "Coin_Type": { "dims": [19.0, 19.0, 5.0, 2.5], "limits": { "max_v": 5.5, "cv": 20000000 }, "esl": 10.0 },
    }
    
    # Dissipation Factor (DF) - The chemistry factor for ESR calculation
    DF_MAP = {
        "Ceramic_MLCC":         0.02,
        "Ceramic_C0G":          0.001,
        "Electrolytic_Alum":    0.15,
        "Electrolytic_Polymer": 0.05,
        "Tantalum_Solid":       0.06,
        "Tantalum_Polymer":     0.04,
        "Film_Polyester":       0.008,
        "Film_Polypropylene":   0.001,
        "Supercapacitor":       1.0,
    }

    # Minimum realistic capacitance per archetype (Farads)
    # Prevents log-uniform from picking pF values for electrolytic types.
    MIN_CAP_BY_ARCHETYPE = {
        "Ceramic_MLCC":         1e-12,    # 1 pF
        "Ceramic_C0G":          1e-12,    # 1 pF
        "Electrolytic_Alum":    1e-6,     # 1 µF
        "Electrolytic_Polymer": 10e-6,    # 10 µF
        "Tantalum_Solid":       100e-9,   # 100 nF
        "Tantalum_Polymer":     10e-6,    # 10 µF
        "Film_Polyester":       10e-9,    # 10 nF
        "Film_Polypropylene":   1e-9,     # 1 nF
        "Supercapacitor":       0.1,      # 100 mF
    }
    
    TOLERANCE_MAP = {
        "Ceramic_MLCC": 0.10, "Electrolytic_Alum": 0.20, "Tantalum_Solid": 0.10, 
        "Film_Polypropylene": 0.05, "Supercapacitor": 0.30
    }

# ============================================================================
# STRATEGY CLASS
# ============================================================================
class CapacitorStrategy(ComponentStrategy):
    """
    Hermetic Capacitor Strategy.
    Physics Chain: Package -> Limits (CV) -> Voltage -> Capacitance -> ESR/SRF (Derived)
    """

    def __init__(self):
        self.constants = CapacitorConstants()

    # ------------------------------------------------------------------------
    # 1. CREATE CONTEXT (THE HERMETIC SELECTION)
    # ------------------------------------------------------------------------
    def create_context(self, schema: Dict, requested_corner: Optional[str]) -> GenerationContext:
        archetype = random.choice(schema.get('archetypes', ["Ceramic_MLCC"]))

        # Filter packages: use archetype-specific list, falling back to all known packages
        archetype_pkgs = self.constants.ARCHETYPE_PACKAGES.get(archetype)
        if archetype_pkgs:
            valid_packages = [p for p in archetype_pkgs if p in self.constants.PACKAGE_SPECS]
        else:
            valid_packages = list(self.constants.PACKAGE_SPECS.keys())
        if not valid_packages:
            valid_packages = list(self.constants.PACKAGE_SPECS.keys())

        target_package = random.choice(valid_packages)
        tolerance = self.constants.TOLERANCE_MAP.get(archetype, 0.20)
        
        # --- CRITICAL: Link Voltage & Capacitance Physically ---
        v_rated, c_val = self._generate_physics_compliant_values(archetype, target_package, schema)
        
        extras = {
            'voltage_rating': v_rated,
            'capacitance_value': c_val,
            'is_polar': archetype in ['Electrolytic_Alum', 'Tantalum_Solid', 'Supercapacitor']
        }

        return GenerationContext(
            sample_id=str(uuid.uuid4())[:8],
            component_type="CAPACITOR",
            package=target_package,
            archetype=archetype,
            tolerance=tolerance,
            process_corner=requested_corner or "TYPICAL",
            extras=extras
        )

    # ------------------------------------------------------------------------
    # 2. HELPER: CV PRODUCT LOGIC
    # ------------------------------------------------------------------------
    def _generate_physics_compliant_values(self, archetype: str, package: str, schema: Dict) -> Tuple[float, float]:
        """
        Generates Voltage and Capacitance that FIT inside the chosen package.
        Formula: Capacitance * Voltage <= Max_CV_Product_of_Package
        """
        pkg_data = self.constants.PACKAGE_SPECS.get(package)
        if not pkg_data: return 50.0, 1e-9 # Fallback

        limits = pkg_data['limits']
        max_v_pkg = limits['max_v']
        max_cv_si = limits['cv'] * 1e-6 # Convert uF*V to F*V

        # 1. Pick a Voltage
        std_volts = [4.0, 6.3, 10, 16, 25, 35, 50, 63, 100, 200, 250, 400, 630]
        valid_std = [v for v in std_volts if v <= max_v_pkg]
        v_rated = random.choice(valid_std) if valid_std else max_v_pkg

        # 2. Calculate Max Capacitance allowed
        max_cap_si = max_cv_si / v_rated

        # 3. Pick Capacitance (Log-Uniform) — floor is archetype-specific
        min_cap_si = self.constants.MIN_CAP_BY_ARCHETYPE.get(archetype, 1e-12)

        if max_cap_si < min_cap_si: max_cap_si = min_cap_si * 1.1

        log_min = math.log10(min_cap_si)
        log_max = math.log10(max_cap_si)
        c_final = 10 ** random.uniform(log_min, log_max)

        # Snap to E-series
        c_final = snap_to_e_series(c_final, "E12")
        
        return v_rated, c_final

    # ------------------------------------------------------------------------
    # 3. CREATE PARAMETERS
    # ------------------------------------------------------------------------
    def create_custom_parameter(self, key: str, context: GenerationContext, param_def: Dict) -> Optional[GeneratedParameter]:
        
        if key == 'capacitance':
            c_val = context.extras['capacitance_value']
            tol = context.tolerance
            disp_val, disp_unit = self._auto_scale(c_val, 'F')
            
            return GeneratedParameter(
                key='capacitance', label="Capacitance", symbol="C", section="ELEC_CHAR",
                value_min=self._round(disp_val * (1-tol)),
                value_typ=self._round(disp_val),
                value_max=self._round(disp_val * (1+tol)),
                unit=disp_unit,
                condition="1kHz, 25°C",
                spec_type=SpecType.NOMINAL, engineering_class=EngineeringClass.PERFORMANCE
            )

        if key == 'rated_voltage':
            v_val = context.extras['voltage_rating']
            return GeneratedParameter(
                key='rated_voltage', label="Rated Voltage", symbol="V_R", section="ABS_MAX",
                value_typ=v_val, unit="V",
                spec_type=SpecType.MAX_RATING, engineering_class=EngineeringClass.SAFETY_LIMIT
            )

        if key == 'operating_temp_range':
            for scenario in param_def.get("scenarios", []):
                arch_limits = scenario.get("limits", {}).get(context.archetype)
                if not arch_limits or not isinstance(arch_limits, list):
                    continue
                pair = random.choice(arch_limits)
                if isinstance(pair, list) and len(pair) == 2:
                    return GeneratedParameter(
                        key=key,
                        label=param_def["llm_context"]["formal_name"],
                        symbol=param_def.get("symbol", ""),
                        section="ABS_MAX",
                        value_min=float(pair[0]),
                        value_typ=None,
                        value_max=float(pair[1]),
                        unit="°C",
                        condition=scenario.get("condition", ""),
                        spec_type=SpecType.OPERATIONAL_RANGE,
                        engineering_class=EngineeringClass.OPERATING_CONDITION,
                    )
            return None

        if key == 'capacitance_tolerance':
            for scenario in param_def.get("scenarios", []):
                arch_limits = scenario.get("limits", {}).get(context.archetype)
                if not arch_limits or not isinstance(arch_limits, list):
                    continue
                val_str = str(random.choice(arch_limits))
                m = re.search(r'(\d+(?:\.\d+)?)', val_str)
                if m:
                    return GeneratedParameter(
                        key=key,
                        label=param_def["llm_context"]["formal_name"],
                        symbol=param_def.get("symbol", ""),
                        section="ELEC_CHAR",
                        value_min=None,
                        value_typ=float(m.group(1)),
                        value_max=None,
                        unit="%",
                        condition=scenario.get("condition", ""),
                        spec_type=SpecType.NOMINAL,
                        engineering_class=EngineeringClass.NOMINAL_PARAMETER,
                    )
            return None

        return None

    # ------------------------------------------------------------------------
    # 4. PHYSICS ENGINE: BASE VALUES (DIMS & SPECS)
    # ------------------------------------------------------------------------
    def calculate_base_value(self, key: str, limits: Any, context: GenerationContext) -> Any:
        pkg_data = self.constants.PACKAGE_SPECS.get(context.package)
        if not pkg_data: return None
        dims = pkg_data['dims']
        
        if key == 'length': return dims[0]
        if key == 'width':  return dims[1]
        if key == 'height': return dims[2]
        if key == 'weight': return dims[3]
        if key == 'esl':    return pkg_data.get('esl', 0.5)
        if key == 'dissipation_factor': return self.constants.DF_MAP.get(context.archetype, 0.05)

        # These keys are owned by apply_correlations which builds complete,
        # physically consistent triplets. Returning None here prevents the
        # schema fallback from creating a half-baked parameter that correlations
        # would later partially overwrite (causing min/max vs typ mismatches).
        if key in ('esr', 'self_resonant_freq', 'ripple_current'):
            return None

        # General fallback: pick a random archetype-specific numeric value.
        # Skip if value is 0 (used as N/A marker in the schema).
        if isinstance(limits, dict):
            arch_vals = limits.get(context.archetype, [])
            if isinstance(arch_vals, list):
                numeric = [v for v in arch_vals if isinstance(v, (int, float)) and v != 0]
                return random.choice(numeric) if numeric else None

        return None

    # ------------------------------------------------------------------------
    # 5. DERIVED PHYSICS (CORRELATIONS) - THE OPTIMIZED LOGIC
    # ------------------------------------------------------------------------
    def apply_correlations(self, result: DatasheetResult) -> None:
        """
        Creates ESR, SRF, and Ripple Current parameters from first principles.
        These are appended as new GeneratedParameter objects rather than patching
        existing ones, which prevents min/max vs typ mismatches caused by the
        schema-based fallback path running before correlations.
        """
        ctx = result.context

        if "capacitance_value" not in ctx.extras:
            return
        C = ctx.extras["capacitance_value"]
        if C <= 0:
            return

        pkg_data = self.constants.PACKAGE_SPECS.get(ctx.package, {})
        ESL = pkg_data.get("esl", 1.0) * 1e-9  # nH → H
        DF  = self.constants.DF_MAP.get(ctx.archetype, 0.05)
        is_ceramic = "Ceramic" in ctx.archetype

        # ── ESR ──────────────────────────────────────────────────────────────
        freq_esr = 100e3 if is_ceramic else 1e3
        esr_ohm  = DF / (2 * math.pi * freq_esr * C) + (0.005 if is_ceramic else 0.05)

        if esr_ohm < 1.0:
            esr_typ  = self._round(esr_ohm * 1000)
            esr_max  = self._round(esr_ohm * 1000 * 1.5)
            esr_unit = "mΩ"
        else:
            esr_typ  = self._round(esr_ohm)
            esr_max  = self._round(esr_ohm * 1.5)
            esr_unit = "Ω"

        result.parameters.append(GeneratedParameter(
            key="esr", label="Equivalent Series Resistance", symbol="ESR",
            section="DYNAMIC_CHAR",
            value_min=None, value_typ=esr_typ, value_max=esr_max,
            unit=esr_unit,
            condition=f"{int(freq_esr / 1000)}kHz, T_A=25°C",
            spec_type=SpecType.MAX_LIMIT,
            engineering_class=EngineeringClass.PERFORMANCE_LIMIT,
        ))

        # ── SRF ──────────────────────────────────────────────────────────────
        if ESL > 0:
            f_mhz    = round(1.0 / (2 * math.pi * math.sqrt(ESL * C)) / 1e6, 1)
            srf_min  = round(f_mhz * 0.8, 1)

            result.parameters.append(GeneratedParameter(
                key="self_resonant_freq", label="Self Resonant Frequency", symbol="SRF",
                section="DYNAMIC_CHAR",
                value_min=srf_min, value_typ=f_mhz, value_max=None,
                unit="MHz",
                condition="T_A=25°C",
                spec_type=SpecType.NOMINAL,
                engineering_class=EngineeringClass.PERFORMANCE_LIMIT,
            ))

        # ── Ripple Current ────────────────────────────────────────────────────
        # Thermal model: P_max = volume × 1µW/mm³.
        # ESR floor of 1mΩ prevents blow-up for very large capacitors where
        # the formula ESR = DF/(2πfC) yields sub-mΩ values at 100kHz.
        dims       = pkg_data.get("dims", [1, 1, 1])
        vol_mm3    = dims[0] * dims[1] * dims[2]
        esr_ripple = max(DF / (2 * math.pi * 100e3 * C), 0.001)  # floor 1 mΩ
        p_max_w    = vol_mm3 * 1e-6                               # 1 µW/mm³
        i_ma       = max(int(math.sqrt(p_max_w / esr_ripple) * 1000), 100)

        result.parameters.append(GeneratedParameter(
            key="ripple_current", label="Ripple Current", symbol="I_r",
            section="DYNAMIC_CHAR",
            value_min=None, value_typ=i_ma, value_max=None,
            unit="mA",
            condition="T_A=85°C, f=100kHz",
            spec_type=SpecType.MIN_LIMIT,
            engineering_class=EngineeringClass.PERFORMANCE_LIMIT,
        ))

    # ------------------------------------------------------------------------
    # UTILS
    # ------------------------------------------------------------------------
    def _auto_scale(self, val, unit):
        if val < 1e-9: return val * 1e12, "pF"
        if val < 1e-6: return val * 1e9, "nF"
        if val < 1e-3: return val * 1e6, "µF"
        if val < 1:    return val * 1e3, "mF"
        return val, unit

    def _round(self, val):
        if val is None: return None
        if val < 10: return round(val, 2)
        return int(val)
