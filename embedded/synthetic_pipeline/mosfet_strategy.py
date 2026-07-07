
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
# CONSTANTS CLASS - SINGLE SOURCE OF TRUTH
# ============================================================================
class MosfetConstants:
    """Constants and lookup tables for MOSFET generation"""
    
    # ========================================================================
    # MASTER PACKAGE SPECIFICATIONS - SINGLE SOURCE OF TRUTH
    # ========================================================================
    PACKAGE_SPECS = {
        # ====================================================================
        # HV_Power_THT (Through-Hole)
        # ====================================================================
        "TO-220": {
            "dimensions": [10.0, 4.5, 9.0, 2.0],
            "limits": { "max_power_watts": 150, "max_current_a": 70, "max_voltage_v": 1000, "rth_jc": 1.0, "rth_ja": 62.5 }
        },
        "TO-220AB": {
            "dimensions": [10.0, 4.5, 9.0, 2.0],
            "limits": { "max_power_watts": 150, "max_current_a": 70, "max_voltage_v": 1000, "rth_jc": 1.0, "rth_ja": 62.5 }
        },
        "TO-247": {
            "dimensions": [16.0, 5.0, 21.0, 6.0],
            "limits": { "max_power_watts": 300, "max_current_a": 100, "max_voltage_v": 1200, "rth_jc": 0.5, "rth_ja": 40.0 }
        },
        "TO-247-3": {
            "dimensions": [16.0, 5.0, 21.0, 6.0],
            "limits": { "max_power_watts": 300, "max_current_a": 100, "max_voltage_v": 1700, "rth_jc": 0.5, "rth_ja": 40.0 }
        },
        "TO-247-4": {
            "dimensions": [16.0, 5.0, 21.0, 6.0],
            "limits": { "max_power_watts": 300, "max_current_a": 100, "max_voltage_v": 1700, "rth_jc": 0.5, "rth_ja": 40.0 }
        },
        "TO-3P": {
            "dimensions": [15.6, 4.8, 19.9, 5.5],
            "limits": { "max_power_watts": 250, "max_current_a": 80, "max_voltage_v": 1000, "rth_jc": 0.7, "rth_ja": 40.0 }
        },
        "TO-264": {
            "dimensions": [20.0, 5.0, 26.0, 10.0],
            "limits": { "max_power_watts": 500, "max_current_a": 150, "max_voltage_v": 1500, "rth_jc": 0.2, "rth_ja": 30.0 }
        },
        "ITO-220": {
            "dimensions": [10.0, 4.5, 9.0, 1.8],
            "limits": { "max_power_watts": 50, "max_current_a": 30, "max_voltage_v": 1500, "rth_jc": 3.0, "rth_ja": 65.0 }
        },
        "TO-220FP": {
            "dimensions": [10.0, 4.5, 9.0, 1.8],
            "limits": { "max_power_watts": 40, "max_current_a": 30, "max_voltage_v": 1500, "rth_jc": 4.0, "rth_ja": 65.0 }
        },

        # ====================================================================
        # MV_Power_SMD (Surface Mount Power)
        # ====================================================================
        "DPAK(TO-252)": {
            "dimensions": [6.6, 6.1, 2.3, 0.35],
            "limits": { "max_power_watts": 60, "max_current_a": 30, "max_voltage_v": 200, "rth_jc": 1.5, "rth_ja": 50.0 }
        },
        "TO-252": {
            "dimensions": [6.6, 6.1, 2.3, 0.35],
            "limits": { "max_power_watts": 60, "max_current_a": 30, "max_voltage_v": 200, "rth_jc": 1.5, "rth_ja": 50.0 }
        },
        "D2PAK(TO-263)": {
            "dimensions": [10.0, 9.0, 4.5, 1.5],
            "limits": { "max_power_watts": 150, "max_current_a": 70, "max_voltage_v": 600, "rth_jc": 0.8, "rth_ja": 40.0 }
        },
        "TO-263-7": {
            "dimensions": [10.0, 9.0, 4.5, 1.5],
            "limits": { "max_power_watts": 180, "max_current_a": 80, "max_voltage_v": 1200, "rth_jc": 0.7, "rth_ja": 40.0 }
        },
        "D2PAK-7L": {
            "dimensions": [10.0, 9.0, 4.5, 1.5],
            "limits": { "max_power_watts": 180, "max_current_a": 80, "max_voltage_v": 1200, "rth_jc": 0.7, "rth_ja": 40.0 }
        },
        "PowerPAK_SO-8": {
            "dimensions": [6.15, 5.15, 1.0, 0.1],
            "limits": { "max_power_watts": 50, "max_current_a": 40, "max_voltage_v": 150, "rth_jc": 1.5, "rth_ja": 50.0 }
        },
        "PQFN_5x6": {
            "dimensions": [5.0, 6.0, 0.9, 0.08],
            "limits": { "max_power_watts": 30, "max_current_a": 30, "max_voltage_v": 150, "rth_jc": 2.0, "rth_ja": 50.0 }
        },
        "DFN_5x6": {
            "dimensions": [5.0, 6.0, 0.9, 0.08],
            "limits": { "max_power_watts": 30, "max_current_a": 30, "max_voltage_v": 150, "rth_jc": 2.0, "rth_ja": 50.0 }
        },
        "DFN_8x8": {
            "dimensions": [8.0, 8.0, 0.9, 0.15],
            "limits": { "max_power_watts": 80, "max_current_a": 60, "max_voltage_v": 650, "rth_jc": 1.0, "rth_ja": 40.0 }
        },
        "TOLL": {
            "dimensions": [10.0, 11.7, 2.3, 0.6],
            "limits": { "max_power_watts": 300, "max_current_a": 120, "max_voltage_v": 200, "rth_jc": 0.4, "rth_ja": 40.0 }
        },
        "DirectFET": {
            "dimensions": [6.3, 4.9, 0.7, 0.1],
            "limits": { "max_power_watts": 40, "max_current_a": 35, "max_voltage_v": 100, "rth_jc": 1.0, "rth_ja": 45.0 }
        },

        # ====================================================================
        # LV_Logic_Level (Small Signal)
        # ====================================================================
        "SOT-23": {
            "dimensions": [2.9, 1.3, 1.0, 0.008],
            "limits": { "max_power_watts": 0.35, "max_current_a": 3.0, "max_voltage_v": 60, "rth_jc": 100, "rth_ja": 350 }
        },
        "SOT-23-3": {
            "dimensions": [2.9, 1.3, 1.0, 0.008],
            "limits": { "max_power_watts": 0.35, "max_current_a": 3.0, "max_voltage_v": 60, "rth_jc": 100, "rth_ja": 350 }
        },
        "SOT-23-6": {
            "dimensions": [2.9, 1.6, 1.1, 0.015],
            "limits": { "max_power_watts": 0.3, "max_current_a": 2.0, "max_voltage_v": 60, "rth_jc": 110, "rth_ja": 300 }
        },
        "SOT-323": {
            "dimensions": [2.0, 1.25, 0.95, 0.005],
            "limits": { "max_power_watts": 0.2, "max_current_a": 1.0, "max_voltage_v": 50, "rth_jc": 150, "rth_ja": 500 }
        },
        "SC-70": {
            "dimensions": [2.0, 1.25, 0.95, 0.005],
            "limits": { "max_power_watts": 0.2, "max_current_a": 1.0, "max_voltage_v": 50, "rth_jc": 150, "rth_ja": 500 }
        },
        "SC-70-6": {
            "dimensions": [2.0, 1.25, 0.95, 0.006],
            "limits": { "max_power_watts": 0.15, "max_current_a": 0.8, "max_voltage_v": 50, "rth_jc": 160, "rth_ja": 550 }
        },
        "SOT-363": {
            "dimensions": [2.0, 1.25, 0.95, 0.006],
            "limits": { "max_power_watts": 0.15, "max_current_a": 0.8, "max_voltage_v": 50, "rth_jc": 160, "rth_ja": 550 }
        },
        "SOT-223": {
            "dimensions": [6.5, 3.5, 1.6, 0.12],
            "limits": { "max_power_watts": 1.5, "max_current_a": 5.0, "max_voltage_v": 100, "rth_jc": 15, "rth_ja": 60 }
        },
        "SOT-89": {
            "dimensions": [4.5, 2.5, 1.5, 0.05],
            "limits": { "max_power_watts": 1.0, "max_current_a": 4.0, "max_voltage_v": 100, "rth_jc": 20, "rth_ja": 100 }
        },
        "TSOP-6": {
            "dimensions": [2.9, 1.6, 1.0, 0.015],
            "limits": { "max_power_watts": 1.0, "max_current_a": 3.0, "max_voltage_v": 60, "rth_jc": 50, "rth_ja": 150 }
        },
        "DFN_2x2": {
            "dimensions": [2.0, 2.0, 0.6, 0.01],
            "limits": { "max_power_watts": 0.8, "max_current_a": 3.0, "max_voltage_v": 30, "rth_jc": 40, "rth_ja": 100 }
        },
        "DFN_3x3": {
            "dimensions": [3.3, 3.3, 0.9, 0.04],
            "limits": { "max_power_watts": 1.5, "max_current_a": 10, "max_voltage_v": 60, "rth_jc": 15, "rth_ja": 60 }
        },
        "SON": {
            "dimensions": [3.0, 3.0, 0.8, 0.03],
            "limits": { "max_power_watts": 1.2, "max_current_a": 8, "max_voltage_v": 40, "rth_jc": 20, "rth_ja": 70 }
        },

        # ====================================================================
        # RF_Power
        # ====================================================================
        "Flange_Mount": {
            "dimensions": [20.0, 6.0, 4.0, 5.0],
            "limits": { "max_power_watts": 300, "max_current_a": 50, "max_voltage_v": 100, "rth_jc": 0.3, "rth_ja": 30.0 }
        },
        "NI-780": {
            "dimensions": [20.0, 10.0, 4.0, 3.0],
            "limits": { "max_power_watts": 200, "max_current_a": 40, "max_voltage_v": 120, "rth_jc": 0.4, "rth_ja": 35.0 }
        },
        "NI-1230": {
            "dimensions": [32.0, 12.0, 5.0, 8.0],
            "limits": { "max_power_watts": 500, "max_current_a": 80, "max_voltage_v": 150, "rth_jc": 0.2, "rth_ja": 25.0 }
        }
    }
    
    # Physics Scaling Factors (Voltage -> Resistance penalty)
    RDS_VOLTAGE_SCALING = {
        "HV_Power_THT": 2.5, "MV_Power_SMD": 2.0, "LV_Logic_Level": 1.2,
        "SiC_High_Voltage": 2.2, "GaN_High_Frequency": 1.5, "RF_Power": 2.0,
        "Dual_N_Channel": 1.5, "Dual_P_Channel": 1.8,
        "Complementary_Pair": 1.6, "Depletion_Mode": 2.0
    }
    
    # Gate Threshold Defaults
    VGS_TH_DEFAULTS = {
        "HV_Power_THT": 3.0, "MV_Power_SMD": 2.0, "LV_Logic_Level": 1.5,
        "SiC_High_Voltage": 3.0, "GaN_High_Frequency": 1.4,
        "Dual_P_Channel": -2.0, "Depletion_Mode": -2.0
    }

    TECH_FOM = {
        "Low_Voltage_Trench": 0.5,   # Great for <100V
        "Planar_HV": 8.0,            # Old tech, high Rds for HV
        "SuperJunction_HV": 2.5,     # Modern HV tech
        "P_Channel_Standard": 2.0,   # P-Channel always has higher Rds than N-Channel
        "SiC_Standard": 1.5,         # Very low Rds for HV
        "GaN_Standard": 1.0          # Extremely efficient
    }
    
    # 🆕 Gate Capacitance Density (pF/mm²)
    CAP_DENSITY = {
        "Low_Voltage_Trench": 400,    # High density (thin oxide)
        "Planar_HV": 100,             # Low density (thick oxide)
        "SuperJunction_HV": 150,
        "SiC_Standard": 80,           # Wide bandgap = thicker oxide
        "GaN_Standard": 60,
        "P_Channel_Standard": 200
    }


