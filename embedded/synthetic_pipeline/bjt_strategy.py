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
# CONSTANTS CLASS - Physics-Aware with SI Units
# ============================================================================
class BJTConstants:
    """Constants and lookup tables for BJT generation with accurate physics"""
    
    # Process Corners for variation
    # Allows simulation of Worst Case vs Best Case scenarios
    CORNERS = {
        "TYPICAL":  {"hfe": 1.0, "vce_sat": 1.0, "vceo": 1.0},
        "MIN_SPEC": {"hfe": 0.7, "vce_sat": 1.2, "vceo": 0.9}, 
        "MAX_SPEC": {"hfe": 1.3, "vce_sat": 0.8, "vceo": 1.1},
        # Fallback support
        "WORST_CASE": {"hfe": 0.7, "vce_sat": 1.2, "vceo": 0.9},
        "BEST_CASE":  {"hfe": 1.3, "vce_sat": 0.8, "vceo": 1.1}
    }
    
    # Physics: Early Voltage scales with breakdown voltage
    EARLY_VOLTAGE_RATIO = {"Small_Signal": 3.0, "Power_BJT": 1.5}
    
    # Physics: hFE Curve Parameters
    HFE_PEAK_IC_RATIO = 0.3 # Peak gain happens at 30% of rated current usually
    KIRK_EFFECT_KNEE_RATIO = 0.8 # High current rolloff starts here
    HFE_LOW_CURRENT_ROLLOFF = 0.5 # Low current rolloff factor
    
    # Parasitic Capacitance of Package (Farads)
    PKG_PARASITIC_C = {
        "SOT-23": 0.5e-12, "TO-92": 1.0e-12, "TO-220": 2.0e-12, "DPAK": 1.5e-12
    }

    # Standard Ratings (SI Units: Amperes, Volts)
    VCEO_STANDARD = {
        "Small_Signal": [20, 30, 40, 50, 60, 80],
        "Power_BJT": [60, 80, 100, 120, 150, 200, 400, 600]
    }
    
    # Package Specifications - SOURCE OF TRUTH (SI Units)
    # pd_pkg_limit: Limit of the case itself
    # rth_ja: Thermal resistance Junction-to-Ambient (C/W)
    # ic_limit: Max current for bond wires/leadframe
    PACKAGE_SPECS = {
        "SC-70": {
            "pd_pkg_limit": 0.15, "rth_jc": 200, "rth_ja": 500, 
            "ic_limit": 0.2, "archetype": "Small_Signal",
            "dims": [2.0, 1.25, 0.95, 0.005] # L, W, H, Weight
        },
        "SOT-23": {
            "pd_pkg_limit": 0.35, "rth_jc": 150, "rth_ja": 350, 
            "ic_limit": 0.8, "archetype": "Small_Signal",
            "dims": [2.9, 1.3, 1.0, 0.008]
        },
        "TO-92": {
            "pd_pkg_limit": 0.625, "rth_jc": 83, "rth_ja": 200, 
            "ic_limit": 1.0, "archetype": "Small_Signal",
            "dims": [4.8, 3.7, 4.5, 0.19]
        },
        "SOT-223": {
            "pd_pkg_limit": 1.5, "rth_jc": 25, "rth_ja": 60, 
            "ic_limit": 3.0, "archetype": "Power_BJT",
            "dims": [6.5, 3.5, 1.6, 0.13]
        },
        "DPAK": {
            "pd_pkg_limit": 2.5, "rth_jc": 15, "rth_ja": 50, 
            "ic_limit": 5.0, "archetype": "Power_BJT",
            "dims": [6.6, 6.1, 2.3, 0.35]
        },
        "TO-220": {
            "pd_pkg_limit": 20.0, "rth_jc": 2.5, "rth_ja": 62.5, 
            "ic_limit": 15.0, "archetype": "Power_BJT",
            "dims": [10.0, 4.5, 9.0, 2.0]
        },
        "TO-247": {
            "pd_pkg_limit": 50.0, "rth_jc": 1.0, "rth_ja": 40, 
            "ic_limit": 30.0, "archetype": "Power_BJT",
            "dims": [16.0, 5.5, 4.8, 6.0]
        },
        "TO-3": {
            "pd_pkg_limit": 5.0, "rth_jc": 0.8, "rth_ja": 35, 
            "ic_limit": 30.0, "archetype": "Power_BJT", 
            "dims": [24.0, 20.0, 4.8, 15.0]
        }
    }

    # Physics: VCE(sat) Intrinsic Drop
    VCE_SAT_INTERNAL = {"Small_Signal": 0.05, "Power_BJT": 0.2}
    
    # Physics: Capacitance (Farads)
    COB_AREA_BASE = {"Small_Signal": 4.0e-12, "Power_BJT": 50.0e-12}
    CIB_CURRENT_SCALING = 0.5
    CIB_HFE_FACTOR = 0.3
    
    # Physics: fT (Hz)
    FT_BASE = {"Small_Signal": 300.0e6, "Power_BJT": 50.0e6}
