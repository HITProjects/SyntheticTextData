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
class OpampConstants:
    """Constants and lookup tables for OPAMP generation with accurate physics"""
    
    # Process Corners for variation
    # Allows simulation of Worst Case vs Best Case scenarios
    CORNERS = {
        "TYPICAL":    {"bw": 1.0, "iq": 1.0, "vos": 1.0, "ios": 1.0, "sr": 1.0},
        "WORST_CASE": {"bw": 0.8, "iq": 1.2, "vos": 1.5, "ios": 1.5, "sr": 0.8}, # Slower, hungrier, less precise
        "BEST_CASE":  {"bw": 1.2, "iq": 0.8, "vos": 0.6, "ios": 0.6, "sr": 1.2}  # Faster, efficient, precise
    }

    # Archetype Physics Metadata
    # tech: 'Bipolar' or 'CMOS' determines Gm vs Id relationship
    # sr_factor: Base multiplier for Slew Rate physics
    # noise_k: Coefficient for noise density calculation
    # bias_base: Base input bias current
    PHYSICS_META = {
        "General_Purpose":      {"tech": "Bipolar", "sr_factor": 1.0, "noise_k": 20e-9, "bias_base": 20e-9, "max_gbw": 20e6, "is_cmos": False},
        "Precision_Zero_Drift": {"tech": "CMOS",    "sr_factor": 0.5, "noise_k": 40e-9, "bias_base": 10e-12,"max_gbw": 10e6, "is_cmos": True},
        "High_Speed":           {"tech": "Bipolar", "sr_factor": 5.0, "noise_k": 3e-9,  "bias_base": 2e-6,  "max_gbw": 500e6, "is_cmos": False},
        "Low_Power":            {"tech": "CMOS",    "sr_factor": 0.8, "noise_k": 80e-9, "bias_base": 1e-12, "max_gbw": 5e6, "is_cmos": True},
        "JFET_Input":           {"tech": "JFET",    "sr_factor": 3.0, "noise_k": 15e-9, "bias_base": 50e-12,"max_gbw": 50e6, "is_cmos": False}
    }

    # Supply Voltage Ranges (Min, Max)
    SUPPLY_RANGES = {
        "General_Purpose": [(3.0, 32.0), (4.5, 36.0)],
        "Precision_Zero_Drift": [(1.8, 5.5), (2.7, 16.0)],
        "High_Speed": [(2.5, 5.5), (4.5, 12.0), (8.0, 24.0)],
        "Low_Power": [(1.8, 5.5), (2.2, 16.0)],
        "JFET_Input": [(4.5, 36.0)]
    }

    # Package Thermal Limits (Watts) & Rth_ja (C/W)
    # pd_max: Limit of the case itself
    PACKAGE_SPECS = {
        "SOT-23-5": {"pd_max": 0.25, "rth_ja": 250, "dims": [2.9, 1.6, 1.1]},
        "SC-70":    {"pd_max": 0.15, "rth_ja": 300, "dims": [2.0, 1.25, 0.95]},
        "SOIC-8":   {"pd_max": 0.65, "rth_ja": 120, "dims": [4.9, 3.9, 1.5]},
        "TSSOP-8":  {"pd_max": 0.45, "rth_ja": 160, "dims": [3.0, 4.4, 1.1]},
        "DIP-8":    {"pd_max": 1.00, "rth_ja": 90,  "dims": [9.3, 6.4, 3.3]},
        "QFN-16":   {"pd_max": 1.50, "rth_ja": 40,  "dims": [3.0, 3.0, 0.85]}
    }