# ============================================================================
# STRATEGY CLASS
# ============================================================================
class MosfetStrategy(ComponentStrategy):
    """Hermetic MOSFET Strategy - FIXED VERSION"""

    # Keys excluded to keep document under 512 tokens
    EXCLUDED_KEYS = {
        'weight',                    # PACKAGE — trivial physical property
        'failure_rate',              # RELIABILITY — not a numeric electrical spec
        'moisture_sensitivity_level',  # RELIABILITY — not numeric
        'qg',                        # DYNAMIC_CHAR — total gate charge (qgs+qgd covers this)
        'thermal_resistance_ja',     # THERMAL — jc is more circuit-relevant
        'package_code',              # PACKAGE — string, no numeric training value
    }

    def __init__(self):
        self.constants = MosfetConstants()

    # ----------------------------------------------------------------------
    # CONTEXT - The Lock-in Phase
    # ----------------------------------------------------------------------
    def create_context(self, schema: Dict, requested_corner: Optional[str]) -> GenerationContext:
        archetype = random.choice(schema.get("archetypes", ["MV_Power_SMD"]))
        
        # 1. Filter Packages
        valid_packages = list(self.constants.PACKAGE_SPECS.keys())
        if "valid_packages" in schema:
            valid_packages = [p for p in valid_packages if p in schema["valid_packages"]]
        
        # Ensure small archetypes don't get huge packages
        if "LV" in archetype or "Logic" in archetype:
            valid_packages = [p for p in valid_packages if "TO-247" not in p]
            
        # Fallback
        if not valid_packages:
            valid_packages = ["SOT-23"]

        package = random.choice(valid_packages)

        # 2. Physics Lock: Generate Voltage & Resistance Base
        phys_data = self._generate_physics_values(archetype, package)

        extras = {
            "vdss": phys_data["vdss"],
            "id_rated": phys_data["id_rated"],
            "rds_on_target": phys_data["rds_on"],
            "is_p_channel": "P_Channel" in archetype,
            "tech_type": phys_data["tech_type"],
            "ciss_est": phys_data["ciss_est"],  # 🆕 Pre-calculate for reuse
            "rg_internal": phys_data["rg_internal"]  # 🆕 Internal gate resistance
        }

        return GenerationContext(
            sample_id=f"MOS_{uuid.uuid4().hex[:8]}",
            component_type="MOSFET",
            package=package,
            archetype=archetype,
            tolerance=0.1,
            process_corner=requested_corner or "TYPICAL",
            extras=extras,
        )

    # ----------------------------------------------------------------------
    # PHYSICS ENGINE (IMPROVED)
    # ----------------------------------------------------------------------
    def _generate_physics_values(self, archetype: str, package: str) -> Dict[str, Any]:
        pkg_limits = self.constants.PACKAGE_SPECS[package]["limits"]
        
        # A. Choose Voltage (Vdss)
        is_hv = "HV" in archetype or pkg_limits["max_voltage_v"] > 200
        possible_volts = [20, 30, 40, 60, 100, 200, 400, 600, 650, 800, 1000, 1200, 1700]
        
        valid_volts = [v for v in possible_volts if v <= pkg_limits["max_voltage_v"]]
        
        if is_hv: 
            valid_volts = [v for v in valid_volts if v >= 200]
        else: 
            valid_volts = [v for v in valid_volts if v < 200]
        
        if not valid_volts: 
            valid_volts = [pkg_limits["max_voltage_v"]] 
        vdss = random.choice(valid_volts)

        # B. Choose Technology & Calculate Rds(on)
        is_p_channel = "P_Channel" in archetype
        if is_p_channel: 
            tech = "P_Channel_Standard"
        elif "SiC" in archetype:
            tech = "SiC_Standard"
        elif "GaN" in archetype:
            tech = "GaN_Standard"
        elif vdss <= 100: 
            tech = "Low_Voltage_Trench"
        elif vdss >= 500: 
            tech = "SuperJunction_HV"
        else: 
            tech = "Planar_HV"
            
        tech_fom = self.constants.TECH_FOM[tech]
        
        # Estimate Die Size available in package
        die_size_factor = pkg_limits["max_power_watts"] / 50.0 
        
        # Physics: Rds * Area ~ V^2.0
        base_rds = tech_fom * (vdss / 50.0)**2.0 * 0.01 
        
        rds_on = base_rds / max(die_size_factor, 0.05)
        
        # C. Calculate Max Current (Id) with THERMAL VALIDATION
        # Thermal current limit
        i_thermal = math.sqrt(pkg_limits["max_power_watts"] / rds_on)
        
        # 🔧 VALIDATION: Check if junction temp stays below limit
        p_actual = (i_thermal ** 2) * rds_on
        t_rise = p_actual * pkg_limits["rth_ja"]
        tj_estimated = 25 + t_rise
        
        # If junction temp exceeds 150°C, reduce current
        if tj_estimated > 150:
            i_thermal_limited = math.sqrt((150 - 25) / (rds_on * pkg_limits["rth_ja"]))
            i_thermal = min(i_thermal, i_thermal_limited)
        
        id_rated = min(i_thermal, pkg_limits["max_current_a"])
        id_rated = float(f"{id_rated:.1f}")
        
        # D. 🆕 Calculate Gate Capacitance (Ciss)
        # Physics: Ciss ∝ Die_Area
        # Die area estimated from Id_rated and Rds
        die_area_mm2 = id_rated * rds_on * 100  # Rough estimate
        
        cap_density = self.constants.CAP_DENSITY.get(tech, 200)
        ciss_est = die_area_mm2 * cap_density
        ciss_est = min(max(ciss_est, 50), 50000)  # Realistic range 50pF - 50nF
        
        # E. 🆕 Internal Gate Resistance (affects switching speed)
        rg_internal = 1.0 + vdss / 200  # Ω, higher voltage = higher Rg
        
        return {
            "vdss": vdss,
            "id_rated": id_rated,
            "rds_on": rds_on,
            "tech_type": tech,
            "ciss_est": ciss_est,
            "rg_internal": rg_internal
        }

    # ----------------------------------------------------------------------
    # PARAMETER GENERATION (ENHANCED)
    # ----------------------------------------------------------------------
    def create_custom_parameter(self, key: str, context: GenerationContext, param_def: Dict):
        if key in self.EXCLUDED_KEYS:
            return None
        extras = context.extras
        vdss = extras["vdss"]
        id_rated = extras["id_rated"]
        rds_on = extras["rds_on_target"]
        ciss_est = extras["ciss_est"]
        rg_int = extras["rg_internal"]
        
        if key == "vdss":
            return self._abs_max("vdss", vdss, "V", "V_DSS", context)

        if key == "id_cont":
            return self._abs_max("id_cont", id_rated, "A", "I_D", context)

        if key == "rds_on":
            val_typ = rds_on * random.uniform(0.9, 1.0)
            val_max = rds_on * 1.3
            
            disp_val, disp_unit = self._auto_scale(val_max, "Ω")
            return GeneratedParameter(
                key="rds_on", label="Drain-Source On Resistance", symbol="R_DS(on)",
                section="ELEC_CHAR",
                value_typ=round(self._auto_scale(val_typ, "Ω")[0], 2),
                value_max=round(disp_val, 2),
                unit=disp_unit,
                condition=f"V_GS=10V, I_D={round(id_rated/2, 1)}A",
                spec_type=SpecType.MAX_RATING, engineering_class=EngineeringClass.PERFORMANCE
            )

        if key == "vgs_th":
            base = self.constants.VGS_TH_DEFAULTS.get(context.archetype, 2.0)
            if extras["is_p_channel"]: 
                base = -abs(base)
            
            # 🔧 FIXED: Realistic variation ±0.5V (not percentage)
            return GeneratedParameter(
                key="vgs_th", label="Gate Threshold Voltage", symbol="V_GS(th)",
                section="ELEC_CHAR",
                value_min=round(base - 0.5, 1),
                value_typ=round(base, 1),
                value_max=round(base + 0.5, 1),
                unit="V", condition="V_DS=V_GS, I_D=250µA",
                spec_type=SpecType.NOMINAL
            )
        
        # 🆕 Gate Capacitances
        cap_cond = "V_DS=25V, V_GS=0V, f=1MHz"

        if key == "ciss":
            return GeneratedParameter(
                key="ciss", label="Input Capacitance", symbol="C_iss",
                section="ELEC_CHAR",
                value_typ=int(ciss_est),
                value_max=int(ciss_est * 1.2),
                unit="pF",
                condition=cap_cond,
                spec_type=SpecType.NOMINAL
            )

        if key == "coss":
            # Coss (output cap) typically 30-50% of Ciss
            coss = ciss_est * random.uniform(0.3, 0.5)
            return GeneratedParameter(
                key="coss", label="Output Capacitance", symbol="C_oss",
                section="ELEC_CHAR",
                value_typ=int(coss),
                value_max=int(coss * 1.2),
                unit="pF",
                condition=cap_cond,
                spec_type=SpecType.NOMINAL
            )

        if key == "crss":
            # Crss (reverse transfer, Miller cap) typically 5-15% of Ciss
            crss = ciss_est * random.uniform(0.05, 0.15)
            return GeneratedParameter(
                key="crss", label="Reverse Transfer Capacitance", symbol="C_rss",
                section="ELEC_CHAR",
                value_typ=max(1, int(crss)),
                value_max=max(1, int(crss * 1.2)),
                unit="pF",
                condition=cap_cond,
                spec_type=SpecType.NOMINAL
            )
        
        if key == "qg":
            # 🔧 FIXED: Proper Gate Charge Physics
            # Qg = Ciss × ΔVgs + Cgd × ΔVds (Miller charge dominant)
            # For typical gate drive: 0→10V with Vds=Vdss/2
            ciss_nf = ciss_est / 1000  # Convert to nF
            cgd_nf = (ciss_est * 0.1) / 1000  # Cgd ≈ 10% of Ciss
            
            qg_total = ciss_nf * 10 + cgd_nf * (vdss / 2)
            
            return GeneratedParameter(
                key="qg", label="Total Gate Charge", symbol="Q_g",
                section="ELEC_CHAR",
                value_typ=round(qg_total, 1),
                unit="nC",
                condition=f"V_DS={vdss/2:.0f}V, V_GS=10V, I_D={round(id_rated/2, 1)}A",
                spec_type=SpecType.NOMINAL
            )
        
        # 🆕 Switching Times
        sw_cond = f"V_DS={vdss/2:.0f}V, I_D={round(id_rated/2, 1)}A, R_G=10Ω"

        if key == "td_on":
            # Turn-on delay: td(on) ∝ Rg_internal × Ciss
            td = rg_int * (ciss_est / 1000) * 2  # ns
            return self._typ_max_obj("td_on", round(td, 1), "ns", "t_d(on)",
                                     label=param_def["llm_context"]["formal_name"],
                                     condition=sw_cond)

        if key == "tr":
            # Rise time: tr ∝ Rg × (Ciss + Cgd)
            tr = rg_int * (ciss_est / 1000) * 1.5
            return self._typ_max_obj("tr", round(tr, 1), "ns", "t_r",
                                     condition=sw_cond)

        if key == "td_off":
            # Turn-off delay (longer than td_on)
            td_off = rg_int * (ciss_est / 1000) * 3
            return self._typ_max_obj("td_off", round(td_off, 1), "ns", "t_d(off)",
                                     label=param_def["llm_context"]["formal_name"],
                                     condition=sw_cond)

        if key == "tf":
            # Fall time
            tf = rg_int * (ciss_est / 1000) * 2
            return self._typ_max_obj("tf", round(tf, 1), "ns", "t_f",
                                     condition=sw_cond)

        # 🆕 Body Diode Parameters
        diode_cond = f"I_F={round(id_rated/2, 1)}A, V_R=30V, dI/dt=100A/µs"

        if key == "vsd":
            # Body diode forward voltage
            vsd = 0.7 if vdss <= 100 else (1.0 if vdss <= 600 else 1.2)
            return GeneratedParameter(
                key="vsd", label="Source-Drain Diode Voltage", symbol="V_SD",
                section="ELEC_CHAR",
                value_typ=vsd, value_max=round(vsd * 1.2, 1),
                unit="V", condition=f"I_S={round(id_rated/2, 1)}A, T_A=25°C",
                spec_type=SpecType.NOMINAL
            )

        if key == "trr":
            # Reverse recovery time (HV devices slower)
            trr_base = 50 if vdss <= 100 else (200 if vdss <= 600 else 500)
            return self._typ_max_obj("trr", trr_base, "ns", "t_rr",
                                     condition=diode_cond)

        if key == "qrr":
            # Reverse recovery charge: Qrr ∝ trr × Id
            trr_base = 50 if vdss <= 100 else (200 if vdss <= 600 else 500)
            qrr = (trr_base * 1e-9) * (id_rated / 2) * 1e9  # nC
            return self._typ_max_obj("qrr", round(qrr, 1), "nC", "Q_rr",
                                     condition=diode_cond)
        
        # 🆕 Temperature Coefficient
        if key == "rds_on_temp_coeff":
            # Positive temp coefficient: SiC lower than Silicon
            tc = 0.3 if "SiC" in extras["tech_type"] else 0.6
            
            return GeneratedParameter(
                key="rds_on_temp_coeff",
                label="Rds(on) Temperature Coefficient",
                symbol="α_Rds",
                section="ELEC_CHAR",
                value_typ=tc,
                unit="%/°C",
                condition="25°C to 175°C",
                spec_type=SpecType.NOMINAL
            )

        return None

    # ----------------------------------------------------------------------
    # BASE VALUES (ENHANCED)
    # ----------------------------------------------------------------------
    def calculate_base_value(self, key: str, limits: Any, context: GenerationContext) -> Any:
        if key in self.EXCLUDED_KEYS:
            return None
        pkg_spec = self.constants.PACKAGE_SPECS.get(context.package)
        if not pkg_spec:
            return None

        dims = pkg_spec["dimensions"]
        pkg_limits = pkg_spec["limits"]
        extras = context.extras
        
        if key == "length": return dims[0]
        if key == "width": return dims[1]
        if key == "height": return dims[2]
        if key == "weight": return dims[3] if len(dims) > 3 else 0.1

        if key == "package_code": 
            return context.package
        
        if key == "power_dissipation":
            # 🔧 IMPROVED: Realistic power dissipation calculation
            
            # A. Conduction loss: P_cond = Id² × Rds(on)
            p_cond = (extras["id_rated"] ** 2) * extras["rds_on_target"]
            
            # B. Switching loss (assume 100kHz, hard switching)
            # P_sw = 0.5 × Vds × Id × (tr + tf) × f_sw
            ciss_est = extras["ciss_est"]
            rg_int = extras["rg_internal"]
            t_sw_total = (ciss_est / 1000) * rg_int * 3.5  # ns, tr+tf estimate
            f_sw = 100e3  # 100 kHz typical
            p_sw = 0.5 * extras["vdss"] * extras["id_rated"] * (t_sw_total * 1e-9) * f_sw
            
            p_total = p_cond + p_sw
            
            # Can't exceed package thermal limit
            pkg_limit = pkg_limits["max_power_watts"]
            return min(round(p_total, 2), pkg_limit)
        
        if key == "thermal_resistance_ja": 
            return pkg_limits["rth_ja"]
        
        if key == "thermal_resistance_jc": 
            return pkg_limits["rth_jc"]
        
        if key == "tj_max":
            # Junction temperature max
            tj = 175 if "SiC" in extras["tech_type"] else 150
            return tj

        return None

    # ----------------------------------------------------------------------
    # CORRELATIONS (SIMPLIFIED - already calculated in context)
    # ----------------------------------------------------------------------
    def apply_correlations(self, result: DatasheetResult):
        """
        Apply final correlations and adjustments to parameters.
        Most physics is already handled in create_custom_parameter,
        but this allows for cross-parameter validation.
        """
        ctx = result.context
        
        # Round all numeric values to reasonable precision
        for p in result.parameters:
            if p.value_typ is not None and isinstance(p.value_typ, float):
                p.value_typ = round(p.value_typ, 3)
            if p.value_min is not None and isinstance(p.value_min, float):
                p.value_min = round(p.value_min, 3)
            if p.value_max is not None and isinstance(p.value_max, float):
                p.value_max = round(p.value_max, 3)

    # ----------------------------------------------------------------------
    # HELPERS
    # ----------------------------------------------------------------------
    def _abs_max(self, key, val, unit, symbol, ctx):
        cond = "T_C=25°C"
        return GeneratedParameter(
            key=key, label="Absolute Maximum Rating", symbol=symbol,
            section="ABS_MAX", value_max=val, unit=unit,
            condition=cond, spec_type=SpecType.MAX_RATING,
            engineering_class=EngineeringClass.SAFETY_LIMIT
        )
    
    def _typ_max_obj(self, key, val_typ, unit, symbol, label=None, condition=""):
        return GeneratedParameter(
            key=key, label=label or symbol, symbol=symbol,
            section="ELEC_CHAR",
            value_typ=val_typ, value_max=round(val_typ * 1.5, 2),
            unit=unit,
            condition=condition,
            spec_type=SpecType.NOMINAL
        )

    def _auto_scale(self, value, unit):
        if value >= 1: return value, unit
        if value >= 1e-3: return value * 1e3, "m" + unit
        return value * 1e6, "µ" + unit
