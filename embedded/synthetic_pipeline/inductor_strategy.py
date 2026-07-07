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

from synthetic_pipeline.strategy_utils import snap_to_e_series
from synthetic_pipeline.strategy_base import ComponentStrategy

# ============================================================================
# CONSTANTS CLASS - SINGLE SOURCE OF TRUTH
# ============================================================================
class InductorConstants:
    """Constants and lookup tables for inductor generation"""
    
    # ========================================================================
    # MASTER PACKAGE SPECIFICATIONS - SINGLE SOURCE OF TRUTH
    # ========================================================================
    PACKAGE_SPECS = {
        # --- ULTRA-SMALL SMD (RF / Signal) ---
        "01005": {
            "dimensions": [0.4, 0.2, 0.13, 0.0001],  # L, W, H (mm), Weight (g)
            "limits": { "max_current_a": 0.1, "max_inductance_h": 47e-9, "max_power_watts": 0.03, "dcr_max_ohm": 0.8, "footprint_area_mm2": 0.08, "core_volume_mm3": 0.01 }
        },
        "0201": {
            "dimensions": [0.6, 0.3, 0.23, 0.0002],
            "limits": { "max_current_a": 0.2, "max_inductance_h": 100e-9, "max_power_watts": 0.05, "dcr_max_ohm": 0.5, "footprint_area_mm2": 0.18, "core_volume_mm3": 0.04 }
        },
        "0402": {
            "dimensions": [1.0, 0.5, 0.5, 0.001],
            "limits": { "max_current_a": 0.5, "max_inductance_h": 220e-9, "max_power_watts": 0.1, "dcr_max_ohm": 0.3, "footprint_area_mm2": 0.5, "core_volume_mm3": 0.25 }
        },
        "0603": {
            "dimensions": [1.6, 0.8, 0.8, 0.003],
            "limits": { "max_current_a": 1.0, "max_inductance_h": 1e-6, "max_power_watts": 0.15, "dcr_max_ohm": 0.2, "footprint_area_mm2": 1.28, "core_volume_mm3": 1.15 }
        },
        "0805": {
            "dimensions": [2.0, 1.25, 1.25, 0.008],
            "limits": { "max_current_a": 2.0, "max_inductance_h": 4.7e-6, "max_power_watts": 0.25, "dcr_max_ohm": 0.15, "footprint_area_mm2": 2.5, "core_volume_mm3": 3.1 }
        },
        
        # --- STANDARD SMD (Power / General) ---
        "1008": {
            "dimensions": [2.5, 2.0, 2.0, 0.015],
            "limits": { "max_current_a": 2.5, "max_inductance_h": 10e-6, "max_power_watts": 0.4, "dcr_max_ohm": 0.12, "footprint_area_mm2": 5.0, "core_volume_mm3": 10.0 }
        },
        "1206": {
            "dimensions": [3.2, 1.6, 1.6, 0.02],
            "limits": { "max_current_a": 3.0, "max_inductance_h": 22e-6, "max_power_watts": 0.5, "dcr_max_ohm": 0.1, "footprint_area_mm2": 5.12, "core_volume_mm3": 8.2 }
        },
        "1210": {
            "dimensions": [3.2, 2.5, 2.5, 0.04],
            "limits": { "max_current_a": 4.0, "max_inductance_h": 47e-6, "max_power_watts": 0.8, "dcr_max_ohm": 0.08, "footprint_area_mm2": 8.0, "core_volume_mm3": 20.0 }
        },
        "1812": {
            "dimensions": [4.5, 3.2, 3.2, 0.08],
            "limits": { "max_current_a": 6.0, "max_inductance_h": 100e-6, "max_power_watts": 1.2, "dcr_max_ohm": 0.06, "footprint_area_mm2": 14.4, "core_volume_mm3": 46.0 }
        },
        
        # --- POWER INDUCTOR PACKAGES ---
        "2520": {
            "dimensions": [2.5, 2.0, 1.0, 0.025],
            "limits": { "max_current_a": 5.0, "max_inductance_h": 22e-6, "max_power_watts": 1.5, "dcr_max_ohm": 0.05, "footprint_area_mm2": 5.0, "core_volume_mm3": 5.0 }
        },
        "3225": {
            "dimensions": [3.2, 2.5, 2.0, 0.045],
            "limits": { "max_current_a": 6.5, "max_inductance_h": 47e-6, "max_power_watts": 2.0, "dcr_max_ohm": 0.04, "footprint_area_mm2": 8.0, "core_volume_mm3": 16.0 }
        },
        "4040": {
            "dimensions": [4.0, 4.0, 3.0, 0.15],
            "limits": { "max_current_a": 8.0, "max_inductance_h": 100e-6, "max_power_watts": 3.0, "dcr_max_ohm": 0.03, "footprint_area_mm2": 16.0, "core_volume_mm3": 48.0 }
        },
        "5050": {
            "dimensions": [5.0, 5.0, 4.0, 0.3],
            "limits": { "max_current_a": 10.0, "max_inductance_h": 220e-6, "max_power_watts": 5.0, "dcr_max_ohm": 0.02, "footprint_area_mm2": 25.0, "core_volume_mm3": 100.0 }
        },
        "6060": {
            "dimensions": [6.0, 6.0, 5.0, 0.6],
            "limits": { "max_current_a": 15.0, "max_inductance_h": 470e-6, "max_power_watts": 8.0, "dcr_max_ohm": 0.015, "footprint_area_mm2": 36.0, "core_volume_mm3": 180.0 }
        },
        
        # --- THROUGH-HOLE / SPECIALTY ---
        "Radial": {
            "dimensions": [8.0, 8.0, 10.0, 1.5],
            "limits": { "max_current_a": 12.0, "max_inductance_h": 10e-3, "max_power_watts": 5.0, "dcr_max_ohm": 0.05, "footprint_area_mm2": 64.0, "core_volume_mm3": 640.0 }
        },
        "Axial": {
            "dimensions": [12.0, 4.0, 4.0, 0.8],
            "limits": { "max_current_a": 5.0, "max_inductance_h": 1e-3, "max_power_watts": 2.0, "dcr_max_ohm": 0.1, "footprint_area_mm2": 48.0, "core_volume_mm3": 192.0 }
        },
        "Toroid": {
            "dimensions": [20.0, 20.0, 10.0, 10.0],
            "limits": { "max_current_a": 30.0, "max_inductance_h": 100e-3, "max_power_watts": 25.0, "dcr_max_ohm": 0.005, "footprint_area_mm2": 400.0, "core_volume_mm3": 4000.0 }
        }
    }

    ARCHETYPES = ["Multilayer_Ceramic", "Wirewound_Ferrite", "Power_Shielded"]
    
    # Tolerance mapping
    TOLERANCE_MAP = {
        "Power_Ferrite": 0.20,
        "RF_Ceramic": 0.05,
        "Common_Mode_Choke": 0.25
    }
    
    # Core material properties
    CORE_MATERIALS = {
        "Power_Ferrite": {
            "permeability": 1500,
            "saturation_t": 0.4,  # Tesla (SI)
            "curie_temp_c": 220,
            "has_saturation": True
        },
        "RF_Ceramic": {
            "permeability": 1,  # Air core
            "saturation_t": None,
            "curie_temp_c": 800,
            "has_saturation": False
        },
        "Common_Mode_Choke": {
            "permeability": 5000,
            "saturation_t": 0.35,
            "curie_temp_c": 150,
            "has_saturation": True
        }
    }
    
    # Physical constants (SI units)
    COPPER_RESISTIVITY_OHM_M = 1.72e-8  # Ω·m at 20°C
    MU_0 = 4 * math.pi * 1e-7  # H/m
    WIRE_FILL_FACTOR = 0.35
    
    # Parasitic capacitance base (Farads - SI)
    SRF_BASE_CAPACITANCE_F = {
        "Power_Ferrite": 3e-12,  # 3 pF
        "RF_Ceramic": 0.3e-12,   # 0.3 pF
        "Common_Mode_Choke": 8e-12
    }
    
    # Q factor baseline
    Q_FACTOR_BASE = {
        "Power_Ferrite": 30,
        "RF_Ceramic": 60,
        "Common_Mode_Choke": 20
    }
    
    # Thermal resistance baseline (°C/W)
    THERMAL_RESISTANCE_BASE = {
        "Power_Ferrite": 100,
        "RF_Ceramic": 150,
        "Common_Mode_Choke": 80
    }