# ============================================================================
# STRATEGY CLASS - Physics-Aware with SI Units
# ============================================================================
class BJTStrategy(ComponentStrategy):
    """Strategy for generating synthetic BJT datasheets with accurate physics"""
    
    def __init__(self):
        self.constants = BJTConstants()
    
    # ------------------------------------------------------------------------
    # 1. CREATE CONTEXT
    # ------------------------------------------------------------------------
    def create_context(self, schema: Dict, requested_corner: Optional[str]) -> GenerationContext:
        archetype = random.choice(schema.get('archetypes', ["Small_Signal"]))
        
        # Filter packages by archetype
        valid_packages = [p for p, data in self.constants.PACKAGE_SPECS.items() 
                          if data["archetype"] == archetype]
        if not valid_packages: valid_packages = ["SOT-23"] # Fallback
        
        package = random.choice(valid_packages)
        pkg_data = self.constants.PACKAGE_SPECS[package]
        
        corner = requested_corner if requested_corner in self.constants.CORNERS else "TYPICAL"
        
        # --- PHYSICS LOCK-IN ---
        # Determine VCEO and IC_MAX based on package limits + random selection
        primary = self._generate_primary_ratings(archetype, pkg_data)
        
        extras = {
            'requested_corner': requested_corner,
            'process_corner': corner,
            'vceo': primary['vceo'],
            'ic_max': primary['ic_max'],
            'pd_max': primary['pd_max'],
            'hfe_peak': primary['hfe_peak'],
            'ft_typ': primary['ft_typ'],
            'pkg_data': pkg_data,
            # Physics params calculated later
            'rc_bulk': None, 
            'early_voltage': None
        }
        
        return GenerationContext(
            sample_id=f"BJT_{archetype}_{package}_{uuid.uuid4().hex[:4]}",
            component_type="BJT",
            package=package,
            archetype=archetype,
            tolerance=0.1,
            process_corner=corner,
            extras=extras
        )
    
    # ------------------------------------------------------------------------
    # 2. GENERATE PRIMARY RATINGS (The Physics Engine)
    # ------------------------------------------------------------------------
    def _generate_primary_ratings(self, archetype: str, pkg_data: Dict) -> Dict[str, float]:
        
        # A. VCEO (Breakdown Voltage)
        vceo_opts = self.constants.VCEO_STANDARD[archetype]
        vceo = float(random.choice(vceo_opts))
        
        # B. IC MAX (Current Rating)
        # Must act as a constraint on the package limit
        pkg_i_lim = pkg_data['ic_limit']
        # Generate a value logarithmically up to the package limit
        ic_target = 10 ** random.uniform(math.log10(pkg_i_lim * 0.1), math.log10(pkg_i_lim))
        # Snap to nice numbers
        ic_max = self._snap_to_grid(ic_target)
        
        # C. PD MAX (Power Dissipation) - THERMAL PHYSICS
        # Pd = (Tj_max - Ta) / Rth_ja
        tj_max = 150.0
        ta = 25.0
        pd_thermal = (tj_max - ta) / pkg_data['rth_ja']
        # The rating is the minimum of Package Limit and Thermal Limit
        pd_max = min(pkg_data['pd_pkg_limit'], pd_thermal)
        
        # D. Gain (hFE)
        hfe_opts = [100, 150, 200, 300] if archetype == "Small_Signal" else [40, 60, 80, 100]
        hfe_peak = float(random.choice(hfe_opts))
        
        # E. fT (Speed)
        # Higher voltage/power usually means slower (larger base width/parasitics)
        ft_base = self.constants.FT_BASE[archetype]
        ft_typ = ft_base * (50.0 / vceo) ** 0.3  # Slight penalty for HV
        
        return {
            'vceo': vceo,
            'ic_max': ic_max,
            'pd_max': pd_max,
            'hfe_peak': hfe_peak,
            'ft_typ': ft_typ
        }

    # ------------------------------------------------------------------------
    # 3. CREATE CUSTOM PARAMETER
    # ------------------------------------------------------------------------
    def create_custom_parameter(self, key: str, context: GenerationContext, param_def: Dict) -> Optional[GeneratedParameter]:
        extras = context.extras
        corner_mult = self.constants.CORNERS[extras['process_corner']]
        
        # --- VCEO ---
        if key == 'vceo':
            val = extras['vceo'] * corner_mult['vceo']
            return self._build_param(key, val, "V", param_def, is_max=True)

        # --- IC MAX ---
        if key == 'ic_max':
            val_si = extras['ic_max']
            disp_val, unit = self._auto_scale(val_si, 'A')
            return self._build_param(key, disp_val, unit, param_def, is_max=True)

        # --- POWER DISSIPATION ---
        if key == 'power_dissipation':
            # Already calculated thermally
            val_si = extras['pd_max']
            disp_val, unit = self._auto_scale(val_si, 'W')
            return self._build_param(key, disp_val, unit, param_def, is_max=True)

        # --- hFE (DC Current Gain) ---
        if key == 'hfe':
            # Logic for test condition
            ic_test_si = self._get_safe_test_current(param_def, extras['ic_max'])
            
            # Physics Calculation
            hfe_val = self._calculate_hfe_physics(ic_test_si, context)
            hfe_val *= corner_mult['hfe']
            
            # Construct Display
            ic_disp, i_unit = self._auto_scale(ic_test_si, 'A')
            cond = f"VCE=5V, IC={ic_disp:.1f}{i_unit}"
            
            return GeneratedParameter(
                key='hfe', label="DC Current Gain", symbol="hFE",
                section='ELEC_CHAR', value_min=int(hfe_val*0.6), value_typ=int(hfe_val),
                value_max=int(hfe_val*1.5), unit="", condition=cond,
                spec_type=SpecType.NOMINAL, engineering_class=EngineeringClass.PERFORMANCE
            )

        # --- VCE(sat) ---
        if key == 'vce_sat':
            ic_test_si = self._get_safe_test_current(param_def, extras['ic_max'])
            ib_test_si = ic_test_si / 10.0 # Forced Beta = 10 standard
            
            # Physics Calculation
            v_sat = self._calculate_vce_sat_physics(ic_test_si, context)
            v_sat *= corner_mult['vce_sat']
            
            v_disp, v_unit = self._auto_scale(v_sat, 'V')
            ic_disp, i_unit = self._auto_scale(ic_test_si, 'A')
            ib_disp, ib_unit = self._auto_scale(ib_test_si, 'A')
            
            return GeneratedParameter(
                key='vce_sat', label="Collector-Emitter Saturation Voltage", symbol="VCE(sat)",
                section='ELEC_CHAR', value_typ=v_disp, value_max=v_disp*1.3,
                unit=v_unit, condition=f"IC={ic_disp:.1f}{i_unit}, IB={ib_disp:.1f}{ib_unit}",
                spec_type=SpecType.MAX_LIMIT, engineering_class=EngineeringClass.PERFORMANCE
            )

        # --- Output Capacitance (Cob) ---
        if key == 'cob':
            # Physics: Area based + Package Parasitic
            # Area scales roughly with Ic_max
            area_factor = math.sqrt(extras['ic_max'] / 0.1) 
            base_cob = self.constants.COB_AREA_BASE[context.archetype]
            pkg_c = self.constants.PKG_PARASITIC_C.get(context.package, 1e-12)
            
            # Cob = C_junction + C_pkg. Junction C decreases with Voltage (V^-0.5)
            # Standard test is VCB=10V
            v_test = 10.0
            cob_junc = (base_cob * area_factor) / math.sqrt(v_test)
            cob_total = cob_junc + pkg_c
            
            val_disp, unit = self._auto_scale(cob_total, 'F')
            return GeneratedParameter(
                key='cob', label="Output Capacitance", symbol="Cob",
                section='ELEC_CHAR', value_typ=val_disp, value_max=val_disp*1.3,
                unit=unit, condition="VCB=10V, f=1MHz",
                spec_type=SpecType.MAX_LIMIT
            )

        # --- fT (Transition Frequency) ---
        if key == 'ft':
            val_disp, unit = self._auto_scale(extras['ft_typ'], 'Hz')
            return GeneratedParameter(
                key='ft', label="Transition Frequency", symbol="fT",
                section='ELEC_CHAR', value_typ=val_disp, unit=unit,
                condition="VCE=10V, f=100MHz", spec_type=SpecType.TYPICAL
            )

        return None

    # ------------------------------------------------------------------------
    # 4. PHYSICS HELPERS
    # ------------------------------------------------------------------------
    def _calculate_hfe_physics(self, ic: float, ctx: GenerationContext) -> float:
        """
        Calculates hFE at a specific current using a roll-off model.
        
        """
        extras = ctx.extras
        peak_hfe = extras['hfe_peak']
        ic_max = extras['ic_max']
        
        # Normalized current
        ic_norm = ic / ic_max
        
        # 1. Low Current Roll-off (Recombination)
        # Below 1% of rated current, gain drops
        low_current_factor = 1.0
        if ic_norm < 0.01:
            low_current_factor = (ic_norm / 0.01) ** 0.5
            
        # 2. High Current Roll-off (Kirk Effect / High Injection)
        # Above 50% of rated current, gain drops
        high_current_factor = 1.0
        if ic_norm > 0.5:
            high_current_factor = 1.0 / (1.0 + 2.0 * (ic_norm - 0.5)**2)
            
        return peak_hfe * low_current_factor * high_current_factor

    def _calculate_vce_sat_physics(self, ic: float, ctx: GenerationContext) -> float:
        """
        Calculates VCE(sat) = V_offset + I * R_bulk
        """
        extras = ctx.extras
        
        # Lazy load Rc_bulk if not set
        if extras['rc_bulk'] is None:
            # We want Vce(sat) to be approx 0.3V - 0.5V at max current
            target_v = 0.4 # Volts
            v_int = self.constants.VCE_SAT_INTERNAL[ctx.archetype]
            extras['rc_bulk'] = (target_v - v_int) / extras['ic_max']
            
        r_bulk = extras['rc_bulk']
        v_int = self.constants.VCE_SAT_INTERNAL[ctx.archetype]
        
        # Temperature effect (Simulation): Hotter = Higher Resistance
        if ctx.process_corner == "MAX_SPEC" or "HOT" in str(ctx.extras.get('requested_corner')):
             r_bulk *= 1.4 # Silicon resistance increases with temp
             
        return v_int + (ic * r_bulk)

    def _get_safe_test_current(self, param_def: Dict, ic_max: float) -> float:
        """Extracts a test current from schema condition, bounded by physics"""
        cond = param_def['scenarios'][0].get('condition', '')
        
        # Try to parse "IC=..."
        match = re.search(r'IC\s*=\s*([\d.]+)\s*([mµu]?)A', cond, re.IGNORECASE)
        if match:
            val = float(match.group(1))
            prefix = match.group(2).lower()
            if prefix == 'm': val *= 1e-3
            elif prefix in ['µ', 'u']: val *= 1e-6
            return val
            
        # Default logic if no condition found
        # Return 10% of max current, but lower bound 1mA
        return max(ic_max * 0.1, 1e-3)

    # ------------------------------------------------------------------------
    # 5. UTILS
    # ------------------------------------------------------------------------
    def _auto_scale(self, value: float, base_unit: str) -> Tuple[float, str]:
        if value is None or value == 0: return 0, base_unit
        
        # Special case for Ohms
        if base_unit == 'Ω':
            if value < 1.0: return value*1000, 'mΩ'
            return value, 'Ω'

        prefixes = [(1e9,'G'), (1e6,'M'), (1e3,'k'), (1,''), (1e-3,'m'), (1e-6,'µ'), (1e-9,'n'), (1e-12,'p')]
        
        for scale, prefix in prefixes:
            if abs(value) >= scale:
                # formatting to avoid 0.005 kA -> 5 A logic loop if not careful, 
                # but simple greedy works for standard BOM
                if abs(value) < scale * 1000: 
                    return value / scale, f"{prefix}{base_unit}"
        
        return value, base_unit

    def _build_param(self, key, val, unit, pd, is_max=False):
        return GeneratedParameter(
            key=key, label=pd['llm_context']['formal_name'], symbol=pd['symbol'],
            section='ABS_MAX' if is_max else 'ELEC_CHAR',
            value_typ=val if not is_max else None, value_max=val if is_max else None,
            unit=unit, condition=pd['scenarios'][0]['condition'],
            spec_type=SpecType.MAX_RATING if is_max else SpecType.NOMINAL
        )

    def _snap_to_grid(self, val):
        # Helper to make numbers look "engineered" (e.g. 0.15 instead of 0.14832)
        if val < 1: return round(val, 3)
        if val < 10: return round(val, 2)
        return int(val)

    # Required abstract method implementation
    def calculate_base_value(self, key: str, limits: Any, context: GenerationContext) -> Any:
        # Pass-through for package dims if needed by pipeline
        if key == 'package_code': return context.package
        if key in ['width', 'length', 'height']:
            idx = {'length':0, 'width':1, 'height':2}[key]
            return context.extras['pkg_data']['dims'][idx]
        # Generic fallback: pick a random numeric value from the archetype's limits array
        if isinstance(limits, dict):
            arch_list = limits.get(context.archetype, [])
            if isinstance(arch_list, list):
                numeric = [v for v in arch_list if isinstance(v, (int, float))]
                return random.choice(numeric) if numeric else None
        return None

    def apply_correlations(self, result: DatasheetResult) -> None:
        pass