# ============================================================================
# STRATEGY CLASS
# ============================================================================
class OpampStrategy(ComponentStrategy):
    """
    Hermetic OPAMP Strategy with rigorous Physics Engine.
    Enforces correlations between Iq, GBW, SR, Noise, and Package Limits.
    """

    def __init__(self):
        self.constants = OpampConstants()

    # ------------------------------------------------------------------------
    # 1. CREATE CONTEXT
    # ------------------------------------------------------------------------
    def create_context(self, schema: Dict, requested_corner: Optional[str]) -> GenerationContext:
        archetype = random.choice(schema.get('archetypes', ['General_Purpose']))
        
        # Package Selection with Validity Check
        valid_pkgs = list(self.constants.PACKAGE_SPECS.keys())
        if archetype == "High_Speed":
            # High speed needs low inductance, prefer SMT
            valid_pkgs = [p for p in valid_pkgs if "DIP" not in p]
        elif archetype == "Precision_Zero_Drift":
            # Precision often comes in standard pinouts
            valid_pkgs = [p for p in valid_pkgs if "SOIC" in p or "SOT" in p]
            
        package = random.choice(valid_pkgs)
        corner = requested_corner if requested_corner in self.constants.CORNERS else "TYPICAL"

        # --- HERMETIC PHYSICS GENERATION ---
        # Calculate all dependent values BEFORE creating parameters
        phys_data = self._generate_physics_state(archetype, package, corner)
        
        extras = {
            'requested_corner': requested_corner,
            'process_corner': corner,
            'package': package,
            'pkg_specs': self.constants.PACKAGE_SPECS[package],
            
            # Locked Values (SI Units)
            'supply_min': phys_data['supply_min'],
            'supply_max': phys_data['supply_max'],
            'iq_typ': phys_data['iq_typ'],
            'gbw_typ': phys_data['gbw_typ'],
            'sr_typ': phys_data['sr_typ'],
            'vos_typ': phys_data['vos_typ'],
            'bias_typ': phys_data['bias_typ'],
            'ios_typ': phys_data['ios_typ'],
            'en_typ': phys_data['en_typ'],
            'cmrr_typ': phys_data['cmrr_typ'],
            'psrr_typ': phys_data['psrr_typ'],
            
            # Metadata
            'tech': self.constants.PHYSICS_META[archetype]['tech']
        }

        return GenerationContext(
            sample_id=f"OPAMP_{archetype[:3].upper()}_{uuid.uuid4().hex[:4]}",
            component_type="OPAMP",
            package=package,
            archetype=archetype,
            tolerance=0.1,
            process_corner=corner,
            extras=extras
        )

    # ------------------------------------------------------------------------
    # 2. PHYSICS ENGINE (The Core Logic)
    # ------------------------------------------------------------------------
    def _generate_physics_state(self, archetype: str, package: str, corner: str) -> Dict[str, float]:
        """
        Calculates a consistent set of parameters based on physics constraints.
        """
        meta = self.constants.PHYSICS_META[archetype]
        pkg_data = self.constants.PACKAGE_SPECS[package]
        c_data = self.constants.CORNERS[corner]
        
        # 1. Supply Voltage Selection
        # High speed often means lower voltage due to breakdown/speed tradeoffs
        v_range = random.choice(self.constants.SUPPLY_RANGES[archetype])
        v_min, v_max = v_range
        
        # 2. Quiescent Current (Iq) - The Driver
        # Iq drives GBW and SR. Constrained by Package Power.
        if archetype == "Low_Power":
            iq_target = random.uniform(0.5e-6, 50e-6)
        elif archetype == "High_Speed":
            iq_target = random.uniform(1e-3, 20e-3)
        else:
            iq_target = random.uniform(100e-6, 3e-3)
            
        # Apply Corner variation to Iq
        iq_target *= c_data['iq']
            
        # Thermal Safety Check: P_d = V_max * Iq
        # Limit Iq so P_d < 50% of Package Max (Headroom for load current)
        max_iq_thermal = (pkg_data['pd_max'] * 0.5) / v_max
        iq_target = min(iq_target, max_iq_thermal)
        
        # 3. GBW Calculation (Technology Dependent)
        # Bipolar: gm ~ Ic/Vt -> GBW linear with Iq
        # CMOS/JFET: gm ~ sqrt(Id) -> GBW sqrt with Iq
        # C_comp assumed roughly constant (~5-10pF internal)
        if meta['tech'] == "Bipolar":
            # Efficiency: ~10-20 MHz/mA for good bipolar
            gbw_efficiency = random.uniform(10e9, 20e9) 
            gbw = iq_target * gbw_efficiency
        else: # CMOS/JFET
            # Efficiency: ~2-5 MHz/sqrt(mA) 
            gbw_efficiency = random.uniform(100e6, 200e6) 
            gbw = math.sqrt(iq_target) * gbw_efficiency
            
        # Clamp GBW to realistic max per archetype
        gbw = min(gbw, meta['max_gbw'])
        gbw *= c_data['bw'] # Corner effect
        
        # 4. Slew Rate (SR)
        # SR = I_tail / C_c. Since GBW = gm / C_c, and gm ~ I (Bip) or sqrt(I) (MOS),
        # SR tracks Iq strongly.
        # Physics model: SR [V/s] approx = k * Iq
        sr_k = 1e9 if meta['tech'] == "Bipolar" else 5e8 # V/s per Ampere rough scaling
        if archetype == "High_Speed": sr_k *= 5.0 # Current feedback / slew enhanced
        
        sr_val_si = iq_target * sr_k * c_data['sr']
        
        # Slew Rate Saturation Check: SR cannot exceed physics of supply rails vs freq
        # This prevents 500V/us in a 5V part which implies unrealistic bandwidth
        # No strict limit, but sanity clamp:
        sr_val_si = max(sr_val_si, 0.01e6) # Min 0.01 V/us
        
        # 5. Noise (en)
        # Thermal noise dominant: Vn ~ sqrt(4kTR) ~ 1/sqrt(gm)
        # So Vn scales with 1/sqrt(Iq) generally for both techs (simplified)
        en_val = meta['noise_k'] * math.sqrt(1e-3 / max(iq_target, 1e-9))
        
        # 6. Offset (Vos) & Bias (Ib)
        # Vos: Random process mismatch. Better in Bipolar, worse in CMOS (unless Chopper)
        vos_base = 50e-6 if "Precision" in archetype else 1e-3
        vos = vos_base * random.uniform(0.5, 2.0) * c_data['vos']
        
        # Ib: Technology definition
        # Bipolar: Ib ~ Iq / Beta. Beta ~ 100-200.
        # CMOS/JFET: Leakage driven.
        if meta['tech'] == "Bipolar":
            beta = random.uniform(100, 300)
            ib = iq_target / beta
        else:
            ib = meta['bias_base'] * random.uniform(0.5, 5.0) # Leakage variation
            
        ib *= c_data['ios']
        ios = ib * 0.1 # Offset current typically 10% of bias
        
        # 7. CMRR / PSRR
        # Linked to Open Loop Gain (Aol). Higher GBW usually implies lower DC gain in simple stages,
        # but modern topologies compensate.
        # High precision = High CMRR.
        cmrr_base = 120 if "Precision" in archetype else 90
        cmrr = cmrr_base + random.uniform(-10, 10)
        psrr = cmrr - random.uniform(0, 20)
        
        return {
            'supply_min': v_min,
            'supply_max': v_max,
            'iq_typ': iq_target,
            'gbw_typ': gbw,
            'sr_typ': sr_val_si,
            'vos_typ': vos,
            'bias_typ': ib,
            'ios_typ': ios,
            'en_typ': en_val,
            'cmrr_typ': cmrr,
            'psrr_typ': psrr
        }

    # ------------------------------------------------------------------------
    # 3. PARAMETER CREATION (Display Layer)
    # ------------------------------------------------------------------------
    def create_custom_parameter(self, key: str, context: GenerationContext, param_def: Dict) -> Optional[GeneratedParameter]:
        extras = context.extras
        
        if key == 'supply_voltage_range':
            return GeneratedParameter(
                key=key, label="Supply Voltage Range", symbol="Vs", section="REC_OP_COND",
                value_min=extras['supply_min'], value_max=extras['supply_max'], unit="V",
                condition="Single Supply", spec_type=SpecType.OPERATIONAL_RANGE,
                engineering_class=EngineeringClass.OPERATING_CONDITION
            )

        if key == 'supply_current':
            val = extras['iq_typ']
            disp, unit = self._auto_scale(val, 'A')
            return GeneratedParameter(
                key=key, label="Quiescent Current", symbol="Iq", section="ELEC_CHAR",
                value_typ=self._round(disp, 2), value_max=self._round(disp*1.2, 2), unit=unit,
                condition="No Load", spec_type=SpecType.TYPICAL,
                engineering_class=EngineeringClass.PERFORMANCE
            )

        if key == 'gbw':
            val = extras['gbw_typ']
            disp, unit = self._auto_scale(val, 'Hz')
            return GeneratedParameter(
                key=key, label="Gain Bandwidth Product", symbol="GBW", section="ELEC_CHAR",
                value_typ=self._round(disp, 1), unit=unit, condition="RL=10k",
                spec_type=SpecType.TYPICAL, engineering_class=EngineeringClass.PERFORMANCE
            )

        if key == 'slew_rate':
            # Display in V/µs
            val_us = extras['sr_typ'] / 1e6
            # Intelligent rounding
            disp = self._round(val_us, 2) if val_us < 10 else self._round(val_us, 0)
            return GeneratedParameter(
                key=key, label="Slew Rate", symbol="SR", section="ELEC_CHAR",
                value_typ=disp, unit="V/µs", condition="RL=2k",
                spec_type=SpecType.TYPICAL, engineering_class=EngineeringClass.PERFORMANCE
            )

        if key == 'offset_voltage':
            val = extras['vos_typ']
            disp, unit = self._auto_scale(val, 'V')
            return GeneratedParameter(
                key=key, label="Input Offset Voltage", symbol="Vos", section="ELEC_CHAR",
                value_typ=self._round(disp, 2), value_max=self._round(disp*2, 2), unit=unit,
                spec_type=SpecType.MAX_LIMIT, engineering_class=EngineeringClass.PERFORMANCE
            )

        if key == 'input_bias_current':
            val = extras['bias_typ']
            disp, unit = self._auto_scale(val, 'A')
            return GeneratedParameter(
                key=key, label="Input Bias Current", symbol="Ib", section="ELEC_CHAR",
                value_typ=self._round(disp, 2), value_max=self._round(disp*2, 2), unit=unit,
                spec_type=SpecType.MAX_LIMIT, engineering_class=EngineeringClass.PERFORMANCE
            )
            
        if key == 'input_offset_current':
            val = extras['ios_typ']
            disp, unit = self._auto_scale(val, 'A')
            return GeneratedParameter(
                key=key, label="Input Offset Current", symbol="Ios", section="ELEC_CHAR",
                value_typ=self._round(disp, 2), value_max=self._round(disp*2, 2), unit=unit,
                spec_type=SpecType.MAX_LIMIT, engineering_class=EngineeringClass.PERFORMANCE
            )

        if key == 'voltage_noise_density':
            val = extras['en_typ']
            disp, unit = self._auto_scale(val, 'V')
            return GeneratedParameter(
                key=key, label="Voltage Noise Density", symbol="en", section="ELEC_CHAR",
                value_typ=self._round(disp, 1), unit=f"{unit}/√Hz", condition="f=1kHz",
                spec_type=SpecType.TYPICAL, engineering_class=EngineeringClass.PERFORMANCE
            )
            
        if key == 'cmrr':
            val = extras['cmrr_typ']
            return GeneratedParameter(
                key=key, label="Common Mode Rejection Ratio", symbol="CMRR", section="ELEC_CHAR",
                value_min=int(val-10), value_typ=int(val), unit="dB",
                spec_type=SpecType.MIN_LIMIT, engineering_class=EngineeringClass.PERFORMANCE
            )

        return None

    # ------------------------------------------------------------------------
    # 4. BASE VALUES
    # ------------------------------------------------------------------------
    def calculate_base_value(self, key: str, limits: Any, context: GenerationContext) -> Any:
        pkg_spec = context.extras['pkg_specs']
        if key == 'package_code': return context.package
        if key == 'dimensions_lxwxh': return pkg_spec['dims']
        if key == 'power_dissipation': return pkg_spec['pd_max']
        if key == 'thermal_resistance_ja': return pkg_spec['rth_ja']
        # Generic fallback: pick a random numeric value from the archetype's limits array
        if isinstance(limits, dict):
            arch_list = limits.get(context.archetype, [])
            if isinstance(arch_list, list):
                # Handle nested [min, max] pairs (e.g. ta_range)
                if arch_list and isinstance(arch_list[0], list):
                    pair = random.choice(arch_list)
                    return pair[0]  # return lower bound; upper bound handled by column_model
                numeric = [v for v in arch_list if isinstance(v, (int, float))]
                return random.choice(numeric) if numeric else None
        return None

    # ------------------------------------------------------------------------
    # 5. CORRELATIONS
    # ------------------------------------------------------------------------
    def apply_correlations(self, result: DatasheetResult) -> None:
        """Apply secondary correlations"""
        extras = result.context.extras
        
        for param in result.parameters:
            if param.key == 'settling_time':
                gbw = extras['gbw_typ']
                # ts (0.01%) ~ 0.7 / GBW  (Single pole approx)
                ts_sec = 0.7 / gbw 
                disp, unit = self._auto_scale(ts_sec, 's')
                param.value_typ = self._round(disp, 1)
                param.unit = unit

    # ------------------------------------------------------------------------
    # UTILS
    # ------------------------------------------------------------------------
    def _auto_scale(self, value: float, base_unit: str) -> Tuple[float, str]:
        if value is None or value == 0: return 0, base_unit
        
        prefixes = [(1e-12,'p'), (1e-9,'n'), (1e-6,'µ'), (1e-3,'m'), (1,''), (1e6,'M')]
        val_abs = abs(value)
        best_scale = 1.0
        best_prefix = ''
        
        for scale, prefix in prefixes:
            if val_abs >= scale:
                # Avoid scaling 0.005A to 5mA if standard is A, but usually valid
                if val_abs < scale * 1000:
                    best_scale = scale
                    best_prefix = prefix
        
        # Cleanup
        if best_prefix == '' and base_unit == 'V' and val_abs < 1.0: # Prefer mV for small volts
             return value * 1000, 'mV'

        return value / best_scale, f"{best_prefix}{base_unit}"

    def _round(self, val, digits):
        if val is None: return None
        return round(val, digits)