# ============================================================================
# STRATEGY CLASS
# ============================================================================
class InductorStrategy(ComponentStrategy):
    """Physics-validated synthetic inductor datasheet generator"""

    # Non-electrical params — excluded to keep document clean
    EXCLUDED_KEYS = {'package_code', 'height', 'weight', 'length', 'width'}

    def __init__(self):
        self.constants = InductorConstants()
    
    # ------------------------------------------------------------------------
    # 1. CREATE CONTEXT (HIERARCHICAL SELECTION)
    # ------------------------------------------------------------------------
    def create_context(self, schema: Dict, requested_corner: Optional[str]) -> GenerationContext:
        """Select archetype and package, precompute primary values"""
        
        # Step 1: Select archetype
        archetypes = schema.get('archetypes', ["Power_Ferrite"])
        archetype = random.choice(archetypes)
        
        # Step 2: Get valid packages for archetype
        package_param = next((p for p in schema['PACKAGE'] if p['key']=='package_code'), None)
        valid_packages = ["0603"] # Fallback
        
        if package_param:
            raw_limits = package_param['scenarios'][0]['limits']
            if isinstance(raw_limits, dict):
                valid_packages = raw_limits.get(archetype, [])
            
        # Ensure packages exist in our physics constants
        valid_packages = [p for p in valid_packages if p in self.constants.PACKAGE_SPECS]
        if not valid_packages: 
            valid_packages = ["0603"] 
        
        # Step 3: Select package
        target_package = random.choice(valid_packages)
        tolerance = self.constants.TOLERANCE_MAP.get(archetype, 0.20)
        
        # Step 4: Generate primary values (L)
        # We calculate Inductance NOW to lock the physics.
        primary_values = self._generate_primary_values(schema, archetype, target_package)
        
        # Build extras
        extras = {
            'requested_corner': requested_corner,
            'inductance_h': primary_values['inductance_h'],
            # שאר הערכים יחושבו "על המקום" (Just-in-Time) בפעם הראשונה שיידרשו
            'physics_calculated': False, 
            'rated_current_a': None,
            'saturation_current_a': None,
            'dcr_ohm': None,
            'srf_hz': None,
            'q_factor': None
        }
        
        return GenerationContext(
            sample_id=f"IND_{archetype}_{target_package}_{random.randint(1000,9999)}",
            component_type="INDUCTOR",
            package=target_package,
            archetype=archetype,
            tolerance=tolerance,
            process_corner=requested_corner or "TYPICAL",
            extras=extras
        )
    
    # ------------------------------------------------------------------------
    # 2. PHYSICS ENGINE (CALCULATED ON DEMAND)
    # ------------------------------------------------------------------------
    def _ensure_physics(self, context: GenerationContext):
        """
        Runs the heavy physics math.
        Called automatically before accessing dependent parameters.
        """
        if context.extras.get('physics_calculated'):
            return

        l_si = context.extras.get('inductance_h')
        if not l_si or l_si <= 0:
            # Fallback: pick a sensible inductance for the package
            pkg_spec = self.constants.PACKAGE_SPECS.get(context.package)
            max_l = pkg_spec['limits']['max_inductance_h'] if pkg_spec else 10e-6
            l_si = max_l * 0.1  # 10% of package max — safe default
            context.extras['inductance_h'] = l_si
        
        archetype = context.archetype
        pkg_spec = self.constants.PACKAGE_SPECS[context.package]
        material = self.constants.CORE_MATERIALS.get(archetype, self.constants.CORE_MATERIALS["Power_Ferrite"])
        
        # --- Core geometry ---
        core_area_m2 = pkg_spec['limits']['footprint_area_mm2'] * 1e-6
        mu_r = material['permeability']
        
        # --- Number of turns (N) ---
        # L = (mu_0 * mu_r * A * N^2) / l_path
        # Approximation: l_path ~ 4 * sqrt(Area) (Toroid-like loop)
        l_path_m = math.sqrt(core_area_m2) * 4.0
        
        if archetype == "RF_Ceramic":
            # Air core (mu_r = 1 effectively for calculation structure)
            k = self.constants.MU_0 * core_area_m2 / l_path_m
        else:
            k = self.constants.MU_0 * mu_r * core_area_m2 / l_path_m
            
        n_turns = math.sqrt(l_si / k)
        n_turns = max(n_turns, 1.0)
        
        # --- Wire Geometry ---
        # Window area ~ 40% of core footprint (simplification)
        window_area_m2 = core_area_m2 * 0.4
        wire_area_m2 = (window_area_m2 * self.constants.WIRE_FILL_FACTOR) / n_turns
        wire_diameter_m = 2 * math.sqrt(wire_area_m2 / math.pi)
        
        # Physical clamp (wire can't be microscopic or huge)
        wire_diameter_m = max(10e-6, min(wire_diameter_m, 2e-3))
        
        # Total wire length
        mean_turn_length_m = math.sqrt(core_area_m2) * 4
        total_wire_length_m = n_turns * mean_turn_length_m
        
        # --- DCR Calculation ---
        # R = rho * L / A
        wire_cross_section_m2 = math.pi * (wire_diameter_m/2)**2
        dcr_calc = (self.constants.COPPER_RESISTIVITY_OHM_M * total_wire_length_m) / wire_cross_section_m2
        
        # Adjustments (Skin effect, termination, imperfections)
        dcr_final = dcr_calc * 1.3 + 0.005 
        dcr_final = min(dcr_final, pkg_spec['limits']['dcr_max_ohm']) # Clamp to package limit
        
        context.extras['dcr_ohm'] = dcr_final
        
        # --- Saturation Current ---
        i_sat = None
        if material['has_saturation']:
            # B = mu * N * I / l_path  => I_sat = B_sat * l_path / (mu * N)
            i_sat_calc = (material['saturation_t'] * l_path_m) / (self.constants.MU_0 * mu_r * n_turns)
            i_sat = i_sat_calc * 0.7 # Safety margin
            context.extras['saturation_current_a'] = i_sat
        
        # --- Rated Current (Thermal) ---
        # P = I^2 * R. Max power defined by package.
        max_p = pkg_spec['limits']['max_power_watts']
        i_thermal = math.sqrt(max_p / dcr_final)
        
        # Combined Rated Current
        pkg_max_i = pkg_spec['limits']['max_current_a']
        i_rated = min(i_thermal, pkg_max_i)
        if i_sat:
            i_rated = min(i_rated, i_sat)
            
        context.extras['rated_current_a'] = i_rated
        
        # --- SRF Calculation ---
        # C_parasitic scales with size and turns
        c_base = self.constants.SRF_BASE_CAPACITANCE_F.get(archetype, 1e-12)
        c_parasitic = c_base * math.sqrt(n_turns) + 0.1e-12
        f_srf = 1.0 / (2 * math.pi * math.sqrt(l_si * c_parasitic))
        context.extras['srf_hz'] = f_srf

        # --- Q Factor ---
        # Approximation around 100MHz or SRF/10
        q_base = self.constants.Q_FACTOR_BASE.get(archetype, 30)
        context.extras['q_factor'] = q_base

        context.extras['physics_calculated'] = True

    # ------------------------------------------------------------------------
    # 3. CREATE CUSTOM PARAMETER (THE INTERFACE)
    # ------------------------------------------------------------------------
    def create_custom_parameter(self, key: str, context: GenerationContext, param_def: Dict) -> Optional[GeneratedParameter]:
        """
        Creates the datasheet parameters using the calculated physics.
        """
        if key in self.EXCLUDED_KEYS:
            return None

        # Ensure we have data
        self._ensure_physics(context)
        extras = context.extras

        # --- Inductance ---
        if key == 'inductance':
            val_si = extras['inductance_h']
            disp_val, unit = self._auto_scale(val_si, 'H')
            tol = context.tolerance
            ndigits = 3 if disp_val < 1 else 2

            return GeneratedParameter(
                key=key, label=param_def['llm_context']['formal_name'], symbol="L",
                section="ELEC_CHAR",
                value_min=round(disp_val * (1 - tol), ndigits),
                value_typ=round(disp_val, ndigits),
                value_max=round(disp_val * (1 + tol), ndigits),
                unit=unit,
                condition="1kHz/100kHz",
                spec_type=SpecType.NOMINAL,
                engineering_class=EngineeringClass.PERFORMANCE
            )

        # --- Rated Current ---
        if key == 'rated_current':
            i_r = extras.get('rated_current_a', 0.1)
            disp_val, unit = self._auto_scale(i_r, 'A')

            return GeneratedParameter(
                key=key, label="Rated Current", symbol="I_R",
                section="ABS_MAX",
                value_max=round(disp_val, 2),
                unit=unit,
                condition="T_A=25°C, ΔT=40°C",
                spec_type=SpecType.MAX_RATING,
                engineering_class=EngineeringClass.PERFORMANCE
            )

        # --- DC Resistance (schema key: dcr) ---
        if key == 'dcr':
            dcr = extras.get('dcr_ohm', 0.1)
            disp_val, unit = self._auto_scale(dcr, 'Ω')

            return GeneratedParameter(
                key=key, label="DC Resistance", symbol="DCR",
                section="ELEC_CHAR",
                value_typ=round(disp_val * 0.85, 3),
                value_max=round(disp_val, 3),
                unit=unit,
                condition="T_A=25°C",
                spec_type=SpecType.MAX_LIMIT
            )

        # --- Saturation Current ---
        if key == 'saturation_current':
            i_sat = extras.get('saturation_current_a')
            if i_sat is None: return None # Not all inductors specify this

            disp_val, unit = self._auto_scale(i_sat, 'A')
            return GeneratedParameter(
                key=key, label="Saturation Current", symbol="I_sat",
                section="ELEC_CHAR",
                value_typ=round(disp_val, 2),
                unit=unit,
                condition="L drop 30%, T_A=25°C",
                spec_type=SpecType.TYPICAL
            )

        # --- SRF (schema key: srf) ---
        if key == 'srf':
            srf = extras.get('srf_hz', 1e6)
            disp_val, unit = self._auto_scale(srf, 'Hz')

            return GeneratedParameter(
                key=key, label="Self Resonant Frequency", symbol="SRF",
                section="ELEC_CHAR",
                value_min=round(disp_val * 0.8, 1),
                value_typ=round(disp_val, 1),
                unit=unit,
                condition="T_A=25°C",
                spec_type=SpecType.MIN_LIMIT
            )

        # --- Quality Factor ---
        if key == 'quality_factor':
            q = extras.get('q_factor', 30)
            return GeneratedParameter(
                key=key, label="Quality Factor", symbol="Q",
                section="ELEC_CHAR",
                value_min=int(q * 0.7),
                value_typ=int(q),
                unit="",
                condition="f=1MHz, T_A=25°C",
                spec_type=SpecType.TYPICAL
            )

        return None

    # ------------------------------------------------------------------------
    # 4. BASE VALUES & HELPERS
    # ------------------------------------------------------------------------
    def calculate_base_value(self, key: str, limits: Any, context: GenerationContext) -> Any:
        if key in self.EXCLUDED_KEYS:
            return None

        pkg_spec = self.constants.PACKAGE_SPECS.get(context.package)
        if not pkg_spec:
            return None

        return None

    def _generate_primary_values(self, schema: Dict, archetype: str, package: str) -> Dict[str,float]:
        pkg_spec = self.constants.PACKAGE_SPECS[package]
        max_l = pkg_spec['limits']['max_inductance_h']
        
        # Try to pull from schema
        l_param = next((p for p in schema.get('ELEC_CHAR', []) if p['key']=='inductance'), None)
        valid_l = []
        
        if l_param:
            l_options = self._extract_numeric_list(l_param['scenarios'][0]['limits'].get(archetype, []))
            # Convert values (heuristic: if > 1 it's likely uH)
            l_si = [l * 1e-6 if l > 0.1 else l for l in l_options]
            valid_l = [l for l in l_si if l <= max_l]
            
        if not valid_l:
            # Physics Fallback: Log-Uniform choice
            min_l = 1e-9
            val = 10 ** random.uniform(math.log10(min_l), math.log10(max_l))
            valid_l = [val]
            
        return {'inductance_h': random.choice(valid_l)}

    def _extract_numeric_list(self, limits: Any) -> List[float]:
        if isinstance(limits, list):
            vals = []
            for x in limits:
                if isinstance(x, (int, float)): vals.append(float(x))
                elif isinstance(x, str):
                    try:
                        m = re.search(r'[\d.]+', x)
                        if m: vals.append(float(m.group()))
                    except: pass
            return vals
        if isinstance(limits, (int, float)): return [float(limits)]
        return []

    def _auto_scale(self, value: float, base_unit: str) -> Tuple[float, str]:
        if value is None or value == 0: return 0, base_unit
        
        # Standard Engineering Prefixes
        prefixes = [(1e-9,'n'), (1e-6,'µ'), (1e-3,'m'), (1,''), (1e3,'k'), (1e6,'M'), (1e9,'G')]
        
        val_abs = abs(value)
        best_scale = 1.0
        best_prefix = ''
        
        for scale, prefix in prefixes:
            if val_abs < scale * 1000: # Try to keep number < 1000
                best_scale = scale
                best_prefix = prefix
                break
        
        # Correction for Ohms (prefer mOhm only for small values)
        if base_unit == 'Ω' and value < 1.0:
            return value * 1000, 'mΩ'
        if base_unit == 'Ω' and value >= 1.0:
            return value, 'Ω'
            
        return value / best_scale, f"{best_prefix}{base_unit}"

    def apply_correlations(self, result: DatasheetResult) -> None:
        pass
