MODEL_TO_USE = 'qwen2.5:3b' 

# ==========================================
# UNIFIED COMPONENT DATABASE - EXPANDED EDITION
# ==========================================

UNIFIED_COMPONENT_DB = {

    # ==============================================================================
    # 1. RESISTOR חלק1
    # ==============================================================================
    
    "RESISTOR": {
        "archetypes": ["Standard_SMD", "High_Power_THT", "Precision_ThinFilm"],
        
        "ABS_MAX": [
            {
                "key": "power_rating",
                "symbol": "P<sub>rated</sub>",
                "spec_type": "max_rating",
                "column_model": "MAX_ONLY",
                "engineering_class": "SAFETY_LIMIT",
                "special_semantics": "NONE",
                "llm_context": {
                    "formal_name": "Power Rating",
                    "aliases": ["P_rated (Max. Dissipation)", "Rated Power Dissipation [W]", "P rated derate above 70C", "Max. Power Dissip. (P_D)", "P(rated) Continuous", "Power Diss. Capability (W)", "PRATED – Maximum Allowable Dissipation", "Rated Dissipation P_max (W) (Note 1)", "Power (W) [derate linearly above 70°C]"]                },
                "possible_units": ["W", "mW"],
                "std_unit": "W",
                "scenarios": [
                    {
                        "condition": "Ambient 70°C",
                        "limits": {
                            "Standard_SMD": [0.031, 0.063, 0.1, 0.125, 0.25, 0.5, 0.75, 1.0],
                            "High_Power_THT": [1, 2, 3, 5, 7, 10, 15, 20, 25, 50, 100, 150, 225],
                            "Precision_ThinFilm": [0.063, 0.1, 0.125, 0.25, 0.4, 0.5]
                        }
                    }
                ]
            },
            {
                "key": "max_working_voltage",
                "symbol": "V<sub>max</sub>",
                "spec_type": "max_rating",
                "column_model": "MAX_ONLY",
                "engineering_class": "SAFETY_LIMIT",
                "special_semantics": "NONE",
                "llm_context": {
                    "formal_name": "Maximum Working Voltage",
                    "aliases": ["V_max (DC Continuous)", "Max. Working Voltage V_WM [V]", "VRMS / VDC Max Working", "Rated Voltage (DC), V_max", "V_max – Maximum Continuous DC Voltage", "Max. Cont. Voltage [V] (DC)", "V(max) Working – See Derating Curve", "Maximum Continuous Voltage V_RWV", "Rated Volt. (V_R) DC Continuous"]
                },
                "possible_units": ["V", "kV"],
                "std_unit": "V",
                "scenarios": [
                    {
                        "condition": "DC Continuous",
                        "limits": {
                            "Standard_SMD": [25, 50, 75, 100, 150, 200, 250, 400, 500],
                            "High_Power_THT": [250, 350, 500, 750, 1000, 1500, 2000, 2500, 3500, 5000],
                            "Precision_ThinFilm": [25, 50, 75, 100, 150, 200, 250]
                        }
                    }
                ]
            },
            {
                "key": "max_overload_voltage",
                "symbol": "V<sub>OL</sub>",
                "spec_type": "max_rating",
                "column_model": "MAX_ONLY",
                "engineering_class": "SAFETY_LIMIT",
                "special_semantics": "NONE",
                "llm_context": {
                    "formal_name": "Maximum Overload Voltage",
                    "aliases": ["V_OL Short-Time Overload", "Dielectric Withstanding Voltage", "V(OL) – Short Duration Overload", "Short-time Overload V [V]", "V_overload (Peak, Non-Repetitive)", "Max. Overload V (Surge) [V]", "Peak Overload Voltage", "V_OV – Overload Withstand", "Surge Voltage Rating V_S (Single Event)"]
                },
                "possible_units": ["V"],
                "std_unit": "V",
                "scenarios": [
                    {
                        "condition": "5 seconds",
                        "limits": {
                            "Standard_SMD": [50, 100, 150, 200, 300, 400, 500, 800],
                            "High_Power_THT": [500, 700, 1000, 1500, 2000, 3000, 5000, 7500],
                            "Precision_ThinFilm": [50, 100, 150, 200, 300, 400, 500]
                        }
                    }
                ]
            },
            {
                "key": "pulse_withstanding",
                "symbol": "P<sub>pulse</sub>",
                "spec_type": "max_rating",
                "column_model": "MAX_ONLY",
                "engineering_class": "SAFETY_LIMIT",
                "special_semantics": "NONE",
                "llm_context": {
                    "formal_name": "Pulse Withstanding Power",
                    "aliases": ["P_pulse – Non-Repetitive Surge", "Peak Pulse Power P_pk [W]", "P(pulse) – Non-Repetitive Surge", "Single Pulse Surge Power", "P_PULSE Max. (W) Note: Derated for Repetitive", "Pulse Rating P_surge", "Max. Peak Pulse Dissipation", "Surge Pwr Capability P_sp [kW]"]
                },
                "possible_units": ["W", "kW"],
                "std_unit": "W",
                "scenarios": [
                    {
                        "condition": "1ms pulse",
                        "limits": {
                            "Standard_SMD": [0.25, 0.5, 1, 2, 3, 5, 10],
                            "High_Power_THT": [25, 50, 100, 150, 200, 300, 500, 1000],
                            "Precision_ThinFilm": [0.25, 0.5, 1, 2, 3]
                        }
                    }
                ]
            },
            {
                "key": "max_operating_temp",
                "symbol": "T<sub>max</sub>",
                "spec_type": "max_rating",
                "column_model": "MAX_ONLY",
                "engineering_class": "SAFETY_LIMIT",
                "special_semantics": "NONE",
                "llm_context": {
                    "formal_name": "Maximum Operating Temperature",
                    "aliases": ["T_max (Upper Category Temp.)", "Max. Oper. Temp T_A(max) [°C]", "T(max) – Maximum Ambient Temperature", "Upper Category Temp. T_cat(max) °C", "T_AMB Max. (Continuous Operation)", "Max. Operating T [°C] (Continuous, Still Air)", "T_OP(max) – See Power Derating Curve", "Maximum Ambient Temp. T_A ≤ ? °C", "Tmax Continuous Rated Ambient [°C]", "T_MAX (Operational Limit, Refer to Fig. 2)"]
                },
                "possible_units": ["°C"],
                "std_unit": "°C",
                "scenarios": [
                    {
                        "condition": "Continuous",
                        "limits": {
                            "Standard_SMD": [125, 155, 170],
                            "High_Power_THT": [155, 175, 200, 225, 275, 350],
                            "Precision_ThinFilm": [125, 155, 175]
                        }
                    }
                ]
            },
            {
                "key": "min_operating_temp",
                "symbol": "T<sub>min</sub>",
                "spec_type": "min_rating",
                "column_model": "MIN_ONLY",
                "engineering_class": "SAFETY_LIMIT",
                "special_semantics": "NONE",
                "llm_context": {
                    "formal_name": "Minimum Operating Temperature",
                    "aliases": ["T_min (Lower Category Temp.)", "Min. Oper. Temp T_A(min) [°C]", "T(min) – Lower Ambient Temperature Limit", "Lower Category Temp. T_cat(min) °C", "T_AMB Min. [°C]", "Min. Operating T [°C] (Storage and Operation)", "T_OP(min) – Cold Operational Limit", "Minimum Ambient Temp. T_A ≥ ? °C", "Tmin Continuous Rated Ambient [°C]", "T_MIN (Operational Lower Bound)"]
                },
                "possible_units": ["°C"],
                "std_unit": "°C",
                "scenarios": [
                    {
                        "condition": "Continuous",
                        "limits": {
                            "Standard_SMD": [-55, -40],
                            "High_Power_THT": [-65, -55, -40],
                            "Precision_ThinFilm": [-55, -40]
                        }
                    }
                ]
            },
            {
                "key": "max_current",
                "symbol": "I<sub>max</sub>",
                "spec_type": "max_rating",
                "column_model": "MAX_ONLY",
                "engineering_class": "SAFETY_LIMIT",
                "special_semantics": "DERIVED",
                "llm_context": {
                    "formal_name": "Maximum Continuous Current",
                    "aliases": ["I_max (Continuous DC, P=I²R)", "Max. Current I_rated [A] (Calc. from P=I²·R)", "Rated Current I_R [A] (Derived, P=I²R)", "I_MAX – Max. Allowable Continuous Current", "Max. Cont. Current (DC) [A] Note: I²R limited", "Maximum Current I_MAX [mA] (I²R Basis)", "I_CONT Max. [A] (Calculated: √(P_rated / R))"]
                },
                "possible_units": ["A", "mA"],
                "std_unit": "A",
                "scenarios": [
                    {
                        "condition": "Continuous DC, calculated from P=I²R",
                        "limits": {
                            "Standard_SMD": [0.05, 0.1, 0.2, 0.5, 1, 2],
                            "High_Power_THT": [1, 2, 5, 10, 15, 20, 30, 50],
                            "Precision_ThinFilm": [0.05, 0.1, 0.2, 0.5, 1]
                        }
                    }
                ]
            },
            {
                "key": "esd_rating",
                "symbol": "ESD",
                "spec_type": "max_rating",
                "column_model": "MAX_ONLY",
                "engineering_class": "SAFETY_LIMIT",
                "special_semantics": "NONE",
                "llm_context": {
                    "formal_name": "Electrostatic Discharge Rating",
                    "aliases": ["ESD (HBM) [kV]", "ESD Sensitivity – Human Body Model (HBM, JESD22-A114)", "ESD Rating V_ESD [kV] (Human Body Model)", "Electrostatic Discharge Withstand HBM [kV]", "ESD HBM Class (per JEDEC JESD22-A114)", "V_ESD (Human Body Model) kV", "ESD Susceptibility [kV] HBM Model", "Electrostatic Sensitivity (HBM) – See Handling Note", "HBM ESD Rating [kV] ANSI/ESD STM5.1"]
                },
                "possible_units": ["kV"],
                "std_unit": "kV",
                "scenarios": [
                    {
                        "condition": "Human Body Model (HBM)",
                        "limits": {
                            "Standard_SMD": [0.5, 1, 2, 4, 8, 15],
                            "High_Power_THT": [2, 4, 8, 15, 25],
                            "Precision_ThinFilm": [0.5, 1, 2, 4, 8]
                        }
                    }
                ]
            },
            {
                "key": "max_element_temp",
                "symbol": "T<sub>elem</sub>",
                "spec_type": "max_rating",
                "column_model": "MAX_ONLY",
                "engineering_class": "SAFETY_LIMIT",
                "special_semantics": "NONE",
                "llm_context": {
                    "formal_name": "Maximum Element Temperature",
                    "aliases": ["T_elem (Max. Hot Spot @ Rated Power)", "Max. Resistive Element Temp. T_hs [°C]", "T(elem) – Hot Spot Temperature", "Max. Hot Spot T [°C] at Rated Dissipation", "T_hotspot (Max, @ full rated power)", "Element Temp. T_RE(max) [°C] (Note: Not T_ambient)", "Max. Film/Element Temperature [°C]", "T_elem Max. (°C) – Resistive Film Hot Spot", "T_ELEM – Internal Element Temp. Limit [°C]"]
                },
                "possible_units": ["°C"],
                "std_unit": "°C",
                "scenarios": [
                    {
                        "condition": "At rated power",
                        "limits": {
                            "Standard_SMD": [155, 175],
                            "High_Power_THT": [275, 350, 400, 450, 500],
                            "Precision_ThinFilm": [155, 175]
                        }
                    }
                ]
            }
        ],
        
        "ELEC_CHAR": [
            {
                "key": "resistance",
                "symbol": "R",
                "spec_type": "nominal",
                "column_model": "MIN_TYP_MAX",
                "engineering_class": "NOMINAL_PARAMETER",
                "special_semantics": "NONE",
                "llm_context": {
                    "formal_name": "Resistance",
                    "aliases": ["R (Nominal, Ω) E96 Series", "DC Resistance R_DC [Ω / kΩ / MΩ]", "Resistance Value R_nom (Ω, ±Tol%)", "Ohmic Value [kΩ] (E24/E96/E192)", "R_NOM – Nominal Resistance", "Resistance R [Ω] (Before Load Life, Initial Value)", "R (DC) [Ω] See Tolerance & TCR", "Nominal Resistance R_0 (Ω)", "Resistance (kΩ) – E-Series, ±0.1% Initial Tol."]
                },
                "possible_units": ["Ω", "kΩ", "MΩ", "mΩ"],
                "std_unit": "Ω",
                "scenarios": [
                    {
                        "condition": "Standard E-Series (E24/E96/E192)",
                        "limits": {
                            "Standard_SMD": [0.01, 0.1, 1, 10, 22, 47, 100, 220, 470, 1000, 2200, 4700, 10000, 22000, 47000, 100000, 220000, 470000, 1000000, 10000000],
                            "High_Power_THT": [0.001, 0.01, 0.1, 0.22, 0.47, 1, 2.2, 4.7, 10, 22, 47, 100, 220, 470, 1000, 10000],
                            "Precision_ThinFilm": [10, 24.9, 49.9, 100, 249, 499, 1000, 2000, 4990, 10000, 20000, 49900, 100000, 249000, 1000000]
                        }
                    }
                ]
            },
            {
                "key": "tolerance",
                "symbol": "Tol",
                "spec_type": "nominal",
                "column_model": "TYP_ONLY",
                "engineering_class": "NOMINAL_PARAMETER",
                "special_semantics": "NONE",
                "llm_context": {
                    "formal_name": "Resistance Tolerance",
                    "aliases": ["Tol. (%) Initial", "Resistance Accuracy ±[%] (Initial)", "Initial Tolerance ΔR/R₀ [%]", "R Tolerance [%] – See Table 1 for E-Series", "±Tol% (Initial, Before Aging)", "Tolerance (Resistance, %) – IEC 60062 Code", "Resistance Tol. ±% (Pre-Load-Life)", "ΔR/R Initial [%] (Measured Low Power)", "Tol [%] (Initial Value; Excl. TCR & Drift)"]
                },
                "possible_units": ["%"],
                "std_unit": "%",
                "scenarios": [
                    {
                        "condition": "At 25°C",
                        "limits": {
                            "Standard_SMD": [0.5, 1, 2, 5, 10],
                            "High_Power_THT": [1, 2, 5, 10, 20],
                            "Precision_ThinFilm": [0.01, 0.02, 0.05, 0.1, 0.25, 0.5, 1]
                        }
                    }
                ]
            },
            {
                "key": "tcr",
                "symbol": "TCR",
                "spec_type": "max_limit",
                "column_model": "TYP_MAX",
                "engineering_class": "PERFORMANCE_LIMIT",
                "special_semantics": "NONE",
                "llm_context": {
                    "formal_name": "Temperature Coefficient of Resistance",
                    "aliases": ["TCR [ppm/°C] (Over Operating Range)", "Temp. Coeff. of Resistance ΔR/R·ΔT [ppm/K]", "TCR (ppm/°C) – Full Temp. Range", "Temperature Coefficient (Tempco) [ppm/°C]", "ΔR/R per °C [ppm] (Temp. Coefficient)", "T.C.R. [ppm/K] IEC 60115, Box Method", "Tempco TCR [ppm/°C]", "Resistance Temp. Coeff. α_R [10⁻⁶/°C]", "TCR (ppm/°C) Max. Magnitude |+TCR / -TCR|"]
                },
                "possible_units": ["ppm/°C", "ppm/K"],
                "std_unit": "ppm/°C",
                "scenarios": [
                    {
                        "condition": "Over operating range",
                        "limits": {
                            "Standard_SMD": [50, 100, 200, 400, 600],
                            "High_Power_THT": [100, 200, 350, 500, 1000, 1500],
                            "Precision_ThinFilm": [2, 5, 10, 15, 25, 50, 100]
                        }
                    }
                ]
            },
            {
                "key": "load_life_stability",
                "symbol": "ΔR/R",
                "spec_type": "max_limit",
                "column_model": "MAX_ONLY",
                "engineering_class": "PERFORMANCE_LIMIT",
                "special_semantics": "NONE",
                "llm_context": {
                    "formal_name": "Load Life Stability",
                    "aliases": ["ΔR/R (%) Load Life", "Load Life (Long-Term Drift) ΔR/R₀ [%]", "Stability ΔR/R [%]", "Long-Term Stability [%] (IEC 60068)", "ΔR/R₀ Max [%] after Load Life Test", "Resistance Change After Endurance ΔR/R₀ ≤ ±?%", "Stability (Life) [%] Rated Power"]
                },
                "possible_units": ["%"],
                "std_unit": "%",
                "scenarios": [
                    {
                        "condition": "1000h @ Rated Power & 70°C",
                        "limits": {
                            "Standard_SMD": [0.5, 1, 2, 3, 5],
                            "High_Power_THT": [2, 3, 5, 10],
                            "Precision_ThinFilm": [0.02, 0.05, 0.1, 0.25, 0.5]
                        }
                    },
                    {
                        "condition": "2000h @ Rated Power & 70°C",
                        "limits": {
                            "Standard_SMD": [1, 2, 3, 5],
                            "High_Power_THT": [3, 5, 10],
                            "Precision_ThinFilm": [0.05, 0.1, 0.25, 0.5]
                        }
                    }
                ]
            },
            {
                "key": "voltage_coefficient",
                "symbol": "VCR",
                "spec_type": "max_limit",
                "column_model": "MAX_ONLY",
                "engineering_class": "PERFORMANCE_LIMIT",
                "special_semantics": "NONE",
                "llm_context": {
                    "formal_name": "Voltage Coefficient of Resistance",
                    "aliases": ["VCR [ppm/V]", "Voltage Coefficient V.C.R. [ppm/V]", "Voltage Dependence ΔR/R·ΔV [ppm/V]", "VCR (ppm/V) – Voltage Induced Resistance Change", "Resistance Voltage Coeff. α_V [ppm/V]", "V.C.R. [ppm/V]", "Voltage Coefficient (VC) [ppm/V] Max.", "ΔR/R per Volt [ppm/V]", "VCR Max. [ppm/V] (Non-linearity, Voltage Induced)"]
                },
                "possible_units": ["ppm/V"],
                "std_unit": "ppm/V",
                "scenarios": [
                    {
                        "condition": "At rated voltage",
                        "limits": {
                            "Standard_SMD": [10, 50, 100, 200],
                            "High_Power_THT": [50, 100, 200, 500],
                            "Precision_ThinFilm": [0.1, 0.5, 1, 2, 5, 10]
                        }
                    }
                ]
            },
            {
                "key": "noise",
                "symbol": "NI",
                "spec_type": "max_limit",
                "column_model": "MAX_ONLY",
                "engineering_class": "PERFORMANCE_LIMIT",
                "special_semantics": "NONE",
                "llm_context": {
                    "formal_name": "Current Noise Index",
                    "aliases": ["NI [dB] (Current Noise, Per Voltage Decade)", "Excess Noise Index [dB] (1/f, per Decade)", "Current Noise [µV/V] (1 Decade BW)", "Noise Index NI [dB] (IEC 60195)", "1/f Noise [dB] @ 1 Decade Bandwidth", "Excess Noise [dB] – Flicker/Contact Noise", "N.I. [dB] (Low-Freq. Excess Noise, per Decade V)", "Current Noise (µV/V rms, per Voltage Decade)", "Noise Index (dB) – Per MIL-STD-202, Method 308", "Flicker Noise / 1f Noise NI [dB] (per V decade)"]
                },
                "possible_units": ["dB", "µV/V"],
                "std_unit": "dB",
                "scenarios": [
                    {
                        "condition": "Per voltage decade",
                        "limits": {
                            "Standard_SMD": [-20, -10, 0, 10],
                            "High_Power_THT": [-10, 0, 10, 20],
                            "Precision_ThinFilm": [-40, -35, -30, -25]
                        }
                    }
                ]
            },
            {
                "key": "thermal_resistance",
                "symbol": "θ<sub>JA</sub>",
                "spec_type": "nominal",
                "column_model": "TYP_MAX",
                "engineering_class": "NOMINAL_PARAMETER",
                "special_semantics": "NONE",
                "llm_context": {
                    "formal_name": "Thermal Resistance Junction to Ambient",
                    "aliases": ["θ_JA [°C/W] (Junction-to-Ambient, Still Air)", "Rth(j-a) [°C/W] – Still Air Condition", "Thermal Resistance J-A θ_JA [K/W]", "R_th(JA) (°C/W), No Heat Sink, Still Air", "θ JA [°C/W] (Mounted on PCB, No Airflow)", "Junction-to-Ambient Thermal Impedance [°C/W]", "Rth J→A [K/W] (Worst Case, Free Convection)", "Thermal Res. Junct. to Amb. θ_JA [°C/W]", "θ(JA) °C/W (FR4 PCB, 1oz Cu, No Forced Air)"]
                },
                "possible_units": ["°C/W", "K/W"],
                "std_unit": "°C/W",
                "scenarios": [
                    {
                        "condition": "Junction to Ambient, Still Air",
                        "limits": {
                            "Standard_SMD": [400, 300, 200, 150, 100, 50, 35, 25],
                            "High_Power_THT": [100, 75, 50, 35, 25, 15, 10, 5, 3, 2, 1],
                            "Precision_ThinFilm": [400, 300, 200, 150, 100, 75]
                        }
                    }
                ]
            },
            {
                "key": "derating_curve",
                "symbol": "T<sub>derate</sub>",
                "spec_type": "nominal",
                "column_model": "TYP_ONLY",
                "engineering_class": "NOMINAL_PARAMETER",
                "special_semantics": "NONE",
                "llm_context": {
                    "formal_name": "Power Derating Temperature",
                    "aliases": ["T_derate – Derating Starts at [°C]", "Rated Ambient Temp. T_R (Derating Knee) [°C]", "Power Derating Start Temp. T_A [°C]", "T_AMB (Above Which P_rated Is Derated) [°C]", "Derating Temp. T_D [°C] (Linear Derating Begins)", "T_derate [°C] – See Power Derating Curve (Fig.1)", "Rated T_amb (°C) – Full Power Below This Temp.", "Derating Knee Temperature [°C] (Refer Fig. 3)", "Power Reduction Start Temp. [°C] (Above = Derate)"]
                },
                "possible_units": ["°C"],
                "std_unit": "°C",
                "scenarios": [
                    {
                        "condition": "Linear derating starts",
                        "limits": {
                            "Standard_SMD": [70, 85],
                            "High_Power_THT": [25, 50, 70],
                            "Precision_ThinFilm": [70, 85, 100]
                        }
                    }
                ]
            },
            
            {
                "key": "self_resonant_freq",
                "symbol": "f<sub>res</sub>",
                "spec_type": "nominal",
                "column_model": "MIN_TYP_MAX",
                "engineering_class": "NOMINAL_PARAMETER",
                "special_semantics": "NONE",
                "llm_context": {
                    "formal_name": "Self Resonant Frequency",
                    "aliases": ["SRF [MHz] – Self-Resonant Frequency", "f_res (Self Resonance) [MHz] Typical", "Resonant Freq. f_SRF [GHz] (Typ.)", "f_resonance [MHz] (Parasitic L & C Dependent)", "SRF (MHz) – Above This Freq., Becomes Inductive", "f_SRF [GHz] Typ. (Measured S11, 50Ω System)", "Self Resonance f_r [MHz] (Chip Size Dependent)", "SRF [MHz] Min. Typ. (Network Analyzer Measured)", "Resonant Freq. [MHz] (L_par, C_par Interaction)"]
                },
                "possible_units": ["MHz", "GHz"],
                "std_unit": "MHz",
                "scenarios": [
                    {
                        "condition": "Typical",
                        "limits": {
                            "Standard_SMD": [100, 500, 1000, 2000, 5000, 10000],
                            "High_Power_THT": [1, 5, 10, 50, 100],
                            "Precision_ThinFilm": [500, 1000, 2000, 5000]
                        }
                    }
                ]
            },
            {
                "key": "parasitic_inductance",
                "symbol": "L<sub>par</sub>",
                "spec_type": "nominal",
                "column_model": "TYP_MAX",
                "engineering_class": "NOMINAL_PARAMETER",
                "special_semantics": "NONE",
                "llm_context": {
                    "formal_name": "Parasitic Inductance",
                    "aliases": ["L_par [nH] (Series, Typ.)", "ESL [nH] – Equivalent Series Inductance", "Series Inductance L_s [nH] Typ.", "Parasitic Series L [nH] (Package & Lead)", "L_parasitic [pH] (Typ., Chip Inductance)", "Self-Inductance L [nH]", "ESL (nH) Equiv. Series Inductance, Typ.", "Lead/Package Inductance L [nH] (Typ.)", "Inductive Parasitics L_par [nH] (Note: SRF Limited)", "Series L [nH] Typ. Max. (RF Performance Relevant)"]
                },
                "possible_units": ["nH", "pH"],
                "std_unit": "nH",
                "scenarios": [
                    {
                        "condition": "Typical at 1MHz",
                        "limits": {
                            "Standard_SMD": [0.2, 0.5, 1, 2, 5],
                            "High_Power_THT": [5, 10, 20, 50, 100],
                            "Precision_ThinFilm": [0.2, 0.5, 1, 2]
                        }
                    }
                ]
            },
            {
                "key": "parasitic_capacitance",
                "symbol": "C<sub>par</sub>",
                "spec_type": "nominal",
                "column_model": "TYP_MAX",
                "engineering_class": "NOMINAL_PARAMETER",
                "special_semantics": "NONE",
                "llm_context": {
                    "formal_name": "Parasitic Capacitance",
                    "aliases": ["C_par [pF] (Shunt, Typ.)", "Parallel Capacitance C_p [pF] Typ.", "Shunt Capacitance C_shunt [pF] (Typ.)", "Parasitic Shunt C [fF] (Chip, Typ.)", "C_parasitic [pF] (Terminal-to-Terminal)", "Equiv. Parallel Capacitance C_par [pF] Typ. Max.", "C_p [pF] Parasitic (High-Freq. Performance Impact)", "Shunt C [pF] Typ. (See SRF and L_par for Context)", "Parallel C_stray [pF] Typ. Max. (Package Dependent)"]
                },
                "possible_units": ["pF", "fF"],
                "std_unit": "pF",
                "scenarios": [
                    {
                        "condition": "Typical",
                        "limits": {
                            "Standard_SMD": [0.05, 0.1, 0.2, 0.5, 1],
                            "High_Power_THT": [1, 2, 5, 10, 20],
                            "Precision_ThinFilm": [0.05, 0.1, 0.2, 0.5]
                        }
                    }
                ]
            }
        ],
        
        "PACKAGE": [
            {
                "key": "package_code",
                "symbol": "PKG",
                "spec_type": "mechanical",
                "column_model": "TYP_ONLY",
                "engineering_class": "MECHANICAL",
                "special_semantics": "CATEGORICAL",
                "llm_context": {
                    "formal_name": "Package Type",
                    "aliases": ["PKG / Case Size (EIA Code)", "Case / Package Code (e.g., 0402, 0805)", "Form Factor – EIA / IEC Size Code", "Package Style (SMD Size / THT Case)", "Size Code [EIA-198] (e.g., '0603' = 1.6x0.8mm)", "Component Package (Case Outline)", "PKG Code (Chip Size, EIA Metric / Imperial)", "Pkg. Type – SMD Chip / THT Axial / Power Tab", "Body Size (LxW) Case Code (EIA / JEDEC)", "Package / Case (e.g., TO-220, Axial-1W, 1206)"]
                },
                "possible_units": [""],
                "std_unit": "",
                "scenarios": [
                    {
                        "condition": "Standard packages",
                        "limits": {
                            "Standard_SMD": ["01005", "0201", "0402", "0603", "0805", "1206", "1210", "1218", "2010", "2512"],
                            "High_Power_THT": [
                                "Axial_0.4W", "Axial_0.6W", "Axial_1W", "Axial_2W", "Axial_3W", "Axial_5W", "Axial_7W", "Axial_10W", 
                                "TO-220", "TO-263", "TO-247"
                            ],
                            "Precision_ThinFilm": ["0402", "0603", "0805", "1206", "1210", "2010"]
                        }
                    }
                ]
            },
            {
                "key": "moisture_sensitivity",
                "symbol": "MSL",
                "spec_type": "nominal",
                "column_model": "TYP_ONLY",
                "engineering_class": "MECHANICAL",
                "special_semantics": "CATEGORICAL",
                "llm_context": {
                    "formal_name": "Moisture Sensitivity Level",
                    "aliases": ["MSL (JEDEC J-STD-020)", "Moisture Sensitivity Level MSL [1-6]", "MSL Rating per JEDEC J-STD-020E", "Moisture Sensitivity (MSL Class)", "MSL Level (J-STD-020, Floor Life)", "Moisture Sensitivity Level – IPC/JEDEC", "MSL (Moisture Sensitivity, Reflow Related)", "Moisture Sensitivity Rating MSL (JEDEC Std.)", "MSL Category (1=Unlimited, 2=1yr, 3=168h…)", "Moisture Sensitivity (MSL) per J-STD-020 Rev. E"]
                },
                "possible_units": [""],
                "std_unit": "",
                "scenarios": [
                    {
                        "condition": "Per JEDEC J-STD-020",
                        "limits": {
                            "Standard_SMD": [1, 2, 3],
                            "High_Power_THT": [1],
                            "Precision_ThinFilm": [1, 2, 3]
                        }
                    }
                ]
            },
            {
                "key": "length",
                "symbol": "L",
                "spec_type": "mechanical",
                "column_model": "MIN_TYP_MAX",
                "engineering_class": "MECHANICAL",
                "special_semantics": "NONE",
                "llm_context": {
                    "formal_name": "Package Length",
                    "aliases": ["L (Length) [mm] Nom. (EIA Body Dim.)", "Body Length L [mm] Min. / Typ. / Max.", "Overall Length L [mm] (Incl. Terminations)", "Dim. L – Chip Body Length [mm] ±0.05", "L_body [mm] (Per Package Drawing, Note A)", "Package Length [mm] (See Land Pattern Fig.)", "Length L [mm] (IPC-SM-782 Footprint Ref.)", "L [mm] Nom. (Refer to Mechanical Outline Dwg.)", "Body Length (X Dimension) [mm] Min/Typ/Max", "Overall Chip Length L [mm] (Solder Termination Incl.)"]
                },
                "possible_units": ["mm", "inch"],
                "std_unit": "mm",
                "scenarios": [
                    {
                        "condition": "Nominal dimensions",
                        "limits": {
                            "Standard_SMD": [0.4, 0.6, 1.0, 1.6, 2.0, 3.2, 3.2, 3.2, 5.0, 6.4],
                            "High_Power_THT": [
                                3.5, 6.5, 9.0, 11.0, 15.0, 25.0, 35.0, 52.0, 
                                15.0, 15.0, 20.0
                            ],
                            "Precision_ThinFilm": [1.0, 1.6, 2.0, 3.2, 3.2, 5.0]
                        }
                    }
                ]
            },
            {
                "key": "width",
                "symbol": "W",
                "spec_type": "mechanical",
                "column_model": "MIN_TYP_MAX",
                "engineering_class": "MECHANICAL",
                "special_semantics": "NONE",
                "llm_context": {
                    "formal_name": "Package Width",
                    "aliases": ["W (Width) [mm] Nom. (EIA Body Dim.)", "Body Width W [mm] Min. / Typ. / Max.", "Overall Width W [mm]", "Dim. W – Chip Body Width [mm] ±0.05", "W_body [mm] (Per Package Drawing, Note B)", "Package Width [mm] (See Land Pattern Fig.)", "Width W [mm] (IPC-SM-782 Footprint Ref.)", "W [mm] Nom. (Refer to Mechanical Outline Dwg.)", "Body Width (Y Dimension) [mm] Min/Typ/Max", "Chip Width / Diameter [mm] (Body, Excl. Leads)"]
                },
                "possible_units": ["mm", "inch"],
                "std_unit": "mm",
                "scenarios": [
                    {
                        "condition": "Nominal dimensions",
                        "limits": {
                            "Standard_SMD": [0.2, 0.3, 0.5, 0.8, 1.25, 1.6, 2.5, 3.2, 2.5, 3.2],
                            "High_Power_THT": [
                                1.9, 2.5, 3.5, 4.5, 5.5, 8.0, 8.5, 8.5, 
                                10.0, 10.0, 15.0
                            ],
                            "Precision_ThinFilm": [0.5, 0.8, 1.25, 1.6, 2.5, 2.5]
                        }
                    }
                ]
            },
            {
                "key": "height",
                "symbol": "H",
                "spec_type": "mechanical",
                "column_model": "MIN_TYP_MAX",
                "engineering_class": "MECHANICAL",
                "special_semantics": "NONE",
                "llm_context": {
                    "formal_name": "Package Height",
                    "aliases": ["H (Height / Thickness) [mm] Max.", "Body Height H [mm] Min. / Typ. / Max.", "Overall Height H [mm] (Mounted Profile)", "Dim. H – Chip Thickness [mm] ±0.03", "H_body [mm] (Per Package Drawing, Note C)", "Package Height [mm] (Max. Standoff)", "Thickness t [mm] (Max. Profile Above Board)", "H [mm] Max. (Mounted Height, Incl. Solder)", "Component Height (Z Dimension) [mm] Max.", "Max. Height H [mm] (Above PCB Surface, Mounted)"]
                },
                "possible_units": ["mm", "inch"],
                "std_unit": "mm",
                "scenarios": [
                    {
                        "condition": "Nominal dimensions",
                        "limits": {
                            "Standard_SMD": [0.13, 0.23, 0.35, 0.45, 0.55, 0.55, 0.55, 0.55, 0.55, 0.55],
                            "High_Power_THT": [
                                1.9, 2.5, 3.5, 4.5, 5.5, 8.0, 8.5, 8.5, 
                                4.5, 4.5, 5.0
                            ],
                            "Precision_ThinFilm": [0.35, 0.45, 0.55, 0.55, 0.55, 0.55]
                        }
                    }
                ]
            },
            {
                "key": "weight",
                "symbol": "m",
                "spec_type": "mechanical",
                "column_model": "TYP_MAX",
                "engineering_class": "MECHANICAL",
                "special_semantics": "NONE",
                "llm_context": {
                    "formal_name": "Package Weight",
                    "aliases": ["m (Mass / Weight) [mg] Typ.", "Component Weight [mg] Typ. (Approx.)", "Mass m [mg] (Typical, Excl. Packaging)", "Wt. [g] Approx. (Per Piece, Bare Component)", "Package Weight [mg] Typ. Max.", "m_pkg [mg] (Typ., For Lead-Free Assessment)", "Weight [mg] (Typical Per Component, Note: ±20%)", "Component Mass [g] (Approx., Chip Only)", "Net Weight Per Piece [mg] Typ.", "Wt. (mg) Typ. (Suitable for Pick-and-Place Calc.)"]
                },
                "possible_units": ["mg", "g"],
                "std_unit": "mg",
                "scenarios": [
                    {
                        "condition": "",
                        "limits": {
                            "Standard_SMD": [0.2, 0.5, 1, 3, 8, 15, 25, 40, 40, 80],
                            "High_Power_THT": [
                                150, 300, 500, 1000, 1500, 3000, 5000, 8000, 
                                2000, 1500, 5000
                            ],
                            "Precision_ThinFilm": [1, 3, 8, 15, 25, 40]
                        }
                    }
                ]
            },
            {
               "key": "terminal_finish",
               "symbol": "Finish",
               "spec_type": "mechanical",
               "column_model": "TYP_ONLY",
               "engineering_class": "MECHANICAL",
               "special_semantics": "CATEGORICAL",
               "llm_context": {
                   "formal_name": "Terminal Finish", 
                   "aliases": ["Lead Finish / Termination Material", "Contact Plating (e.g., Matte Sn, Au)", "Terminal Plating – Lead-Free (RoHS)", "Termination Finish (e.g., 100% Matte Tin)", "Lead / Terminal Finish Code (e.g., Sn, NiAu)", "Solder Finish – Termination Material", "End Cap / Lead Plating (RoHS Compliant)", "Termination (e.g., Sn/Pb 60/40 or SAC305)", "Lead Plating Material (See RoHS Compliance Note)", "Electrode / Terminal Material (e.g., Ag, Au, Sn)"]
               },
               "possible_units": [""],
               "std_unit": "",
               "scenarios": [
                   {
                       "condition": "Standard",
                       "limits": {
                           "Standard_SMD": [
                               "100% Matte Tin (Sn)", 
                               "Sn/Pb (60/40)", 
                               "Gold (Au) Flash", 
                               "Tin-Silver-Copper (SAC305)"
                           ],
                           "High_Power_THT": [
                               "100% Matte Tin", 
                               "Tin-Copper (SnCu)", 
                               "Silver (Ag)", 
                               "Nickel-plated"
                           ],
                           "Precision_ThinFilm": [
                               "Gold (Au)", 
                               "100% Matte Tin (Sn)", 
                               "Sn/Pb (63/37)", 
                               "Palladium-Silver"
                           ]
                       }
                   }
               ]
            }
        ]
      },

    # ==============================================================================
    # 2. CAPACITOR (FINAL FULL VERSION) חלק2
    # ==============================================================================    
    "CAPACITOR": {
        "archetypes": [
            "Ceramic_MLCC", 
            "Electrolytic_Alum", 
            "Electrolytic_Polymer",
            "Tantalum_Solid",
            "Tantalum_Polymer",
            "Film_Polyester",
            "Film_Polypropylene",
            "Supercapacitor"
        ],
    
    # --- TABLE 1: ABSOLUTE MAXIMUM RATINGS ---
    "ABS_MAX": [
        {
            "key": "rated_voltage",
            "symbol": "V<sub>R</sub>",
            "spec_type": "max_rating",
            "column_model": "MAX_ONLY",
            "engineering_class": "SAFETY_LIMIT",
            "special_semantics": "NONE",
            "llm_context": {"formal_name": "Rated Voltage", "aliases": ["V_R (Rated DC Voltage) [V]", "Working Voltage V_W [V] DC Continuous", "Rated DC Voltage V_R – Do Not Exceed", "V_R [V] DC (Max. Continuous Working Voltage)", "Rated Voltage V_DC [V] (Derate Above T_rated)", "Max. Cont. DC Voltage V_R [V] (See Derating Curve)", "Nominal DC Working Voltage [V] (V_R)", "V(R) – DC Rated Voltage (Ref. IEC 60384)", "WVDC [V] – Working Voltage DC (Continuous)"]},
            "possible_units": ["V", "kV"],
            "std_unit": "V",
            "scenarios": [{"condition": "DC", "limits": {
                "Ceramic_MLCC": [6.3, 10, 16, 25, 50, 100], 
                "Electrolytic_Alum": [6.3, 10, 16, 25, 35, 50, 63, 100],
                "Electrolytic_Polymer": [2.5, 6.3, 16, 25],
                "Tantalum_Solid": [4, 6.3, 10, 16, 25, 35],
                "Tantalum_Polymer": [2.5, 6.3, 10, 16],
                "Film_Polyester": [50, 63, 100, 250, 400, 630],
                "Film_Polypropylene": [250, 400, 630, 1000],
                "Supercapacitor": [2.7, 3.0, 5.5]
            }}]
        },
        {
            "key": "surge_voltage",
            "symbol": "V<sub>S</sub>",
            "spec_type": "max_rating",
            "column_model": "MAX_ONLY",
            "engineering_class": "SAFETY_LIMIT",
            "special_semantics": "NONE",
            "llm_context": {"formal_name": "Surge Voltage", "aliases": ["V_S (Surge / Peak Voltage) [V]", "Peak Voltage V_peak [V] (Non-Repetitive)", "V_surge [V] – Short-Term Peak (Max.)", "Surge Voltage V_S = 1.3 × V_R (Typical Rule)", "V(S) Peak [V] (Single Event, Limited Duration)", "Peak Working Voltage V_pk [V] (Max., See Note)", "Transient Voltage V_surge [V] (Max. Non-Rep.)", "Max. Peak Voltage [V] (Surge, Non-Continuous)"]},
            "possible_units": ["V"],
            "std_unit": "V",
            "scenarios": [{"condition": "Non-repetitive, T_A=25°C", "limits": {
                "Ceramic_MLCC": [15, 25, 40, 75, 150],
                "Electrolytic_Alum": [8, 13, 20, 32, 44, 79],
                "Electrolytic_Polymer": [3, 8, 20, 31],
                "Tantalum_Solid": [5, 8, 13, 20, 31, 44],
                "Tantalum_Polymer": [3, 8, 13, 20],
                "Film_Polyester": [63, 79, 125, 312, 500, 787],
                "Film_Polypropylene": [312, 500, 787, 1250],
                "Supercapacitor": [2.8, 3.1, 5.8]
            }}]
        },
        {
            "key": "operating_temp_range",
            "symbol": "T<sub>op</sub>",
            "spec_type": "operational_range",
            "column_model": "MIN_MAX",
            "engineering_class": "OPERATING_CONDITION",
            "special_semantics": "NONE",
            "llm_context": {"formal_name": "Operating Temperature Range", "aliases": ["T_op (Operating Temp. Range) [°C]", "Op. Temp. Range T_min / T_max [°C]", "Category Temp. Range [°C] (Lower / Upper)", "Temperature Range (Operating) [°C]: Low to High", "Operating Ambient Temp. Range [°C] (IEC 60068)"]},
            "possible_units": ["°C"],
            "std_unit": "°C",
            "scenarios": [{"condition": "Standard", "limits": {
                "Ceramic_MLCC": [[-55, 125]],
                "Electrolytic_Alum": [[-40, 105]],
                "Electrolytic_Polymer": [[-55, 105]],
                "Tantalum_Solid": [[-55, 125]],
                "Tantalum_Polymer": [[-55, 105]],
                "Film_Polyester": [[-55, 105], [-55, 125]],
                "Film_Polypropylene": [[-55, 105]],
                "Supercapacitor": [[-40, 70]]
            }}]
        }
    ],
    
    # --- TABLE 2: ELECTRICAL CHARACTERISTICS (STATIC) ---
    "ELEC_CHAR": [
        {
            "key": "capacitance",
            "symbol": "C",
            "spec_type": "nominal",
            "column_model": "TYP_ONLY",
            "engineering_class": "NOMINAL_PARAMETER",
            "special_semantics": "NONE",
            "llm_context": {"formal_name": "Nominal Capacitance", "aliases": ["Nominal Capacitance C_nom [µF] ±Tol%", "C [nF] Nominal – EIA/IEC Standard Value", "Capacitance [pF/nF/µF]"]},
            "possible_units": ["µF", "nF", "pF", "F"],
            "std_unit": "µF",
            "scenarios": [{"condition": "1kHz, 25°C", "limits": {
                "Ceramic_MLCC": [0.1, 1, 10, 22],
                "Electrolytic_Alum": [10, 47, 100, 470, 1000],
                "Electrolytic_Polymer": [10, 47, 100, 330],
                "Tantalum_Solid": [1, 10, 47, 100],
                "Tantalum_Polymer": [10, 47, 150, 330],
                "Film_Polyester": [0.01, 0.1, 0.47, 1.0, 2.2, 4.7],
                "Film_Polypropylene": [0.01, 0.1, 1.0],
                "Supercapacitor": [1000000, 5000000]
            }}]
        },
        {
            "key": "capacitance_tolerance",
            "symbol": "Tol",
            "spec_type": "nominal",
            "column_model": "TYP_ONLY",
            "engineering_class": "NOMINAL_PARAMETER",
            "special_semantics": "NONE",
            "llm_context": {"formal_name": "Capacitance Tolerance", "aliases": ["C Tolerance – EIA Letter Code (e.g., K=±10%)", "±Cap. Tol. [%] (Before Aging / Load Life)", "Tolerance (Cap.) [%] – J=±5%, K=±10%, M=±20%", "ΔC/C [%] Initial (Measured, Low-Level AC Signal)", "Tol [%] (Capacitance, Initial; Excl. Temp. & Aging)"]},
            "possible_units": ["%"],
            "std_unit": "%",
            "scenarios": [{"condition": "Standard", "limits": {
                "Ceramic_MLCC": ["±10%", "±20%"],
                "Electrolytic_Alum": ["±20%"],
                "Electrolytic_Polymer": ["±20%"],
                "Tantalum_Solid": ["±10%", "±20%"],
                "Tantalum_Polymer": ["±20%"],
                "Film_Polyester": ["±5%", "±10%"],
                "Film_Polypropylene": ["±5%"],
                "Supercapacitor": ["-20%/+80%"]
            }}]
        },
        {
            "key": "leakage_current",
            "symbol": "I<sub>leak</sub>",
            "spec_type": "max_limit",
            "column_model": "MAX_ONLY",
            "engineering_class": "PERFORMANCE_LIMIT",
            "special_semantics": "NONE",
            "llm_context": {"formal_name": "Leakage Current", "aliases": ["DC Leakage Current DCL [µA]", "Leakage Current I_L [µA] Max.", "DCL [µA] Max. (Measured After 2 Min. Charge)", "DC Leakage I_DC [µA] Max. @ Rated Voltage", "Max. DCL [µA] (See Formula: I ≤ 0.01CV or 3µA)", "DCL Max. [µA] (Electrolytic, Measured @ V_R)"]},
            "possible_units": ["µA"],
            "std_unit": "µA",
            "scenarios": [{"condition": "At rated voltage", "limits": {
                "Ceramic_MLCC": [0], # Not applicable (use IR)
                "Electrolytic_Alum": [3, 10, 50],
                "Electrolytic_Polymer": [50, 100],
                "Tantalum_Solid": [0.5, 1, 5],
                "Tantalum_Polymer": [10, 50],
                "Film_Polyester": [0], # Not applicable (use IR)
                "Film_Polypropylene": [0], # Not applicable (use IR)
                "Supercapacitor": [10, 50]
            }}]
        },
        {
            "key": "insulation_resistance",
            "symbol": "R<sub>ins</sub>",
            "spec_type": "min_limit",
            "column_model": "MIN_ONLY",
            "engineering_class": "PERFORMANCE_LIMIT",
            "special_semantics": "NONE",
            "llm_context": {"formal_name": "Insulation Resistance", "aliases": ["R_ins (IR) [GΩ]", "Insulation Resistance IR [GΩ] Min.", "IR [MΩ] Min.", "R_insulation [GΩ] (Min., After 1 Min. Electrification)", "IR Min. [GΩ] – or – CR ≥ ? [MΩ·µF]", "Insulation Res. [GΩ] (or CR Product, MΩ·µF)", "Insulation Resistance R_ins ≥ ? GΩ or ? MΩ·µF"]},
            "possible_units": ["GΩ", "MΩ"],
            "std_unit": "GΩ",
            "scenarios": [{"condition": "At rated voltage", "limits": {
                "Ceramic_MLCC": [10, 100],
                "Electrolytic_Alum": [0],
                "Electrolytic_Polymer": [0],
                "Tantalum_Solid": [0],
                "Tantalum_Polymer": [0],
                "Film_Polyester": [3.75, 7.5, 15, 30],
                "Film_Polypropylene": [30, 100],
                "Supercapacitor": [0]
            }}]
        }
    ],

    # --- TABLE 3: DYNAMIC CHARACTERISTICS ---
    "DYNAMIC_CHAR": [
        {
            "key": "esr",
            "symbol": "ESR",
            "spec_type": "max_limit",
            "column_model": "TYP_MAX",
            "engineering_class": "PERFORMANCE_LIMIT",
            "special_semantics": "NONE",
            "llm_context": {"formal_name": "Equivalent Series Resistance", "aliases": ["ESR [mΩ]", "Equiv. Series Resistance ESR [mΩ] Typ.", "ESR (mΩ) Max.", "R_S (ESR) [mΩ] Typ./Max.", "Series Resistance ESR [Ω]", "Equivalent Series Res. R_ESR [mΩ] Typ.", "ESR – Key Ripple Current Parameter", "R_eq(series) [mΩ] (See Ripple Current Rating)"]},
            "possible_units": ["mΩ", "Ω"],
            "std_unit": "mΩ",
            "scenarios": [{"condition": "100kHz", "limits": {
                "Ceramic_MLCC": [2, 10],
                "Electrolytic_Alum": [50, 200, 500],
                "Electrolytic_Polymer": [10, 25, 40],
                "Tantalum_Solid": [100, 500, 1500],
                "Tantalum_Polymer": [25, 45, 60],
                "Film_Polyester": [15, 30, 60],
                "Film_Polypropylene": [5, 10, 20],
                "Supercapacitor": [30, 50, 100]
            }}]
        },
        {
            "key": "dissipation_factor",
            "symbol": "tan δ",
            "spec_type": "max_limit",
            "column_model": "TYP_MAX",
            "engineering_class": "PERFORMANCE_LIMIT",
            "special_semantics": "NONE",
            "llm_context": {"formal_name": "Dissipation Factor", "aliases": ["tan δ [%] (DF)", "Dissipation Factor DF [%] Max.", "tan δ Max. [%] – Loss Tangent", "Loss Tangent tan δ [%]", "Dielectric Loss Angle tan δ [%]", "D [%] Dissipation Factor (tan δ)"]},
            "possible_units": ["%"],
            "std_unit": "%",
            "scenarios": [{"condition": "1kHz", "limits": {
                "Ceramic_MLCC": [2.5, 5],
                "Electrolytic_Alum": [10, 20],
                "Electrolytic_Polymer": [10, 12],
                "Tantalum_Solid": [6, 8],
                "Tantalum_Polymer": [8, 10],
                "Film_Polyester": [0.8, 1.0],
                "Film_Polypropylene": [0.1],
                "Supercapacitor": [0]
            }}]
        },
        {
            "key": "impedance",
            "symbol": "Z",
            "spec_type": "max_limit",
            "column_model": "TYP_MAX",
            "engineering_class": "PERFORMANCE_LIMIT",
            "special_semantics": "NONE",
            "llm_context": {"formal_name": "Impedance", "aliases": ["|Z| [mΩ]", "Impedance Z [mΩ] Max.", "Z [mΩ] Typ./Max. (Magnitude)", "Impedance |Z| [mΩ]", "Impedance Magnitude [mΩ]", "Total Impedance |Z| [Ω] (See Fig. Freq. vs Z)"]},
            "possible_units": ["mΩ"],
            "std_unit": "mΩ",
            "scenarios": [{"condition": "100kHz", "limits": {
                "Ceramic_MLCC": [5, 20],
                "Electrolytic_Alum": [50, 300],
                "Electrolytic_Polymer": [15, 40],
                "Tantalum_Solid": [200, 1000],
                "Tantalum_Polymer": [40, 80],
                "Film_Polyester": [20, 50],
                "Film_Polypropylene": [10, 30],
                "Supercapacitor": [100]
            }}]
        },
        {
            "key": "self_resonant_freq",
            "symbol": "SRF",
            "spec_type": "nominal",
            "column_model": "MIN_TYP",
            "engineering_class": "PERFORMANCE_LIMIT",
            "special_semantics": "NONE",
            "llm_context": {"formal_name": "Self Resonant Frequency", "aliases": ["SRF [MHz] – Self-Resonant Frequency (Typical)", "f_res (SRF) [MHz] Typ. (C & ESL Dependent)", "Self-Resonant Freq. f_SRF [MHz] Min. Typ.", "SRF [MHz] (Above This Freq., Becomes Inductive)", "Resonant Frequency f_r [MHz] (LC Resonance)", "f_SRF [MHz] Min. (Cap. Usable Below SRF Only)", "Self Resonance f_0 [MHz] (ESL & C Interaction)", "Resonant Freq. [MHz] (See Impedance vs Freq. Curve)"]},
            "possible_units": ["MHz"],
            "std_unit": "MHz",
            "scenarios": [{"condition": "", "limits": {
                "Ceramic_MLCC": [10, 50, 100],
                "Electrolytic_Alum": [0.1, 1],
                "Electrolytic_Polymer": [1, 5],
                "Tantalum_Solid": [1, 10],
                "Tantalum_Polymer": [5, 20],
                "Film_Polyester": [5, 15, 30],
                "Film_Polypropylene": [10, 40],
                "Supercapacitor": [0]
            }}]
        }
    ],

    # --- TABLE 4: RELIABILITY ---
    "RELIABILITY": [
        {
            "key": "rated_lifetime",
            "symbol": "L<sub>rated</sub>",
            "spec_type": "min_limit",
            "column_model": "MIN_ONLY",
            "engineering_class": "RELIABILITY",
            "special_semantics": "NONE",
            "llm_context": {"formal_name": "Rated Lifetime", "aliases": ["L_rated (Rated Lifetime) [h]", "Load Life [h] Min. (Rated Temp. & Voltage)", "Useful Life [hours] Min. @ Rated Conditions", "Endurance [h] (Min., Full V_R)", "Rated Life L_H [h]", "Life Rating [h] Min. (Continuous)", "Load Life Test [hours] – Rated Temp. & Voltage", "L_0 [h] Rated Lifetime (See Lifetime Calculation)", "Operational Lifetime [h] Min."]},
            "possible_units": ["hours"],
            "std_unit": "hours",
            "scenarios": [{"condition": "At rated temp", "limits": {
                "Ceramic_MLCC": [1000],
                "Electrolytic_Alum": [2000, 5000],
                "Electrolytic_Polymer": [2000, 5000],
                "Tantalum_Solid": [1000],
                "Tantalum_Polymer": [1000],
                "Film_Polyester": [1000, 2000, 5000],
                "Film_Polypropylene": [30000, 100000],
                "Supercapacitor": [1000]
            }}]
        },
        {
            "key": "capacitance_drift",
            "symbol": "ΔC/C",
            "spec_type": "max_limit",
            "column_model": "MAX_ONLY",
            "engineering_class": "RELIABILITY",
            "special_semantics": "NONE",
            "llm_context": {"formal_name": "Capacitance Drift", "aliases": ["ΔC/C [%] Max. (After Load Life)", "Capacitance Change ΔC/C₀ [%] (Post Endurance)", "Cap. Drift ΔC/C [%] Max.", "ΔC/C [%] Stability (After Load Life Test, Max.)", "Capacitance Drift (%) Max. @ End of Rated Life", "Long-Term Cap. Stability ΔC/C [%]", "Capacitance Change After Endurance ΔC/C ≤ ±?%", "ΔC/C [%] (Post Load Life; Ref. IEC 60384)"]},
            "possible_units": ["%"],
            "std_unit": "%",
            "scenarios": [{"condition": "1000 hours", "limits": {
                "Ceramic_MLCC": [1, 2],
                "Electrolytic_Alum": [10, 20],
                "Electrolytic_Polymer": [5],
                "Tantalum_Solid": [1],
                "Tantalum_Polymer": [1],
                "Film_Polyester": [2, 5],
                "Film_Polypropylene": [0.5, 1],
                "Supercapacitor": [20]
            }}]
        },
        {
            "key": "moisture_sensitivity",
            "symbol": "MSL",
            "spec_type": "nominal",
            "column_model": "TYP_ONLY",
            "engineering_class": "RELIABILITY",
            "special_semantics": "NOT_APPLICABLE",
            "llm_context": {"formal_name": "Moisture Sensitivity Level", "aliases": ["MSL (JEDEC J-STD-020)", "Moisture Sensitivity Level MSL [1-6]", "MSL Rating per JEDEC J-STD-020E", "Moisture Sensitivity (MSL Class, Floor Life)", "MSL Level (J-STD-020, Reflow Process)", "Moisture Sensitivity – IPC/JEDEC J-STD-020", "MSL (SMD Only; N/A for THT Parts)", "Moisture Sensitivity Rating MSL (JEDEC Std.)", "MSL Category (1=Unlimited Floor Life…)", "Moisture Sensitivity (MSL) per J-STD-020 Rev. E"]},
            "possible_units": [""],
            "std_unit": "",
            "scenarios": [{"condition": "J-STD-020", "limits": {
                "Ceramic_MLCC": ["1"],
                "Electrolytic_Alum": [0], # N/A for THT
                "Electrolytic_Polymer": ["3"],
                "Tantalum_Solid": ["1"],
                "Tantalum_Polymer": ["3"],
                "Film_Polyester": [0],
                "Film_Polypropylene": [0],
                "Supercapacitor": [0]
            }}]
        }
    ],

    # --- TABLE 5: PACKAGE ---
    "PACKAGE": [
        {
            "key": "package_code",
            "symbol": "PKG",
            "spec_type": "mechanical",
            "column_model": "TYP_ONLY",
            "engineering_class": "MECHANICAL",
            "special_semantics": "NONE",
            "llm_context": {"formal_name": "Package Code", "aliases": ["PKG / Case Size (EIA Code)", "Case / Package Code (e.g., 0805, Case_A)", "Form Factor – EIA / IEC Size Code", "Package Style (SMD Chip / Radial THT / Coin)", "Size Code [EIA-198] (e.g., '0603' = 1.6×0.8mm)", "Component Package – Case Outline (SMD/THT)", "PKG Code (Chip Size or Can Diameter Code)", "Pkg. Type – MLCC Size / Electrolytic Can / Radial", "Body Size Code (EIA / JEDEC / IEC)", "Package / Case (e.g., Radial 8mm, SMD 7343, Case B)"]},
            "possible_units": [""],
            "std_unit": "",
            "scenarios": [{"condition": "N/A", "limits": {
                "Ceramic_MLCC": ["0402", "0603", "0805", "1206"],
                "Electrolytic_Alum": ["Radial_6.3mm", "Radial_8mm", "Radial_10mm"],
                "Electrolytic_Polymer": ["SMD_7343"],
                "Tantalum_Solid": ["Case_A", "Case_B"],
                "Tantalum_Polymer": ["Case_D"],
                "Film_Polyester": ["Radial_5mm", "Radial_7.5mm", "Radial_10mm"],
                "Film_Polypropylene": ["Radial_15mm", "Radial_22.5mm"],
                "Supercapacitor": ["Coin_Type", "Radial_Lead"]
            }}]
        },
        {
            "key": "lead_spacing",
            "symbol": "LS",
            "spec_type": "mechanical",
            "column_model": "TYP_ONLY",
            "engineering_class": "MECHANICAL",
            "special_semantics": "NONE",
            "llm_context": {"formal_name": "Lead Spacing", "aliases": ["LS (Lead Spacing / Pitch) [mm]", "Lead Pitch P [mm] Nominal (PCB Drill Centers)", "Pin Spacing [mm] (Center-to-Center, Nominal)", "Lead Spacing LS [mm] (Radial, Nominal)", "Pitch P [mm] – Lead-to-Lead (Nominal, ±0.5mm)", "Terminal Spacing [mm] (Ref. PCB Land Pattern)", "Lead Distance [mm] Nom. (Drill Hole Spacing)", "Pin Pitch [mm] (THT, Radial; N/A for SMD)", "LS [mm] Nominal (Center-to-Center, Radial Lead)", "Lead Separation [mm] Nom. (See Mechanical Dwg.)"]},
            "possible_units": ["mm"],
            "std_unit": "mm",
            "scenarios": [{"condition": "", "limits": {
                "Ceramic_MLCC": 0,
                "Electrolytic_Alum": [2.5, 3.5, 5.0],
                "Electrolytic_Polymer": 0,
                "Tantalum_Solid": 0,
                "Tantalum_Polymer": 0,
                "Film_Polyester": [5.0, 7.5, 10.0],
                "Film_Polypropylene": [15.0, 22.5],
                "Supercapacitor": [5.0]
            }}]
        },
        {
            "key": "polarization",
            "symbol": "POL",
            "spec_type": "mechanical",
            "column_model": "TYP_ONLY",
            "engineering_class": "MECHANICAL",
            "special_semantics": "NONE",
            "llm_context": {"formal_name": "Polarization", "aliases": ["POL (Polarity) – Polar / Non-Polar", "Polarization – Observe Correct Polarity (Polar)", "Polarity (POL): Polar = Yes / No", "Polar / Non-Polarized (See Marking on Component)", "Polarization Type (Polar: + Lead Marked)", "POL – Positive Terminal Identified by Marking", "Polarity: Unipolar (Polar) / Bipolar (Non-Polar)", "Polarization (Polar = Observe +/- ; Non-Polar = N/A)", "Polarity [Polar / Non-Polar] (CAUTION: Reverse = Failure)", "POL: Polar (Electrolytic/Ta) or Non-Polar (Ceramic/Film)"]},
            "possible_units": [""],
            "std_unit": "",
            "scenarios": [{"condition": "N/A", "limits": {
                "Ceramic_MLCC": ["Non-Polar"],
                "Electrolytic_Alum": ["Polar"],
                "Electrolytic_Polymer": ["Polar"],
                "Tantalum_Solid": ["Polar"],
                "Tantalum_Polymer": ["Polar"],
                "Film_Polyester": ["Non-Polar"],
                "Film_Polypropylene": ["Non-Polar"],
                "Supercapacitor": ["Polar"]
  
                            }
                          } 
                         ]
        }
    ]
    },

    # ==============================================================================
    # 3. DIODE חלק3
    # ==============================================================================
    "DIODE": {
    "archetypes": [
        "Signal_Small_Signal",      # 1N4148, 1N914, BAV70
        "Power_Rectifier",          # 1N4001-1N4007, 1N5400 series
        "Schottky_Barrier",         # 1N5817-1N5819, SS14-SS54, MBRS series
        "Fast_Recovery",            # UF4001-UF4007, RHRP series
        "Ultra_Fast_Recovery",      # MUR series, STTH series
        "Zener",                    # 1N47xx series, BZX series
        "TVS_Transient",            # SMAJ, P6KE, 1.5KE series
        "Switching",                # High-speed switching diodes
        "PIN_Diode",                # RF switching, attenuators
        "Avalanche"                 # High voltage, avalanche rated
    ],
    
    # ==========================================================================
    # ABSOLUTE MAXIMUM RATINGS
    # ==========================================================================
    "ABS_MAX": [
        {
            "key": "reverse_voltage",
            "symbol": "V<sub>RRM</sub>",
            "spec_type": "max_rating",
            "column_model": "MAX_ONLY",
            "engineering_class": "SAFETY_LIMIT",
            "special_semantics": "NONE",
            "llm_context": {
                "formal_name": "Repetitive Peak Reverse Voltage",
                "aliases": ["V_RRM (Repetitive Peak Reverse Voltage) [V]", "VRRM [V] – Max. Repetitive Reverse Voltage", "PRV [V] (Peak Reverse Voltage, Max.)", "Max. Reverse Voltage V_R [V] (Repetitive Peak)", "Repetitive Peak Reverse V_RRM [V] (Do Not Exceed)", "Peak Reverse Blocking Voltage [V] V_RRM", "VRRM [V] Max. (Repetitive, See Derating for Temp.)"]
            },
            "possible_units": ["V", "kV"],
            "std_unit": "V",
            "scenarios": [
                {
                    "condition": "Tj=25°C",
                    "limits": {
                        "Signal_Small_Signal": [50, 75, 100, 200, 300],
                        "Power_Rectifier": [50, 100, 200, 400, 600, 800, 1000, 1200, 1500],
                        "Schottky_Barrier": [15, 20, 30, 40, 45, 60, 100, 150, 200],
                        "Fast_Recovery": [200, 400, 600, 800, 1000, 1200],
                        "Ultra_Fast_Recovery": ["1", "2"],
                        "Zener": ["1", "2"],
                        "TVS_Transient": ["1", "2"],
                        "Switching": ["1"],
                        "PIN_Diode": ["1", "2"],
                        "Avalanche": ["2", "3"]
                    }
                }
            ]
        },
        {
            "key": "esd_rating",
            "symbol": "V<sub>ESD</sub>",
            "spec_type": "min_limit",
            "column_model": "MIN_ONLY",
            "engineering_class": "RELIABILITY",
            "special_semantics": "NONE",
            "llm_context": {
                "formal_name": "ESD Withstand Voltage",
                "aliases": ["V_ESD (HBM) [V] – Human Body Model", "ESD Rating V_ESD [kV] (HBM, ANSI/ESDA/JEDEC JS-001)", "ESD Withstand Voltage [V] HBM per JS-001", "ESD Sensitivity (HBM) V_ESD [kV]", "ESD HBM Class [V] – ANSI/ESDA/JEDEC JS-001", "Electrostatic Discharge Withstand HBM [kV]", "ESD Withstand V [V] HBM (See Handling Caution)", "ESD HBM [kV] Min. (Per JEDEC JESD22-A114)"]
            },
            "possible_units": ["V", "kV"],
            "std_unit": "V",
            "scenarios": [
                {
                    "condition": "HBM per ANSI/ESDA/JEDEC JS-001",
                    "limits": {
                        "Signal_Small_Signal": [1000, 2000, 4000],
                        "Power_Rectifier": [1000, 2000],
                        "Schottky_Barrier": [1000, 2000],
                        "Fast_Recovery": [1000, 2000],
                        "Ultra_Fast_Recovery": [1000, 2000],
                        "Zener": [2000, 4000],
                        "TVS_Transient": [0],  # NOT_APPLICABLE - these ARE ESD protection
                        "Switching": [2000, 4000],
                        "PIN_Diode": [1000, 2000],
                        "Avalanche": [1000]
                    }
                }
            ]
        },
        {
            "key": "soldering_temp",
            "symbol": "T<sub>solder</sub>",
            "spec_type": "max_rating",
            "column_model": "MAX_ONLY",
            "engineering_class": "RELIABILITY",
            "special_semantics": "NONE",
            "llm_context": {
                "formal_name": "Maximum Soldering Temperature",
                "aliases": ["T_solder (Peak Reflow) [°C] Max.", "Max. Soldering Temp. T_sol [°C]", "T_SOLDER Max [°C] – Wave / Reflow", "Soldering Temperature T_S [°C] Max. (Lead-Free)", "Max. Solder Temp (°C) Iron Tip / Reflow Peak", "T_PEAK [°C] Max. (Reflow Soldering, J-STD-020)"]
            },
            "possible_units": ["°C"],
            "std_unit": "°C",
            "scenarios": [
                {
                    "condition": "Peak temperature, 10s max",
                    "limits": {
                        "Signal_Small_Signal": [260],
                        "Power_Rectifier": [260, 300],
                        "Schottky_Barrier": [260],
                        "Fast_Recovery": [260],
                        "Ultra_Fast_Recovery": [260],
                        "Zener": [260],
                        "TVS_Transient": [260],
                        "Switching": [260],
                        "PIN_Diode": [260],
                        "Avalanche": [300]
                    }
                }
            ]
        },
        {
            "key": "thermal_shock",
            "symbol": "ΔT",
            "spec_type": "min_limit",
            "column_model": "MIN_ONLY",
            "engineering_class": "RELIABILITY",
            "special_semantics": "NONE",
            "llm_context": {
                "formal_name": "Thermal Shock Test",
                "aliases": ["Thermal Shock ΔT [cycles]", "Thermal Cycle Endurance [cycles]", "ΔT Thermal Shock [cycles] Per MIL-STD-750", "Thermal Shock Withstand [cycles] (Condition B)", "Temp. Shock Test [cycles] – Per JESD22-A104", "Thermal Cycling Reliability [cycles] (Min.)", "Therm. Shock Test [cycles] Min. (Ref. MIL-STD-750, Meth. 1051)"]
            },
            "possible_units": ["cycles"],
            "std_unit": "cycles",
            "scenarios": [
                {
                    "condition": "-65°C to +150°C",
                    "limits": {
                        "Signal_Small_Signal": [1000],
                        "Power_Rectifier": [500, 1000],
                        "Schottky_Barrier": [1000],
                        "Fast_Recovery": [1000],
                        "Ultra_Fast_Recovery": [1000],
                        "Zener": [1000],
                        "TVS_Transient": [500],
                        "Switching": [1000],
                        "PIN_Diode": [500],
                        "Avalanche": [500]
                    }
                }
            ]
        },
        {
            "key": "surge_rating",
            "symbol": "N",
            "spec_type": "nominal",
            "column_model": "TYP_ONLY",
            "engineering_class": "RELIABILITY",
            "special_semantics": "NONE",
            "llm_context": {
                "formal_name": "Surge Current Rating Derating",
                "aliases": ["N (Surge Cycles) – Max. Allowable Surge Events", "Number of Surge Cycles N [cycles] (At I_FSM)", "Surge Life N [cycles] (Non-Repetitive)", "Surge Rating Derating N [cycles] (At Peak Surge)", "Surge Cycle Count N (Non-Rep. Peak Current)", "N [cycles] – Max. Allowable Surge Events", "Surge Life Expectancy [cycles]", "Number of Non-Repetitive Surge Pulses N (cycles)"]
            },
            "possible_units": ["cycles"],
            "std_unit": "cycles",
            "scenarios": [
                {
                    "condition": "At IFSM max",
                    "limits": {
                        "Signal_Small_Signal": [1000],
                        "Power_Rectifier": [1000, 10000],
                        "Schottky_Barrier": [1000],
                        "Fast_Recovery": [1000],
                        "Ultra_Fast_Recovery": [1000],
                        "Zener": [100],
                        "TVS_Transient": [100, 1000],
                        "Switching": [1000],
                        "PIN_Diode": [100],
                        "Avalanche": [10000]
                    }
                }
            ]
        }
    ],
    
    # ==========================================================================
    # TEST CONDITIONS & SPECIAL PARAMETERS
    # ==========================================================================
    "TEST_CONDITIONS": [
        {
            "key": "test_current_if",
            "symbol": "I<sub>F(test)</sub>",
            "spec_type": "nominal",
            "column_model": "TYP_ONLY",
            "engineering_class": "TEST_CONDITION",
            "special_semantics": "NONE",
            "llm_context": {
                "formal_name": "Forward Test Current for VF",
                "aliases": ["I_F(test) [A/mA] – Forward Current for V_F Measurement", "I_F(test) – Forward Bias Current (V_F Condition)", "Forward Test Current I_F(test) [A] (Specified for V_F)", "Forward Current Test Level [mA] (V_F Meas. Cond.)"]
            },
            "possible_units": ["A", "mA"],
            "std_unit": "A",
            "scenarios": [
                {
                    "condition": "For VF measurement",
                    "limits": {
                        "Signal_Small_Signal": [0.01, 0.05, 0.1, 0.15],
                        "Power_Rectifier": [1, 2, 5, 10],
                        "Schottky_Barrier": [1, 3, 5, 10],
                        "Fast_Recovery": [1, 5, 10],
                        "Ultra_Fast_Recovery": [1, 5, 10],
                        "Zener": [0.005, 0.01],
                        "TVS_Transient": [0.001],
                        "Switching": [0.01, 0.1],
                        "PIN_Diode": [0.01, 0.1],
                        "Avalanche": [1, 5]
                    }
                }
            ]
        },
        {
            "key": "test_current_iz",
            "symbol": "I<sub>ZT</sub>",
            "spec_type": "nominal",
            "column_model": "TYP_ONLY",
            "engineering_class": "TEST_CONDITION",
            "special_semantics": "NOT_APPLICABLE",
            "llm_context": {
                "formal_name": "Zener Test Current",
                "aliases": ["I_ZT [mA] – Zener Test Current for V_Z Meas.", "I_ZT – Test Current Condition for V_Z Spec.", "IZT [mA] (Specified Test Current, V_Z Measurement)", "I_ZT [mA] Zener Bias Current (V_Z Test Condition)", "I_Z(test) [mA] – Forward Bias for Zener Voltage Meas.", "Zener Current I_ZT (mA) for V_Z Characterization", "Test Condition I_ZT [mA] (V_Z Measurement Reference)"]
            },
            "possible_units": ["mA"],
            "std_unit": "mA",
            "scenarios": [
                {
                    "condition": "For VZ measurement",
                    "limits": {
                        "Signal_Small_Signal": [0],
                        "Power_Rectifier": [0],
                        "Schottky_Barrier": [0],
                        "Fast_Recovery": [0],
                        "Ultra_Fast_Recovery": [0],
                        "Zener": [5, 20, 50, 75, 100, 200],
                        "TVS_Transient": [0],
                        "Switching": [0],
                        "PIN_Diode": [0],
                        "Avalanche": [0]
                    }
                }
            ]
        },
        {
            "key": "test_voltage_vr",
            "symbol": "V<sub>R(test)</sub>",
            "spec_type": "nominal",
            "column_model": "TYP_ONLY",
            "engineering_class": "TEST_CONDITION",
            "special_semantics": "NONE",
            "llm_context": {
                "formal_name": "Reverse Test Voltage",
                "aliases": ["V_R(test) [V] – Reverse Bias for I_R / C_J Meas.", "Reverse Test Voltage V_R [V] (I_R Measurement Cond.)", "V_R(test) = ? V (Test Voltage for I_R & C_J)", "Test Voltage V_R [V] (Applied for Leakage / Cap. Meas.)", "Reverse Bias Test Level [V] (I_R & C_J Characterization)", "V_R(test) [V] – DC Reverse Bias (Leakage Test Cond.)", "V_R Test [V] (For I_R & C_J, Per Fig. Test Circuit)"]
            },
            "possible_units": ["V"],
            "std_unit": "V",
            "scenarios": [
                {
                    "condition": "For IR and CJ measurement",
                    "limits": {
                        "Signal_Small_Signal": [20, 50, 75],
                        "Power_Rectifier": [100, 200, 400, 600],
                        "Schottky_Barrier": [10, 20, 30, 40],
                        "Fast_Recovery": [200, 400, 600],
                        "Ultra_Fast_Recovery": [200, 400, 600],
                        "Zener": [1, 2],
                        "TVS_Transient": [5, 10, 15],
                        "Switching": [20, 50],
                        "PIN_Diode": [20, 50],
                        "Avalanche": [500, 1000]
                    }
                }
            ]
        },
        {
            "key": "test_frequency",
            "symbol": "f<sub>test</sub>",
            "spec_type": "nominal",
            "column_model": "TYP_ONLY",
            "engineering_class": "TEST_CONDITION",
            "special_semantics": "NONE",
            "llm_context": {
                "formal_name": "Test Frequency for Capacitance",
                "aliases": ["f_test [MHz] – Test Frequency for C_J Measurement", "Test Frequency f [MHz] (C_J / C_T Meas. Condition)", "f_test = ? MHz (For Junction Capacitance Meas.)", "Test Freq. f_test [kHz / MHz] (C_T Measurement)", "f_test [MHz] – Capacitance Measurement Frequency", "Test Frequency for Junction Cap. [MHz]"]
            },
            "possible_units": ["MHz", "kHz"],
            "std_unit": "MHz",
            "scenarios": [
                {
                    "condition": "For CJ measurement",
                    "limits": {
                        "Signal_Small_Signal": [1],
                        "Power_Rectifier": [1],
                        "Schottky_Barrier": [1],
                        "Fast_Recovery": [1],
                        "Ultra_Fast_Recovery": [1],
                        "Zener": [1],
                        "TVS_Transient": [1],
                        "Switching": [1],
                        "PIN_Diode": [0.001, 0.1, 1, 10],  # DC to GHz range
                        "Avalanche": [1]
                    }
                }
            ]
        },
        {
            "key": "configuration",
            "symbol": "CONFIG",
            "spec_type": "mechanical",
            "column_model": "TYP_ONLY",
            "engineering_class": "MECHANICAL",
            "special_semantics": "NONE",
            "llm_context": {
                "formal_name": "Diode Configuration",
                "aliases": ["CONFIG – Diode Circuit Configuration", "Circuit Configuration (e.g., Single, Dual CC, Bridge)", "Diode Config. (Single / Dual Common Cathode / Series)", "Configuration – Unidirectional / Bidirectional (TVS)", "Circuit Config (e.g., Common Cathode, Back-to-Back)", "Pkg. Config.: Single / Dual / Bridge / Center-Tap", "Internal Config. (Single, Dual-CA, Dual-CC, Series)", "Topology – See Internal Schematic (Single/Dual/Bridge)", "Configuration Code (e.g., CC=Common Cathode, CA=Common Anode)", "Internal Circuit Config.: Single / Dual / Bidirectional"]
            },
            "possible_units": [""],
            "std_unit": "",
            "scenarios": [
                {
                    "condition": "N/A",
                    "limits": {
                        "Signal_Small_Signal": ["Single", "Dual_Common_Cathode", "Dual_Common_Anode", "Dual_Series"],
                        "Power_Rectifier": ["Single", "Bridge", "Center_Tap"],
                        "Schottky_Barrier": ["Single", "Dual_Common_Cathode", "Dual_Common_Anode"],
                        "Fast_Recovery": ["Single", "Dual_Common_Cathode"],
                        "Ultra_Fast_Recovery": ["Single", "Dual_Common_Cathode"],
                        "Zener": ["Single", "Dual_Series", "Dual_Back_to_Back"],
                        "TVS_Transient": ["Unidirectional", "Bidirectional"],
                        "Switching": ["Single", "Dual_Series"],
                        "PIN_Diode": ["Single"],
                        "Avalanche": ["Single"]
                    }
                }
            ]
        },
        {
            "key": "clamping_voltage",
            "symbol": "V<sub>C</sub>",
            "spec_type": "max_limit",
            "column_model": "MAX_ONLY",
            "engineering_class": "PERFORMANCE_LIMIT",
            "special_semantics": "NOT_APPLICABLE",
            "llm_context": {
                "formal_name": "Maximum Clamping Voltage",
                "aliases": ["V_C (Max. Clamping Voltage) [V]", "V_C [V] Max. – TVS Clamp Voltage @ Peak Current", "Clamp Voltage V_clamp [V] (Max., I=I_PP)", "Maximum Clamp V [V] (V_C at Peak Pulse Current I_PP)", "TVS Clamping Voltage V_C [V] Max.", "V(C) Max [V] – Clamping Level at I_PP (Transient)"]
            },
            "possible_units": ["V"],
            "std_unit": "V",
            "scenarios": [
                {
                    "condition": "At IPP",
                    "limits": {
                        "Signal_Small_Signal": [0],
                        "Power_Rectifier": [0],
                        "Schottky_Barrier": [0],
                        "Fast_Recovery": [0],
                        "Ultra_Fast_Recovery": [0],
                        "Zener": [0],
                        "TVS_Transient": [9.2, 11.5, 17.0, 19.9, 24.4, 27.7, 38.9, 45.7, 58.1, 78.0, 106, 130, 167, 224, 300],
                        "Switching": [0],
                        "PIN_Diode": [0],
                        "Avalanche": [0]
                    }
                }
            ]
        },
        {
            "key": "reverse_recovery_time",
            "symbol": "t<sub>rr</sub>",
            "spec_type": "max_limit",
            "column_model": "TYP_MAX",
            "engineering_class": "PERFORMANCE_LIMIT",
            "special_semantics": "NEGLIGIBLE",
            "llm_context": {
                "formal_name": "Reverse Recovery Time",
                "aliases": ["t_rr [ns] (Reverse Recovery Time, Typ./Max.)", "Recovery Time t_rr [ns] (Per JESD26, Standard Test)", "t(rr) [ns] – Reverse Recovery", "Switching Time t_rr [µs/ns] (Max., Standard Conditions)", "t_rr [ns] Typ. Max. (Forward-to-Reverse Transition)", "t_RR [ns] (Max., Measured per Fig. Test Circuit)", "Reverse Recovery Time [ns] Typ./Max."]
            },
            "possible_units": ["ns", "µs"],
            "std_unit": "ns",
            "scenarios": [
                {
                    "condition": "IF=0.5A, IR=1A, IRR=0.25A",
                    "limits": {
                        "Signal_Small_Signal": [2, 4, 8, 10, 50],
                        "Power_Rectifier": [50, 100, 500, 1500, 3000, 5000],
                        "Schottky_Barrier": [0],
                        "Fast_Recovery": [35, 50, 75, 150, 250, 500],
                        "Ultra_Fast_Recovery": [15, 20, 25, 35, 50, 75],
                        "Zener": [100, 500],
                        "TVS_Transient": [0],
                        "Switching": [2, 4, 6, 10],
                        "PIN_Diode": [1000, 5000, 10000],
                        "Avalanche": [75, 150, 500]
                    }
                }
            ]
        },
        {
            "key": "reverse_recovery_charge",
            "symbol": "Q<sub>rr</sub>",
            "spec_type": "max_limit",
            "column_model": "TYP_MAX",
            "engineering_class": "PERFORMANCE_LIMIT",
            "special_semantics": "NEGLIGIBLE",
            "llm_context": {
                "formal_name": "Reverse Recovery Charge",
                "aliases": ["Q_rr [nC] (Reverse Recovery Charge, Typ./Max.)", "Recovery Charge Q_rr [nC] (Standard Test)", "Q_rr [µC] – Stored Charge (Reverse Recovery)", "Reverse Recovery Charge Q_rr [nC]", "Q(rr) [nC] Typ. Max. (Integral of i_rr(t))", "Stored Charge Q_rr (nC) (Forward-to-Reverse Switching)", "Q_rr [nC] Max. (Measured per Standard Test Circuit)", "Q_rr [nC] (Charge, Measured from I_R=0 to Tail)"]
            },
            "possible_units": ["nC", "µC"],
            "std_unit": "nC",
            "scenarios": [
                {
                    "condition": "Standard test",
                    "limits": {
                        "Signal_Small_Signal": [1, 2, 5],
                        "Power_Rectifier": [50, 100, 500, 1000, 5000],
                        "Schottky_Barrier": [0],
                        "Fast_Recovery": [20, 50, 100, 250, 500],
                        "Ultra_Fast_Recovery": [10, 20, 50, 100, 200],
                        "Zener": [50, 100],
                        "TVS_Transient": [0],
                        "Switching": [1, 2, 4],
                        "PIN_Diode": [0],
                        "Avalanche": [100, 500]
                    }
                }
            ]
        },
        {
            "key": "softness_factor",
            "symbol": "S",
            "spec_type": "nominal",
            "column_model": "TYP_ONLY",
            "engineering_class": "NOMINAL_PARAMETER",
            "special_semantics": "NOT_APPLICABLE",
            "llm_context": {
                "formal_name": "Softness Factor",
                "aliases": ["S (Softness Factor) – Recovery Softness Ratio", "Recovery Softness S = t_b / t_a (Dimensionless)", "Snappiness Factor S (t_fall / t_rise of i_RR)", "S Factor – Soft vs. Snap Recovery Indicator", "Softness Factor S = t_b/t_a (< 1 = Snappy, > 1 = Soft)", "Diode Softness S (Typ.) – See Recovery Waveform Fig.", "S [–] Recovery Softness (t_b/t_a Ratio, Standard Test)", "Softness S (Dimensionless) – Reverse Recovery Profile", "Snap / Soft Recovery Factor S = t_2/t_1", "S Factor (Softness) Typ. (Ref. Reverse Recovery Waveform)"]
            },
            "possible_units": [""],
            "std_unit": "",
            "scenarios": [
                {
                    "condition": "Standard",
                    "limits": {
                        "Signal_Small_Signal": [0],
                        "Power_Rectifier": [0.3, 0.5],
                        "Schottky_Barrier": [0],
                        "Fast_Recovery": [0.3, 0.4, 0.5],
                        "Ultra_Fast_Recovery": [0.2, 0.3],
                        "Zener": [0],
                        "TVS_Transient": [0],
                        "Switching": [0],
                        "PIN_Diode": [0],
                        "Avalanche": [0.4]
                    }
                }
            ]
        },
        {
            "key": "forward_recovery_voltage",
            "symbol": "V<sub>FR</sub>",
            "spec_type": "max_limit",
            "column_model": "TYP_MAX",
            "engineering_class": "PERFORMANCE_LIMIT",
            "special_semantics": "NOT_APPLICABLE",
            "llm_context": {
                "formal_name": "Forward Recovery Voltage",
                "aliases": ["V_FR [V] (Forward Recovery / Turn-On Overshoot)", "V_FR [V] Max. – Forward Recovery", "Forward Recovery V_FR [V] Typ./Max.", "V(FR) [V] – Forward Overshoot During Turn-On", "Forward Recovery Overshoot [V] Max. (See Test Fig.)", "V_FR [V] Typ. Max. (Forward Recovery, Standard di/dt)", "Turn-On Transient V_FR [V] (Measured per Test Circuit)", "V_FR(max) [V] – Fwd. Recovery Voltage"]
            },
            "possible_units": ["V"],
            "std_unit": "V",
            "scenarios": [
                {
                    "condition": "di/dt test",
                    "limits": {
                        "Signal_Small_Signal": [0],
                        "Power_Rectifier": [0],
                        "Schottky_Barrier": [0],
                        "Fast_Recovery": [1.5, 2.0, 2.5],
                        "Ultra_Fast_Recovery": [1.8, 2.2, 2.5],
                        "Zener": [0],
                        "TVS_Transient": [0],
                        "Switching": [0],
                        "PIN_Diode": [0],
                        "Avalanche": [2.0, 2.5]
                    }
                }
            ]
        },
        {
            "key": "junction_capacitance",
            "symbol": "C<sub>J</sub>",
            "spec_type": "max_limit",
            "column_model": "TYP_MAX",
            "engineering_class": "PERFORMANCE_LIMIT",
            "special_semantics": "NONE",
            "llm_context": {
                "formal_name": "Junction Capacitance",
                "aliases": ["C_J [pF] (Junction / Total Capacitance)", "Diode Capacitance C_J [pF] (Reverse Biased)", "C_T [pF] – Total Junction Cap.", "CJ [pF] – Measured Between Anode & Cathode @ V_R"]
            },
            "possible_units": ["pF", "nF"],
            "std_unit": "pF",
            "scenarios": [
                {
                    "condition": "VR=4V, f=1MHz",
                    "limits": {
                        "Signal_Small_Signal": [0.8, 1, 2, 4, 8, 10, 15],
                        "Power_Rectifier": [15, 30, 50, 100, 250, 500, 1000, 2500],
                        "Schottky_Barrier": [50, 100, 150, 250, 500, 1000, 1500, 2500],
                        "Fast_Recovery": [30, 50, 100, 250, 500],
                        "Ultra_Fast_Recovery": [25, 50, 100, 250, 500, 1000],
                        "Zener": [15, 50, 150, 500, 1000],
                        "TVS_Transient": [1000, 2000, 5000, 10000, 20000],
                        "Switching": [1, 2, 4],
                        "PIN_Diode": [0.5, 1, 2, 5],
                        "Avalanche": [100, 500, 1000]
                    }
                }
            ]
        },
        {
            "key": "series_resistance",
            "symbol": "R<sub>S</sub>",
            "spec_type": "max_limit",
            "column_model": "TYP_MAX",
            "engineering_class": "PERFORMANCE_LIMIT",
            "special_semantics": "NOT_APPLICABLE",
            "llm_context": {
                "formal_name": "Series Resistance",
                "aliases": ["R_S [Ω/mΩ] (Series / Bulk Resistance)", "Bulk Resistance R_S [mΩ] Typ./Max.", "Series Resistance R_s [Ω] (PIN / Schottky, Typ.)", "R_S [Ω] – Bulk/Series Resistance (Forward Biased)", "Series Resistance R_s [mΩ] Max. (At Rated Fwd. Current)", "Bulk Res. R_B [Ω] (PIN Diode, Series, RF Operation)", "R_S [Ω] Max. (Contact + Bulk Resistance, At I_F)"]
            },
            "possible_units": ["Ω", "mΩ"],
            "std_unit": "Ω",
            "scenarios": [
                {
                    "condition": "At rated IF",
                    "limits": {
                        "Signal_Small_Signal": [0],
                        "Power_Rectifier": [0],
                        "Schottky_Barrier": [10, 15, 20, 30, 50, 100],  # mΩ
                        "Fast_Recovery": [0],
                        "Ultra_Fast_Recovery": [0],
                        "Zener": [0],
                        "TVS_Transient": [0],
                        "Switching": [0],
                        "PIN_Diode": [0.5, 1, 2, 5, 10],
                        "Avalanche": [0]
                    }
                }
            ]
        },
        {
            "key": "isolation_resistance",
            "symbol": "R<sub>ISO</sub>",
            "spec_type": "min_limit",
            "column_model": "MIN_ONLY",
            "engineering_class": "PERFORMANCE_LIMIT",
            "special_semantics": "NOT_APPLICABLE",
            "llm_context": {
                "formal_name": "RF Isolation (Off State)",
                "aliases": ["R_ISO [kΩ] – Off-State RF Isolation", "RF Isolation R_ISO [MΩ] (Reverse Biased)", "Off Resistance R_ISO [kΩ] (PIN, V_R Applied)", "R_ISO Min. [kΩ] – PIN Diode Off-State", "RF Off Isolation [kΩ] (V_R Applied)", "Off-State Resistance R_ISO [kΩ] (RF Switch)", "R(ISO) Off-State [kΩ] Min. (PIN Diode, GHz Operation)", "Isolation Resistance R_OFF [MΩ] Min."]
            },
            "possible_units": ["kΩ", "MΩ"],
            "std_unit": "kΩ",
            "scenarios": [
                {
                    "condition": "VR applied, f=1GHz",
                    "limits": {
                        "Signal_Small_Signal": [0],
                        "Power_Rectifier": [0],
                        "Schottky_Barrier": [0],
                        "Fast_Recovery": [0],
                        "Ultra_Fast_Recovery": [0],
                        "Zener": [0],
                        "TVS_Transient": [0],
                        "Switching": [0],
                        "PIN_Diode": [1, 5, 10, 50],  # kΩ
                        "Avalanche": [0]
                    }
                }
            ]
        }
    ],
    
    # ==========================================================================
    # THERMAL CHARACTERISTICS
    # ==========================================================================
    "THERMAL_CHAR": [
        {
            "key": "thermal_resistance_jc",
            "symbol": "R<sub>θJC</sub>",
            "spec_type": "max_limit",
            "column_model": "TYP_MAX",
            "engineering_class": "NOMINAL_PARAMETER",
            "special_semantics": "NONE",
            "llm_context": {
                "formal_name": "Thermal Resistance Junction to Case",
                "aliases": ["R_θJC [°C/W] (Junction-to-Case, Steady State)", "Rth(j-c) [°C/W] Max. – Steady State", "Thermal Res. J-C θ_JC [°C/W] (Typ./Max.)", "R_TH(JC) [°C/W] Max. (J-to-Case, No Heat Sink)", "θ_JC [°C/W] – Junction to Case Thermal Resistance", "R(θJC) [K/W] Max. (Steady-State, Case = Cathode Tab)", "Junction-to-Case Therm. Res. [°C/W] R_θJC", "Rth J→C [°C/W] Max. (Steady State, Still Air)", "Thermal Impedance J-C [°C/W] R_TH(JC) Typ./Max.", "θ(JC) [°C/W] Max – Refer to Thermal Model (Fig. X)"]
            },
            "possible_units": ["°C/W"],
            "std_unit": "°C/W",
            "scenarios": [
                {
                    "condition": "Steady state",
                    "limits": {
                        "Signal_Small_Signal": [200, 300, 400, 500],
                        "Power_Rectifier": [0.5, 1, 1.5, 2, 3, 5, 10, 15, 20],
                        "Schottky_Barrier": [1, 2, 3, 5, 10, 15, 20],
                        "Fast_Recovery": [1, 2, 3, 5, 8, 10],
                        "Ultra_Fast_Recovery": [0.5, 1, 2, 3, 5, 8],
                        "Zener": [5, 10, 50, 100],
                        "TVS_Transient": [10, 20, 30, 50],
                        "Switching": [200, 300, 400],
                        "PIN_Diode": [50, 100, 200],
                        "Avalanche": [2, 5, 10, 20]
                    }
                }
            ]
        },
        {
            "key": "thermal_resistance_ja",
            "symbol": "R<sub>θJA</sub>",
            "spec_type": "max_limit",
            "column_model": "TYP_MAX",
            "engineering_class": "NOMINAL_PARAMETER",
            "special_semantics": "NONE",
            "llm_context": {
                "formal_name": "Thermal Resistance Junction to Ambient",
                "aliases": ["R_θJA [°C/W] (Junction-to-Ambient, Still Air)", "Rth(j-a) [°C/W] Max. – Standard PCB, Still Air", "Thermal Res. J-A θ_JA [°C/W] (Typ./Max.)", "R_TH(JA) [°C/W] Max. (PCB Mount, No Forced Air)", "θ_JA [°C/W] – Junction to Ambient (Free Convection)", "R(θJA) [K/W] Max. (Std. PCB, 1oz Cu, Still Air)", "Junction-to-Ambient Therm. Res. [°C/W] R_θJA", "Rth J→A [°C/W] Max. (FR4 PCB, No Heat Sink)", "θ(JA) [°C/W] Max – Standard PCB, Still Air (Fig. X)"]
            },
            "possible_units": ["°C/W"],
            "std_unit": "°C/W",
            "scenarios": [
                {
                    "condition": "Standard PCB, still air",
                    "limits": {
                        "Signal_Small_Signal": [300, 400, 500],
                        "Power_Rectifier": [20, 30, 40, 50, 60, 80, 100],
                        "Schottky_Barrier": [30, 40, 50, 60, 80, 100],
                        "Fast_Recovery": [30, 40, 50, 60],
                        "Ultra_Fast_Recovery": [25, 35, 45, 60],
                        "Zener": [50, 100, 200],
                        "TVS_Transient": [50, 70, 100],
                        "Switching": [300, 400],
                        "PIN_Diode": [150, 250],
                        "Avalanche": [40, 60, 80]
                    }
                }
            ]
        },
        {
            "key": "thermal_resistance_jl",
            "symbol": "R<sub>θJL</sub>",
            "spec_type": "max_limit",
            "column_model": "TYP_MAX",
            "engineering_class": "NOMINAL_PARAMETER",
            "special_semantics": "NOT_APPLICABLE",
            "llm_context": {
                "formal_name": "Thermal Resistance Junction to Lead",
                "aliases": ["R_θJL [°C/W] (Junction-to-Lead, Per Lead)", "Rth(j-l) [°C/W] – Junction to Lead Thermal Resistance", "Thermal Res. J-L θ_JL [°C/W] (Typ./Max.)", "R_TH(JL) [°C/W] Max. (Measured at Lead)", "θ_JL [°C/W] – Junction to Lead (Per Lead, Steady State)", "R(θJL) [K/W] Max. (Lead Solder Point Reference)", "Junction-to-Lead Therm. Res. [°C/W] R_θJL", "Rth J→L [°C/W] Max. (Standard Lead Condition)", "θ(JL) [°C/W] Max – Lead Temp. Measured at Solder Point", "R_TH(JL) [°C/W] (Per Lead, See Thermal Model Note)"]
            },
            "possible_units": ["°C/W"],
            "std_unit": "°C/W",
            "scenarios": [
                {
                    "condition": "Per lead",
                    "limits": {
                        "Signal_Small_Signal": [100, 150, 200],
                        "Power_Rectifier": [0],
                        "Schottky_Barrier": [0],
                        "Fast_Recovery": [0],
                        "Ultra_Fast_Recovery": [0],
                        "Zener": [25, 50],
                        "TVS_Transient": [0],
                        "Switching": [100, 150],
                        "PIN_Diode": [50, 100],
                        "Avalanche": [0]
                    }
                }
            ]
        },
        {
            "key": "transient_thermal_impedance",
            "symbol": "Z<sub>θJC</sub>",
            "spec_type": "nominal",
            "column_model": "TYP_ONLY",
            "engineering_class": "NOMINAL_PARAMETER",
            "special_semantics": "NONE",
            "llm_context": {
                "formal_name": "Transient Thermal Impedance",
                "aliases": ["Z_θJC [°C/W] (Transient, Various Pulse Widths)", "Thermal Impedance Z_th(JC) [°C/W] (Pulse Operation)", "Pulse Thermal Resistance Z_θJC [°C/W] (See Fig.)", "Z_TH(JC) [°C/W] – Transient (Refer to Thermal Impedance Curve)", "Transient Therm. Impedance Z(θJC) [°C/W] vs. t_p", "Z_θJC(t) [°C/W] (Function of Pulse Width t_p)", "Thermal Impedance (Transient) Z_JC [°C/W] (Fig. X)", "Z_TH(JC) [°C/W] – See Normalized Thermal Impedance Curve"]
            },
            "possible_units": ["°C/W"],
            "std_unit": "°C/W",
            "scenarios": [
                {
                    "condition": "Various pulse widths",
                    "limits": {
                        "Signal_Small_Signal": [50, 100, 200],
                        "Power_Rectifier": [0.3, 0.5, 1, 2, 5],
                        "Schottky_Barrier": [1, 2, 5, 10],
                        "Fast_Recovery": [1, 2, 5],
                        "Ultra_Fast_Recovery": [0.5, 1, 3],
                        "Zener": [5, 10, 50],
                        "TVS_Transient": [1, 5, 10],
                        "Switching": [100, 200],
                        "PIN_Diode": [20, 50],
                        "Avalanche": [2, 5, 10]
                    }
                }
            ]
        },
        {
            "key": "operating_junction_temp_range",
            "symbol": "T<sub>J</sub>",
            "spec_type": "operational_range",
            "column_model": "MIN_MAX",
            "engineering_class": "OPERATING_CONDITION",
            "special_semantics": "NONE",
            "llm_context": {
                "formal_name": "Operating Junction Temperature Range",
                "aliases": ["Operating Temp", "TJ Range"]
            },
            "possible_units": ["°C"],
            "std_unit": "°C",
            "scenarios": [
                {
                    "condition": "Operating",
                    "limits": {
                        "Signal_Small_Signal": [[-65, 150], [-65, 175]],
                        "Power_Rectifier": [[-65, 150], [-65, 175]],
                        "Schottky_Barrier": [[-65, 125], [-65, 150], [-65, 175]],
                        "Fast_Recovery": [[-65, 150], [-65, 175]],
                        "Ultra_Fast_Recovery": [[-65, 150], [-65, 175]],
                        "Zener": [[-65, 175], [-55, 175]],
                        "TVS_Transient": [[-65, 150], [-65, 175]],
                        "Switching": [[-65, 150], [-65, 175]],
                        "PIN_Diode": [[-65, 125], [-65, 150]],
                        "Avalanche": [[-65, 175]]
                    }
                }
            ]
        }
    ],
    
    # ==========================================================================
    # PACKAGE & MECHANICAL
    # ==========================================================================
    "PACKAGE": [
        {
            "key": "package_code",
            "symbol": "PKG",
            "spec_type": "mechanical",
            "column_model": "TYP_ONLY",
            "engineering_class": "MECHANICAL",
            "special_semantics": "NONE",
            "llm_context": {
                "formal_name": "Package Type",
                "aliases": ["Case Type", "Package Code", "Outline"]
            },
            "possible_units": [""],
            "std_unit": "",
            "scenarios": [
                {
                    "condition": "N/A",
                    "limits": {
                        "Signal_Small_Signal": ["SOD-323", "SOD-123", "SOT-23", "SOT-323", "SC-70", "DO-35", "DO-204"],
                        "Power_Rectifier": ["DO-41", "DO-201AD", "DO-214AC(SMA)", "DO-214AA(SMB)", "DO-214AB(SMC)", "R-6", "TO-220", "TO-220AB", "TO-247", "ITO-220", "D2PAK", "DPAK"],
                        "Schottky_Barrier": ["SOD-123", "DO-214AC(SMA)", "DO-214AA(SMB)", "DO-214AB(SMC)", "DO-201AD", "TO-220", "TO-220AB", "ITO-220", "D2PAK", "DPAK"],
                        "Fast_Recovery": ["DO-41", "DO-201AD", "DO-15", "TO-220", "TO-220AB", "TO-247", "DO-214AB(SMC)", "ITO-220", "D2PAK"],
                        "Ultra_Fast_Recovery": ["DO-41", "DO-201", "TO-220", "TO-220AB", "TO-247", "DO-214AB(SMC)", "ITO-220", "D2PAK", "TO-262"],
                        "Zener": ["SOD-123", "SOD-323", "SOT-23", "DO-35", "DO-41", "DO-201", "DO-214AC(SMA)", "DO-214AA(SMB)", "SMB"],
                        "TVS_Transient": ["DO-214AC(SMA)", "DO-214AA(SMB)", "DO-214AB(SMC)", "DO-201", "DO-15", "5KP", "P600"],
                        "Switching": ["SOD-323", "SOD-123", "SOT-23", "DO-35"],
                        "PIN_Diode": ["SOD-323", "SOT-23", "DO-35", "DO-7"],
                        "Avalanche": ["DO-201", "TO-220", "TO-247", "DO-214AB"]
                    }
                }
            ]
        },
        {
            "key": "mounting_type",
            "symbol": "MNT",
            "spec_type": "mechanical",
            "column_model": "TYP_ONLY",
            "engineering_class": "MECHANICAL",
            "special_semantics": "NONE",
            "llm_context": {
                "formal_name": "Mounting Type",
                "aliases": ["Mounting Style", "Mount"]
            },
            "possible_units": [""],
            "std_unit": "",
            "scenarios": [
                {
                    "condition": "N/A",
                    "limits": {
                        "Signal_Small_Signal": ["SMD", "Through_Hole"],
                        "Power_Rectifier": ["SMD", "Through_Hole", "Stud", "Chassis"],
                        "Schottky_Barrier": ["SMD", "Through_Hole", "Chassis"],
                        "Fast_Recovery": ["SMD", "Through_Hole", "Chassis"],
                        "Ultra_Fast_Recovery": ["SMD", "Through_Hole", "Chassis"],
                        "Zener": ["SMD", "Through_Hole"],
                        "TVS_Transient": ["SMD", "Through_Hole", "Chassis"],
                        "Switching": ["SMD", "Through_Hole"],
                        "PIN_Diode": ["SMD", "Through_Hole"],
                        "Avalanche": ["Through_Hole", "Chassis"]
                    }
                }
            ]
        },
        {
            "key": "polarity_marking",
            "symbol": "POL",
            "spec_type": "mechanical",
            "column_model": "TYP_ONLY",
            "engineering_class": "MECHANICAL",
            "special_semantics": "NONE",
            "llm_context": {
                "formal_name": "Polarity Marking",
                "aliases": ["Cathode Mark", "Polarity"]
            },
            "possible_units": [""],
            "std_unit": "",
            "scenarios": [
                {
                    "condition": "N/A",
                    "limits": {
                        "Signal_Small_Signal": ["Band", "Line"],
                        "Power_Rectifier": ["Band", "Symbol", "Stud"],
                        "Schottky_Barrier": ["Band", "Symbol"],
                        "Fast_Recovery": ["Band", "Symbol"],
                        "Ultra_Fast_Recovery": ["Band", "Symbol"],
                        "Zener": ["Band", "Line"],
                        "TVS_Transient": ["Band", "Bidirectional_None"],
                        "Switching": ["Band", "Line"],
                        "PIN_Diode": ["Band"],
                        "Avalanche": ["Band", "Symbol"]
                    }
                }
            ]
        },
        {
            "key": "lead_finish",
            "symbol": "FINISH",
            "spec_type": "mechanical",
            "column_model": "TYP_ONLY",
            "engineering_class": "MECHANICAL",
            "special_semantics": "NONE",
            "llm_context": {
                "formal_name": "Terminal Finish",
                "aliases": ["Lead Finish", "Plating", "Terminal Plating"]
            },
            "possible_units": [""],
            "std_unit": "",
            "scenarios": [
                {
                    "condition": "N/A",
                    "limits": {
                        "Signal_Small_Signal": ["Matte_Sn", "SnPb"],
                        "Power_Rectifier": ["Matte_Sn", "SnPb", "Solder_Dip"],
                        "Schottky_Barrier": ["Matte_Sn", "SnPb"],
                        "Fast_Recovery": ["Matte_Sn", "SnPb"],
                        "Ultra_Fast_Recovery": ["Matte_Sn", "SnPb"],
                        "Zener": ["Matte_Sn", "SnPb"],
                        "TVS_Transient": ["Matte_Sn", "SnPb"],
                        "Switching": ["Matte_Sn"],
                        "PIN_Diode": ["Au", "Matte_Sn"],
                        "Avalanche": ["Matte_Sn", "SnPb"]
                    }
                }
            ]
        },
        {
            "key": "weight",
            "symbol": "W",
            "spec_type": "mechanical",
            "column_model": "TYP_ONLY",
            "engineering_class": "MECHANICAL",
            "special_semantics": "NONE",
            "llm_context": {
                "formal_name": "Weight",
                "aliases": ["Mass", "Part Weight"]
            },
            "possible_units": ["g", "mg"],
            "std_unit": "g",
            "scenarios": [
                {
                    "condition": "",
                    "limits": {
                        "Signal_Small_Signal": [0.01, 0.02, 0.05, 0.1],
                        "Power_Rectifier": [0.5, 1, 2, 5, 10, 20, 50],
                        "Schottky_Barrier": [0.1, 0.5, 1, 2, 5, 10],
                        "Fast_Recovery": [0.5, 1, 2, 5, 10],
                        "Ultra_Fast_Recovery": [0.5, 1, 2, 5, 10, 20],
                        "Zener": [0.05, 0.1, 0.5, 1],
                        "TVS_Transient": [0.1, 0.5, 1, 5],
                        "Switching": [0.01, 0.05],
                        "PIN_Diode": [0.01, 0.05, 0.1],
                        "Avalanche": [1, 5, 10, 20]
                    }
                }
            ]
        }
    ],
    
    # ==========================================================================
    # RELIABILITY & QUALITY
    # ==========================================================================
    "RELIABILITY": [
        {
            "key": "failure_rate",
            "symbol": "λ",
            "spec_type": "max_limit",
            "column_model": "MAX_ONLY",
            "engineering_class": "RELIABILITY",
            "special_semantics": "NONE",
            "llm_context": {
                "formal_name": "Failure Rate",
                "aliases": ["FIT Rate", "Lambda", "MTBF"]
            },
            "possible_units": ["FIT", "PPM", "%/1000h"],
            "std_unit": "FIT",
            "scenarios": [
                {
                    "condition": "Standard conditions",
                    "limits": {
                        "Signal_Small_Signal": [0.1, 1, 5],
                        "Power_Rectifier": [1, 5, 10],
                        "Schottky_Barrier": [1, 5, 10],
                        "Fast_Recovery": [1, 5],
                        "Ultra_Fast_Recovery": [1, 5],
                        "Zener": [1, 5, 10],
                        "TVS_Transient": [1, 5],
                        "Switching": [0.1, 1],
                        "PIN_Diode": [0.5, 1],
                        "Avalanche": [5, 10]
                    }
                }
            ]
        },
        {
            "key": "moisture_sensitivity_level",
            "symbol": "MSL",
            "spec_type": "nominal",
            "column_model": "TYP_ONLY",
            "engineering_class": "RELIABILITY",
            "special_semantics": "NOT_APPLICABLE",
            "llm_context": {
                "formal_name": "Moisture Sensitivity Level",
                "aliases": ["MSL", "Moisture Level"]
            },
            "possible_units": [""],
            "std_unit": "",
            "scenarios": [
                {
                    "condition": "Per J-STD-020",
                    "limits": {
                        "Signal_Small_Signal": ["1", "2"],
                        "Power_Rectifier": ["1", "2", "3"],
                        "Schottky_Barrier": ["1", "2"],
                        "Fast_Recovery": ["1", "2"],
                        "Ultra_Fast_ode": [50, 100, 200],
                        "Avalanche": [1000, 1500, 2000, 3000, 5000]
                    }
                }
            ]
        },
        {
            "key": "working_reverse_voltage",
            "symbol": "V<sub>RWM</sub>",
            "spec_type": "max_rating",
            "column_model": "MAX_ONLY",
            "engineering_class": "SAFETY_LIMIT",
            "special_semantics": "NOT_APPLICABLE",  # Only for TVS diodes
            "llm_context": {
                "formal_name": "Working Peak Reverse Voltage",
                "aliases": ["Stand-off Voltage", "VRWM", "Working Voltage"]
            },
            "possible_units": ["V"],
            "std_unit": "V",
            "scenarios": [
                {
                    "condition": "Continuous",
                    "limits": {
                        "Signal_Small_Signal": [0],
                        "Power_Rectifier": [0],
                        "Schottky_Barrier": [0],
                        "Fast_Recovery": [0],
                        "Ultra_Fast_Recovery": [0],
                        "Zener": [0],
                        "TVS_Transient": [5, 6.8, 10, 12, 15, 17, 24, 28, 36, 51, 70, 85, 110, 150, 200],
                        "Switching": [0],
                        "PIN_Diode": [0],
                        "Avalanche": [0]
                    }
                }
            ]
        },
        {
            "key": "breakdown_voltage",
            "symbol": "V<sub>BR</sub>",
            "spec_type": "min_max_range",
            "column_model": "MIN_MAX",
            "engineering_class": "SAFETY_LIMIT",
            "special_semantics": "NOT_APPLICABLE",  # Only for TVS and Zener
            "llm_context": {
                "formal_name": "Breakdown Voltage",
                "aliases": ["VBR", "Clamping Voltage", "Avalanche Voltage"]
            },
            "possible_units": ["V"],
            "std_unit": "V",
            "scenarios": [
                {
                    "condition": "At test current",
                    "limits": {
                        "Signal_Small_Signal": [0],
                        "Power_Rectifier": [0],
                        "Schottky_Barrier": [0],
                        "Fast_Recovery": [0],
                        "Ultra_Fast_Recovery": [0],
                        "Zener": [[2.28, 2.52], [3.14, 3.47], [4.85, 5.36], [6.46, 7.14], [8.65, 9.56], [11.4, 12.6], [14.25, 15.75]],
                        "TVS_Transient": [[6.4, 7.1], [9.5, 10.5], [13.3, 14.7], [16.2, 17.9], [20.9, 23.1], [30.4, 33.6], [48.4, 53.6]],
                        "Switching": [0],
                        "PIN_Diode": [0],
                        "Avalanche": [[1050, 1150], [1550, 1650], [2050, 2150]]
                    }
                }
            ]
        },
        {
            "key": "forward_current",
            "symbol": "I<sub>F(AV)</sub>",
            "spec_type": "max_rating",
            "column_model": "MAX_ONLY",
            "engineering_class": "SAFETY_LIMIT",
            "special_semantics": "NONE",
            "llm_context": {
                "formal_name": "Average Rectified Forward Current",
                "aliases": ["Average Forward Current", "Rectified Current", "IF(AV)", "IO"]
            },
            "possible_units": ["A", "mA"],
            "std_unit": "A",
            "scenarios": [
                {
                    "condition": "Tc=specified",
                    "limits": {
                        "Signal_Small_Signal": [0.075, 0.1, 0.15, 0.2, 0.3, 0.5],
                        "Power_Rectifier": [1, 1.5, 2, 3, 5, 6, 10, 15, 20, 30, 40, 50],
                        "Schottky_Barrier": [0.5, 1, 2, 3, 5, 10, 15, 20, 30, 40],
                        "Fast_Recovery": [1, 2, 3, 5, 8, 10, 15, 20, 30],
                        "Ultra_Fast_Recovery": [1, 2, 4, 6, 8, 10, 15, 20, 30, 50],
                        "Zener": [0.5, 1, 5],
                        "TVS_Transient": [0],  # NOT_APPLICABLE - rated by pulse power
                        "Switching": [0.1, 0.15, 0.2, 0.5],
                        "PIN_Diode": [0.01, 0.1, 0.5],
                        "Avalanche": [0.5, 1, 2, 5]
                    }
                }
            ]
        },
        {
            "key": "peak_forward_current",
            "symbol": "I<sub>FSM</sub>",
            "spec_type": "max_rating",
            "column_model": "MAX_ONLY",
            "engineering_class": "SAFETY_LIMIT",
            "special_semantics": "NONE",
            "llm_context": {
                "formal_name": "Non-Repetitive Peak Forward Surge Current",
                "aliases": ["Surge Current", "Peak Forward Surge Current", "IFSM", "Surge Rating"]
            },
            "possible_units": ["A"],
            "std_unit": "A",
            "scenarios": [
                {
                    "condition": "8.3ms half-sine, Tj=25°C",
                    "limits": {
                        "Signal_Small_Signal": [0.5, 1, 2, 4, 5],
                        "Power_Rectifier": [30, 50, 70, 100, 150, 200, 300, 400, 500],
                        "Schottky_Barrier": [20, 30, 50, 75, 100, 150, 200, 300],
                        "Fast_Recovery": [30, 50, 75, 100, 150, 200, 300],
                        "Ultra_Fast_Recovery": [30, 50, 75, 100, 150, 200, 300, 400],
                        "Zener": [10, 25, 100],
                        "TVS_Transient": [0],  # NOT_APPLICABLE
                        "Switching": [1, 2, 4],
                        "PIN_Diode": [1, 5, 10],
                        "Avalanche": [10, 20, 50]
                    }
                }
            ]
        },
        {
            "key": "repetitive_peak_forward_current",
            "symbol": "I<sub>FRM</sub>",
            "spec_type": "max_rating",
            "column_model": "MAX_ONLY",
            "engineering_class": "SAFETY_LIMIT",
            "special_semantics": "NONE",
            "llm_context": {
                "formal_name": "Repetitive Peak Forward Current",
                "aliases": ["IFRM", "Repetitive Peak Current"]
            },
            "possible_units": ["A"],
            "std_unit": "A",
            "scenarios": [
                {
                    "condition": "Square wave",
                    "limits": {
                        "Signal_Small_Signal": [0.5, 0.75, 1],
                        "Power_Rectifier": [5, 10, 15, 30, 60, 100],
                        "Schottky_Barrier": [5, 10, 20, 30, 60, 100],
                        "Fast_Recovery": [5, 10, 20, 30, 60],
                        "Ultra_Fast_Recovery": [5, 10, 20, 40, 60],
                        "Zener": [2, 5],
                        "TVS_Transient": [0],
                        "Switching": [0.5, 1, 2],
                        "PIN_Diode": [0.1, 0.5],
                        "Avalanche": [2, 5, 10]
                    }
                }
            ]
        },
        {
            "key": "power_dissipation",
            "symbol": "P<sub>tot</sub>",
            "spec_type": "max_rating",
            "column_model": "MAX_ONLY",
            "engineering_class": "SAFETY_LIMIT",
            "special_semantics": "NONE",
            "llm_context": {
                "formal_name": "Total Power Dissipation",
                "aliases": ["Power Dissipation", "Power Loss", "Ptot", "PD"]
            },
            "possible_units": ["W", "mW"],
            "std_unit": "W",
            "scenarios": [
                {
                    "condition": "Tc=25°C or Ta=25°C",
                    "limits": {
                        "Signal_Small_Signal": [0.15, 0.2, 0.25, 0.33, 0.5],
                        "Power_Rectifier": [1, 1.5, 2, 3, 5, 10, 25, 50, 100],
                        "Schottky_Barrier": [0.5, 1, 1.5, 2, 5, 10, 25],
                        "Fast_Recovery": [1.5, 2.5, 4, 5, 10, 25],
                        "Ultra_Fast_Recovery": [2, 3, 5, 10, 20, 40],
                        "Zener": [0.5, 1, 5, 10, 50],
                        "TVS_Transient": [0],  # NOT_APPLICABLE - rated by pulse
                        "Switching": [0.2, 0.25, 0.5],
                        "PIN_Diode": [0.1, 0.25, 0.5],
                        "Avalanche": [1, 5, 10, 25]
                    }
                }
            ]
        },
        {
            "key": "peak_pulse_power",
            "symbol": "P<sub>PPM</sub>",
            "spec_type": "max_rating",
            "column_model": "MAX_ONLY",
            "engineering_class": "SAFETY_LIMIT",
            "special_semantics": "NOT_APPLICABLE",  # Only for TVS
            "llm_context": {
                "formal_name": "Peak Pulse Power Dissipation",
                "aliases": ["PPPM", "Pulse Power", "Transient Power"]
            },
            "possible_units": ["W", "kW"],
            "std_unit": "W",
            "scenarios": [
                {
                    "condition": "10/1000µs waveform",
                    "limits": {
                        "Signal_Small_Signal": [0],
                        "Power_Rectifier": [0],
                        "Schottky_Barrier": [0],
                        "Fast_Recovery": [0],
                        "Ultra_Fast_Recovery": [0],
                        "Zener": [0],
                        "TVS_Transient": [400, 600, 1000, 1500, 3000, 5000, 10000, 15000],
                        "Switching": [0],
                        "PIN_Diode": [0],
                        "Avalanche": [0]
                    }
                }
            ]
        },
        {
            "key": "tj_max",
            "symbol": "T<sub>j(max)</sub>",
            "spec_type": "max_rating",
            "column_model": "MAX_ONLY",
            "engineering_class": "SAFETY_LIMIT",
            "special_semantics": "NONE",
            "llm_context": {
                "formal_name": "Maximum Junction Temperature",
                "aliases": ["Max Junction Temp", "Tj max"]
            },
            "possible_units": ["°C"],
            "std_unit": "°C",
            "scenarios": [
                {
                    "condition": "Max",
                    "limits": {
                        "Signal_Small_Signal": [150, 175, 200],
                        "Power_Rectifier": [150, 175, 200],
                        "Schottky_Barrier": [125, 150, 175],
                        "Fast_Recovery": [150, 175],
                        "Ultra_Fast_Recovery": [150, 175],
                        "Zener": [150, 175, 200],
                        "TVS_Transient": [150, 175],
                        "Switching": [150, 175],
                        "PIN_Diode": [125, 150],
                        "Avalanche": [175, 200]
                    }
                }
            ]
        },
        {
            "key": "storage_temp_range",
            "symbol": "T<sub>stg</sub>",
            "spec_type": "operational_range",
            "column_model": "MIN_MAX",
            "engineering_class": "OPERATING_CONDITION",
            "special_semantics": "NONE",
            "llm_context": {
                "formal_name": "Storage Temperature Range",
                "aliases": ["Storage Temp", "Tstg"]
            },
            "possible_units": ["°C"],
            "std_unit": "°C",
            "scenarios": [
                {
                    "condition": "Non-operating",
                    "limits": {
                        "Signal_Small_Signal": [[-65, 175], [-65, 200]],
                        "Power_Rectifier": [[-65, 175], [-55, 200]],
                        "Schottky_Barrier": [[-65, 150], [-65, 175]],
                        "Fast_Recovery": [[-65, 175]],
                        "Ultra_Fast_Recovery": [[-65, 175]],
                        "Zener": [[-65, 175], [-65, 200]],
                        "TVS_Transient": [[-65, 175]],
                        "Switching": [[-65, 175]],
                        "PIN_Diode": [[-65, 150]],
                        "Avalanche": [[-65, 175]]
                    }
                }
            ]
        },
        {
            "key": "avalanche_energy",
            "symbol": "E<sub>AS</sub>",
            "spec_type": "max_rating",
            "column_model": "MAX_ONLY",
            "engineering_class": "SAFETY_LIMIT",
            "special_semantics": "NOT_APPLICABLE",  # Only for avalanche-rated
            "llm_context": {
                "formal_name": "Single Pulse Avalanche Energy",
                "aliases": ["EAS", "Avalanche Energy", "Single Pulse Energy"]
            },
            "possible_units": ["mJ", "J"],
            "std_unit": "mJ",
            "scenarios": [
                {
                    "condition": "Single pulse",
                    "limits": {
                        "Signal_Small_Signal": [0],
                        "Power_Rectifier": [0],
                        "Schottky_Barrier": [0],
                        "Fast_Recovery": [10, 30, 50, 100],
                        "Ultra_Fast_Recovery": [20, 50, 100, 200, 500],
                        "Zener": [0],
                        "TVS_Transient": [0],
                        "Switching": [0],
                        "PIN_Diode": [0],
                        "Avalanche": [100, 250, 500, 1000, 2000]
                    }
                }
            ]
        }
    ],
    
    # ==========================================================================
    # ELECTRICAL CHARACTERISTICS
    # ==========================================================================
    "ELEC_CHAR": [
        {
            "key": "forward_voltage",
            "symbol": "V<sub>F</sub>",
            "spec_type": "max_limit",
            "column_model": "TYP_MAX",
            "engineering_class": "PERFORMANCE_LIMIT",
            "special_semantics": "NONE",
            "llm_context": {
                "formal_name": "Forward Voltage Drop",
                "aliases": ["Forward Voltage", "Max Forward Voltage", "VF", "On Voltage"]
            },
            "possible_units": ["V", "mV"],
            "std_unit": "V",
            "scenarios": [
                {
                    "condition": "IF=rated, Tj=25°C",
                    "limits": {
                        "Signal_Small_Signal": [0.715, 1.0, 1.25],
                        "Power_Rectifier": [0.93, 1.0, 1.1, 1.2, 1.3],
                        "Schottky_Barrier": [0.35, 0.45, 0.50, 0.55, 0.70, 0.85, 1.0],
                        "Fast_Recovery": [1.0, 1.2, 1.5, 1.7],
                        "Ultra_Fast_Recovery": [1.1, 1.3, 1.5, 1.7, 2.0],
                        "Zener": [1.0, 1.2],
                        "TVS_Transient": [3.3, 3.5, 5.0],  # At 1mA test
                        "Switching": [0.715, 1.0],
                        "PIN_Diode": [0.9, 1.0, 1.2],
                        "Avalanche": [1.2, 1.5, 1.7]
                    }
                }
            ]
        },
        {
            "key": "forward_voltage_temp_coeff",
            "symbol": "dV<sub>F</sub>/dT",
            "spec_type": "nominal",
            "column_model": "TYP_ONLY",
            "engineering_class": "NOMINAL_PARAMETER",
            "special_semantics": "NONE",
            "llm_context": {
                "formal_name": "Forward Voltage Temperature Coefficient",
                "aliases": ["VF Temp Coeff", "Thermal Coefficient VF"]
            },
            "possible_units": ["mV/°C"],
            "std_unit": "mV/°C",
            "scenarios": [
                {
                    "condition": "At constant IF",
                    "limits": {
                        "Signal_Small_Signal": [-2.0, -2.5],
                        "Power_Rectifier": [-2.0, -2.5, -3.0],
                        "Schottky_Barrier": [-1.0, -1.5, -2.0],
                        "Fast_Recovery": [-2.0, -2.5],
                        "Ultra_Fast_Recovery": [-2.0, -2.5],
                        "Zener": [-2.0],
                        "TVS_Transient": [-2.0],
                        "Switching": [-2.0],
                        "PIN_Diode": [-2.0],
                        "Avalanche": [-2.5]
                    }
                }
            ]
        },
        {
            "key": "reverse_current",
            "symbol": "I<sub>R</sub>",
            "spec_type": "max_limit",
            "column_model": "TYP_MAX",
            "engineering_class": "PERFORMANCE_LIMIT",
            "special_semantics": "NONE",
            "llm_context": {
                "formal_name": "Reverse Leakage Current",
                "aliases": ["Reverse Current", "Leakage Current", "IR", "IRRM"]
            },
            "possible_units": ["µA", "mA", "nA"],
            "std_unit": "µA",
            "scenarios": [
                {
                    "condition": "At VR rated, Tj=25°C",
                    "limits": {
                        "Signal_Small_Signal": [0.005, 0.010, 0.025, 0.050, 0.1],
                        "Power_Rectifier": [0.5, 1, 5, 10, 30, 50, 100],
                        "Schottky_Barrier": [0.05, 0.1, 0.5, 1, 2, 5, 10, 50, 100, 500],
                        "Fast_Recovery": [0.5, 5, 10, 50],
                        "Ultra_Fast_Recovery": [0.5, 5, 10, 50, 100],
                        "Zener": [1, 10, 50, 100],
                        "TVS_Transient": [1, 5, 10, 100],
                        "Switching": [0.005, 0.025],
                        "PIN_Diode": [0.01, 0.1, 1],
                        "Avalanche": [10, 50, 100]
                    }
                }
            ]
        },
        {
            "key": "reverse_current_at_tj_max",
            "symbol": "I<sub>R</sub>",
            "spec_type": "max_limit",
            "column_model": "MAX_ONLY",
            "engineering_class": "PERFORMANCE_LIMIT",
            "special_semantics": "NONE",
            "llm_context": {
                "formal_name": "Reverse Current at Tj(max)",
                "aliases": ["IR at Max Temp", "Hot Leakage"]
            },
            "possible_units": ["µA", "mA"],
            "std_unit": "µA",
            "scenarios": [
                {
                    "condition": "At VR rated, Tj=Tj(max)",
                    "limits": {
                        "Signal_Small_Signal": [5, 30, 50],
                        "Power_Rectifier": [30, 50, 100, 500],
                        "Schottky_Barrier": [500, 1000, 2000, 5000],
                        "Fast_Recovery": [50, 100, 500],
                        "Ultra_Fast_Recovery": [100, 500],
                        "Zener": [100, 500],
                        "TVS_Transient": [1000],
                        "Switching": [30, 50],
                        "PIN_Diode": [10, 100],
                        "Avalanche": [500, 1000]
                    }
                }
            ]
        },
        {
            "key": "zener_voltage",
            "symbol": "V<sub>Z</sub>",
            "spec_type": "min_max_range",
            "column_model": "MIN_TYP_MAX",
            "engineering_class": "NOMINAL_PARAMETER",
            "special_semantics": "NOT_APPLICABLE",  # Only for Zener
            "llm_context": {
                "formal_name": "Zener Voltage",
                "aliases": ["VZ", "Breakdown Voltage", "Reference Voltage"]
            },
            "possible_units": ["V"],
            "std_unit": "V",
            "scenarios": [
                {
                    "condition": "At IZT",
                    "limits": {
                        "Signal_Small_Signal": [0],
                        "Power_Rectifier": [0],
                        "Schottky_Barrier": [0],
                        "Fast_Recovery": [0],
                        "Ultra_Fast_Recovery": [0],
                        "Zener": [2.4, 3.3, 3.9, 4.7, 5.1, 5.6, 6.2, 6.8, 7.5, 8.2, 9.1, 10, 11, 12, 13, 15, 16, 18, 20, 22, 24, 27, 30, 33, 36, 39, 43, 47, 51, 56, 62, 68, 75, 82, 91, 100, 110, 120, 130, 150, 160, 180, 200],
                        "TVS_Transient": [0],
                        "Switching": [0],
                        "PIN_Diode": [0],
                        "Avalanche": [0]
                    }
                }
            ]
        },
        {
            "key": "zener_impedance",
            "symbol": "Z<sub>ZT</sub>",
            "spec_type": "max_limit",
            "column_model": "TYP_MAX",
            "engineering_class": "PERFORMANCE_LIMIT",
            "special_semantics": "NOT_APPLICABLE",  # Only for Zener
            "llm_context": {
                "formal_name": "Zener Dynamic Impedance",
                "aliases": ["ZZT", "Dynamic Impedance", "Zener Resistance"]
            },
            "possible_units": ["Ω"],
            "std_unit": "Ω",
            "scenarios": [
                {
                    "condition": "At IZT",
                    "limits": {
                        "Signal_Small_Signal": [0],
                        "Power_Rectifier": [0],
                        "Schottky_Barrier": [0],
                        "Fast_Recovery": [0],
                        "Ultra_Fast_Recovery": [0],
                        "Zener": [2, 5, 10, 20, 30, 50, 80, 100, 150, 200, 400, 600, 800, 1000],
                        "TVS_Transient": [0],
                        "Switching": [0],
                        "PIN_Diode": [0],
                        "Avalanche": [0]
                    }
                }
            ]
        },
        {
            "key": "zener_temp_coefficient",
            "symbol": "α<sub>VZ</sub>",
            "spec_type": "nominal",
            "column_model": "TYP_ONLY",
            "engineering_class": "NOMINAL_PARAMETER",
            "special_semantics": "NOT_APPLICABLE",  # Only for Zener
            "llm_context": {
                "formal_name": "Zener Voltage Temperature Coefficient",
                "aliases": ["Temp Coeff", "αVZ", "TCV"]
            },
            "possible_units": ["%/°C", "mV/°C"],
            "std_unit": "%/°C",
            "scenarios": [
                {
                    "condition": "Standard",
                    "limits": {
                        "Signal_Small_Signal": [0],
                        "Power_Rectifier": [0],
                        "Schottky_Barrier": [0],
                        "Fast_Recovery": [0],
                        "Ultra_Fast_Recovery": [0],
                        "Zener": [-0.08, -0.05, -0.03, 0, 0.02, 0.03, 0.05, 0.07, 0.08, 0.10],  
                        "TVS_Transient": [0],
                        "Switching": [0],
                        "PIN_Diode": [0],
                        "Avalanche": [0]
                        }
                    }
                ]
            }
        ]
    },

# ==============================================================================
# MOSFET - Enhanced and Comprehensive Parameter Dictionary חלק4
# ==============================================================================

    "MOSFET": {
    "archetypes": [
        "HV_Power_THT",             # High Voltage Power Through-Hole (500V+)
        "MV_Power_SMD",             # Medium Voltage Power SMD (40-250V)
        "LV_Logic_Level",           # Low Voltage Logic Level (12-30V)
        "SiC_High_Voltage",         # Silicon Carbide (900V-1700V)
        "GaN_High_Frequency",       # Gallium Nitride (100V-650V)
        "RF_Power",                 # RF Power MOSFETs (VHF/UHF)
        "Dual_N_Channel",           # Dual N-Channel configuration
        "Dual_P_Channel",           # Dual P-Channel configuration
        "Complementary_Pair",       # N+P Channel pair
        "Depletion_Mode"            # Normally-ON devices
    ],
    
    # ==========================================================================
    # ABSOLUTE MAXIMUM RATINGS (הוספתי את החלק הזה שהיה חסר)
    # ==========================================================================
    "ABS_MAX": [
        {
            "key": "vdss",
            "symbol": "V<sub>DSS</sub>",
            "spec_type": "max_rating",
            "column_model": "MAX_ONLY",
            "engineering_class": "SAFETY_LIMIT",
            "special_semantics": "NONE",
            "llm_context": {
                "formal_name": "Drain-Source Voltage",
                "aliases": ["V_DSS (Drain-Source Voltage) [V]", "Max. VDS [V] – Drain-to-Source Blocking Voltage", "VDSS [V] Max.", "BV_DSS [V] – Drain-Source Breakdown Rating", "V(DSS) [V] Max. (Continuous)", "Drain-Source Voltage V_DS [V] (Abs. Max.)", "V_DSS [kV] Max. (Do Not Exceed)", "Drain-to-Source Voltage Rating [V] VDSS", "V(BR)DSS [V] Abs. Max. (Drain-Source, Gate Shorted)"]
            },
            "possible_units": ["V", "kV"],
            "std_unit": "V",
            "scenarios": [
                {
                    "condition": "VGS=0V, Tj=25°C",
                    "limits": {
                        "HV_Power_THT": [400, 500, 600, 650, 700, 800, 900, 1000, 1200, 1500, 1700],
                        "MV_Power_SMD": [30, 40, 55, 60, 75, 80, 100, 120, 150, 200, 250, 300],
                        "LV_Logic_Level": [12, 20, 25, 30, 40, 60],
                        "SiC_High_Voltage": [650, 900, 1000, 1200, 1700, 3300],
                        "GaN_High_Frequency": [100, 150, 200, 650, 900],
                        "RF_Power": [28, 50, 65],
                        "Dual_N_Channel": [20, 30, 60, 100],
                        "Dual_P_Channel": [-20, -30, -60],
                        "Complementary_Pair": [60, 100],
                        "Depletion_Mode": [25, 60, 200, 500]
                    }
                }
            ]
        },
        {
            "key": "id_cont",
            "symbol": "I<sub>D</sub>",
            "spec_type": "max_rating",
            "column_model": "MAX_ONLY",
            "engineering_class": "SAFETY_LIMIT",
            "special_semantics": "NONE",
            "llm_context": {
                "formal_name": "Continuous Drain Current",
                "aliases": ["I_D (Continuous) [A] Max.", "Drain Current I_D [A] Max.", "ID(cont) [A] – Continuous DC Drain Current", "Continuous Drain Current I_D [A]", "I_D(AV) [A] Max. (DC)", "ID [A] Continuous (See Derating Fig.)", "Max. Continuous I_D [A]", "Drain Current (Continuous) I_D [A]"]
            },
            "possible_units": ["A", "mA"],
            "std_unit": "A",
            "scenarios": [
                {
                    "condition": "Tc=25°C, VGS=10V",
                    "limits": {
                        "HV_Power_THT": [7, 10, 15, 20, 24, 30, 40, 46, 60, 80, 100, 120],
                        "MV_Power_SMD": [15, 20, 30, 40, 50, 60, 70, 80, 100, 120, 140, 180, 200],
                        "LV_Logic_Level": [0.5, 1, 2, 3, 4, 5, 8, 10, 12, 20, 30],
                        "SiC_High_Voltage": [17, 23, 36, 49, 63, 90, 117],
                        "GaN_High_Frequency": [10, 15, 30, 45, 60, 90],
                        "RF_Power": [1, 2, 4, 6, 10],
                        "Dual_N_Channel": [1, 2, 4, 8, 12],
                        "Dual_P_Channel": [-1, -2, -4, -6],
                        "Complementary_Pair": [4, 8, 12],
                        "Depletion_Mode": [0.2, 0.5, 1, 5, 10]
                    }
                }
            ]
        },
        {
            "key": "id_pulse",
            "symbol": "I<sub>DM</sub>",
            "spec_type": "max_rating",
            "column_model": "MAX_ONLY",
            "engineering_class": "SAFETY_LIMIT",
            "special_semantics": "NONE",
            "llm_context": {
                "formal_name": "Pulsed Drain Current",
                "aliases": ["I_DM (Pulsed) [A] Max.", "Pulsed Drain Current I_DM [A]", "IDM [A] Max. – Non-Repetitive Pulsed Current", "Peak Pulsed Drain Current I_DM [A]", "I_DM [A] – Maximum Pulsed (Single Pulse)", "Pulsed I_D [A] Max. (Non-Repetitive)", "I(DM) [A] Pulsed (Limited by Tj(max))"]
            },
            "possible_units": ["A"],
            "std_unit": "A",
            "scenarios": [
                {
                    "condition": "10µs pulse, Tj=25°C",
                    "limits": {
                        "HV_Power_THT": [28, 40, 60, 80, 96, 120, 160, 184, 240, 320, 400, 480],
                        "MV_Power_SMD": [60, 80, 120, 160, 200, 240, 280, 320, 400, 480, 560, 720, 800],
                        "LV_Logic_Level": [2, 4, 8, 12, 16, 20, 32, 40, 48, 80, 120],
                        "SiC_High_Voltage": [51, 69, 108, 147, 189, 270, 351],
                        "GaN_High_Frequency": [40, 60, 120, 180, 240, 360],
                        "RF_Power": [4, 8, 16, 24, 40],
                        "Dual_N_Channel": [4, 8, 16, 32, 48],
                        "Dual_P_Channel": [-4, -8, -16, -24],
                        "Complementary_Pair": [16, 32, 48],
                        "Depletion_Mode": [0.8, 2, 4, 20, 40]
                    }
                }
            ]
        },
        {
            "key": "vgs_max",
            "symbol": "V<sub>GS</sub>",
            "spec_type": "max_rating",
            "column_model": "MIN_MAX",
            "engineering_class": "SAFETY_LIMIT",
            "special_semantics": "NONE",
            "llm_context": {
                "formal_name": "Gate-Source Voltage",
                "aliases": ["V_GS [V] (Gate-Source Voltage, ±V Max.)", "Max. Gate-Source Voltage ±V_GS [V] (Continuous)", "VGS Rating [V] (Min/Max, Continuous)", "Gate Voltage Range V_GS [V] (±Max., See Note)", "V_GS [V] Max. (Abs., Do Not Exceed ± Limit)", "Gate-to-Source Voltage V_GS [V] (Abs. Max.)", "V(GS) [V] – Gate Drive Voltage Limit (±)", "VGS [V] (Continuous, Gate Oxide Stress Limit)", "Max. V_GS [V] ± (Gate Insulation Breakdown Limit)", "Gate-Source Voltage Rating V_GS [V] (±, Continuous)"]
            },
            "possible_units": ["V"],
            "std_unit": "V",
            "scenarios": [
                {
                    "condition": "Continuous",
                    "limits": {
                        "HV_Power_THT": [[-20, 20], [-30, 30]],
                        "MV_Power_SMD": [[-20, 20], [-10, 20]],
                        "LV_Logic_Level": [[-8, 8], [-12, 12], [-20, 20]],
                        "SiC_High_Voltage": [[-5, 20], [-6, 22]],
                        "GaN_High_Frequency": [[-10, 6], [-6, 10]],
                        "RF_Power": [[-10, 10]],
                        "Dual_N_Channel": [[-20, 20]],
                        "Dual_P_Channel": [[-20, 20]],
                        "Complementary_Pair": [[-20, 20]],
                        "Depletion_Mode": [[-30, 10], [-20, 5]]
                    }
                }
            ]
        },
        {
            "key": "power_dissipation",
            "symbol": "P<sub>D</sub>",
            "spec_type": "max_rating",
            "column_model": "MAX_ONLY",
            "engineering_class": "SAFETY_LIMIT",
            "special_semantics": "NONE",
            "llm_context": {
                "formal_name": "Maximum Power Dissipation",
                "aliases": ["P_D [W] Max.", "Power Dissipation P_D [W] Max.", "P_tot [W] Max. – Total Power Dissipation", "PD [W] Max. (Derate Above 25°C)", "Max. Power P_D [W] (See Derating Curve)", "P_D(max) [W] – Continuous", "Total Power Dissipation [W] P_D", "P_D [W] (Abs. Max., Case Mounted)"]
            },
            "possible_units": ["W", "kW"],
            "std_unit": "W",
            "scenarios": [
                {
                    "condition": "Tc=25°C",
                    "limits": {
                        "HV_Power_THT": [125, 150, 200, 250, 300, 375, 500, 600, 800, 1000],
                        "MV_Power_SMD": [40, 50, 63, 80, 100, 125, 150, 200, 250, 300],
                        "LV_Logic_Level": [0.7, 1, 1.4, 2, 2.5, 5, 8, 10, 15, 20],
                        "SiC_High_Voltage": [208, 278, 417, 556, 694, 833],
                        "GaN_High_Frequency": [50, 75, 100, 150, 200],
                        "RF_Power": [50, 100, 150, 300, 500],
                        "Dual_N_Channel": [1, 2, 3.5, 5, 10],
                        "Dual_P_Channel": [1, 2, 3.5],
                        "Complementary_Pair": [2.5, 5],
                        "Depletion_Mode": [1, 5, 25, 100, 300]
                    }
                }
            ]
        },
        {
            "key": "tj_max",
            "symbol": "T<sub>j(max)</sub>",
            "spec_type": "max_rating",
            "column_model": "MAX_ONLY",
            "engineering_class": "SAFETY_LIMIT",
            "special_semantics": "NONE",
            "llm_context": {
                "formal_name": "Maximum Junction Temperature",
                "aliases": ["T_j(max) [°C] – Maximum Junction Temperature", "Max. Junction Temp. T_J [°C] (Abs. Max.)", "Tj(max) [°C] – Do Not Exceed", "T_J Max. [°C] (Operating & Storage Limit)", "Operating Temperature Max. T_J [°C]", "T_J(max) [°C] (Continuous Operation Limit)", "Max. T_J [°C] (Channel Temperature, Abs. Max.)", "Junction Temp. Limit T_j [°C] Max.", "T_JMAX [°C] – Max. Channel Temperature Rating", "Tj [°C] Max. (Absolute Maximum, See Derating)"]
            },
            "possible_units": ["°C"],
            "std_unit": "°C",
            "scenarios": [
                {
                    "condition": "",
                    "limits": {
                        "HV_Power_THT": [150, 175],
                        "MV_Power_SMD": [150, 175],
                        "LV_Logic_Level": [150, 175],
                        "SiC_High_Voltage": [175, 200],
                        "GaN_High_Frequency": [150, 175, 200],
                        "RF_Power": [200, 225],
                        "Dual_N_Channel": [150, 175],
                        "Dual_P_Channel": [150, 175],
                        "Complementary_Pair": [150, 175],
                        "Depletion_Mode": [150, 175, 200]
                    }
                }
            ]
        }
    ],
    
    # ==========================================================================
    # ELECTRICAL CHARACTERISTICS - STATIC PARAMETERS (הוספתי את ההתחלה החסרה)
    # ==========================================================================
    "ELEC_CHAR": [
        {
            "key": "bvdss",
            "symbol": "BV<sub>DSS</sub>",
            "spec_type": "min_limit",
            "column_model": "MIN_ONLY",
            "engineering_class": "PERFORMANCE_LIMIT",
            "special_semantics": "NONE",
            "llm_context": {
                "formal_name": "Drain-Source Breakdown Voltage",
                "aliases": ["BV_DSS [V] Min.", "V(BR)DSS [V] Min. – Drain-Source Breakdown", "Breakdown Voltage V(BR)DSS [V]", "BV_DSS [V] – Avalanche Breakdown", "Drain-Source Breakdown BV_DSS [V]", "Breakdown Volt. V_DSS [V] Min.", "V_BRDSS [V] Min."]
            },
            "possible_units": ["V"],
            "std_unit": "V",
            "scenarios": [
                {
                    "condition": "VGS=0V, ID=250µA",
                    "limits": {
                        "HV_Power_THT": [400, 500, 600, 650, 800, 1000, 1200],
                        "MV_Power_SMD": [30, 40, 60, 80, 100, 150, 200, 250],
                        "LV_Logic_Level": [12, 20, 25, 30, 40],
                        "SiC_High_Voltage": [650, 900, 1200, 1700],
                        "GaN_High_Frequency": [100, 150, 200, 650],
                        "RF_Power": [28, 50, 65],
                        "Dual_N_Channel": [20, 30, 60],
                        "Dual_P_Channel": [-20, -30, -60],
                        "Complementary_Pair": [60],
                        "Depletion_Mode": [25, 60, 200, 500]
                    }
                }
            ]
        },
        {
            "key": "rds_on",
            "symbol": "R<sub>DS(on)</sub>",
            "spec_type": "max_limit",
            "column_model": "TYP_MAX",
            "engineering_class": "PERFORMANCE_LIMIT",
            "special_semantics": "NONE",
            "llm_context": {
                "formal_name": "Static Drain-Source On-Resistance",
                "aliases": ["R_DS(on) [mΩ] Typ./Max.", "On-Resistance R_DS(on) [mΩ]", "RDS(on) [mΩ] Max.", "R_DS(ON) [Ω] Typ. Max.", "Drain-Source On-State Resistance [mΩ]", "Ron [mΩ] (Static)", "R DS(on) [mΩ]", "R_DS(on) Max. [mΩ]", "Static R_DS(on) [Ω] Typ./Max.", "R(DS)(on) [mΩ] Typ Max."]
            },
            "possible_units": ["mΩ", "Ω"],
            "std_unit": "mΩ",
            "scenarios": [
                {
                    "condition": "VGS=10V, ID=specified, Tj=25°C",
                    "limits": {
                        "HV_Power_THT": [150, 200, 250, 350, 500, 750, 1000, 1200, 1500, 2000],
                        "MV_Power_SMD": [2, 3, 5, 7, 10, 15, 20, 25, 30, 40, 50, 70],
                        "LV_Logic_Level": [2, 3, 5, 8, 10, 15, 20, 30, 45],
                        "SiC_High_Voltage": [25, 40, 60, 80, 120, 160],
                        "GaN_High_Frequency": [15, 25, 50, 100, 150],
                        "RF_Power": [500, 800, 1200, 2000], 
                        "Dual_N_Channel": [10, 20, 40, 60, 100],
                        "Dual_P_Channel": [15, 30, 60, 90],
                        "Complementary_Pair": [20, 40, 80],
                        "Depletion_Mode": [50, 100, 500, 1000, 2000]
                    }
                }
            ]
        },
        {
            "key": "idss",
            "symbol": "I<sub>DSS</sub>",
            "spec_type": "max_limit",
            "column_model": "TYP_MAX",
            "engineering_class": "PERFORMANCE_LIMIT",
            "special_semantics": "NONE",
            "llm_context": {
                "formal_name": "Zero Gate Voltage Drain Current",
                "aliases": ["I_DSS [µA] Max.", "Drain-Source Leakage I_DSS [µA]", "Zero Gate Voltage Drain Current I_DSS [µA] Max.", "IDSS [nA] Max.", "Leakage Current I_DSS [µA]", "I_DSS [µA] – Off-State Drain Leakage", "D-S Leakage I(DSS) [µA] Max.", "Off-State Drain Current I_DSS [µA]", "Zero-Gate Drain Leakage [nA/µA] IDSS"]
            },
            "possible_units": ["µA", "nA", "mA"],
            "std_unit": "µA",
            "scenarios": [
                {
                    "condition": "VDS=rated, VGS=0V, Tj=25°C",
                    "limits": {
                        "HV_Power_THT": [1, 10, 25, 50, 100],
                        "MV_Power_SMD": [1, 10, 50, 100],
                        "LV_Logic_Level": [0.001, 0.01, 0.1, 1, 10],
                        "SiC_High_Voltage": [1, 10, 100],
                        "GaN_High_Frequency": [0.1, 1, 10, 100],
                        "RF_Power": [1, 10, 50],
                        "Dual_N_Channel": [0.01, 1, 10],
                        "Dual_P_Channel": [0.01, 1, 10],
                        "Complementary_Pair": [1, 10],
                        "Depletion_Mode": [0]
                    }
                }
            ]
        },
        {
            "key": "igss",
            "symbol": "I<sub>GSS</sub>",
            "spec_type": "max_limit",
            "column_model": "MAX_ONLY",
            "engineering_class": "PERFORMANCE_LIMIT",
            "special_semantics": "NONE",
            "llm_context": {
                "formal_name": "Gate-Source Leakage Current",
                "aliases": ["I_GSS [nA] Max.", "Gate Leakage I_GSS [nA] Max.", "IGSS [nA] – Gate-Source Leakage", "Gate Leakage Current I_GSS [µA] Max.", "Gate-to-Source Leakage [nA] IGSS", "I(GSS) [nA] Max.", "Gate Insulation Leakage I_GSS [nA]", "IGSS [nA] Max. – Gate Oxide Leakage", "Gate-Source Leakage I_G [nA] Max."]
            },
            "possible_units": ["nA", "µA"],
            "std_unit": "nA",
            "scenarios": [
                {
                    "condition": "VGS=±20V, VDS=0V",
                    "limits": {
                        "HV_Power_THT": [100, 500, 1000],
                        "MV_Power_SMD": [100, 500],
                        "LV_Logic_Level": [10, 100, 500],
                        "SiC_High_Voltage": [100, 500],
                        "GaN_High_Frequency": [100, 500, 1000],
                        "RF_Power": [100, 500],
                        "Dual_N_Channel": [100, 500],
                        "Dual_P_Channel": [100, 500],
                        "Complementary_Pair": [500],
                        "Depletion_Mode": [100, 500]
                    }
                }
            ]
        },
        {
            "key": "gfs",
            "symbol": "g<sub>fs</sub>",
            "spec_type": "min_limit",
            "column_model": "TYP_ONLY",
            "engineering_class": "NOMINAL_PARAMETER",
            "special_semantics": "NONE",
            "llm_context": {
                "formal_name": "Forward Transconductance",
                "aliases": ["g_fs [S] Typ.", "Transconductance g_fs [S] Typ.", "g_m [S] – Forward Transconductance (Typ.)", "gfs [mS] Typ.", "Forward Trans-conductance g_fs [S] (Typ.)", "Transconductance g(fs) [S]", "g_FS [S] Typ. – Gate Transconductance", "Forward Transconductance g_fs (Siemens) Typ.", "g_fs [A/V] Typ."]
            },
            "possible_units": ["S", "mS"],
            "std_unit": "S",
            "scenarios": [
                {
                    "condition": "VDS=specified, ID=specified",
                    "limits": {
                        "HV_Power_THT": [5, 10, 15, 20, 30, 40],
                        "MV_Power_SMD": [10, 20, 40, 60, 80, 120],
                        "LV_Logic_Level": [1, 2, 5, 10, 15],
                        "SiC_High_Voltage": [10, 15, 25, 35],
                        "GaN_High_Frequency": [15, 25, 40, 60],
                        "RF_Power": [2, 5, 8, 12],
                        "Dual_N_Channel": [2, 5, 10],
                        "Dual_P_Channel": [2, 4, 8],
                        "Complementary_Pair": [5, 10],
                        "Depletion_Mode": [0.5, 1, 5, 10]
                    }
                }
            ]
        },
        {
            "key": "vsd",
            "symbol": "V<sub>SD</sub>",
            "spec_type": "max_limit",
            "column_model": "TYP_MAX",
            "engineering_class": "PERFORMANCE_LIMIT",
            "special_semantics": "NONE",
            "llm_context": {
                "formal_name": "Body Diode Forward Voltage",
                "aliases": ["V_SD [V] Typ./Max.", "Source-Drain Diode Voltage V_SD [V]", "Body Diode V_F [V] Max.", "V_SD [V] – Intrinsic Body Diode Forward Drop", "Body Diode Forward Voltage V(SD) [V] Typ. Max.", "V_F (Body Diode) [V] Max.", "Diode Forward Voltage V_SD [V]", "V(SD) [V] Typ./Max. – Integrated Body Diode"]
            },
            "possible_units": ["V"],
            "std_unit": "V",
            "scenarios": [
                {
                    "condition": "IS=ID, VGS=0V",
                    "limits": {
                        "HV_Power_THT": [1.2, 1.3, 1.5, 1.7],
                        "MV_Power_SMD": [0.7, 0.9, 1.0, 1.2, 1.3],
                        "LV_Logic_Level": [0.6, 0.7, 0.8, 1.0],
                        "SiC_High_Voltage": [2.8, 3.2, 3.5, 4.0],
                        "GaN_High_Frequency": [0], 
                        "RF_Power": [1.2, 1.5],
                        "Dual_N_Channel": [0.7, 1.0],
                        "Dual_P_Channel": [0.7, 1.0],
                        "Complementary_Pair": [1.0],
                        "Depletion_Mode": [1.2, 1.5]
                    }
                }
            ]
        },
        {
            "key": "trr",
            "symbol": "t<sub>rr</sub>",
            "spec_type": "max_limit",
            "column_model": "TYP_MAX",
            "engineering_class": "PERFORMANCE_LIMIT",
            "special_semantics": "NOT_APPLICABLE",
            "llm_context": {
                "formal_name": "Body Diode Reverse Recovery Time",
                "aliases": ["t_rr [ns] (Body Diode) Typ./Max.", "Reverse Recovery Time t_rr [ns] Typ./Max. (Body Diode)", "Body Diode t_rr [ns]", "trr [ns] Max. – Body Diode Recovery", "t_rr [ns] (Intrinsic Diode)", "Body Diode Recovery Time [ns] t_rr", "Reverse Recovery t_rr [ns] (Body Diode)", "t(rr) [ns] Max. (Body Diode)", "t_rr [ns] Typ./Max. – Diode Recovery"]
            },
            "possible_units": ["ns"],
            "std_unit": "ns",
            "scenarios": [
                {
                    "condition": "IF=ID, di/dt=100A/µs",
                    "limits": {
                        "HV_Power_THT": [200, 300, 500, 750, 1000],
                        "MV_Power_SMD": [50, 75, 100, 150, 250],
                        "LV_Logic_Level": [20, 30, 50, 75],
                        "SiC_High_Voltage": [15, 20, 30, 40],
                        "GaN_High_Frequency": [0],
                        "RF_Power": [0],
                        "Dual_N_Channel": [30, 50, 100],
                        "Dual_P_Channel": [30, 50],
                        "Complementary_Pair": [50],
                        "Depletion_Mode": [100, 200]
                    }
                }
            ]
        },
        {
            "key": "qrr",
            "symbol": "Q<sub>rr</sub>",
            "spec_type": "max_limit",
            "column_model": "TYP_MAX",
            "engineering_class": "PERFORMANCE_LIMIT",
            "special_semantics": "NOT_APPLICABLE",
            "llm_context": {
                "formal_name": "Body Diode Reverse Recovery Charge",
                "aliases": ["Q_rr [nC] (Body Diode) Typ./Max.", "Recovery Charge Q_rr [nC] Typ./Max. (Body Diode)", "Body Diode Q_rr [µC]", "Qrr [nC] Max. – Body Diode Reverse Recovery Charge", "Q_rr [nC] (Intrinsic Diode)", "Body Diode Recovery Charge [nC] Q_rr", "Reverse Recovery Charge Q_rr [nC] (Body Diode)", "Q(rr) [nC] Max. (Body Diode)", "Q_rr [nC] Typ./Max. – Stored Charge (Body Diode)"]
            },
            "possible_units": ["nC", "µC"],
            "std_unit": "nC",
            "scenarios": [
                {
                    "condition": "IF=ID, di/dt=100A/µs",
                    "limits": {
                        "HV_Power_THT": [500, 1000, 2000, 4000],
                        "MV_Power_SMD": [100, 200, 500, 1000],
                        "LV_Logic_Level": [10, 20, 50, 100],
                        "SiC_High_Voltage": [50, 100, 200],
                        "GaN_High_Frequency": [0],
                        "RF_Power": [0],
                        "Dual_N_Channel": [20, 50, 100],
                        "Dual_P_Channel": [20, 50],
                        "Complementary_Pair": [50],
                        "Depletion_Mode": [100, 500]
                    }
                }
            ]
        },
        {
            "key": "vgs_th",
            "symbol": "V<sub>GS(th)</sub>",
            "spec_type": "min_max_range",
            "column_model": "MIN_TYP_MAX",
            "engineering_class": "NOMINAL_PARAMETER",
            "special_semantics": "NONE",
            "llm_context": {
                "formal_name": "Gate Threshold Voltage",
                "aliases": ["V_GS(th) [V] Min./Typ./Max.", "Gate Threshold V_GS(th) [V]", "Threshold Voltage V_GS(th) [V]", "Vth [V] – Gate Turn-On Threshold", "V_T [V] Min./Max.", "VGS(th) [V]", "V_{GS}(th) [V] Min. Typ. Max.", "V_TH [V] Range", "Gate Threshold V(GS)(th) [V] – Min./Max.", "Turn-On Threshold V_GS(th) [V]"]
            },
            "possible_units": ["V"],
            "std_unit": "V",
            "scenarios": [
                {
                    "condition": "VDS=VGS, ID=250µA, Tj=25°C",
                    "limits": {
                        "HV_Power_THT": [[2, 4], [2.5, 4.5], [3, 5]],
                        "MV_Power_SMD": [[1, 2.5], [1.5, 3], [2, 4]],
                        "LV_Logic_Level": [[0.4, 1], [0.5, 1.5], [0.8, 2], [1, 2.5]],
                        "SiC_High_Voltage": [[2, 4], [2.5, 5]],
                        "GaN_High_Frequency": [[0.5, 2.5], [1, 3]],
                        "RF_Power": [[2, 4], [2.5, 4.5]],
                        "Dual_N_Channel": [[0.5, 1.5], [1, 2.5]],
                        "Dual_P_Channel": [[-2.5, -1], [-2.5, -0.5]],
                        "Complementary_Pair": [[1, 2.5]],
                        "Depletion_Mode": [[-2.5, -0.3], [-4, -1], [-6, -2]]
                    }
                }
            ]
        }
    ],

    # ==========================================================================
    # DYNAMIC CHARACTERISTICS (הוספתי את החלק הזה שהיה חסר)
    # ==========================================================================
    "DYNAMIC_CHAR": [
        {
            "key": "ciss",
            "symbol": "C<sub>iss</sub>",
            "spec_type": "nominal",
            "column_model": "TYP_MAX",
            "engineering_class": "NOMINAL_PARAMETER",
            "special_semantics": "NONE",
            "llm_context": {
                "formal_name": "Input Capacitance",
                "aliases": ["C_iss [pF] Typ./Max.", "Input Capacitance C_iss [pF]", "Ciss [pF] – CGS + CGD", "C_iss [nF] Typ. Max.", "Gate Capacitance C_iss [pF]", "Input Cap. C(iss) [pF] Typ.", "Ciss [pF] (CGS+CGD)", "C_ISS [pF] Typ./Max.", "Total Input Capacitance C_iss [pF]"]
            },
            "possible_units": ["pF", "nF"],
            "std_unit": "pF",
            "scenarios": [
                {
                    "condition": "VGS=0V, VDS=25V, f=1MHz",
                    "limits": {
                        "HV_Power_THT": [2000, 3000, 5000, 8000, 10000, 15000],
                        "MV_Power_SMD": [1000, 2000, 3000, 5000, 8000, 10000],
                        "LV_Logic_Level": [200, 400, 600, 1000, 1500, 2500],
                        "SiC_High_Voltage": [1400, 2300, 3700, 4900],
                        "GaN_High_Frequency": [500, 900, 1400, 2100],
                        "RF_Power": [100, 200, 400, 600],
                        "Dual_N_Channel": [400, 800, 1500],
                        "Dual_P_Channel": [500, 1000],
                        "Complementary_Pair": [1000, 2000],
                        "Depletion_Mode": [500, 1000, 3000, 5000]
                    }
                }
            ]
        },
        {
            "key": "coss",
            "symbol": "C<sub>oss</sub>",
            "spec_type": "nominal",
            "column_model": "TYP_MAX",
            "engineering_class": "NOMINAL_PARAMETER",
            "special_semantics": "NONE",
            "llm_context": {
                "formal_name": "Output Capacitance",
                "aliases": ["C_oss [pF] Typ./Max.", "Output Capacitance C_oss [pF]", "Coss [pF] – CDS + CGD", "C_oss [pF] Typ. Max.", "Drain Capacitance C_oss [pF]", "Output Cap. C(oss) [pF] Typ.", "Coss [pF] (CDS+CGD)", "C_OSS [pF] Typ./Max.", "Total Output Capacitance C_oss [pF]"]
            },
            "possible_units": ["pF", "nF"],
            "std_unit": "pF",
            "scenarios": [
                {
                    "condition": "VGS=0V, VDS=25V, f=1MHz",
                    "limits": {
                        "HV_Power_THT": [200, 300, 500, 800, 1000, 1500],
                        "MV_Power_SMD": [100, 200, 400, 600, 1000, 1500],
                        "LV_Logic_Level": [50, 100, 150, 300, 500],
                        "SiC_High_Voltage": [90, 140, 230, 310],
                        "GaN_High_Frequency": [80, 120, 190, 280],
                        "RF_Power": [30, 60, 100, 150],
                        "Dual_N_Channel": [100, 200, 400],
                        "Dual_P_Channel": [120, 240],
                        "Complementary_Pair": [200, 400],
                        "Depletion_Mode": [100, 300, 800, 1200]
                    }
                }
            ]
        },
        {
            "key": "crss",
            "symbol": "C<sub>rss</sub>",
            "spec_type": "nominal",
            "column_model": "TYP_MAX",
            "engineering_class": "NOMINAL_PARAMETER",
            "special_semantics": "NONE",
            "llm_context": {
                "formal_name": "Reverse Transfer Capacitance",
                "aliases": ["C_rss [pF] Typ./Max.", "Reverse Transfer Capacitance C_rss [pF]", "Crss [pF] – CGD Miller Capacitance", "Miller Capacitance C_rss [pF] Typ. Max.", "Cgd [pF] – Reverse Transfer Cap.", "C_rss [pF] Typ. Max.", "Crss (Miller Cap.) [pF] Typ./Max.", "C(rss) [pF] – Gate-to-Drain Feedback Cap.", "Feedback Capacitance C_rss [pF]", "C_GD (Crss) [pF] Typ./Max."]
            },
            "possible_units": ["pF"],
            "std_unit": "pF",
            "scenarios": [
                {
                    "condition": "VGS=0V, VDS=25V, f=1MHz",
                    "limits": {
                        "HV_Power_THT": [50, 80, 100, 150, 200, 300],
                        "MV_Power_SMD": [20, 40, 60, 100, 150, 250],
                        "LV_Logic_Level": [10, 20, 30, 50, 80, 150],
                        "SiC_High_Voltage": [6, 12, 19, 25],
                        "GaN_High_Frequency": [4, 8, 12, 18],
                        "RF_Power": [5, 10, 20, 30],
                        "Dual_N_Channel": [20, 40, 80],
                        "Dual_P_Channel": [25, 50],
                        "Complementary_Pair": [40, 80],
                        "Depletion_Mode": [20, 50, 150, 250]
                    }
                }
            ]
        },
        {
            "key": "qg",
            "symbol": "Q<sub>g</sub>",
            "spec_type": "nominal",
            "column_model": "TYP_MAX",
            "engineering_class": "NOMINAL_PARAMETER",
            "special_semantics": "NONE",
            "llm_context": {
                "formal_name": "Total Gate Charge",
                "aliases": ["Q_g [nC] Typ./Max.", "Gate Charge Q_g [nC] Typ.", "Qg [nC] – Total Gate Charge", "Q_g Total [nC]", "Total Gate Charge Q_g [µC]", "Q_gate [nC] Typ. Max.", "Qg [nC] Typ./Max. – Full Gate Charge", "Gate Charge Q(g) [nC]", "Q_G [nC] Total", "Total Q_g [nC] Typ. Max."]
            },
            "possible_units": ["nC", "µC"],
            "std_unit": "nC",
            "scenarios": [
                {
                    "condition": "VDD=rated/2, ID=rated, VGS=10V",
                    "limits": {
                        "HV_Power_THT": [50, 80, 100, 150, 200, 300],
                        "MV_Power_SMD": [20, 40, 60, 80, 120, 180],
                        "LV_Logic_Level": [3, 5, 10, 15, 20, 30],
                        "SiC_High_Voltage": [49, 82, 123, 164],
                        "GaN_High_Frequency": [5, 10, 20, 30, 45],
                        "RF_Power": [10, 20, 40],
                        "Dual_N_Channel": [5, 10, 20],
                        "Dual_P_Channel": [8, 15],
                        "Complementary_Pair": [15, 30],
                        "Depletion_Mode": [10, 30, 80, 150]
                    }
                }
            ]
        },
        {
            "key": "qgs",
            "symbol": "Q<sub>gs</sub>",
            "spec_type": "nominal",
            "column_model": "TYP_ONLY",
            "engineering_class": "NOMINAL_PARAMETER",
            "special_semantics": "NONE",
            "llm_context": {
                "formal_name": "Gate-Source Charge",
                "aliases": ["Q_gs [nC] Typ.", "Gate-Source Charge Q_gs [nC] (Before Miller Plateau)", "Qgs [nC] – Gate-to-Source Charge Component", "Q_GS [nC] Typ. (Phase 1+2 of Gate Charge Waveform)", "Gate-Source Charge Q_gs [nC] (VGS=0→V_plateau)", "Q(gs) [nC] Typ.", "Qgs [nC] – Portion of Q_g Before Miller Effect", "Q_gs Component [nC] Typ. (From Gate Charge Waveform)", "Gate-Source Charge [nC] Q_gs", "Q_GS [nC] (Pre-Miller)"]
            },
            "possible_units": ["nC"],
            "std_unit": "nC",
            "scenarios": [
                {
                    "condition": "VDD=rated/2, ID=rated",
                    "limits": {
                        "HV_Power_THT": [15, 25, 35, 50, 70],
                        "MV_Power_SMD": [8, 15, 25, 35, 50],
                        "LV_Logic_Level": [1, 2, 4, 6, 10],
                        "SiC_High_Voltage": [18, 30, 45, 60],
                        "GaN_High_Frequency": [2, 4, 8, 12],
                        "RF_Power": [4, 8, 15],
                        "Dual_N_Channel": [2, 4, 8],
                        "Dual_P_Channel": [3, 6],
                        "Complementary_Pair": [6, 12],
                        "Depletion_Mode": [4, 12, 30, 50]
                    }
                }
            ]
        },
        {
            "key": "qgd",
            "symbol": "Q<sub>gd</sub>",
            "spec_type": "nominal",
            "column_model": "TYP_ONLY",
            "engineering_class": "NOMINAL_PARAMETER",
            "special_semantics": "NONE",
            "llm_context": {
                "formal_name": "Gate-Drain Charge (Miller Charge)",
                "aliases": ["Q_gd [nC] Typ. – Miller Charge", "Miller Charge Q_gd [nC]", "Qgd [nC] – Gate-to-Drain (Miller Plateau) Charge", "Q_GD [nC] Typ. (Miller Plateau Region)", "Gate-Drain Charge Q_gd [nC] (Miller Effect, Typ.)", "Q(gd) [nC] Typ. (Plateau Phase of Gate Waveform)", "Qgd [nC] – Miller Cap. Charge", "Q_gd Component [nC] Typ. (Miller Plateau)", "Gate-Drain Miller Charge [nC] Q_gd", "Q_GD [nC] Typ. (Phase 3 Gate Charge, Miller Plateau)"]
            },
            "possible_units": ["nC"],
            "std_unit": "nC",
            "scenarios": [
                {
                    "condition": "VDD=rated/2, ID=rated",
                    "limits": {
                        "HV_Power_THT": [20, 35, 50, 75, 100],
                        "MV_Power_SMD": [8, 15, 25, 35, 55],
                        "LV_Logic_Level": [1, 2, 4, 6, 10],
                        "SiC_High_Voltage": [14, 23, 35, 47],
                        "GaN_High_Frequency": [1.5, 3, 6, 9],
                        "RF_Power": [3, 6, 12],
                        "Dual_N_Channel": [2, 4, 8],
                        "Dual_P_Channel": [3, 5],
                        "Complementary_Pair": [5, 10],
                        "Depletion_Mode": [3, 10, 30, 50]
                    }
                }
            ]
        },
        {
            "key": "rg",
            "symbol": "R<sub>g</sub>",
            "spec_type": "nominal",
            "column_model": "TYP_ONLY",
            "engineering_class": "NOMINAL_PARAMETER",
            "special_semantics": "NONE",
            "llm_context": {
                "formal_name": "Gate Resistance (Internal)",
                "aliases": ["R_g [Ω] Typ. (Internal Gate Resistance)", "Internal Gate Resistance R_g [Ω]", "Rg [Ω] – Intrinsic Gate Resistance", "R_GATE [Ω] Typ. (Internal)", "Gate Resistor R_g [Ω] Typ.", "R_g(int) [Ω] – Internal Gate Mesh Resistance", "Rg [Ω] Typ.", "Internal R_g [Ω]", "Gate Resistance (Internal) R_g [Ω]", "R(g) [Ω] Typ. – Polysilicon Gate Resistance"]
            },
            "possible_units": ["Ω"],
            "std_unit": "Ω",
            "scenarios": [
                {
                    "condition": "f=1MHz, open drain",
                    "limits": {
                        "HV_Power_THT": [1, 1.5, 2, 3, 5],
                        "MV_Power_SMD": [0.5, 1, 1.5, 2, 3],
                        "LV_Logic_Level": [0.3, 0.5, 1, 1.5, 2],
                        "SiC_High_Voltage": [2, 3, 4, 5],
                        "GaN_High_Frequency": [0.5, 1, 2, 3],
                        "RF_Power": [1, 2, 3],
                        "Dual_N_Channel": [1, 2, 3],
                        "Dual_P_Channel": [1.5, 3],
                        "Complementary_Pair": [2, 4],
                        "Depletion_Mode": [2, 4, 8]
                    }
                }
            ]
        }
    ],

    # ==========================================================================
    # SWITCHING CHARACTERISTICS (הוספתי את ההתחלה, שילבתי את המידע שלך בהמשך)
    # ==========================================================================
    "SWITCHING_CHAR": [
        {
            "key": "td_on",
            "symbol": "t<sub>d(on)</sub>",
            "spec_type": "nominal",
            "column_model": "TYP_MAX",
            "engineering_class": "NOMINAL_PARAMETER",
            "special_semantics": "NONE",
            "llm_context": {
                "formal_name": "Turn-On Delay Time",
                "aliases": ["t_d(on) [ns] Typ./Max.", "Turn-On Delay t_d(on) [ns]", "td(on) [ns] – Delay Time Turn-On (Inductive Load)", "t_d(on) [ns] Typ. Max.", "Turn-On Delay Time [ns] td(on)", "Delay Time On t_d(on) [ns] (Inductive)", "td(on) [ns] Typ./Max. – Gate Turn-On Delay", "Turn-On Delay t_d(ON) [ns]", "t_d(on) [ns] (10% VGS to 10% ID)"]
            },
            "possible_units": ["ns"],
            "std_unit": "ns",
            "scenarios": [
                {
                    "condition": "VDD=rated/2, ID=rated, RG=specified, VGS=10V",
                    "limits": {
                        "HV_Power_THT": [20, 30, 50, 75, 100, 150],
                        "MV_Power_SMD": [10, 15, 20, 30, 50, 75],
                        "LV_Logic_Level": [3, 5, 8, 10, 15, 25],
                        "SiC_High_Voltage": [12, 18, 25, 35],
                        "GaN_High_Frequency": [2, 4, 6, 10, 15],
                        "RF_Power": [5, 10, 15],
                        "Dual_N_Channel": [5, 10, 20],
                        "Dual_P_Channel": [8, 15],
                        "Complementary_Pair": [12, 25],
                        "Depletion_Mode": [10, 30, 75]
                    }
                }
            ]
        },
        {
            "key": "tr",
            "symbol": "t<sub>r</sub>",
            "spec_type": "nominal",
            "column_model": "TYP_MAX",
            "engineering_class": "NOMINAL_PARAMETER",
            "special_semantics": "NONE",
            "llm_context": {
                "formal_name": "Rise Time",
                "aliases": ["t_r [ns] Typ./Max.", "Rise Time t_r [ns] – Turn-On", "tr [ns] – Current Rise Time (10%→90% ID)", "Turn-On Rise Time t_r [ns] (Inductive Load)", "t_r [ns] Typ. Max. (10%–90% I_D)", "t(r) [ns] – Current Rise Time (Inductive Test)", "t_RISE [ns] Typ./Max.", "Rise Time t_r [ns] (ID 10% to 90%)", "tr [ns] Typ./Max. – Turn-On Transition (ID: 10→90%)"]
            },
            "possible_units": ["ns"],
            "std_unit": "ns",
            "scenarios": [
                {
                    "condition": "VDD=rated/2, ID=rated, RG=specified",
                    "limits": {
                        "HV_Power_THT": [30, 50, 75, 100, 150, 200],
                        "MV_Power_SMD": [20, 30, 50, 80, 120, 150],
                        "LV_Logic_Level": [3, 5, 10, 15, 25, 40],
                        "SiC_High_Voltage": [15, 23, 35, 50],
                        "GaN_High_Frequency": [2, 4, 8, 12, 20],
                        "RF_Power": [8, 15, 25],
                        "Dual_N_Channel": [8, 15, 30],
                        "Dual_P_Channel": [12, 25],
                        "Complementary_Pair": [20, 40],
                        "Depletion_Mode": [20, 50, 150]
                    }
                }
            ]
        },
        {
            "key": "td_off",
            "symbol": "t<sub>d(off)</sub>",
            "spec_type": "nominal",
            "column_model": "TYP_MAX",
            "engineering_class": "NOMINAL_PARAMETER",
            "special_semantics": "NONE",
            "llm_context": {
                "formal_name": "Turn-Off Delay Time",
                "aliases": ["t_d(off) [ns] Typ./Max.", "Turn-Off Delay t_d(off) [ns]", "td(off) [ns] – Delay Time Turn-Off (Inductive Load)", "t_d(off) [ns] Typ. Max.", "Turn-Off Delay Time [ns] td(off)", "Delay Time Off t_d(off) [ns] (Inductive)", "td(off) [ns] Typ./Max. – Gate Turn-Off Delay", "Turn-Off Delay t_d(OFF) [ns]", "t_d(off) [ns] (90% VGS to 90% ID)"]
            },
            "possible_units": ["ns"],
            "std_unit": "ns",
            "scenarios": [
                {
                    "condition": "VDD=rated/2, ID=rated, RG=specified",
                    "limits": {
                        "HV_Power_THT": [50, 75, 100, 150, 200, 300],
                        "MV_Power_SMD": [20, 30, 50, 75, 100, 150],
                        "LV_Logic_Level": [5, 10, 15, 20, 30, 50],
                        "SiC_High_Voltage": [20, 30, 45, 60],
                        "GaN_High_Frequency": [3, 6, 10, 15, 25],
                        "RF_Power": [10, 20, 30],
                        "Dual_N_Channel": [10, 20, 40],
                        "Dual_P_Channel": [15, 30],
                        "Complementary_Pair": [25, 50],
                        "Depletion_Mode": [20, 50, 150]
                    }
                }
            ]
        },
        {
            "key": "tf",
            "symbol": "t<sub>f</sub>",
            "spec_type": "nominal",
            "column_model": "TYP_MAX",
            "engineering_class": "NOMINAL_PARAMETER",
            "special_semantics": "NONE",
            "llm_context": {
                "formal_name": "Fall Time",
                "aliases": ["t_f [ns] Typ./Max.", "Fall Time t_f [ns] – Turn-Off", "tf [ns] – Current Fall Time (90%→10% ID)", "Turn-Off Fall Time t_f [ns] (Inductive Load)", "t_f [ns] Typ. Max. (90%–10% I_D)", "t(f) [ns] – Current Fall Time (Inductive Test)", "t_FALL [ns] Typ./Max.", "Fall Time t_f [ns] (ID 90% to 10%)", "tf [ns] Typ./Max. – Turn-Off Transition (ID: 90→10%)"]
            },
            "possible_units": ["ns"],
            "std_unit": "ns",
            "scenarios": [
                {
                    "condition": "VDD=rated/2, ID=rated, RG=specified",
                    "limits": {
                        "HV_Power_THT": [40, 60, 100, 150, 200, 300],
                        "MV_Power_SMD": [20, 30, 50, 75, 120, 180],
                        "LV_Logic_Level": [4, 8, 12, 20, 30, 50],
                        "SiC_High_Voltage": [18, 28, 42, 56],
                        "GaN_High_Frequency": [3, 5, 10, 15, 25],
                        "RF_Power": [10, 20, 30],
                        "Dual_N_Channel": [10, 20, 40],
                        "Dual_P_Channel": [15, 30],
                        "Complementary_Pair": [25, 50],
                        "Depletion_Mode": [25, 60, 180]
                    }
                }
            ]
        },
        {
            "key": "eon",
            "symbol": "E<sub>on</sub>",
            "spec_type": "nominal",
            "column_model": "TYP_MAX",
            "engineering_class": "NOMINAL_PARAMETER",
            "special_semantics": "NONE",
            "llm_context": {
                "formal_name": "Turn-On Switching Energy",
                "aliases": ["E_on [µJ] Typ./Max.", "Turn-On Energy E_on [µJ]", "Eon [µJ] – Turn-On Switching Loss (Inductive Load)", "E_on [mJ] Typ. Max.", "Switching Loss (On) E_on [µJ]", "E(on) [µJ] Typ.", "Turn-On Energy Loss E_on [µJ] (Inductive)", "E_on [µJ] (Turn-On, Hard Switching)"]
            },
            "possible_units": ["µJ", "mJ"],
            "std_unit": "µJ",
            "scenarios": [
                {
                    "condition": "VDD=rated/2, ID=rated, RG=specified, Tj=25°C",
                    "limits": {
                        "HV_Power_THT": [500, 1000, 2000, 3000, 5000, 8000],
                        "MV_Power_SMD": [50, 100, 200, 400, 800, 1500],
                        "LV_Logic_Level": [5, 10, 20, 40, 80, 150],
                        "SiC_High_Voltage": [200, 350, 600, 900],
                        "GaN_High_Frequency": [10, 20, 40, 80, 150],
                        "RF_Power": [50, 100, 200],
                        "Dual_N_Channel": [20, 50, 100],
                        "Dual_P_Channel": [30, 75],
                        "Complementary_Pair": [60, 150],
                        "Depletion_Mode": [100, 300, 1000]
                    }
                }
            ]
        },
        {
            "key": "eoff",
            "symbol": "E<sub>off</sub>",
            "spec_type": "nominal",
            "column_model": "TYP_MAX",
            "engineering_class": "NOMINAL_PARAMETER",
            "special_semantics": "NONE",
            "llm_context": {
                "formal_name": "Turn-Off Switching Energy",
                "aliases": ["E_off [µJ] Typ./Max.", "Turn-Off Energy E_off [µJ]", "Eoff [µJ] – Turn-Off Switching Loss (Inductive Load)", "E_off [mJ] Typ. Max.", "Switching Loss (Off) E_off [µJ]", "E(off) [µJ] Typ.", "Turn-Off Energy Loss E_off [µJ] (Inductive)", "E_off [µJ] (Turn-Off, Hard Switching)"]
            },
            "possible_units": ["µJ", "mJ"],
            "std_unit": "µJ",
            "scenarios": [
                {
                    "condition": "VDD=rated/2, ID=rated, RG=specified, Tj=25°C",
                    "limits": {
                        "HV_Power_THT": [300, 600, 1200, 2000, 3500, 6000],
                        "MV_Power_SMD": [30, 60, 120, 250, 500, 1000],
                        "LV_Logic_Level": [3, 6, 12, 25, 50, 100],
                        "SiC_High_Voltage": [100, 180, 320, 480],
                        "GaN_High_Frequency": [5, 10, 20, 40, 80],
                        "RF_Power": [30, 60, 120],
                        "Dual_N_Channel": [12, 30, 60],
                        "Dual_P_Channel": [18, 45],
                        "Complementary_Pair": [36, 90],
                        "Depletion_Mode": [60, 180, 600]
                    }
                }
            ]
        },
        {
            "key": "etot",
            "symbol": "E<sub>tot</sub>",
            "spec_type": "nominal",
            "column_model": "TYP_MAX",
            "engineering_class": "NOMINAL_PARAMETER",
            "special_semantics": "NONE",
            "llm_context": {
                "formal_name": "Total Switching Energy",
                "aliases": ["E_tot [µJ] Typ./Max. (Eon + Eoff)", "Total Switching Energy E_tot [µJ] (Eon+Eoff)", "Etot [µJ] – Total Energy Loss Per Cycle", "E_sw(total) [µJ] (= E_on + E_off, Inductive Load)", "Total Switching Loss E_tot [mJ]", "E(tot) [µJ] Typ./Max. (Sum of Eon + Eoff)", "E_total [µJ] – Per-Cycle Switching Energy (Inductive)", "Etot [µJ] = E_on + E_off", "Total Energy E_tot [µJ] (Hard Switch)"]
            },
            "possible_units": ["µJ", "mJ"],
            "std_unit": "µJ",
            "scenarios": [
                {
                    "condition": "VDD=rated/2, ID=rated, RG=specified, Tj=25°C",
                    "limits": {
                        "HV_Power_THT": [800, 1600, 3200, 5000, 8500, 14000],
                        "MV_Power_SMD": [80, 160, 320, 650, 1300, 2500],
                        "LV_Logic_Level": [8, 16, 32, 65, 130, 250],
                        "SiC_High_Voltage": [300, 530, 920, 1380],
                        "GaN_High_Frequency": [15, 30, 60, 120, 230],
                        "RF_Power": [80, 160, 320],
                        "Dual_N_Channel": [32, 80, 160],
                        "Dual_P_Channel": [48, 120],
                        "Complementary_Pair": [96, 240],
                        "Depletion_Mode": [160, 480, 1600]
                    }
                }
            ]
        }
    ],

    # ==========================================================================
    # THERMAL CHARACTERISTICS
    # ==========================================================================
    "THERMAL_CHAR": [
        {
            "key": "thermal_resistance_jc",
            "symbol": "R<sub>θJC</sub>",
            "spec_type": "max_limit",
            "column_model": "TYP_MAX",
            "engineering_class": "NOMINAL_PARAMETER",
            "special_semantics": "NONE",
            "llm_context": {
                "formal_name": "Thermal Resistance Junction to Case",
                "aliases": ["R_θJC [°C/W] Typ./Max. (Steady State, Drain Tab)", "Rth(j-c) [°C/W] Max. – Junction to Case", "Thermal Res. J-C θ_JC [°C/W] (Drain Tab, SS)", "R_TH(JC) [°C/W] Max. (Steady-State, Drain Mounted)", "θ_JC [°C/W] – Junction to Case (Steady State)", "R(θJC) [K/W] Max. (Drain = Thermal Contact)", "Theta JC [°C/W] Max. – R_θJC (Steady State)", "Rth J→C [°C/W] Max. (Case = Drain Tab, SS)", "Thermal Impedance J-C R_θJC [°C/W] Typ./Max.", "θ(JC) [°C/W] Max – Refer to Normalized Thermal Curve"]
            },
            "possible_units": ["°C/W"],
            "std_unit": "°C/W",
            "scenarios": [
                {
                    "condition": "Steady state, drain-tab",
                    "limits": {
                        "HV_Power_THT": [0.3, 0.4, 0.5, 0.6, 0.8, 1.0, 1.5, 2.0],
                        "MV_Power_SMD": [0.5, 0.8, 1.0, 1.2, 1.5, 2.0, 2.5, 3.0],
                        "LV_Logic_Level": [10, 15, 20, 30, 50, 80, 125],
                        "SiC_High_Voltage": [0.6, 0.9, 1.2, 1.5, 1.8],
                        "GaN_High_Frequency": [1.0, 1.5, 2.5, 4.0, 6.0],
                        "RF_Power": [1.0, 2.0, 3.0, 5.0],
                        "Dual_N_Channel": [20, 40, 60, 100],
                        "Dual_P_Channel": [30, 60],
                        "Complementary_Pair": [50, 100],
                        "Depletion_Mode": [5, 10, 20, 50, 100]
                    }
                }
            ]
        },
        {
            "key": "thermal_resistance_ja",
            "symbol": "R<sub>θJA</sub>",
            "spec_type": "max_limit",
            "column_model": "TYP_MAX",
            "engineering_class": "NOMINAL_PARAMETER",
            "special_semantics": "NONE",
            "llm_context": {
                "formal_name": "Thermal Resistance Junction to Ambient",
                "aliases": ["R_θJA [°C/W] Typ./Max. (Standard PCB, Still Air)", "Rth(j-a) [°C/W] Max. – PCB Mount, Still Air", "Thermal Res. J-A θ_JA [°C/W] (1oz Cu, Still Air)", "R_TH(JA) [°C/W] Max. (Standard PCB, No Forced Air)", "θ_JA [°C/W] – Junction to Ambient (Free Convection)", "R(θJA) [K/W] Max. (FR4 PCB, 1oz Cu, Still Air)", "Theta JA [°C/W] Max. – R_θJA (PCB, No Heat Sink)", "Rth J→A [°C/W] Max. (Standard PCB, No Airflow)", "Thermal Impedance J-A R_θJA [°C/W] (Still Air)", "θ(JA) [°C/W] Max – Standard PCB, No Forced Cooling"]
            },
            "possible_units": ["°C/W"],
            "std_unit": "°C/W",
            "scenarios": [
                {
                    "condition": "Standard PCB, still air",
                    "limits": {
                        "HV_Power_THT": [40, 50, 60, 70, 85, 100],
                        "MV_Power_SMD": [40, 50, 62, 80, 100, 125],
                        "LV_Logic_Level": [100, 125, 150, 200, 250, 400],
                        "SiC_High_Voltage": [35, 45, 55, 70],
                        "GaN_High_Frequency": [50, 70, 100, 150],
                        "RF_Power": [40, 60, 80],
                        "Dual_N_Channel": [150, 200, 300],
                        "Dual_P_Channel": [200, 300],
                        "Complementary_Pair": [250, 350],
                        "Depletion_Mode": [100, 150, 200, 300]
                    }
                }
            ]
        },
        {
            "key": "thermal_resistance_cs",
            "symbol": "R<sub>θCS</sub>",
            "spec_type": "nominal",
            "column_model": "TYP_ONLY",
            "engineering_class": "NOMINAL_PARAMETER",
            "special_semantics": "NOT_APPLICABLE",
            "llm_context": {
                "formal_name": "Thermal Resistance Case to Sink",
                "aliases": ["R_θCS [°C/W] Typ. (With Thermal Interface Material)", "Rth(c-s) [°C/W] – Case to Heat Sink (With TIM)", "Thermal Res. C-S θ_CS [°C/W] (Greased Interface)", "R_TH(CS) [°C/W] Typ. (Thermal Interface Material)", "θ_CS [°C/W] – Case to Sink (Insulation Pad Incl.)", "R(θCS) [K/W] Typ. (Contact: Case-to-Heatsink, TIM)", "Theta CS [°C/W] Typ. – R_θCS (With/Without TIM)", "Rth C→S [°C/W] Typ. (Thermal Pad, Greased)", "Thermal Contact Resistance C-S [°C/W] (TIM Dep.)", "θ(CS) [°C/W] Typ. (See Thermal Model Note)"]
            },
            "possible_units": ["°C/W"],
            "std_unit": "°C/W",
            "scenarios": [
                {
                    "condition": "With thermal interface material",
                    "limits": {
                        "HV_Power_THT": [0.1, 0.15, 0.2, 0.25, 0.3, 0.5],
                        "MV_Power_SMD": [0],
                        "LV_Logic_Level": [0],
                        "SiC_High_Voltage": [0.15, 0.2, 0.3],
                        "GaN_High_Frequency": [0],
                        "RF_Power": [0.2, 0.3, 0.5],
                        "Dual_N_Channel": [0],
                        "Dual_P_Channel": [0],
                        "Complementary_Pair": [0],
                        "Depletion_Mode": [0.25, 0.4]
                    }
                }
            ]
        },
        {
            "key": "transient_thermal_impedance_jc",
            "symbol": "Z<sub>θJC</sub>",
            "spec_type": "nominal",
            "column_model": "TYP_ONLY",
            "engineering_class": "NOMINAL_PARAMETER",
            "special_semantics": "NONE",
            "llm_context": {
                "formal_name": "Transient Thermal Impedance Junction to Case",
                "aliases": ["Z_θJC [°C/W] Typ. (Single Pulse, Various t_p)", "Transient Thermal Impedance Z_th(JC) [°C/W] (Pulse)", "Pulse Thermal Impedance Z_θJC [°C/W] (See Fig.)", "Z_TH(JC) [°C/W] – See Normalized Thermal Impedance Curve", "Transient Therm. Impedance Z(θJC) [°C/W] vs. t_p", "Z_θJC(t) [°C/W] (Single Pulse, f(pulse width))", "Thermal Impedance (Transient) Z_JC [°C/W] (Fig. X)", "Z_TH(JC) [°C/W] – Normalized Pulse Thermal Curve", "ZθJC [°C/W] Typ. (Single Pulse; See Duty Cycle Graph)"]
            },
            "possible_units": ["°C/W"],
            "std_unit": "°C/W",
            "scenarios": [
                {
                    "condition": "Single pulse, various durations",
                    "limits": {
                        "HV_Power_THT": [0.15, 0.2, 0.25, 0.3, 0.4, 0.5],
                        "MV_Power_SMD": [0.25, 0.4, 0.5, 0.6, 0.75, 1.0],
                        "LV_Logic_Level": [5, 7.5, 10, 15, 25, 40],
                        "SiC_High_Voltage": [0.3, 0.45, 0.6, 0.75],
                        "GaN_High_Frequency": [0.5, 0.75, 1.25, 2.0],
                        "RF_Power": [0.5, 1.0, 1.5],
                        "Dual_N_Channel": [10, 20, 30],
                        "Dual_P_Channel": [15, 30],
                        "Complementary_Pair": [25, 50],
                        "Depletion_Mode": [2.5, 5, 10, 25]
                    }
                }
            ]
        },
        {
            "key": "operating_junction_temp_range",
            "symbol": "T<sub>J</sub>",
            "spec_type": "operational_range",
            "column_model": "MIN_MAX",
            "engineering_class": "OPERATING_CONDITION",
            "special_semantics": "NONE",
            "llm_context": {
                "formal_name": "Operating Junction Temperature Range",
                "aliases": ["T_J [°C] Operating Range (Min. to Max.)", "Operating Temp. T_J [°C] (Min/Max, Continuous)", "TJ Range [°C] – Junction Temp. Operating Limits", "T_J(op) [°C] Min. to Max. (Continuous Operation)", "Junction Temp. Range T_J [°C] (Operating, See Derating)", "T_J [°C] Operating (Lower Limit to Upper Limit)", "Junction Temperature Range [°C] T_J (Min. / Max.)", "T_J [°C] – Min. to Max. (Operating, Continuous)", "Channel Temp. Range T_J [°C] Min./Max. (Continuous)"]
            },
            "possible_units": ["°C"],
            "std_unit": "°C",
            "scenarios": [
                {
                    "condition": "Operating",
                    "limits": {
                        "HV_Power_THT": [[-55, 150], [-55, 175]],
                        "MV_Power_SMD": [[-55, 150], [-55, 175]],
                        "LV_Logic_Level": [[-55, 150], [-55, 175]],
                        "SiC_High_Voltage": [[-55, 175], [-40, 200]],
                        "GaN_High_Frequency": [[-55, 150], [-55, 175], [-40, 200]],
                        "RF_Power": [[-65, 200], [-55, 225]],
                        "Dual_N_Channel": [[-55, 150], [-55, 175]],
                        "Dual_P_Channel": [[-55, 150]],
                        "Complementary_Pair": [[-55, 150]],
                        "Depletion_Mode": [[-55, 150], [-55, 175]]
                    }
                }
            ]
        }
    ],

    # ==========================================================================
    # PACKAGE & MECHANICAL  
    # ==========================================================================
    "PACKAGE": [
        {
            "key": "package_code",
            "symbol": "PKG",
            "spec_type": "mechanical",
            "column_model": "TYP_ONLY",
            "engineering_class": "MECHANICAL",
            "special_semantics": "NONE",
            "llm_context": {
                "formal_name": "Package Type",
                "aliases": ["PKG – Package / Case Style (e.g., TO-220, DPAK)", "Case Style / Package Code (e.g., TO-247, D2PAK)", "Package Outline (e.g., TO-263, PowerPAK SO-8)", "PKG Code (e.g., TO-220AB, DFN 5×6, TOLL)", "Case Type – SMD / THT / Flange (e.g., TO-252)", "Package (e.g., SOT-23, SOT-223, DFN_3x3)", "Component Package – Case Outline (JEDEC Ref.)", "Pkg. Type (e.g., PQFN, DirectFET, TO-264)", "Package Code / Outline Designation (JEDEC/IEC)", "Case / Package (e.g., ITO-220, TO-3P, NI-780)"]
            },
            "possible_units": [""],
            "std_unit": "",
            "scenarios": [
                {
                    "condition": "N/A",
                    "limits": {
                        "HV_Power_THT": ["TO-220", "TO-220AB", "TO-247", "TO-3P", "TO-264", "ITO-220", "TO-220FP"],
                        "MV_Power_SMD": ["DPAK(TO-252)", "D2PAK(TO-263)", "TO-263-7", "PowerPAK_SO-8", "PQFN_5x6", "DFN_5x6", "TOLL", "DirectFET"],
                        "LV_Logic_Level": ["SOT-23", "SOT-23-3", "SOT-23-6", "SOT-323", "SC-70", "SOT-223", "TSOP-6", "DFN_2x2", "DFN_3x3", "SON"],
                        "SiC_High_Voltage": ["TO-247-3", "TO-247-4", "TO-263-7", "D2PAK-7L"],
                        "GaN_High_Frequency": ["PQFN_5x6", "DFN_5x6", "DFN_8x8", "TOLL"],
                        "RF_Power": ["TO-220", "TO-247", "Flange_Mount", "NI-780", "NI-1230"],
                        "Dual_N_Channel": ["SOT-23-6", "SOT-363", "SC-70-6", "TSOP-6", "DFN_3x3", "PowerPAK_SO-8"],
                        "Dual_P_Channel": ["SOT-23-6", "SOT-363", "SC-70-6", "TSOP-6"],
                        "Complementary_Pair": ["SOT-23-6", "SOT-363", "SC-70-6"],
                        "Depletion_Mode": ["TO-220", "TO-252", "SOT-23", "SOT-89"]
                    }
                }
            ]
        },
        {
            "key": "pin_configuration",
            "symbol": "PIN",
            "spec_type": "mechanical",
            "column_model": "TYP_ONLY",
            "engineering_class": "MECHANICAL",
            "special_semantics": "NONE",
            "llm_context": {
                "formal_name": "Pin Configuration",
                "aliases": ["PIN – Pinout (e.g., G-D-S, G-D-S-Kelvin_S)", "Pin Assignment (e.g., Gate-Drain-Source Order)", "Pinout Code (e.g., G-D-S, S-G-S-D-D-D-D-D)", "Terminal Arrangement (G/D/S – See Package Dwg.)", "Pin Config. (e.g., Dual: G1-S1-S2-G2-D1-D2)", "Lead Assignment – G / D / S (See Outline Fig.)", "Pin Order (Gate-Source-Drain, Package Dependent)", "Electrode Configuration (G-D-S or G-D-S-Kelvin)", "Terminal Identification (G / D / S; See Marking)", "Pinout (e.g., SOT-23: Pin1=G, Pin2=S, Pin3=D)"]
            },
            "possible_units": [""],
            "std_unit": "",
            "scenarios": [
                {
                    "condition": "N/A",
                    "limits": {
                        "HV_Power_THT": ["G-D-S", "G-D-S-S"],
                        "MV_Power_SMD": ["G-D-S", "S-G-S-D-D-D-D-D"],
                        "LV_Logic_Level": ["G-S-D", "G-D-S", "S-G-D"],
                        "SiC_High_Voltage": ["G-D-S-Kelvin_S"],
                        "GaN_High_Frequency": ["G-S-D", "S-G-D-S"],
                        "RF_Power": ["G-D-S"],
                        "Dual_N_Channel": ["G1-S1-S2-G2-D1-D2", "G1-S1-D1-D2-S2-G2"],
                        "Dual_P_Channel": ["G1-S1-S2-G2-D1-D2"],
                        "Complementary_Pair": ["GN-SN-SP-GP-DN-DP"],
                        "Depletion_Mode": ["G-D-S"]
                    }
                }
            ]
        },
        {
            "key": "mounting_type",
            "symbol": "MNT",
            "spec_type": "mechanical",
            "column_model": "TYP_ONLY",
            "engineering_class": "MECHANICAL",
            "special_semantics": "NONE",
            "llm_context": {
                "formal_name": "Mounting Type",
                "aliases": ["MNT – Mounting Type (THT / SMD / Flange)", "Mounting Style (Through_Hole / SMD / Chassis)", "Mount Type (e.g., SMD, Through-Hole, Stud)", "Assembly Method – SMD / THT / Flange Mount", "Mounting (SMD with Tab / Through-Hole / Chassis)", "PCB Mount Style – SMD or Through Hole", "Mounting Configuration (SMD / THT / Stud Mount)", "MNT (e.g., Through_Hole, Flange_Mount, SMD_Tab)", "Board Mount Type – SMT / THT / Chassis", "Mounting Category (SMD = Reflow; THT = Wave/Hand)"]
            },
            "possible_units": [""],
            "std_unit": "",
            "scenarios": [
                {
                    "condition": "N/A",
                    "limits": {
                        "HV_Power_THT": ["Through_Hole", "Chassis_Mount"],
                        "MV_Power_SMD": ["SMD", "SMD_with_Tab"],
                        "LV_Logic_Level": ["SMD"],
                        "SiC_High_Voltage": ["Through_Hole", "Chassis_Mount"],
                        "GaN_High_Frequency": ["SMD"],
                        "RF_Power": ["Through_Hole", "Flange_Mount", "Stud_Mount"],
                        "Dual_N_Channel": ["SMD"],
                        "Dual_P_Channel": ["SMD"],
                        "Complementary_Pair": ["SMD"],
                        "Depletion_Mode": ["Through_Hole", "SMD"]
                    }
                }
            ]
        },
        {
            "key": "polarity",
            "symbol": "POL",
            "spec_type": "mechanical",
            "column_model": "TYP_ONLY",
            "engineering_class": "MECHANICAL",
            "special_semantics": "NONE",
            "llm_context": {
                "formal_name": "Channel Polarity",
                "aliases": ["POL – Channel Type (N-Channel / P-Channel)", "N-Channel or P-Channel (Enhancement / Depletion)", "MOSFET Type – N / P Channel (Enhancement Mode)", "Channel Polarity (N-Ch., P-Ch., Complementary)", "Device Type – N-Channel / P-Channel MOSFET", "Polarity (N = Low-Side; P = High-Side Typical)", "Channel Type N/P (See V_GS(th) Polarity)", "N-Channel Enhancement Mode / P-Channel (POL)", "Type – N-Ch. / P-Ch. / Dual-N / Complementary", "MOSFET Polarity (N-Channel or P-Channel, Mode)"]
            },
            "possible_units": [""],
            "std_unit": "",
            "scenarios": [
                {
                    "condition": "N/A",
                    "limits": {
                        "HV_Power_THT": ["N-Channel"],
                        "MV_Power_SMD": ["N-Channel", "P-Channel"],
                        "LV_Logic_Level": ["N-Channel", "P-Channel"],
                        "SiC_High_Voltage": ["N-Channel"],
                        "GaN_High_Frequency": ["N-Channel", "P-Channel"],
                        "RF_Power": ["N-Channel"],
                        "Dual_N_Channel": ["Dual_N-Channel"],
                        "Dual_P_Channel": ["Dual_P-Channel"],
                        "Complementary_Pair": ["N+P_Channel"],
                        "Depletion_Mode": ["N-Channel", "P-Channel"]
                    }
                }
            ]
        },
        {
            "key": "lead_finish",
            "symbol": "FINISH",
            "spec_type": "mechanical",
            "column_model": "TYP_ONLY",
            "engineering_class": "MECHANICAL",
            "special_semantics": "NONE",
            "llm_context": {
                "formal_name": "Terminal Finish",
                "aliases": ["Lead Finish / Terminal Plating (e.g., Matte Sn)", "Contact Plating – RoHS Compliant (e.g., NiPdAu)", "Terminal Finish (e.g., 100% Matte Tin, SnPb)", "Lead Plating Material (e.g., Au, Matte_Sn)", "FINISH – Termination Plating (RoHS / Non-RoHS)", "Solder Finish – Lead-Free (e.g., NiPdAu, Matte Sn)", "Lead / Terminal Finish Code (e.g., Sn, SnPb, Au)", "Electrode Plating (e.g., 100% Sn, Au Flash)", "Terminal Material (e.g., Matte Tin, Ni/Pd/Au)", "Lead Finish (RoHS: Matte Sn / Non-RoHS: SnPb)"]
            },
            "possible_units": [""],
            "std_unit": "",
            "scenarios": [
                {
                    "condition": "N/A",
                    "limits": {
                        "HV_Power_THT": ["Matte_Sn", "SnPb"],
                        "MV_Power_SMD": ["Matte_Sn", "NiPdAu"],
                        "LV_Logic_Level": ["Matte_Sn", "NiPdAu"],
                        "SiC_High_Voltage": ["Matte_Sn"],
                        "GaN_High_Frequency": ["NiPdAu", "Matte_Sn"],
                        "RF_Power": ["Au", "Matte_Sn"],
                        "Dual_N_Channel": ["Matte_Sn"],
                        "Dual_P_Channel": ["Matte_Sn"],
                        "Complementary_Pair": ["Matte_Sn"],
                        "Depletion_Mode": ["Matte_Sn", "SnPb"]
                    }
                }
            ]
        },
        {
            "key": "weight",
            "symbol": "W",
            "spec_type": "mechanical",
            "column_model": "TYP_ONLY",
            "engineering_class": "MECHANICAL",
            "special_semantics": "NONE",
            "llm_context": {
                "formal_name": "Weight",
                "aliases": ["Mass", "Part Weight"]
            },
            "possible_units": ["g", "mg"],
            "std_unit": "g",
            "scenarios": [
                {
                    "condition": "",
                    "limits": {
                        "HV_Power_THT": [1.5, 2, 3, 5, 8, 15],
                        "MV_Power_SMD": [0.1, 0.2, 0.4, 0.8, 1.5],
                        "LV_Logic_Level": [0.002, 0.005, 0.01, 0.02, 0.05],
                        "SiC_High_Voltage": [3, 5, 8],
                        "GaN_High_Frequency": [0.2, 0.5, 1],
                        "RF_Power": [10, 20, 50, 100],
                        "Dual_N_Channel": [0.01, 0.02, 0.05],
                        "Dual_P_Channel": [0.01, 0.02],
                        "Complementary_Pair": [0.02, 0.05],
                        "Depletion_Mode": [1, 2, 5]
                    }
                }
            ]
        }
    ],

    # ==========================================================================
    # RELIABILITY & QUALITY
    # ==========================================================================
    "RELIABILITY": [
        {
            "key": "failure_rate",
            "symbol": "λ",
            "spec_type": "max_limit",
            "column_model": "MAX_ONLY",
            "engineering_class": "RELIABILITY",
            "special_semantics": "NONE",
            "llm_context": {
                "formal_name": "Failure Rate",
                "aliases": ["λ [FIT] Max. (Standard Conditions)", "FIT Rate λ [FIT] Max.", "Failure Rate λ [FIT] (Per 10⁹ Device Hours)", "Lambda [FIT] – Failure Rate (Standard Conditions)", "FIT [failures/10⁹h] Max.", "λ [PPM/%/1000h] – Reliability (Standard Conditions)", "MTBF Equivalent λ [FIT] Max.", "λ_FIT Max. (Per MIL-HDBK-217 / IEC 62380)", "Failure Rate λ [FIT] (Ref. JEDEC JESD74 Method)"]
            },
            "possible_units": ["FIT", "PPM"],
            "std_unit": "FIT",
            "scenarios": [
                {
                    "condition": "Standard conditions",
                    "limits": {
                        "HV_Power_THT": [1, 5, 10],
                        "MV_Power_SMD": [1, 5, 10],
                        "LV_Logic_Level": [0.5, 1, 5],
                        "SiC_High_Voltage": [5, 10],
                        "GaN_High_Frequency": [5, 10],
                        "RF_Power": [5, 10],
                        "Dual_N_Channel": [1, 5],
                        "Dual_P_Channel": [1, 5],
                        "Complementary_Pair": [2, 10],
                        "Depletion_Mode": [5, 10]
                    }
                }
            ]
        },
        {
            "key": "moisture_sensitivity_level",
            "symbol": "MSL",
            "spec_type": "nominal",
            "column_model": "TYP_ONLY",
            "engineering_class": "RELIABILITY",
            "special_semantics": "NOT_APPLICABLE",
            "llm_context": {
                "formal_name": "Moisture Sensitivity Level",
                "aliases": ["MSL (JEDEC J-STD-020) – SMD Only", "Moisture Sensitivity Level MSL [1-6] (J-STD-020E)", "MSL Rating – Per JEDEC J-STD-020 (SMD Packages)", "Moisture Sensitivity (MSL Class, Floor Life)", "MSL Level (J-STD-020; N/A for THT Packages)", "Moisture Sensitivity – IPC/JEDEC J-STD-020", "MSL (SMD: Level 1–3; THT: N/A)", "Moisture Sensitivity Rating MSL (JEDEC Standard)", "MSL Category (1=Unlimited; 2=1yr; 3=168h Floor Life)", "Moisture Sensitivity (MSL) Per J-STD-020 Rev. E"]
            },
            "possible_units": [""],
            "std_unit": "",
            "scenarios": [
                {
                    "condition": "Per J-STD-020",
                    "limits": {
                        "HV_Power_THT": [0],
                        "MV_Power_SMD": ["1", "2", "3"],
                        "LV_Logic_Level": ["1", "2"],
                        "SiC_High_Voltage": ["1", "2"],
                        "GaN_High_Frequency": ["1", "2", "3"],
                        "RF_Power": [0],
                        "Dual_N_Channel": ["1"],
                        "Dual_P_Channel": ["1"],
                        "Complementary_Pair": ["1"],
                        "Depletion_Mode": [0]
                    }
                }
            ]
        }
    ]
},
    # ==========================================================================
    # 5. VOLTAGE_REGULATOR חלק5
    # ==========================================================================
    
  "VOLTAGE_REGULATOR": {
    "archetypes": [
      "LDO_Low_Voltage_CMOS",
      "LDO_High_Voltage_Bipolar"
    ],
    "ABS_MAX": [
      {
        "key": "vin_max",
        "symbol": "V<sub>IN(max)</sub>",
        "spec_type": "max_rating",
        "column_model": "MAX_ONLY",
        "engineering_class": "SAFETY_LIMIT",
        "special_semantics": "NONE",
        "llm_context": {
          "formal_name": "Maximum Input Voltage",
          "aliases": ["V_IN(max) [V] – Absolute Maximum Input Voltage", "Input Voltage Max. V_IN [V] (Abs. Max., Do Not Exceed)", "Abs. Max. Input Voltage V_IN [V] (Note: Transients Included)", "V_IN(max) [V] – Supply Voltage Absolute Maximum", "Maximum Supply Voltage V_S [V] (Abs. Max.)", "V_IN Abs. Max. [V] (Continuous, No Transients)", "Input Voltage Rating V_IN [V] Max. (Abs.)", "V(IN) Max. [V] – Do Not Apply Above This Level", "Absolute Max. V_IN [V] (Input Pin, Cont. DC)"]
        },
        "possible_units": ["V"],
        "std_unit": "V",
        "scenarios": [
          {
            "condition": "",
            "limits": {
              "LDO_Low_Voltage_CMOS": [6.0, 7.0],
              "LDO_High_Voltage_Bipolar": [40, 60]
            }
          }
        ]
      },
      {
        "key": "vout_max",
        "symbol": "V<sub>OUT(max)</sub>",
        "spec_type": "max_rating",
        "column_model": "MAX_ONLY",
        "engineering_class": "SAFETY_LIMIT",
        "special_semantics": "NONE",
        "llm_context": {
          "formal_name": "Maximum Output Voltage",
          "aliases": ["V_OUT(max) [V] – Absolute Maximum Output Voltage", "Output Voltage Max. V_OUT [V] (Abs. Max.)", "Abs. Max. Output Voltage V_OUT [V]", "V_OUT Abs. Max. [V] (Do Not Exceed)", "Max. Output Voltage Rating V_O [V] (Abs.)", "V_OUT(max) [V] – Output Pin Absolute Maximum", "Absolute Max. V_OUT [V] (Output Terminal)", "Max. V_OUT [V] Abs. (Includes Load Transients)", "V(OUT) Abs. Max. [V] – Output Voltage Limit", "Output Voltage Rating V_OUT [V] (Abs. Max., Note 1)"]
        },
        "possible_units": ["V"],
        "std_unit": "V",
        "scenarios": [
          {
            "condition": "",
            "limits": {
              "LDO_Low_Voltage_CMOS": [5.5, 6.0],
              "LDO_High_Voltage_Bipolar": [30, 40]
            }
          }
        ]
      },
      {
        "key": "power_dissipation",
        "symbol": "P<sub>D</sub>",
        "spec_type": "max_rating",
        "column_model": "MAX_ONLY",
        "engineering_class": "SAFETY_LIMIT",
        "special_semantics": "NONE",
        "llm_context": {
          "formal_name": "Maximum Power Dissipation",
          "aliases": ["P_D [W/mW] Max.", "Power Dissipation P_D [mW] Max. (See Derating)", "Max. Power P_tot [W] (Linearly Derate Above)", "PD [mW] Max. (Derate to Zero at T_J(max))", "Total Power Dissipation P_D [W] (Abs. Max.)", "P_D(max) [mW] – Continuous (See θJA)", "Power Dissip. [W] Max.", "P_D [W] Abs. Max. (Refer to Derating Curve)", "Maximum Allowable Power P_D [mW] (Fig. X)"]
        },
        "possible_units": ["W", "mW"],
        "std_unit": "W",
        "scenarios": [
          {
            "condition": "Ta=25°C",
            "limits": {
              "LDO_Low_Voltage_CMOS": [0.3, 0.5, 1],
              "LDO_High_Voltage_Bipolar": [1, 2, 20]
            }
          }
        ]
      },
      {
        "key": "tj_max",
        "symbol": "T<sub>j(max)</sub>",
        "spec_type": "max_rating",
        "column_model": "MAX_ONLY",
        "engineering_class": "SAFETY_LIMIT",
        "special_semantics": "NONE",
        "llm_context": {
          "formal_name": "Maximum Junction Temperature",
          "aliases": ["T_j(max) [°C] – Maximum Junction Temperature", "Max. Junction Temp. T_J [°C] (Abs. Max.)", "Tj(max) [°C] – Internal Die Temp. Limit", "T_J Max. [°C] (Do Not Exceed, See Thermal Derating)", "Maximum Operating Junction Temp. T_J [°C]", "T_J(max) [°C] – Channel/Junction Temperature Limit", "Max. T_J [°C] (Abs. Max., All Conditions)", "Junction Temp. Limit T_j [°C] Abs. Max.", "T_JMAX [°C] – Thermal Shutdown Precedes This", "Tj [°C] Max. (Absolute Maximum, Per Thermal Model)"]
        },
        "possible_units": ["°C"],
        "std_unit": "°C",
        "scenarios": [
          {
            "condition": "",
            "limits": {
              "LDO_Low_Voltage_CMOS": [125, 150],
              "LDO_High_Voltage_Bipolar": [125, 150]
            }
          }
        ]
      },
      {
        "key": "storage_temp",
        "symbol": "T<sub>STG</sub>",
        "spec_type": "max_rating",
        "column_model": "MIN_MAX",
        "engineering_class": "SAFETY_LIMIT",
        "special_semantics": "NONE",
        "llm_context": {
          "formal_name": "Storage Temperature Range",
          "aliases": ["T_STG [°C] Storage Temp. Range (Min. to Max.)", "Storage Temperature T_STG [°C] (Non-Operating)", "T_stg Range [°C] (Non-Operating, Unpowered)", "T_S [°C] Storage (Min./Max., Non-Operational)", "Storage Temp. T_STG [°C] – Non-Operating Range", "T_storage [°C] Min. Max. (Device Unpowered)", "Storage Temperature Range [°C] T_stg (Min/Max)", "Non-Operating Storage Temp. [°C] T_STG Range", "T_STG [°C] – Component Storage (Unpowered, Min–Max)"]
        },
        "possible_units": ["°C"],
        "std_unit": "°C",
        "scenarios": [
          {
            "condition": "Range",
            "limits": {
              "LDO_Low_Voltage_CMOS": ["-65 to 150"],
              "LDO_High_Voltage_Bipolar": ["-65 to 150"]
            }
          }
        ]
      },
      {
        "key": "esd_hbm",
        "symbol": "V<sub>ESD</sub>",
        "spec_type": "max_rating",
        "column_model": "MIN_ONLY",
        "engineering_class": "SAFETY_LIMIT",
        "special_semantics": "NONE",
        "llm_context": {
          "formal_name": "ESD Human Body Model",
          "aliases": ["V_ESD (HBM) [kV] – Human Body Model Rating", "ESD HBM [kV] Min. (ANSI/ESDA/JEDEC JS-001)", "ESD HBM Class [kV] – Per JEDEC JESD22-A114", "V_ESD [kV] (Human Body Model, All Pins)", "ESD Rating V_ESD [kV] (HBM, JS-001 Test Method)", "Electrostatic Discharge HBM [kV] Min.", "ESD HBM [kV] – All Pins to GND (JEDEC Class ?)", "V(ESD) HBM [kV] Min. (Per ANSI/ESDA/JEDEC JS-001)"]
        },
        "possible_units": ["kV"],
        "std_unit": "kV",
        "scenarios": [
          {
            "condition": "HBM",
            "limits": {
              "LDO_Low_Voltage_CMOS": [1, 2, 4],
              "LDO_High_Voltage_Bipolar": [2, 4]
            }
          }
        ]
      },
      {
        "key": "reverse_current",
        "symbol": "I<sub>REV</sub>",
        "spec_type": "max_rating",
        "column_model": "MAX_ONLY",
        "engineering_class": "SAFETY_LIMIT",
        "special_semantics": "NONE",
        "llm_context": {
          "formal_name": "Maximum Reverse Current",
          "aliases": ["I_REV [mA] Max. (V_OUT > V_IN Condition)", "Reverse Current I_REV [mA] Max. (V_OUT > V_IN)", "Max. Reverse Current I_R [mA] (Output > Input)", "I_REV [mA] – Max. Allowable Reverse (V_OUT > V_IN)", "Reverse Input Current I_REV [mA] Max. (Boost Condition)", "I(REV) [mA] Max. – Anti-Reverse Condition", "Max. Reverse I [mA] (V_OUT Applied > V_IN, Unpowered)", "Reverse Current Limit I_REV [mA] (Output Backfeed)", "Max. Reverse I_R [mA] (Output Exceeds Input Voltage)"]
        },
        "possible_units": ["mA"],
        "std_unit": "mA",
        "scenarios": [
          {
            "condition": "Vout > Vin",
            "limits": {
              "LDO_Low_Voltage_CMOS": [10, 50],
              "LDO_High_Voltage_Bipolar": [50, 100]
            }
          }
        ]
      },
      {
        "key": "lead_temp",
        "symbol": "T<sub>LEAD</sub>",
        "spec_type": "max_rating",
        "column_model": "MAX_ONLY",
        "engineering_class": "SAFETY_LIMIT",
        "special_semantics": "NONE",
        "llm_context": {
          "formal_name": "Lead Temperature (Soldering)",
          "aliases": ["T_LEAD [°C] Max. – Soldering Temperature", "Soldering Temp. T_sol [°C] Max.", "Lead Temperature (Soldering) [°C] Max.", "T_LEAD [°C] (Max., Wave/Iron Soldering)", "Max. Solder Temp. T_LEAD [°C]", "T_LEAD Max. [°C] – Iron/Wave Solder", "Lead Temp. (Solder Point) [°C] Max.", "T_S(solder) [°C] Max. (Solder Iron or Wave)", "Reflow / Hand Solder Peak Temp. T_LEAD [°C] Max."]
        },
        "possible_units": ["°C"],
        "std_unit": "°C",
        "scenarios": [
          {
            "condition": "10s",
            "limits": {
              "LDO_Low_Voltage_CMOS": [260, 300],
              "LDO_High_Voltage_Bipolar": [260, 300]
            }
          }
        ]
      }
    ],
    "DYNAMIC_CHAR": [
      {
        "key": "loop_bandwidth",
        "symbol": "f<sub>BW</sub>",
        "spec_type": "nominal",
        "column_model": "TYP_ONLY",
        "engineering_class": "NOMINAL_PARAMETER",
        "special_semantics": "NONE",
        "llm_context": {
          "formal_name": "Control Loop Bandwidth",
          "aliases": ["f_BW [kHz/MHz] Typ. – Control Loop Bandwidth", "Loop Bandwidth f_BW [kHz] (Typ.)", "Control Loop BW [kHz] Typ. (Closed Loop)", "Feedback Loop Bandwidth f_BW [MHz] (Typ.)", "BW [kHz] – Regulator Control Loop (Typ.)", "Unity-Gain Loop Bandwidth [kHz] f_BW (Typ.)", "Closed-Loop Bandwidth f_c [kHz] (Typ.)", "Loop f_BW [MHz] Typ."]
        },
        "possible_units": ["kHz", "MHz"],
        "std_unit": "kHz",
        "scenarios": [
          {
            "condition": "Nominal load",
            "limits": {
              "LDO_Low_Voltage_CMOS": [10, 50, 500],
              "LDO_High_Voltage_Bipolar": [1, 10, 50]
            }
          }
        ]
      },
      {
        "key": "phase_margin",
        "symbol": "φ<sub>M</sub>",
        "spec_type": "nominal",
        "column_model": "TYP_ONLY",
        "engineering_class": "NOMINAL_PARAMETER",
        "special_semantics": "NONE",
        "llm_context": {
          "formal_name": "Phase Margin",
          "aliases": ["φ_M [deg] Typ. – Phase Margin", "Phase Margin PM [°] (Typ.)", "φ_M [°] Typ. (Loop Phase Margin)", "PM [deg] Typ. – Stability Margin", "Phase Margin φ_M [°] (Typ., See Stability Note)", "Loop Phase Margin [°] PM (Typ.)", "φ(M) [deg] Typ. (Bode Plot)", "Phase Margin PM [°] Typ. (At Unity-Gain Frequency)", "φ_M Typ. [°] – Guaranteed Stability"]
        },
        "possible_units": ["deg", "°"],
        "std_unit": "deg",
        "scenarios": [
          {
            "condition": "Nominal load",
            "limits": {
              "LDO_Low_Voltage_CMOS": [45, 60, 70],
              "LDO_High_Voltage_Bipolar": [45, 60]
            }
          }
        ]
      },
      {
        "key": "gain_margin",
        "symbol": "GM",
        "spec_type": "nominal",
        "column_model": "TYP_ONLY",
        "engineering_class": "NOMINAL_PARAMETER",
        "special_semantics": "NONE",
        "llm_context": {
          "formal_name": "Gain Margin",
          "aliases": ["GM [dB] Typ. – Loop Gain Margin", "Gain Margin GM [dB] (Typ.)", "Loop Gain Margin [dB] GM (Typ.)", "GM [dB] Typ. (At Phase Crossover Frequency)", "Gain Margin G_M [dB] Typ. (Stability Indicator)", "G_M [dB] – Gain Margin (Bode Analysis)", "GM Typ. [dB] (Loop, f=Phase-Zero Crossing)", "Gain Margin [dB] (Typ., See Loop Gain Bode Plot)"]
        },
        "possible_units": ["dB"],
        "std_unit": "dB",
        "scenarios": [
          {
            "condition": "Nominal load",
            "limits": {
              "LDO_Low_Voltage_CMOS": [10, 15, 20],
              "LDO_High_Voltage_Bipolar": [10, 15]
            }
          }
        ]
      }
    ],
    "PACKAGE": [
      {
        "key": "package_code",
        "symbol": "PKG",
        "spec_type": "mechanical",
        "column_model": "TYP_ONLY",
        "engineering_class": "MECHANICAL",
        "special_semantics": "NONE",
        "llm_context": {
          "formal_name": "Package",
          "aliases": ["PKG – Package / Case Type (e.g., SOT-23, TO-220)", "Case / Package Code (e.g., DFN, SOT-223, DPAK)", "Package Outline (e.g., CSP, SOT-23, TO-220AB)", "PKG Code (e.g., SOT-23-5, DFN-6, TO-220-3)", "Component Package – Case Designation (JEDEC Ref.)", "Pkg. Type (e.g., SOT-23, DPAK, DFN, CSP)", "Package / Case (e.g., SOT-23-3, SOT-223, TO-220)", "Case Style – SMD / THT (e.g., DFN 2×2, SOT-223)", "Body Type / Outline (e.g., CSP, DFN, SOT-23)", "PKG (e.g., TO-220, SOT-23-5, DPAK, DFN-4)"]
        },
        "possible_units": [""],
        "std_unit": "",
        "scenarios": [
          {
            "condition": "Type",
            "limits": {
              "LDO_Low_Voltage_CMOS": ["SOT-23", "DFN", "CSP"],
              "LDO_High_Voltage_Bipolar": ["TO-220", "SOT-223", "DPAK"]
            }
          }
        ]
      },
      {
        "key": "thermal_resistance_ja",
        "symbol": "θ<sub>JA</sub>",
        "spec_type": "nominal",
        "column_model": "TYP_MAX",
        "engineering_class": "NOMINAL_PARAMETER",
        "special_semantics": "NONE",
        "llm_context": {
          "formal_name": "Thermal Resistance Junction to Ambient",
          "aliases": ["θ_JA [°C/W] Typ./Max. (Standard PCB, Still Air)", "Rth(j-a) [°C/W] Max. – Standard PCB, Still Air", "Thermal Res. J-A θ_JA [°C/W] (Typ./Max.)", "R_TH(JA) [°C/W] Max. (Standard PCB, No Forced Air)", "θ_JA [°C/W] – Junction to Ambient (Free Convection)", "R(θJA) [K/W] Max. (FR4 PCB, 1oz Cu, Still Air)", "Theta JA [°C/W] Typ./Max. – R_θJA (No Heat Sink)", "Rth J→A [°C/W] Max. (PCB Mount, No Forced Cooling)", "Thermal Impedance J-A θ_JA [°C/W] (Still Air, PCB)", "θ(JA) [°C/W] Max – Standard FR4 PCB, No Airflow"]
        },
        "possible_units": ["°C/W"],
        "std_unit": "°C/W",
        "scenarios": [
          {
            "condition": "Standard PCB",
            "limits": {
              "LDO_Low_Voltage_CMOS": [150, 200, 300],
              "LDO_High_Voltage_Bipolar": [40, 60, 100]
            }
          }
        ]
      },
      {
        "key": "thermal_resistance_jc",
        "symbol": "θ<sub>JC</sub>",
        "spec_type": "nominal",
        "column_model": "TYP_MAX",
        "engineering_class": "NOMINAL_PARAMETER",
        "special_semantics": "NONE",
        "llm_context": {
          "formal_name": "Thermal Resistance Junction to Case",
          "aliases": ["θ_JC [°C/W] Typ./Max. (Steady State)", "Rth(j-c) [°C/W] Max. – Junction to Case", "Thermal Res. J-C θ_JC [°C/W] (Typ./Max.)", "R_TH(JC) [°C/W] Max. (Case = Thermal Tab/Bottom)", "θ_JC [°C/W] – Junction to Case (Steady State)", "R(θJC) [K/W] Max. (Exposed Pad Reference)", "Theta JC [°C/W] Typ./Max. – R_θJC (Steady State)", "Rth J→C [°C/W] Max. (Thermal Contact = Case/Tab)", "Thermal Impedance J-C θ_JC [°C/W] Typ./Max.", "θ(JC) [°C/W] Max – See Package Thermal Model"]
        },
        "possible_units": ["°C/W"],
        "std_unit": "°C/W",
        "scenarios": [
          {
            "condition": "N/A",
            "limits": {
              "LDO_Low_Voltage_CMOS": [50, 80, 120],
              "LDO_High_Voltage_Bipolar": [2, 5, 15]
            }
          }
        ]
      }
    ],
    "ELEC_CHAR": [
      {
        "key": "vin_operating",
        "symbol": "V<sub>IN</sub>",
        "spec_type": "nominal",
        "column_model": "MIN_MAX",
        "engineering_class": "NOMINAL_PARAMETER",
        "special_semantics": "NONE",
        "llm_context": {
          "formal_name": "Operating Input Voltage Range",
          "aliases": ["V_IN [V] Operating Range (Min. to Max.)", "Input Voltage Range V_IN [V] (Min/Max, For Regulation)", "V_IN Operating [V] (Min. to Max., Full Spec.)", "Supply Voltage Range V_IN [V] (Operating, Min–Max)", "V_IN [V] Range (Operating; V_OUT+V_DO to V_IN(max))", "Operating Input Voltage V_IN [V] Min. to Max.", "Input Supply Range [V] V_IN (Operating Conditions)", "V_IN [V] (Min/Max Operating, See V_DO Requirement)", "Input Voltage V_S [V] Range (Operating, All Conditions)", "V(IN) Operating [V] – Min. to Max. (Full Spec. Guaranteed)"]
        },
        "possible_units": ["V"],
        "std_unit": "V",
        "scenarios": [
          {
            "condition": "Operating",
            "limits": {
              "LDO_Low_Voltage_CMOS": ["1.8 to 5.5", "2.5 to 6.0"],
              "LDO_High_Voltage_Bipolar": ["3.0 to 40"]
            }
          }
        ]
      },
      {
        "key": "minimum_input_voltage",
        "symbol": "V<sub>IN(min)</sub>",
        "spec_type": "min_limit",
        "column_model": "MIN_ONLY",
        "engineering_class": "PERFORMANCE_LIMIT",
        "special_semantics": "NONE",
        "llm_context": {
          "formal_name": "Minimum Input Voltage",
          "aliases": ["V_IN(min) [V] – Minimum Input Voltage for Regulation", "Min. Input Voltage V_IN [V] (For Guaranteed Regulation)", "V_IN(min) [V] (= V_OUT + V_DO, Min. Headroom)", "Minimum Operating Voltage V_IN(min) [V]", "V_IN Min. [V] (For V_OUT Regulation, All Conditions)", "Min. V_IN [V] (V_OUT + Dropout, For Regulation)", "V(IN)(min) [V] – Minimum Supply for Output Regulation", "Input Voltage Min. V_IN [V] (Regulation Guaranteed Above)", "V_IN(min) [V] – Start-Up & Regulation Minimum", "Minimum V_IN [V] (For Full-Spec Output, See V_DO)"]
        },
        "possible_units": ["V"],
        "std_unit": "V",
        "scenarios": [
          {
            "condition": "For regulation",
            "limits": {
              "LDO_Low_Voltage_CMOS": [1.6, 1.8, 2.2],
              "LDO_High_Voltage_Bipolar": [2.5, 3.0, 4.5]
            }
          }
        ]
      },
      {
        "key": "output_voltage",
        "symbol": "V<sub>OUT</sub>",
        "spec_type": "nominal",
        "column_model": "MIN_TYP_MAX",
        "engineering_class": "NOMINAL_PARAMETER",
        "special_semantics": "NONE",
        "llm_context": {
          "formal_name": "Output Voltage",
          "aliases": ["V_OUT [V] Nominal (Min./Typ./Max.)", "Nominal Output Voltage V_OUT [V] (Min/Typ/Max)", "V_O [V] Nom. – Regulated Output", "Output Voltage V_OUT [V] (Typ., Pre-Set / Adjustable)", "Regulated Output Voltage [V] V_OUT (Min./Typ./Max.)", "V_OUT [V] – Fixed / Adjustable Regulated Output", "V_REG [V] Output (Nominal, ±Tol%)"]
        },
        "possible_units": ["V"],
        "std_unit": "V",
        "scenarios": [
          {
            "condition": "T_A=25°C, I_OUT=10mA",
            "limits": {
              "LDO_Low_Voltage_CMOS": [1.2, 1.8, 3.3],
              "LDO_High_Voltage_Bipolar": [5.0, 12.0, 24.0]
            }
          }
        ]
      },
      {
        "key": "iout_max",
        "symbol": "I<sub>OUT</sub>",
        "spec_type": "max_rating",
        "column_model": "MAX_ONLY",
        "engineering_class": "PERFORMANCE_LIMIT",
        "special_semantics": "NONE",
        "llm_context": {
          "formal_name": "Rated Output Current",
          "aliases": ["I_OUT [mA/A] Max. – Rated (Continuous) Output Current", "Max. Output Current I_OUT [mA] (Continuous)", "I_OUT(max) [A] – Maximum Continuous Load Current", "Rated Output Current I_O [mA] Max.", "I_LOAD [mA] Max. (Continuous)", "Max. Load Current I_OUT [A] (Continuous, TC Limited)", "Output Current Rating I_O [A] Max. (Continuous)", "I_OUT(max) [mA] – Guaranteed Regulation Up To This Level", "Maximum I_LOAD [A] (Continuous, Full Spec. Maintained)"]
        },
        "possible_units": ["mA", "A"],
        "std_unit": "mA",
        "scenarios": [
          {
            "condition": "T_A=25°C",
            "limits": {
              "LDO_Low_Voltage_CMOS": [150, 300, 500],
              "LDO_High_Voltage_Bipolar": [1000, 3000, 5000]
            }
          }
        ]
      },
      {
        "key": "iout_min",
        "symbol": "I<sub>OUT(min)</sub>",
        "spec_type": "min_limit",
        "column_model": "MIN_ONLY",
        "engineering_class": "PERFORMANCE_LIMIT",
        "special_semantics": "NONE",
        "llm_context": {
          "formal_name": "Minimum Load Current",
          "aliases": ["I_OUT(min) [µA/mA] – Minimum Load for Regulation", "Min. Load Current I_LOAD [µA] (For Regulation)", "I_OUT(min) [µA] (Min. Load; Below = Out-of-Regulation)", "Minimum Output Current [µA] I_OUT(min) (Regulation)", "Min. Load I_OUT [µA] (Required for V_OUT Regulation)", "I_LOAD(min) [µA] – Min. Current for Stable Output", "I_OUT Min. [µA] (Regulation Guaranteed Above This)", "Minimum Load Current Requirement I_L(min) [µA]", "Min. Output Current [µA/mA] for Regulation I_OUT(min)"]
        },
        "possible_units": ["µA", "mA"],
        "std_unit": "µA",
        "scenarios": [
          {
            "condition": "For regulation",
            "limits": {
              "LDO_Low_Voltage_CMOS": [0, 1, 10],
              "LDO_High_Voltage_Bipolar": [0, 5, 50]
            }
          }
        ]
      },
      {
        "key": "efficiency",
        "symbol": "η",
        "spec_type": "nominal",
        "column_model": "TYP_ONLY",
        "engineering_class": "NOMINAL_PARAMETER",
        "special_semantics": "NONE",
        "llm_context": {
          "formal_name": "Efficiency",
          "aliases": ["η [%] Typ. – Power Efficiency", "Power Efficiency η [%] Typ.", "η Typ. [%] = (P_OUT / P_IN) × 100", "Efficiency [%] Typ. (V_OUT × I_OUT / V_IN × I_IN)", "Power Conversion Efficiency η [%] Typ.", "LDO Efficiency [%] Typ. (= V_OUT / V_IN × 100 approx.)", "η(%) Typ. – Regulator Efficiency", "Power Efficiency [%] (η = P_OUT/P_IN, Typical)"]
        },
        "possible_units": ["%"],
        "std_unit": "%",
        "scenarios": [
          {
            "condition": "Nominal load",
            "limits": {
              "LDO_Low_Voltage_CMOS": [70, 80, 90],
              "LDO_High_Voltage_Bipolar": [60, 70, 80]
            }
          }
        ]
      },
      {
        "key": "dropout_voltage",
        "symbol": "V<sub>DO</sub>",
        "spec_type": "max_limit",
        "column_model": "TYP_MAX",
        "engineering_class": "PERFORMANCE_LIMIT",
        "special_semantics": "NONE",
        "llm_context": {
          "formal_name": "Dropout Voltage",
          "aliases": ["V_DO [mV/V] Typ./Max. (@ I_OUT=Max.)", "Dropout Voltage V_DO [mV] Max. (I_OUT=I_MAX)", "Min. Input-Output Voltage V_DO [mV] (@ Full Load)", "V_DROP [mV] (V_IN - V_OUT Min., @ I_OUT=Rated)", "LDO Dropout V_DO [mV] Typ./Max. (I_OUT=Max.)", "V_DO [mV] Max. (@ I_OUT Max.; V_IN = V_OUT + V_DO)", "Dropout Voltage [mV] V_DO (Typ./Max., Full Load)", "V(DO) [mV] Typ. Max. – Min. Input-to-Output Diff.", "V_IN – V_OUT [mV] Min. (For Regulation @ I_MAX)"]
        },
        "possible_units": ["mV", "V"],
        "std_unit": "mV",
        "scenarios": [
          {
            "condition": "At Iout Max",
            "limits": {
              "LDO_Low_Voltage_CMOS": [100, 200, 300],
              "LDO_High_Voltage_Bipolar": [300, 500, 1500]
            }
          }
        ]
      },
      {
        "key": "vin_to_vout_differential",
        "symbol": "V<sub>IN</sub>-V<sub>OUT</sub>",
        "spec_type": "min_limit",
        "column_model": "MIN_ONLY",
        "engineering_class": "PERFORMANCE_LIMIT",
        "special_semantics": "NONE",
        "llm_context": {
          "formal_name": "Minimum Input-Output Differential",
          "aliases": ["V_IN - V_OUT [mV/V] Min. (Headroom, For Regulation)", "Headroom Voltage [mV] Min. (V_IN - V_OUT, I_OUT=Max.)", "Min. Input-Output Differential [mV] (For Regulation)", "V_IN - V_OUT Min. [mV] (= V_DO @ Full Load)", "Headroom V [mV] Min. (Required Above V_OUT for Regulation)", "Differential Voltage V_IN-V_OUT [mV] Min.", "Min. V_IN - V_OUT [mV] (Headroom, See Dropout Note)", "Input-Output Voltage Difference Min. [mV] (Regulation)", "Overhead Voltage [mV] Min. (V_IN over V_OUT, Full Load)", "V_DIFF(min) [mV] = V_IN - V_OUT (At Max. I_OUT)"]
        },
        "possible_units": ["V", "mV"],
        "std_unit": "mV",
        "scenarios": [
          {
            "condition": "For regulation",
            "limits": {
              "LDO_Low_Voltage_CMOS": [100, 200, 300],
              "LDO_High_Voltage_Bipolar": [300, 500, 1000]
            }
          }
        ]
      },
      {
        "key": "output_voltage_accuracy",
        "symbol": "ΔV<sub>OUT</sub>",
        "spec_type": "nominal",
        "column_model": "MIN_TYP_MAX",
        "engineering_class": "NOMINAL_PARAMETER",
        "special_semantics": "NONE",
        "llm_context": {
          "formal_name": "Output Voltage Accuracy",
          "aliases": ["ΔV_OUT [%] – Output Voltage Accuracy (±%)", "Output Tolerance ΔV_OUT [%] (Min/Typ/Max)", "V_OUT Accuracy [%] (±, Nom. Conditions)", "Output Voltage Accuracy ±[%] (Nom. Load)", "ΔV_OUT/V_OUT [%] (Initial Accuracy)", "V_OUT Set Accuracy [%] (Typ./Max., No Load)", "Output Voltage Error [%] (±, Pre-Load)", "ΔV_OUT [%] – Initial Accuracy (Before Load/Temp Effects)", "V_OUT Tolerance ±[%] (Excl. Load & Line Reg.)"]
        },
        "possible_units": ["%"],
        "std_unit": "%",
        "scenarios": [
          {
            "condition": "25°C",
            "limits": {
              "LDO_Low_Voltage_CMOS": [0.5, 1, 2],
              "LDO_High_Voltage_Bipolar": [1, 2, 4]
            }
          }
        ]
      },
      {
        "key": "line_regulation",
        "symbol": "ΔV<sub>OUT</sub>/ΔV<sub>IN</sub>",
        "spec_type": "max_limit",
        "column_model": "TYP_MAX",
        "engineering_class": "PERFORMANCE_LIMIT",
        "special_semantics": "NONE",
        "llm_context": {
          "formal_name": "Line Regulation",
          "aliases": ["ΔV_OUT/ΔV_IN [mV/V] Typ./Max. – Line Regulation", "Line Regulation [mV/V] (ΔV_OUT for ΔV_IN)", "ΔV_OUT/ΔV_IN [%/V] Typ./Max. (Full V_IN Range)", "Line Reg. [mV/V] Max. (V_IN: Min to Max)", "Supply Voltage Rejection ΔV_OUT/ΔV_IN [mV/V] (DC)", "Line Regulation [%/V] (ΔV_OUT, V_IN swept)", "ΔV_OUT [mV] per ΔV_IN [V] – Line Reg. Typ./Max.", "V_OUT Change vs. V_IN [mV/V] (Typ., Full V_IN Swing)", "Line Regulation [%] (ΔV_OUT/V_OUT for Full V_IN Range)"]
        },
        "possible_units": ["mV/V", "%/V"],
        "std_unit": "mV/V",
        "scenarios": [
          {
            "condition": "Vin range",
            "limits": {
              "LDO_Low_Voltage_CMOS": [0.01, 0.1, 1],
              "LDO_High_Voltage_Bipolar": [1, 5, 10]
            }
          }
        ]
      },
      {
        "key": "load_regulation",
        "symbol": "ΔV<sub>OUT</sub>/ΔI<sub>OUT</sub>",
        "spec_type": "max_limit",
        "column_model": "TYP_MAX",
        "engineering_class": "PERFORMANCE_LIMIT",
        "special_semantics": "NONE",
        "llm_context": {
          "formal_name": "Load Regulation",
          "aliases": ["ΔV_OUT/ΔI_OUT [mV] Typ./Max. – Load Regulation", "Load Regulation [mV] (ΔV_OUT, I_OUT: 0 to I_MAX)", "ΔV_OUT [mV] for ΔI_OUT (0mA to I_MAX)", "Load Reg. [mV] Max. (I_OUT: 0 → Max.)", "Load Regulation ΔV_OUT [%] (I_OUT Step, Typ./Max.)", "V_OUT Change [mV] vs. Load Current (0 to I_MAX)", "ΔV_OUT/ΔI [mV] – Load Regulation (0→I_MAX)", "Load Reg. [mV] Max. (ΔI_OUT = 0 to Full Load)", "V_OUT Variation [mV] (I_OUT: Min to Max, Static)", "Load Regulation [%] (ΔV_OUT/V_OUT, 0→I_MAX)"]
        },
        "possible_units": ["mV", "%"],
        "std_unit": "mV",
        "scenarios": [
          {
            "condition": "0mA to Imax",
            "limits": {
              "LDO_Low_Voltage_CMOS": [5, 10, 20],
              "LDO_High_Voltage_Bipolar": [10, 50, 100]
            }
          }
        ]
      },
      {
        "key": "psrr",
        "symbol": "PSRR",
        "spec_type": "min_limit",
        "column_model": "MIN_TYP_MAX",
        "engineering_class": "PERFORMANCE_LIMIT",
        "special_semantics": "NONE",
        "llm_context": {
          "formal_name": "Power Supply Rejection Ratio",
          "aliases": ["PSRR [dB] – Power Supply Rejection Ratio", "Ripple Rejection PSRR [dB] (Min./Typ.)", "PSRR [dB] Min. Typ.", "Power Supply Rejection [dB]", "PSRR = ΔV_IN / ΔV_OUT [dB]", "Supply Rejection Ratio PSRR [dB] Typ.", "Ripple Rejection Ratio [dB]", "PSRR [dB] Typ./Min. (See PSRR vs. Freq. Fig.)"]
        },
        "possible_units": ["dB"],
        "std_unit": "dB",
        "scenarios": [
          {
            "condition": "1kHz",
            "limits": {
              "LDO_Low_Voltage_CMOS": [45, 55, 75],
              "LDO_High_Voltage_Bipolar": [35, 45, 55]
            }
          }
        ]
      },
      {
        "key": "quiescent_current",
        "symbol": "I<sub>Q</sub>",
        "spec_type": "max_limit",
        "column_model": "TYP_MAX",
        "engineering_class": "PERFORMANCE_LIMIT",
        "special_semantics": "NONE",
        "llm_context": {
          "formal_name": "Quiescent Current",
          "aliases": ["I_Q [µA/mA] Typ./Max. – Quiescent Current (No Load)", "Ground Current I_GND [µA] Typ./Max. (I_OUT=0)", "Quiescent Current I_Q [µA] (I_IN - I_OUT @ No Load)", "Ground Pin Current I_GND [µA] Max. (No Load)", "I_Q Typ./Max. [µA] (No-Load Quiescent)", "I_GND [µA] – Regulator Ground Current (I_OUT=0)", "Ground Current [µA] I_Q (No Load)", "I_Q [mA] Typ. Max. – Ground Pin (No Output Load)"]
        },
        "possible_units": ["µA", "mA"],
        "std_unit": "µA",
        "scenarios": [
          {
            "condition": "No load",
            "limits": {
              "LDO_Low_Voltage_CMOS": [1, 5, 100],
              "LDO_High_Voltage_Bipolar": [500, 1000, 5000]
            }
          }
        ]
      },
      {
        "key": "shutdown_current",
        "symbol": "I<sub>SD</sub>",
        "spec_type": "max_limit",
        "column_model": "TYP_MAX",
        "engineering_class": "PERFORMANCE_LIMIT",
        "special_semantics": "NONE",
        "llm_context": {
          "formal_name": "Shutdown Current",
          "aliases": ["I_SD [µA/nA] Typ./Max. – Shutdown Current (EN=Low)", "Standby Current I_SD [µA] Max. (Enable = Low)", "I_SD [nA] Typ./Max. (Device Disabled, V_IN Applied)", "Shutdown Supply Current I_SD [µA] Max. (EN=0V)", "I_SD [µA] – Total Input Current in Shutdown Mode", "Off-State Current I_SD [nA] Max. (Enable Low)", "Standby / Shutdown Current I_SD [nA] Max. (EN=Low)", "Quiescent Current in Shutdown I_SD [nA] Max."]
        },
        "possible_units": ["µA", "nA"],
        "std_unit": "µA",
        "scenarios": [
          {
            "condition": "Enable Low",
            "limits": {
              "LDO_Low_Voltage_CMOS": [0.01, 0.1, 1],
              "LDO_High_Voltage_Bipolar": [1, 5, 10]
            }
          }
        ]
      },
      {
        "key": "input_supply_current",
        "symbol": "I<sub>IN</sub>",
        "spec_type": "nominal",
        "column_model": "TYP_ONLY",
        "engineering_class": "NOMINAL_PARAMETER",
        "special_semantics": "NONE",
        "llm_context": {
          "formal_name": "Input Supply Current",
          "aliases": ["I_IN [mA/A] Typ. – Total Input Current @ I_OUT=Max.", "Total Input Current I_IN [mA] (I_OUT=Max.)", "I_IN [mA] Typ. (= I_OUT + I_Q)", "Input Supply Current [mA] I_IN (At Max. Load)", "I_S [mA] Typ. – Supply Current", "I_IN Typ. [mA] (Total: Load + Ground, I_OUT=Max.)", "Supply Current I_IN [A] (At Full Output Load)", "Input Current I_IN [mA] Typ. (= I_LOAD + I_GND)", "I_INPUT [mA] Typ. – V_IN Pin Current at I_OUT(max)"]
        },
        "possible_units": ["mA", "A"],
        "std_unit": "mA",
        "scenarios": [
          {
            "condition": "At Iout Max",
            "limits": {
              "LDO_Low_Voltage_CMOS": [150, 300, 500],
              "LDO_High_Voltage_Bipolar": [500, 1000, 5000]
            }
          }
        ]
      },
      {
        "key": "reverse_leakage_current",
        "symbol": "I<sub>R(LEAK)</sub>",
        "spec_type": "max_limit",
        "column_model": "TYP_MAX",
        "engineering_class": "PERFORMANCE_LIMIT",
        "special_semantics": "NONE",
        "llm_context": {
          "formal_name": "Reverse Leakage Current",
          "aliases": ["I_R(LEAK) [µA/nA] Typ./Max. (V_OUT=V_IN, Device Off)", "Reverse Leakage I_R [nA] Max. (V_OUT=V_IN, EN=Low)", "I_R(LEAK) [µA] Max. – Reverse Current (Output > Input)", "Reverse Current Leakage [nA] (Device Off, V_OUT≥V_IN)", "Off-State Reverse Leakage I_REV [nA] Max.", "Reverse Leakage Current I_R [µA] (Shutdown, V_OUT>V_IN)", "I(R)(LEAK) [nA] Max. – Backfeed Leakage (Device Off)", "I_REVERSE(LEAK) [µA] Max. (Output Backfeed, Device Off)"]
        },
        "possible_units": ["µA", "nA"],
        "std_unit": "µA",
        "scenarios": [
          {
            "condition": "Vout = Vin, device off",
            "limits": {
              "LDO_Low_Voltage_CMOS": [0.001, 0.01, 0.1],
              "LDO_High_Voltage_Bipolar": [0.1, 1, 10]
            }
          }
        ]
      },
      {
        "key": "output_noise",
        "symbol": "V<sub>n</sub>",
        "spec_type": "max_limit",
        "column_model": "TYP_MAX",
        "engineering_class": "PERFORMANCE_LIMIT",
        "special_semantics": "NONE",
        "llm_context": {
          "formal_name": "Output Noise Voltage",
          "aliases": ["V_n [µVrms] Typ./Max. – Output Noise (10Hz–100kHz)", "RMS Noise V_n [µVrms] (BW: 10Hz to 100kHz, Typ.)", "Output Noise Voltage [µVrms] (10Hz–100kHz, Typ.)", "V_noise [µVrms] Typ./Max. (Integrated, 10Hz–100kHz)", "V_n [µVrms] – LDO Output Noise (10Hz to 100kHz)", "Output Noise V_n [µVrms] (RMS, 10Hz to 100kHz, Typ.)", "Noise V_n [µVrms] Typ. Max. (10Hz–100kHz Band)", "Output RMS Noise [µVrms] V_n (10Hz–100kHz)"]
        },
        "possible_units": ["µVrms"],
        "std_unit": "µVrms",
        "scenarios": [
          {
            "condition": "10Hz to 100kHz",
            "limits": {
              "LDO_Low_Voltage_CMOS": [10, 30, 100],
              "LDO_High_Voltage_Bipolar": [50, 100, 200]
            }
          }
        ]
      },
      {
        "key": "output_noise_density",
        "symbol": "e<sub>n</sub>",
        "spec_type": "max_limit",
        "column_model": "TYP_MAX",
        "engineering_class": "PERFORMANCE_LIMIT",
        "special_semantics": "NONE",
        "llm_context": {
          "formal_name": "Output Noise Spectral Density",
          "aliases": ["e_n [nV/√Hz] Typ./Max. – Noise Density", "Noise Density e_n [µV/√Hz] Typ.", "e_n [nV/√Hz] – Output Noise Spectral Density", "Noise Spectral Density [nV/√Hz] e_n (Typ.)", "Output Noise Density e_n [nV/√Hz] Typ.", "Spot Noise e_n [nV/√Hz]", "Noise Floor [nV/√Hz] e_n (Typ.)", "Output Voltage Noise Density [nV/√Hz] (Typ.)"]
        },
        "possible_units": ["µV/√Hz", "nV/√Hz"],
        "std_unit": "nV/√Hz",
        "scenarios": [
          {
            "condition": "At 1kHz",
            "limits": {
              "LDO_Low_Voltage_CMOS": [10, 30, 100],
              "LDO_High_Voltage_Bipolar": [50, 100, 200]
            }
          }
        ]
      },
      {
        "key": "enable_threshold_high",
        "symbol": "V<sub>EN(H)</sub>",
        "spec_type": "nominal",
        "column_model": "MIN_TYP_MAX",
        "engineering_class": "NOMINAL_PARAMETER",
        "special_semantics": "NONE",
        "llm_context": {
          "formal_name": "Enable Threshold Voltage High",
          "aliases": ["V_EN(H) [V] Min. – Enable Input High Threshold", "Enable Input High V_EN(H) [V] (Min., For Turn-On)", "V_EN(H) [V] Min./Typ./Max. – Logic High Enable", "V_IH [V] Min. (Enable Pin)", "Enable Threshold High V_EN(H) [V] (Device Turns ON)", "EN Pin High Threshold V_EN(H) [V] Min./Typ./Max.", "V_EN High [V] (Min. for Device Enable, Logic High)", "V_EN(H) Min. [V] – Enable Pin Logic-High Level", "Enable High Voltage V_EN(H) [V] (Turn-On Threshold)", "V_IH(EN) [V] Min. Typ. (Enable Pin, High = ON State)"]
        },
        "possible_units": ["V"],
        "std_unit": "V",
        "scenarios": [
          {
            "condition": "Logic high",
            "limits": {
              "LDO_Low_Voltage_CMOS": [0.8, 1.2, 2.0],
              "LDO_High_Voltage_Bipolar": [2.0, 2.4]
            }
          }
        ]
      },
      {
        "key": "enable_threshold_low",
        "symbol": "V<sub>EN(L)</sub>",
        "spec_type": "nominal",
        "column_model": "MIN_TYP_MAX",
        "engineering_class": "NOMINAL_PARAMETER",
        "special_semantics": "NONE",
        "llm_context": {
          "formal_name": "Enable Threshold Voltage Low",
          "aliases": ["V_EN(L) [V] Max. – Enable Input Low / Disable Threshold", "Disable Threshold V_EN(L) [V] (Max., For Shutdown)", "V_EN(L) [V] Max./Typ. – Logic Low Disable Level", "V_IL [V] Max. (Enable Pin = Low = Device OFF)", "Enable Threshold Low V_EN(L) [V] (Device Disabled Below)", "EN Pin Low Threshold V_EN(L) [V] Max./Typ./Min.", "V_EN Low [V] Max. (Shutdown Threshold, EN=Logic Low)", "V_EN(L) Max. [V] – Enable Pin Logic-Low Level", "Disable Input Voltage V_EN(L) [V] Max. (Turn-Off Level)", "V_IL(EN) [V] Max. Typ. (Enable Pin, Low = OFF State)"]
        },
        "possible_units": ["V"],
        "std_unit": "V",
        "scenarios": [
          {
            "condition": "Logic low",
            "limits": {
              "LDO_Low_Voltage_CMOS": [0.3, 0.4, 0.5],
              "LDO_High_Voltage_Bipolar": [0.4, 0.8]
            }
          }
        ]
      },
      {
        "key": "enable_input_current",
        "symbol": "I<sub>EN</sub>",
        "spec_type": "max_limit",
        "column_model": "TYP_MAX",
        "engineering_class": "PERFORMANCE_LIMIT",
        "special_semantics": "NONE",
        "llm_context": {
          "formal_name": "Enable Pin Input Current",
          "aliases": ["I_EN [nA/µA] Typ./Max. – Enable Pin Leakage Current", "Enable Pin Leakage I_EN [nA] Max.", "I_EN [nA] Typ./Max. (Enable Pin)", "Enable Pin Bias Current I_EN [µA] Max. (EN=High)", "EN Pin Input Current I_EN [nA] (Typ.)", "I(EN) [nA] Max. – Enable Input Pin Leakage", "Enable Input Bias I_EN [nA] Max. (EN Pin, Both States)", "I_EN Leakage [nA] Typ./Max.", "EN Pin Current I_EN [nA] Max.", "Enable Pin Input Leakage I_EN [µA] (High/Low, Typ.)"]
        },
        "possible_units": ["µA", "nA"],
        "std_unit": "nA",
        "scenarios": [
          {
            "condition": "Enable High/Low",
            "limits": {
              "LDO_Low_Voltage_CMOS": [1, 10, 100],
              "LDO_High_Voltage_Bipolar": [10, 100, 1000]
            }
          }
        ]
      },
      {
        "key": "uvlo_threshold",
        "symbol": "V<sub>UVLO</sub>",
        "spec_type": "nominal",
        "column_model": "MIN_TYP_MAX",
        "engineering_class": "NOMINAL_PARAMETER",
        "special_semantics": "NONE",
        "llm_context": {
          "formal_name": "Under-Voltage Lockout Threshold",
          "aliases": ["V_UVLO [V] – UVLO Rising Threshold (Min./Typ./Max.)", "UVLO Threshold V_UVLO [V] (Rising V_IN, Typ./Max.)", "Under-Voltage Lockout V_UVLO [V] (Rising, Enable)", "V_UVLO [V] Min./Typ./Max. (Input Rising, Startup Enable)", "UVLO Turn-On Threshold [V] V_UVLO (V_IN Rising)", "V_UVLO Rising [V] – V_IN Must Exceed for Operation", "Under-Voltage Lockout Rising V_UVLO [V] (Typ.)", "UVLO V_IN Threshold [V] (Rising Edge, Startup)", "V(UVLO) Rising [V] Min. Typ. Max. (Enable Threshold)"]
        },
        "possible_units": ["V"],
        "std_unit": "V",
        "scenarios": [
          {
            "condition": "Rising",
            "limits": {
              "LDO_Low_Voltage_CMOS": [1.5, 1.8, 2.0],
              "LDO_High_Voltage_Bipolar": [2.5, 3.0, 4.0]
            }
          }
        ]
      },
      {
        "key": "uvlo_hysteresis",
        "symbol": "ΔV<sub>UVLO</sub>",
        "spec_type": "nominal",
        "column_model": "TYP_ONLY",
        "engineering_class": "NOMINAL_PARAMETER",
        "special_semantics": "NONE",
        "llm_context": {
          "formal_name": "UVLO Hysteresis",
          "aliases": ["ΔV_UVLO [mV] Typ. – UVLO Hysteresis", "Under-Voltage Lockout Hysteresis ΔV_UVLO [mV] (Typ.)", "UVLO Hysteresis [mV] (Rising - Falling Threshold)", "ΔV_UVLO [mV] (Hysteresis: V_UVLO_RISE - V_UVLO_FALL)", "UVLO Hyst. ΔV [mV] Typ. (Prevents Chattering Near Threshold)", "UVLO Hysteresis Voltage [mV] Typ. (V_UVLO_R - V_UVLO_F)", "ΔV_UVLO Typ. [mV] – UVLO Window (Rise-Fall Diff.)", "Under-Voltage Lockout ΔV [mV] Hysteresis (Typ.)", "V_UVLO Hysteresis [mV] Typ. (Turn-On minus Turn-Off)", "UVLO Hyst. [mV] Typ. (ΔV_IN Hysteresis Band)"]
        },
        "possible_units": ["mV"],
        "std_unit": "mV",
        "scenarios": [
          {
            "condition": "",
            "limits": {
              "LDO_Low_Voltage_CMOS": [50, 100, 200],
              "LDO_High_Voltage_Bipolar": [100, 200, 500]
            }
          }
        ]
      },
      {
        "key": "soft_start_time",
        "symbol": "t<sub>SS</sub>",
        "spec_type": "nominal",
        "column_model": "MIN_TYP_MAX",
        "engineering_class": "NOMINAL_PARAMETER",
        "special_semantics": "NONE",
        "llm_context": {
          "formal_name": "Soft-Start Time",
          "aliases": ["t_SS [ms/µs] Typ. – Soft-Start Time (0V to 90% V_OUT)", "Soft Start Time t_SS [ms] (0→90% V_OUT)", "t_SS [ms] Min./Typ./Max. – Ramp Time to 90% V_OUT", "Soft-Start Duration t_SS [ms] (Startup, 0 to 90% V_OUT)", "Output Ramp Time t_SS [µs] (Soft-Start, 0→90%)", "Soft Start t_SS [ms] Typ.", "t_SOFTSTART [ms] Typ. – V_OUT Rise Time (0→90%)", "Soft-Start Time [ms] t_SS (Min./Typ./Max.)", "V_OUT Soft-Start Ramp t_SS [ms] (0V to 90%, Typ.)"]
        },
        "possible_units": ["ms", "µs"],
        "std_unit": "ms",
        "scenarios": [
          {
            "condition": "0V to 90% Vout",
            "limits": {
              "LDO_Low_Voltage_CMOS": [0.5, 1, 5],
              "LDO_High_Voltage_Bipolar": [1, 5, 20]
            }
          }
        ]
      },
      {
        "key": "current_limit",
        "symbol": "I<sub>LIM</sub>",
        "spec_type": "nominal",
        "column_model": "MIN_TYP_MAX",
        "engineering_class": "NOMINAL_PARAMETER",
        "special_semantics": "NONE",
        "llm_context": {
          "formal_name": "Current Limit",
          "aliases": ["I_LIM [mA/A] Typ. – Current Limit Threshold", "Current Limit Threshold I_LIM [mA] (Min./Typ./Max.)", "I_LIM [mA] Typ. (Overcurrent Protection Trip Level)", "Current Limit I_CL [A] (Min./Typ./Max.)", "I_LIMIT [mA] Typ./Max. (Output Current Clamp Level)", "OCP Threshold I_LIM [mA] (Trip, V_OUT Still Regulated)", "Current Limiting Threshold [mA] I_LIM (Typ.)", "I_LIM [A] Min. Typ. Max. – Current Protection Level", "I_LIMIT Typ. [mA] (Activation at This I_OUT Level)"]
        },
        "possible_units": ["mA", "A"],
        "std_unit": "mA",
        "scenarios": [
          {
            "condition": "T_A=25°C",
            "limits": {
              "LDO_Low_Voltage_CMOS": [200, 400, 600],
              "LDO_High_Voltage_Bipolar": [600, 1200, 6000]
            }
          }
        ]
      },
      {
        "key": "short_circuit_current",
        "symbol": "I<sub>SC</sub>",
        "spec_type": "nominal",
        "column_model": "MIN_TYP_MAX",
        "engineering_class": "NOMINAL_PARAMETER",
        "special_semantics": "NONE",
        "llm_context": {
          "formal_name": "Short Circuit Current",
          "aliases": ["I_SC [mA/A] Typ. – Short Circuit Current (V_OUT=0V)", "Short Circuit Current I_SC [mA] (V_OUT=0, Min./Typ./Max.)", "I_SC [mA] Typ. (Output Shorted to GND, V_OUT=0V)", "Short-Circuit I_SC [A] Min./Typ./Max. (V_OUT=GND)", "I_SC [mA] – Current Under Short (V_OUT = 0V)", "Output Short-Circuit Current I_SC [mA] (V_OUT=0V)", "Short Circuit Output Current I_SC [A] (Min./Typ./Max.)", "ISC [mA] Typ. – Sustained Current at V_OUT=0V"]
        },
        "possible_units": ["mA", "A"],
        "std_unit": "mA",
        "scenarios": [
          {
            "condition": "Vout = 0V",
            "limits": {
              "LDO_Low_Voltage_CMOS": [200, 400, 600],
              "LDO_High_Voltage_Bipolar": [600, 1200, 3000]
            }
          }
        ]
      },
      {
        "key": "current_limit_foldback",
        "symbol": "I<sub>FOLD</sub>",
        "spec_type": "nominal",
        "column_model": "MIN_TYP_MAX",
        "engineering_class": "NOMINAL_PARAMETER",
        "special_semantics": "NONE",
        "llm_context": {
          "formal_name": "Foldback Current Limit",
          "aliases": ["I_FOLD [mA/A] Typ. – Foldback Current", "Foldback Current I_FOLD [mA]", "Current Foldback Level I_FOLD [mA] Min./Typ./Max.", "Foldback I_LIMIT [mA] Typ.", "I_FOLD Typ. [mA] – Reduced Limit During Fault", "Foldback Protection Current I_FOLD [mA] (Fault State)", "I_FOLD [A] – Current Limit Reduction (V_OUT Depressed)", "I_FOLD Typ. Min. Max. [mA] (Foldback)"]
        },
        "possible_units": ["mA", "A"],
        "std_unit": "mA",
        "scenarios": [
          {
            "condition": "Vout < 50% nominal",
            "limits": {
              "LDO_Low_Voltage_CMOS": [50, 100, 150],
              "LDO_High_Voltage_Bipolar": [100, 200, 500]
            }
          }
        ]
      },
      {
        "key": "current_limit_response_time",
        "symbol": "t<sub>CL</sub>",
        "spec_type": "max_limit",
        "column_model": "TYP_MAX",
        "engineering_class": "PERFORMANCE_LIMIT",
        "special_semantics": "NONE",
        "llm_context": {
          "formal_name": "Current Limit Response Time",
          "aliases": ["t_CL [µs] Typ./Max. – Current Limit Response Time", "Overcurrent Response Time t_CL [µs] (From Overload to Limit)", "t_CL [µs] Max. (OCP Activation, Overload → Limit)", "Current Limit Reaction Time [µs] t_CL (Typ./Max.)", "t_CL [µs] Typ. Max. – OCP Trip Delay", "Overcurrent Response t_CL [µs] (Overload to I_LIM)", "Current Limit Response [µs] t_CL (Max., Fault Condition)", "t_OCP [µs] Typ./Max. – Time to Activate Current Limit", "OCP Response Time t_CL [µs] Max. (From Fault Onset)"]
        },
        "possible_units": ["µs", "ns"],
        "std_unit": "µs",
        "scenarios": [
          {
            "condition": "From overload to limit",
            "limits": {
              "LDO_Low_Voltage_CMOS": [1, 5, 10],
              "LDO_High_Voltage_Bipolar": [5, 10, 50]
            }
          }
        ]
      },
      {
        "key": "thermal_shutdown",
        "symbol": "T<sub>SD</sub>",
        "spec_type": "nominal",
        "column_model": "MIN_TYP_MAX",
        "engineering_class": "NOMINAL_PARAMETER",
        "special_semantics": "NONE",
        "llm_context": {
          "formal_name": "Thermal Shutdown Temperature",
          "aliases": ["T_SD [°C] Typ. – Thermal Shutdown Temperature", "Over-Temperature Shutdown T_SD [°C] (Min./Typ./Max.)", "T_SD [°C] Typ. (TSD Activation, Junction Temperature)", "Thermal Shutdown Trip T_J [°C] Typ. (T_SD)", "T_SHUTDOWN [°C] Typ. – Internal Overtemp. Protection", "Thermal Overload Shutdown T_SD [°C] Min./Typ./Max.", "T_SD Typ. [°C] (Junction; Device Shuts Off Above This)", "Over-Temp. Shutdown Level T_SD [°C] (Typ., Tj-Based)", "Thermal Protection Threshold T_SD [°C] Typ.", "TSD Trip Temperature [°C] Typ."]
        },
        "possible_units": ["°C"],
        "std_unit": "°C",
        "scenarios": [
          {
            "condition": "",
            "limits": {
              "LDO_Low_Voltage_CMOS": [150, 160, 165],
              "LDO_High_Voltage_Bipolar": [150, 160, 170]
            }
          }
        ]
      },
      {
        "key": "thermal_shutdown_hysteresis",
        "symbol": "ΔT<sub>SD</sub>",
        "spec_type": "nominal",
        "column_model": "TYP_ONLY",
        "engineering_class": "NOMINAL_PARAMETER",
        "special_semantics": "NONE",
        "llm_context": {
          "formal_name": "Thermal Shutdown Hysteresis",
          "aliases": ["ΔT_SD [°C] Typ. – Thermal Shutdown Hysteresis", "TSD Hysteresis ΔT_SD [°C] Typ. (Shutdown - Reset)", "Thermal Shutdown Hyst. ΔT [°C] Typ. (T_SD - T_RESET)", "ΔT_SD [°C] – Hysteresis Band (Shutdown to Re-Enable)", "Thermal Hyst. [°C] Typ. (ΔT_SD: Trip minus Re-Enable)", "T_SD Hysteresis [°C] Typ. (TSD Re-activation Window)", "ΔT_SHUTDOWN [°C] Typ. – Prevents Rapid Cycling Near TSD", "TSD Hyst. ΔT_SD [°C] Typ. (T_SD_TRIP – T_SD_RECOVER)", "Thermal Shutdown Hysteresis [°C] Typ. ΔT_SD", "ΔT_SD Typ. [°C] – Thermal Recovery Hysteresis Window"]
        },
        "possible_units": ["°C"],
        "std_unit": "°C",
        "scenarios": [
          {
            "condition": "",
            "limits": {
              "LDO_Low_Voltage_CMOS": [10, 15, 20],
              "LDO_High_Voltage_Bipolar": [15, 20, 30]
            }
          }
        ]
      },
      {
        "key": "startup_time",
        "symbol": "t<sub>START</sub>",
        "spec_type": "max_limit",
        "column_model": "TYP_MAX",
        "engineering_class": "PERFORMANCE_LIMIT",
        "special_semantics": "NONE",
        "llm_context": {
          "formal_name": "Startup Time",
          "aliases": ["t_START [µs/ms] Typ./Max. – Startup Time", "Turn-on Time t_START [µs] (EN Rising to V_OUT=90%)", "t_START [µs] Max. (Enable to Output in Regulation)", "Startup Time [µs] t_START (EN=High, V_OUT: 0→90%)", "t_ON [µs] Typ./Max. – Enable to V_OUT Regulated", "t_START Typ./Max. [µs]", "Turn-On Time [µs/ms] t_START", "t_STARTUP [µs] Max. – Time to Regulation After Enable", "Start-Up Time t_START [µs] Typ. Max."]
        },
        "possible_units": ["µs", "ms"],
        "std_unit": "µs",
        "scenarios": [
          {
            "condition": "Enable high",
            "limits": {
              "LDO_Low_Voltage_CMOS": [50, 100, 200],
              "LDO_High_Voltage_Bipolar": [100, 500, 1000]
            }
          }
        ]
      },
      {
        "key": "settling_time",
        "symbol": "t<sub>SETTLING</sub>",
        "spec_type": "max_limit",
        "column_model": "TYP_MAX",
        "engineering_class": "PERFORMANCE_LIMIT",
        "special_semantics": "NONE",
        "llm_context": {
          "formal_name": "Output Settling Time",
          "aliases": ["t_SETTLING [µs/ms] Typ./Max. – Output Settling (To 1%)", "Regulation Time t_SETTLING [µs] (V_OUT to ±1%)", "t_SETTLING [µs] Max. (V_OUT Settles to 1% Band)", "Output Settling Time [µs] t_SET (To ±1% of V_OUT)", "t_SETTLE Typ./Max. [µs] (V_OUT Stabilization Time)", "Settling Time t_S [µs] Max. (After Enable, 1% Final)", "t_SETTLING [ms] Typ./Max. – To 1% of Nominal V_OUT", "t_SETTLING [µs] Max. – V_OUT Within 1% After Startup"]
        },
        "possible_units": ["µs", "ms"],
        "std_unit": "µs",
        "scenarios": [
          {
            "condition": "To 1% of Vout",
            "limits": {
              "LDO_Low_Voltage_CMOS": [10, 50, 100],
              "LDO_High_Voltage_Bipolar": [50, 100, 500]
            }
          }
        ]
      },
      {
        "key": "load_transient_response",
        "symbol": "ΔV<sub>LOAD</sub>",
        "spec_type": "max_limit",
        "column_model": "TYP_MAX",
        "engineering_class": "PERFORMANCE_LIMIT",
        "special_semantics": "NONE",
        "llm_context": {
          "formal_name": "Load Transient Response",
          "aliases": ["ΔV_LOAD [mV] Typ./Max. – Load Transient Response", "Load Step Response ΔV_OUT [mV]", "Transient Response [mV] ΔV_LOAD", "ΔV_OUT [mV] (Load Step Response, Typ./Max.)", "Output Voltage Deviation ΔV [mV] (Load Step, Max.)", "Load Transient Deviation [mV]", "ΔV_LOAD Typ./Max. [mV]", "Transient Voltage [mV] Max. (Load Step)", "ΔV_OUT [%] Load Transient"]
        },
        "possible_units": ["mV", "%"],
        "std_unit": "mV",
        "scenarios": [
          {
            "condition": "Iout step 1mA to Imax",
            "limits": {
              "LDO_Low_Voltage_CMOS": [20, 50, 100],
              "LDO_High_Voltage_Bipolar": [50, 100, 200]
            }
          }
        ]
      },
      {
        "key": "load_transient_recovery_time",
        "symbol": "t<sub>REC</sub>",
        "spec_type": "max_limit",
        "column_model": "TYP_MAX",
        "engineering_class": "PERFORMANCE_LIMIT",
        "special_semantics": "NONE",
        "llm_context": {
          "formal_name": "Load Transient Recovery Time",
          "aliases": ["t_REC [µs/ms] Typ./Max. – Load Transient Recovery Time", "Recovery Time t_REC [µs] (After I_OUT Step 10%→90%)", "t_REC [µs] Max. (V_OUT Returns to ±1%, I_STEP 10→90%)", "Load Transient Recovery [µs] t_REC (10% to 90% I_STEP)", "t_REC Typ./Max. [µs] – V_OUT Re-Regulation After Step", "Transient Recovery t_RECOVER [µs]", "Recovery Time [µs] t_REC (After Load Step, ±1% Band)", "t_RECOVERY [µs] Max. – Load Transient Re-Settlement", "Load Recovery t_REC [µs] Typ./Max."]
        },
        "possible_units": ["µs", "ms"],
        "std_unit": "µs",
        "scenarios": [
          {
            "condition": "Iout step 10% to 90%",
            "limits": {
              "LDO_Low_Voltage_CMOS": [10, 50, 100],
              "LDO_High_Voltage_Bipolar": [50, 100, 500]
            }
          }
        ]
      },
      {
        "key": "output_voltage_overshoot",
        "symbol": "V<sub>OS</sub>",
        "spec_type": "max_limit",
        "column_model": "TYP_MAX",
        "engineering_class": "PERFORMANCE_LIMIT",
        "special_semantics": "NONE",
        "llm_context": {
          "formal_name": "Output Voltage Overshoot",
          "aliases": ["V_OS [%/mV] Typ./Max. – Output Overshoot (Startup)", "Startup Overshoot V_OS [%] (During Turn-On, Max.)", "V_OS [mV] Max. – V_OUT Overshoot Above Nominal", "Output Overshoot ΔV_OS [%] (Startup Transient, Max.)", "V_OS Typ./Max. [%] (V_OUT Spike Above V_NOM, Startup)", "Overshoot [mV] Max. (V_OUT Peak Above Nominal, Startup)", "V_OS [%] Max. – V_OUT Spike During Enable", "Output Voltage Overshoot V_OS [mV] (During Startup)", "V_OS [mV/%] Typ. Max. – Startup V_OUT Peak Excursion"]
        },
        "possible_units": ["%", "mV"],
        "std_unit": "%",
        "scenarios": [
          {
            "condition": "During startup",
            "limits": {
              "LDO_Low_Voltage_CMOS": [1, 2, 5],
              "LDO_High_Voltage_Bipolar": [2, 5, 10]
            }
          }
        ]
      },
      {
        "key": "output_voltage_undershoot",
        "symbol": "V<sub>US</sub>",
        "spec_type": "max_limit",
        "column_model": "TYP_MAX",
        "engineering_class": "PERFORMANCE_LIMIT",
        "special_semantics": "NONE",
        "llm_context": {
          "formal_name": "Output Voltage Undershoot",
          "aliases": ["V_US [%/mV] Typ./Max. – Output Undershoot (Load Step)", "Load Transient Undershoot V_US [%] (I_OUT Step Max.)", "V_US [mV] Max. – V_OUT Sag Below Nominal (Load Step)", "Output Undershoot ΔV_US [%] (Load Step, Max.)", "V_US Typ./Max. [%] (V_OUT Dip Below V_NOM, Load Step)", "Undershoot [mV] Max. (V_OUT Valley, Load Step Condition)", "V_US [%] Max. – V_OUT Dip During Load Step", "Output Voltage Undershoot V_US [mV] (Load Step, Typ.)", "V_US [mV/%] Typ. Max. – Load Step V_OUT Sag"]
        },
        "possible_units": ["%", "mV"],
        "std_unit": "%",
        "scenarios": [
          {
            "condition": "Load step",
            "limits": {
              "LDO_Low_Voltage_CMOS": [1, 2, 5],
              "LDO_High_Voltage_Bipolar": [2, 5, 10]
            }
          }
        ]
      },
      {
        "key": "slew_rate",
        "symbol": "SR",
        "spec_type": "nominal",
        "column_model": "TYP_ONLY",
        "engineering_class": "NOMINAL_PARAMETER",
        "special_semantics": "NONE",
        "llm_context": {
          "formal_name": "Output Voltage Slew Rate",
          "aliases": ["SR [mV/µs] Typ. – Output Voltage Slew Rate (Startup)", "Slew Rate SR [V/µs] Typ. (During Soft-Start Ramp)", "SR [mV/µs] – V_OUT Rise Slew (Startup, Typ.)", "Output Slew Rate [V/µs] SR (Startup)", "SR Typ. [mV/µs] (V_OUT Ramp Rate, Enable Rising)", "V_OUT Slew Rate SR [V/µs] (Startup)", "Slew Rate [mV/µs] (V_OUT Startup Ramp, Typ.)", "SR [mV/µs] Typ. – Output Ramp Rate (During Turn-On)", "Output Voltage Slew [mV/µs] Typ. SR (Soft-Start Ramp)"]
        },
        "possible_units": ["V/µs", "mV/µs"],
        "std_unit": "mV/µs",
        "scenarios": [
          {
            "condition": "During startup",
            "limits": {
              "LDO_Low_Voltage_CMOS": [0.1, 1, 10],
              "LDO_High_Voltage_Bipolar": [1, 10, 100]
            }
          }
        ]
      },
      {
        "key": "monotonic_startup",
        "symbol": "MONO",
        "spec_type": "nominal",
        "column_model": "TYP_ONLY",
        "engineering_class": "NOMINAL_PARAMETER",
        "special_semantics": "NONE",
        "llm_context": {
          "formal_name": "Monotonic Startup",
          "aliases": ["MONO – Monotonic Startup (Guaranteed: Yes/No)", "Monotonic Turn-on (V_OUT rises without dip; Guaranteed)", "Monotonic Startup MONO (Yes = No V_OUT Undershoot at Startup)", "Monotonic Output Ramp (Guaranteed, See Startup Waveform)", "MONO – V_OUT Rises Monotonically (No Reversal)", "Monotonic Startup Guaranteed (Yes / Not Specified)", "MONO: Yes – No V_OUT Reversal During Startup", "Monotonic V_OUT Startup (Guaranteed; Power-Sequencing Safe)", "Monotonic Turn-On (V_OUT: Non-Decreasing During Startup)", "MONO Startup [Yes] – Required for FPGA/DSP Power Sequencing"]
        },
        "possible_units": [""],
        "std_unit": "",
        "scenarios": [
          {
            "condition": "",
            "limits": {
              "LDO_Low_Voltage_CMOS": ["Yes"],
              "LDO_High_Voltage_Bipolar": ["Yes"]
            }
          }
        ]
      },
      {
        "key": "pgood_threshold_high",
        "symbol": "V<sub>PG(H)</sub>",
        "spec_type": "nominal",
        "column_model": "MIN_TYP_MAX",
        "engineering_class": "NOMINAL_PARAMETER",
        "special_semantics": "NONE",
        "llm_context": {
          "formal_name": "Power Good Threshold High",
          "aliases": ["V_PG(H) [%] Typ. – Power Good Rising Threshold", "PG High Threshold V_PG(H) [%] (% of V_OUT Nominal)", "V_PG(H) [%] Min./Typ./Max. – PGOOD Assert Level", "Power Good Rising Threshold [%] V_PG(H) (V_OUT Based)", "PGOOD Assert Threshold [%] V_PG(H) (Rising V_OUT)", "V_PG(H) Typ. [%] (PGOOD Goes High at This V_OUT %)", "Power Good High Trip [%] (V_OUT > V_PG(H) → PG=High)", "PG(H) Threshold [%] V_PG(H) Min./Typ./Max.", "PGOOD Rising Threshold V_PG(H) [%] of V_OUT Nominal"]
        },
        "possible_units": ["%"],
        "std_unit": "%",
        "scenarios": [
          {
            "condition": "% of Vout nominal",
            "limits": {
              "LDO_Low_Voltage_CMOS": [90, 92, 95],
              "LDO_High_Voltage_Bipolar": [90, 92, 95]
            }
          }
        ]
      },
      {
        "key": "pgood_output_low",
        "symbol": "V<sub>PG(OL)</sub>",
        "spec_type": "max_limit",
        "column_model": "MAX_ONLY",
        "engineering_class": "PERFORMANCE_LIMIT",
        "special_semantics": "NONE",
        "llm_context": {
          "formal_name": "Power Good Output Low Voltage",
          "aliases": ["V_PG(OL) [V] Max. – Power Good Output Low Voltage", "PG Output Low V_PG(OL) [V] Max.", "V_PG(OL) [V] Max. (PGOOD Pin Low)", "PGOOD Sink Low Voltage [V] Max.", "V_OL(PG) [V] Max. – Open-Drain Low", "Power Good Low V_PG(OL) [V] (Max., Fault Condition)", "PGOOD Output Low [V] Max. (Pin Pulled Low)", "V_PG(OL) Max. [V] – PGOOD Asserted Low", "PG Low Voltage [V] Max. V_PG(OL) (OD Output)"]
        },
        "possible_units": ["V"],
        "std_unit": "V",
        "scenarios": [
          {
            "condition": "Isink = 1mA",
            "limits": {
              "LDO_Low_Voltage_CMOS": [0.3, 0.4],
              "LDO_High_Voltage_Bipolar": [0.4, 0.5]
            }
          }
        ]
      },
      {
        "key": "pgood_leakage",
        "symbol": "I<sub>PG(LEAK)</sub>",
        "spec_type": "max_limit",
        "column_model": "TYP_MAX",
        "engineering_class": "PERFORMANCE_LIMIT",
        "special_semantics": "NONE",
        "llm_context": {
          "formal_name": "Power Good Leakage Current",
          "aliases": ["I_PG(LEAK) [nA/µA] Typ./Max. – PGOOD Leakage", "PG Leakage I_PG(LEAK) [nA] Max.", "I_PG(LEAK) [nA] Typ./Max. (Open-Drain High, PG Off)", "PGOOD Pin Leakage [nA] Max. (PG = Not Asserted)", "I_PG [nA] Max. – PGOOD Off-State Leakage Current", "Power Good Leakage I_PG(LEAK) [µA] Max.", "Leakage Current PGOOD I_PG [nA] Max. (High State)", "I(PG)(LEAK) [nA] Max. – PG Open-Drain Off Current", "PGOOD Leakage [nA] Max. I_PG(LEAK) (Not Asserted)"]
        },
        "possible_units": ["nA", "µA"],
        "std_unit": "nA",
        "scenarios": [
          {
            "condition": "PG high",
            "limits": {
              "LDO_Low_Voltage_CMOS": [1, 10, 100],
              "LDO_High_Voltage_Bipolar": [10, 100, 1000]
            }
          }
        ]
      },
      {
        "key": "pgood_delay",
        "symbol": "t<sub>PG</sub>",
        "spec_type": "nominal",
        "column_model": "TYP_MAX",
        "engineering_class": "NOMINAL_PARAMETER",
        "special_semantics": "NONE",
        "llm_context": {
          "formal_name": "Power Good Delay",
          "aliases": ["t_PG [µs/ms] Typ./Max. – Power Good Delay", "PG Delay t_PG [µs] (V_OUT Crosses Threshold to PG=High)", "t_PG [µs] Typ./Max. (PGOOD Assert Delay)", "PGOOD Assertion Delay t_PG [µs] (After V_OUT In-Reg.)", "t_PG Typ./Max. [ms] – PGOOD De-Bounce Delay", "Power Good Delay [µs] t_PG (Typ.)", "t_PG [µs] – Delay: V_OUT Threshold Crossing to PG High", "PGOOD Delay t_PG [µs] Max.", "PG Pin Propagation Delay [µs] t_PG", "t_PGOOD [µs] Typ./Max. – PGOOD Turn-On Delay"]
        },
        "possible_units": ["µs", "ms"],
        "std_unit": "µs",
        "scenarios": [
          {
            "condition": "Vout crosses threshold",
            "limits": {
              "LDO_Low_Voltage_CMOS": [10, 50, 100],
              "LDO_High_Voltage_Bipolar": [50, 100, 500]
            }
          }
        ]
      },
      {
        "key": "open_loop_gain",
        "symbol": "A<sub>OL</sub>",
        "spec_type": "min_limit",
        "column_model": "MIN_TYP",
        "engineering_class": "PERFORMANCE_LIMIT",
        "special_semantics": "NONE",
        "llm_context": {
          "formal_name": "Open Loop Gain",
          "aliases": ["A_OL [dB] Min./Typ. – Open Loop DC Gain", "DC Gain A_OL [dB] (Min./Typ., Error Amplifier)", "A_OL [dB] Min. Typ. (Open-Loop, DC)", "Open-Loop Voltage Gain [dB] A_OL (DC, Typ.)", "A_V(OL) [dB] Min. Typ. – Error Amp DC Gain", "Open Loop Gain A_OL [dB] (Typ., Error Amplifier, DC)", "A_OL Typ. [dB] – Loop Gain at DC (Error Amplifier)", "Voltage Gain A_OL [dB] Min. Typ. (Open Loop, DC)", "Open Loop DC Gain A_OL [dB] (Typ.)"]
        },
        "possible_units": ["dB"],
        "std_unit": "dB",
        "scenarios": [
          {
            "condition": "DC",
            "limits": {
              "LDO_Low_Voltage_CMOS": [60, 70, 80],
              "LDO_High_Voltage_Bipolar": [50, 60, 70]
            }
          }
        ]
      },
      {
        "key": "pass_element_resistance",
        "symbol": "R<sub>DS(ON)</sub>",
        "spec_type": "max_limit",
        "column_model": "TYP_MAX",
        "engineering_class": "PERFORMANCE_LIMIT",
        "special_semantics": "NONE",
        "llm_context": {
          "formal_name": "Pass Element On-Resistance",
          "aliases": ["R_DS(ON) [mΩ/Ω] Typ./Max. – Pass FET On-Resistance", "Pass Element R_DS(ON) [mΩ]", "On-Resistance R_DS(ON) [mΩ] Max. (Pass Transistor)", "R_DS(ON) [mΩ] Typ. Max. (PFET/NFET Pass Element)", "Pass FET R_DS(ON) [mΩ] (= V_DO / I_OUT, Approx.)", "R_DS(on) [mΩ] (Internal Pass Device)", "On-Resistance Pass Switch R_DS(ON) [Ω] Typ./Max.", "R_DS(ON) [mΩ] Max. – Internal LDO Pass Element", "Pass Element On-Res. [mΩ] Typ. Max.", "R(DS)(ON) [mΩ] Typ. Max. (MOSFET Pass)"]
        },
        "possible_units": ["mΩ", "Ω"],
        "std_unit": "mΩ",
        "scenarios": [
          {
            "condition": "At Iout Max",
            "limits": {
              "LDO_Low_Voltage_CMOS": [100, 200, 1000],
              "LDO_High_Voltage_Bipolar": [200, 500, 2000]
            }
          }
        ]
      },
      {
        "key": "output_discharge_resistance",
        "symbol": "R<sub>DISCH</sub>",
        "spec_type": "nominal",
        "column_model": "TYP_ONLY",
        "engineering_class": "NOMINAL_PARAMETER",
        "special_semantics": "NONE",
        "llm_context": {
          "formal_name": "Output Discharge Resistance",
          "aliases": ["R_DISCH [Ω/kΩ] Typ. – Output Discharge Resistance", "Discharge Resistor R_DISCH [Ω] Typ. (When Disabled)", "R_DISCH [Ω] Typ. (V_OUT Discharge Path, Device Off)", "Output Discharge R [Ω] Typ. (V_OUT Bleed)", "R_DISCH Typ. [kΩ] – Internal Discharge (Shutdown)", "Discharge Resistance R_DISCH [Ω] (Active Discharge, Off)", "R_DISCH [Ω] – V_OUT Bleed Resistor (When EN=Low)", "Output Bleed Resistance [kΩ] R_DISCH (Disabled State)", "Active Discharge R_DISCH [Ω] Typ."]
        },
        "possible_units": ["Ω", "kΩ"],
        "std_unit": "Ω",
        "scenarios": [
          {
            "condition": "When disabled",
            "limits": {
              "LDO_Low_Voltage_CMOS": [100, 200, 500],
              "LDO_High_Voltage_Bipolar": [500, 1000, 5000]
            }
          }
        ]
      },
      {
        "key": "power_on_reset_threshold",
        "symbol": "V<sub>POR</sub>",
        "spec_type": "nominal",
        "column_model": "MIN_TYP_MAX",
        "engineering_class": "NOMINAL_PARAMETER",
        "special_semantics": "NONE",
        "llm_context": {
          "formal_name": "Power-On Reset Threshold",
          "aliases": ["V_POR [V] – Power-On Reset Threshold (V_IN Rising)", "POR Threshold V_POR [V] (Min./Typ./Max., V_IN Rising)", "V_POR [V] Min./Typ./Max. – POR Activation Level", "Power-On Reset V_POR [V] (Rising V_IN, Startup)", "V_POR Rising [V] Typ. (Input Threshold, POR Release)", "POR Trip Voltage V_POR [V] (V_IN Must Exceed for Start)", "V_POR [V] Typ. – POR Threshold (V_IN Rising Edge)", "Power-On Reset Level V_POR [V] (Min./Typ./Max.)", "V(POR) Rising [V] Min. Typ. Max. – POR Release Voltage"]
        },
        "possible_units": ["V"],
        "std_unit": "V",
        "scenarios": [
          {
            "condition": "Vin rising",
            "limits": {
              "LDO_Low_Voltage_CMOS": [1.0, 1.5, 2.0],
              "LDO_High_Voltage_Bipolar": [2.0, 2.5, 3.0]
            }
          }
        ]
      },
      {
        "key": "tracking_accuracy",
        "symbol": "ΔV<sub>TRACK</sub>",
        "spec_type": "max_limit",
        "column_model": "TYP_MAX",
        "engineering_class": "PERFORMANCE_LIMIT",
        "special_semantics": "NONE",
        "llm_context": {
          "formal_name": "Tracking Accuracy",
          "aliases": ["ΔV_TRACK [mV/%] Typ./Max. – Tracking Accuracy", "Voltage Tracking Error ΔV_TRACK [mV] (Typ./Max.)", "ΔV_TRACK [mV] Max. – V_OUT Tracking Error", "Tracking Accuracy [mV] (V_OUT vs. V_TRACK, Max.)", "ΔV_TRACK Typ./Max. [mV] (During Tracking Mode)", "Tracking Error [mV] Max. ΔV_TRACK", "V_OUT Tracking Accuracy [%] Max. ΔV_TRACK", "ΔV_TRACK [mV] Max. – Error Between V_OUT and Reference", "Voltage Tracking Error [mV] Max. (V_OUT vs. V_REF_TRACK)"]
        },
        "possible_units": ["mV", "%"],
        "std_unit": "mV",
        "scenarios": [
          {
            "condition": "During tracking",
            "limits": {
              "LDO_Low_Voltage_CMOS": [5, 10, 20],
              "LDO_High_Voltage_Bipolar": [10, 20, 50]
            }
          }
        ]
      },
      {
        "key": "reference_voltage",
        "symbol": "V<sub>REF</sub>",
        "spec_type": "nominal",
        "column_model": "MIN_TYP_MAX",
        "engineering_class": "NOMINAL_PARAMETER",
        "special_semantics": "NONE",
        "llm_context": {
          "formal_name": "Internal Reference Voltage",
          "aliases": ["V_REF [V] Typ. – Internal Bandgap Reference", "Bandgap Reference V_REF [V] Min./Typ./Max.", "V_REF [V] Typ. (Internal Reference)", "Internal Reference Voltage V_REF [mV] (Typ.)", "V_BG [V] – Bandgap Reference Voltage (Typ.)", "V_REF [V] Min. Typ. Max. (Internal)", "Reference Voltage V_REF [V] (Bandgap)", "V_REF Typ. [V] – Error Amplifier Reference Level", "Internal Reference V_REF [mV] (Typ., All Conditions)"]
        },
        "possible_units": ["V", "mV"],
        "std_unit": "V",
        "scenarios": [
          {
            "condition": "25°C",
            "limits": {
              "LDO_Low_Voltage_CMOS": [0.6, 0.8, 1.2],
              "LDO_High_Voltage_Bipolar": [1.2, 1.25, 2.5]
            }
          }
        ]
      },
      {
        "key": "reference_tempco",
        "symbol": "TC<sub>VREF</sub>",
        "spec_type": "max_limit",
        "column_model": "TYP_MAX",
        "engineering_class": "PERFORMANCE_LIMIT",
        "special_semantics": "NONE",
        "llm_context": {
          "formal_name": "Reference Voltage Temperature Coefficient",
          "aliases": ["TC_VREF [ppm/°C] Typ./Max. – Vref Tempco", "Vref Tempco TC_VREF [ppm/°C] (Over Temp Range)", "V_REF Temperature Coefficient [ppm/°C] Max.", "TC_VREF [ppm/°C] Typ. Max. (V_REF Drift Over Temp.)", "Bandgap Tempco TC_VREF [ppm/°C]", "Reference Voltage TC [ppm/°C] Typ./Max. (Over Temp)", "TC_VREF [ppm/K] Max. – V_REF Thermal Drift", "ΔV_REF / ΔT [ppm/°C] Typ. Max. (Operating Range)", "Tempco V_REF [ppm/°C] Typ. Max."]
        },
        "possible_units": ["ppm/°C"],
        "std_unit": "ppm/°C",
        "scenarios": [
          {
            "condition": "Over temp",
            "limits": {
              "LDO_Low_Voltage_CMOS": [20, 50, 100],
              "LDO_High_Voltage_Bipolar": [50, 100, 200]
            }
          }
        ]
      },
      {
        "key": "feedback_pin_voltage",
        "symbol": "V<sub>FB</sub>",
        "spec_type": "nominal",
        "column_model": "MIN_TYP_MAX",
        "engineering_class": "NOMINAL_PARAMETER",
        "special_semantics": "NONE",
        "llm_context": {
          "formal_name": "Feedback Pin Voltage",
          "aliases": ["V_FB [V] Typ. – Feedback Pin Voltage (Regulation)", "FB Pin Voltage V_FB [V] Min./Typ./Max. (Regulation)", "V_FB [V] Typ. (= V_REF, Regulation)", "Feedback Voltage V_FB [mV] (Error Amp Ref. Level)", "V_FB [V] Min. Typ. Max. (Feedback Pin)", "V_FB Regulation [V] Typ. (FB Pin = V_REF)", "V_FB [V] – FB Pin Target Voltage in Regulation", "Feedback Pin V_FB [V] Typ. (R1/R2 Divider Reference)", "V_FB Typ. Min. Max. [V] (Feedback, All Conditions)", "V(FB) [V] – Feedback Node Voltage (Regulation)"]
        },
        "possible_units": ["V"],
        "std_unit": "V",
        "scenarios": [
          {
            "condition": "Regulation",
            "limits": {
              "LDO_Low_Voltage_CMOS": [0.6, 0.8, 1.2],
              "LDO_High_Voltage_Bipolar": [1.2, 1.25, 2.5]
            }
          }
        ]
      },
      {
        "key": "feedback_pin_current",
        "symbol": "I<sub>FB</sub>",
        "spec_type": "max_limit",
        "column_model": "TYP_MAX",
        "engineering_class": "PERFORMANCE_LIMIT",
        "special_semantics": "NONE",
        "llm_context": {
          "formal_name": "Feedback Pin Bias Current",
          "aliases": ["I_FB [nA/µA] Typ./Max. – Feedback Pin Bias Current", "FB Pin Current I_FB [nA] Max.", "I_FB [nA] Typ./Max. (FB Pin Input Bias)", "Feedback Bias Current I_FB [nA] (Error Amp Input)", "I_FB [nA] Max. – Input Bias at FB Pin", "FB Pin Leakage I_FB [nA] Typ./Max.", "I_FB Typ. Max. [µA] – Error Amp FB Input Current", "Feedback Pin Input Current [nA] I_FB Max.", "I(FB) [nA] Typ./Max. – Bias at Feedback Node"]
        },
        "possible_units": ["nA", "µA"],
        "std_unit": "nA",
        "scenarios": [
          {
            "condition": "",
            "limits": {
              "LDO_Low_Voltage_CMOS": [1, 10, 50],
              "LDO_High_Voltage_Bipolar": [10, 50, 100]
            }
          }
        ]
      },
      {
        "key": "adj_pin_voltage",
        "symbol": "V<sub>ADJ</sub>",
        "spec_type": "nominal",
        "column_model": "MIN_TYP_MAX",
        "engineering_class": "NOMINAL_PARAMETER",
        "special_semantics": "NONE",
        "llm_context": {
          "formal_name": "Adjust Pin Voltage",
          "aliases": ["V_ADJ [V] Typ. – Adjust Pin Voltage (Regulation)", "ADJ Pin Voltage V_ADJ [V] Min./Typ./Max. (Regulation)", "V_ADJ [V] Typ. (= V_REF, Adjustable Output Config.)", "Adjust Voltage V_ADJ [mV] (Reference for Adj. Output)", "V_ADJ [V] Min. Typ. Max. (ADJ Pin)", "V_ADJ Regulation [V] Typ. (ADJ Pin = V_REF)", "V_ADJ [V] – ADJ Pin Target Voltage in Regulation", "Adjust Pin V_ADJ [V] Typ. (R1/R2 Voltage Divider Ref.)", "V_ADJ Typ. Min. Max. [V] (Adjust, All Conditions)", "V(ADJ) [V] – Adjust Node Voltage (Regulation)"]
        },
        "possible_units": ["V"],
        "std_unit": "V",
        "scenarios": [
          {
            "condition": "Regulation",
            "limits": {
              "LDO_Low_Voltage_CMOS": [0.6, 0.8, 1.2],
              "LDO_High_Voltage_Bipolar": [1.2, 1.25, 2.5]
            }
          }
        ]
      },
      {
        "key": "adj_pin_current",
        "symbol": "I<sub>ADJ</sub>",
        "spec_type": "max_limit",
        "column_model": "TYP_MAX",
        "engineering_class": "PERFORMANCE_LIMIT",
        "special_semantics": "NONE",
        "llm_context": {
          "formal_name": "Adjust Pin Current",
          "aliases": ["I_ADJ [nA/µA] Typ./Max. – Adjust Pin Current", "ADJ Pin Current I_ADJ [µA] Max.", "I_ADJ [nA] Typ./Max. (ADJ Pin, Adjustable Config.)", "Adjust Pin Bias Current I_ADJ [µA] (Error Amp Input)", "I_ADJ [nA] Max. – Current Into ADJ Pin", "ADJ Pin Leakage I_ADJ [µA] Typ./Max.", "I_ADJ Typ. Max. [µA] – ADJ Pin Input Current", "Adjust Pin Input Current [nA] I_ADJ Max.", "I(ADJ) [µA] Typ./Max. – Bias at Adjust Node"]
        },
        "possible_units": ["nA", "µA"],
        "std_unit": "nA",
        "scenarios": [
          {
            "condition": "",
            "limits": {
              "LDO_Low_Voltage_CMOS": [1, 10, 50],
              "LDO_High_Voltage_Bipolar": [10, 50, 200]
            }
          }
        ]
      },
      {
        "key": "output_capacitor_min",
        "symbol": "C<sub>OUT(min)</sub>",
        "spec_type": "min_limit",
        "column_model": "MIN_ONLY",
        "engineering_class": "PERFORMANCE_LIMIT",
        "special_semantics": "NONE",
        "llm_context": {
          "formal_name": "Minimum Output Capacitor",
          "aliases": ["C_OUT(min) [µF] – Minimum Output Capacitor for Stability", "Cout Min. C_OUT(min) [µF] (For Stable Operation)", "C_OUT(min) [µF] Min. (Required for Loop Stability)", "Minimum Output Cap. [µF] C_OUT (For Regulation)", "C_OUT Min. [µF] (Stability Requirement, See Note)", "Minimum C_OUT [µF] – Required at V_OUT Pin", "C_OUT(min) [µF] (Stability; See Also ESR Requirement)", "Recommended Minimum C_OUT [µF] (For Stable V_OUT)", "Min. Output Capacitance [µF] C_OUT(min) (Required)", "C_OUT(min) [µF] – Minimum For Stable Loop (ESR Dep.)"]
        },
        "possible_units": ["µF"],
        "std_unit": "µF",
        "scenarios": [
          {
            "condition": "For stability",
            "limits": {
              "LDO_Low_Voltage_CMOS": [1, 2.2, 4.7],
              "LDO_High_Voltage_Bipolar": [4.7, 10, 22]
            }
          }
        ]
      },
      {
        "key": "output_capacitor_esr",
        "symbol": "ESR<sub>OUT</sub>",
        "spec_type": "nominal",
        "column_model": "MIN_MAX",
        "engineering_class": "PERFORMANCE_LIMIT",
        "special_semantics": "NONE",
        "llm_context": {
          "formal_name": "Output Capacitor ESR Range",
          "aliases": ["ESR_OUT [mΩ/Ω] – Output Capacitor ESR Range (Stability)", "Cout ESR Range [mΩ to Ω] (For Stable Operation)", "ESR_OUT [mΩ] Min. to Max. (Stability, C_OUT ESR)", "Output Cap. ESR Range [mΩ–Ω] (For Loop Stability)", "ESR(COUT) [mΩ] Min./Max. – Required ESR Window", "ESR Range [mΩ to Ω] (C_OUT, Loop Stability Req.)", "Cout ESR [mΩ to Ω] – Acceptable Range (See Note)", "ESR_OUT Range [mΩ–Ω] (Min/Max for Stability)", "C_OUT ESR [Ω] Min. Max. (Stability; Typ. MLCC/Al-Cap)", "Required ESR Range [mΩ] – Output Cap. (Stability Note)"]
        },
        "possible_units": ["mΩ", "Ω"],
        "std_unit": "mΩ",
        "scenarios": [
          {
            "condition": "For stability",
            "limits": {
              "LDO_Low_Voltage_CMOS": ["5 to 500"],
              "LDO_High_Voltage_Bipolar": ["10 to 5000"]
            }
          }
        ]
      },
      {
        "key": "input_capacitor_min",
        "symbol": "C<sub>IN(min)</sub>",
        "spec_type": "min_limit",
        "column_model": "MIN_ONLY",
        "engineering_class": "PERFORMANCE_LIMIT",
        "special_semantics": "NONE",
        "llm_context": {
          "formal_name": "Minimum Input Capacitor",
          "aliases": ["C_IN(min) [µF] – Minimum Input Capacitor (Recommended)", "Cin Min. C_IN(min) [µF] (For Stable Input Supply)", "C_IN(min) [µF] Min. (Recommended at V_IN Pin)", "Minimum Input Cap. [µF] C_IN (Recommended, Close to IC)", "C_IN Min. [µF] (Bypass, Recommended at Input Pin)", "Minimum C_IN [µF] – Required at V_IN Supply Pin", "C_IN(min) [µF] (Input Bypass; See Layout Guidelines)", "Recommended Minimum C_IN [µF] (For V_IN Stability)", "Min. Input Capacitance [µF] C_IN(min) (Recommended)", "C_IN(min) [µF] – Min. Input Decoupling (Near Pin)"]
        },
        "possible_units": ["µF"],
        "std_unit": "µF",
        "scenarios": [
          {
            "condition": "Recommended",
            "limits": {
              "LDO_Low_Voltage_CMOS": [0.1, 1, 2.2],
              "LDO_High_Voltage_Bipolar": [1, 4.7, 10]
            }
          }
        ]
      }
    ]
  },

    # ==============================================================================
    # 6. INDUCTOR - CORRECTED WITH METADATA FIELDS חלק6
    # ==============================================================================
  "INDUCTOR": {
    "archetypes": ["Power_Ferrite", "RF_Ceramic", "Common_Mode_Choke"],
    
    "ABS_MAX": [
      {
        "key": "rated_current",
        "symbol": "I<sub>R</sub>",
        "spec_type": "max_rating",
        "column_model": "MAX_ONLY",
        "engineering_class": "SAFETY_LIMIT",
        "special_semantics": "NONE",
        "llm_context": {"formal_name": "Rated Current", "aliases": ["I_R [A/mA] Max. – Rated Current (ΔT=40°C)", "Rated Current I_R [A] Max. (Temp Rise 40°C)", "I_R [mA] Max. – DC Current Rating (ΔT=40°C)", "Rated DC Current I_R [A] (Max., 40°C Rise)", "DC Current Rating [A] I_R (ΔT=40°C or 20°C)", "I_R [mA] Max. (For 40°C / 20°C Temperature Rise)", "Max. Continuous DC Current I_R [A] (ΔT Specified)"]},
        "possible_units": ["mA", "A"],
        "std_unit": "mA",
        "scenarios": [
          {
            "condition": "Temp Rise 40°C",
            "limits": {
              "Power_Ferrite": [1000, 2000, 5000, 10000, 20000],
              "RF_Ceramic": [100, 200, 500],
              "Common_Mode_Choke": [500, 1000, 5000]
            }
          },
          {
            "condition": "Temp Rise 20°C",
            "limits": {
              "Power_Ferrite": [800, 1500, 4000, 8000, 15000],
              "RF_Ceramic": [80, 150, 400],
              "Common_Mode_Choke": [400, 800, 4000]
            }
          }
        ]
      },
      {
        "key": "saturation_current",
        "symbol": "I<sub>sat</sub>",
        "spec_type": "max_rating",
        "column_model": "MAX_ONLY",
        "engineering_class": "SAFETY_LIMIT",
        "special_semantics": "NONE",
        "llm_context": {"formal_name": "Saturation Current", "aliases": ["I_sat [A/mA] – Saturation Current (30% L Drop)", "Saturation Current I_sat [A] (ΔL = -30%, Typ.)", "Isat [mA] – Current at 30% Inductance Drop", "I_sat [A] (L Drops 30% / 10% from Nominal)", "Saturation I_sat [A] (At Which L Drops 30%)", "I_SAT [A] – Core Saturation Current (ΔL=-30%)", "I_sat [mA] (10% or 30% L Drop from Nominal)", "Saturation Current [A] I_sat (L Decrease Criterion)", "I_SAT Typ. [mA] (L = 70% of L_0 at This Current)"]},
        "possible_units": ["mA", "A"],
        "std_unit": "mA",
        "scenarios": [
          {
            "condition": "30% L drop",
            "limits": {
              "Power_Ferrite": [1200, 2500, 6000, 12000, 25000],
              "RF_Ceramic": [150, 300, 700],
              "Common_Mode_Choke": [600, 1200, 6000]
            }
          },
          {
            "condition": "10% L drop",
            "limits": {
              "Power_Ferrite": [800, 1500, 4000, 8000, 18000],
              "RF_Ceramic": [100, 200, 500],
              "Common_Mode_Choke": [400, 800, 4000]
            }
          }
        ]
      },
      {
        "key": "max_operating_temp",
        "symbol": "T<sub>max</sub>",
        "spec_type": "max_rating",
        "column_model": "MAX_ONLY",
        "engineering_class": "SAFETY_LIMIT",
        "special_semantics": "NONE",
        "llm_context": {"formal_name": "Maximum Operating Temperature", "aliases": ["T_max [°C] – Maximum Operating Temperature", "T_max [°C] Max. (Continuous Operation Limit)", "Upper Category Temp. T_max [°C] (Operating)", "Max. Operating T [°C] (Component Surface Incl.)", "T_OP(max) [°C] – Upper Operating Limit", "T_max [°C] (Continuous; Self-Heating Included)", "T_MAX [°C] – Max. Component Temperature (Op.)", "Operating Temperature Max. T_max [°C] (Abs.)"]},
        "possible_units": ["°C"],
        "std_unit": "°C",
        "scenarios": [
          {
            "condition": "",
            "limits": {
              "Power_Ferrite": [125, 155, 175],
              "RF_Ceramic": [125, 150],
              "Common_Mode_Choke": [125, 155]
            }
          }
        ]
      },
      {
        "key": "storage_temp",
        "symbol": "T<sub>STG</sub>",
        "spec_type": "max_rating",
        "column_model": "MIN_MAX",
        "engineering_class": "SAFETY_LIMIT",
        "special_semantics": "NONE",
        "llm_context": {"formal_name": "Storage Temperature Range", "aliases": ["T_STG [°C] Storage Range (Min. to Max.)", "T_stg Range [°C] (Non-Operating, Unpowered)", "Storage Temp. T_STG [°C] Min./Max.", "T_STG [°C] (Unpowered Storage, See Range)", "Storage Temp. Range [°C] T_stg (Min/Max)", "Non-Operating Storage Temp. [°C] T_STG", "T_STG [°C] – Component Storage (Unpowered)", "Storage Temperature [°C] Min. Max. T_STG"]},
        "possible_units": ["°C"],
        "std_unit": "°C",
        "scenarios": [
          {
            "condition": "Min to Max",
            "limits": {
              "Power_Ferrite": ["-55 to 155", "-55 to 175"],
              "RF_Ceramic": ["-55 to 125", "-55 to 150"],
              "Common_Mode_Choke": ["-55 to 155"]
            }
          }
        ]
      },
      {
        "key": "max_ac_voltage",
        "symbol": "V<sub>AC(max)</sub>",
        "spec_type": "max_rating",
        "column_model": "MAX_ONLY",
        "engineering_class": "SAFETY_LIMIT",
        "special_semantics": "NONE",
        "llm_context": {"formal_name": "Maximum AC Voltage", "aliases": ["V_AC(max) [Vrms] – Maximum AC Voltage Rating", "Max AC Voltage V_AC [Vrms] (RMS, Continuous)", "Rated Voltage V_AC [Vrms] (Max., RMS)", "V_AC(max) [V] RMS – Max. Applied AC Voltage", "Max. AC Voltage [Vrms] V_AC (Continuous, RMS)", "Rated AC Voltage V_R [Vrms] (Max., Continuous)", "V(AC) Max. [Vrms] – Continuous AC Voltage Rating", "Max. Rated Voltage [V] V_AC (RMS, Operating)", "AC Voltage Rating V_AC [Vrms] Max. (Continuous)", "V_AC(max) [Vrms] (RMS, Operating, Do Not Exceed)"]},
        "possible_units": ["V", "Vrms"],
        "std_unit": "Vrms",
        "scenarios": [
          {
            "condition": "RMS",
            "limits": {
              "Power_Ferrite": [10, 25, 50, 100],
              "RF_Ceramic": [5, 10, 25],
              "Common_Mode_Choke": [50, 100, 250, 500]
            }
          }
        ]
      },
      {
        "key": "test_voltage",
        "symbol": "V<sub>TEST</sub>",
        "spec_type": "max_rating",
        "column_model": "TYP_ONLY",
        "engineering_class": "SAFETY_LIMIT",
        "special_semantics": "NONE",
        "llm_context": {"formal_name": "Test Voltage (Hi-Pot)", "aliases": ["V_TEST [Vrms] – Hi-Pot Test Voltage", "Dielectric Test Voltage V_TEST [Vrms]", "Hi-Pot Voltage V_TEST [V] (Between Windings)", "Withstanding Voltage [Vrms] V_TEST", "Hi-Pot V_TEST [Vrms] – Insulation Test", "Dielectric Strength Test V_TEST [Vrms]", "Test Voltage V_HI-POT [V] (Between Coils)", "V_TEST [Vrms] Dielectric (No Breakdown)", "Hi-Pot Test Voltage [Vrms] V_TEST (Per IEC)"]},
        "possible_units": ["V", "Vrms"],
        "std_unit": "Vrms",
        "scenarios": [
          {
            "condition": "1 second",
            "limits": {
              "Power_Ferrite": [100, 250, 500],
              "RF_Ceramic": [100],
              "Common_Mode_Choke": [500, 1000, 2500, 4000]
            }
          }
        ]
      },
      {
        "key": "insulation_resistance",
        "symbol": "R<sub>INS</sub>",
        "spec_type": "min_limit",
        "column_model": "MIN_ONLY",
        "engineering_class": "SAFETY_LIMIT",
        "special_semantics": "NONE",
        "llm_context": {"formal_name": "Insulation Resistance", "aliases": ["R_INS [MΩ/GΩ] Min. – Insulation Resistance", "Isolation Resistance R_INS [MΩ] Min.", "Rins [MΩ] Min. (Between Windings)", "Insulation Resistance R_ISO [GΩ] Min.", "R_INS Min. [MΩ] – Between Coils", "R_ins [GΩ] Min. (Winding-to-Winding)", "Insulation Res. R_INS [MΩ] Min. (DC)", "R(INS) [MΩ] Min. – DC Isolation", "Insulation Resistance [MΩ] Min. R_INS"]},
        "possible_units": ["MΩ", "GΩ"],
        "std_unit": "MΩ",
        "scenarios": [
          {
            "condition": "At 500VDC",
            "limits": {
              "Power_Ferrite": [10, 100],
              "RF_Ceramic": [100],
              "Common_Mode_Choke": [100, 1000]
            }
          }
        ]
      }
    ],
    
    "ELEC_CHAR": [
      {
        "key": "inductance",
        "symbol": "L",
        "spec_type": "nominal",
        "column_model": "MIN_TYP_MAX",
        "engineering_class": "NOMINAL_PARAMETER",
        "special_semantics": "NONE",
        "llm_context": {"formal_name": "Inductance", "aliases": ["L [µH/nH/mH] Typ. – Inductance Value", "Inductance L [µH] Min./Typ./Max.", "L [nH] Nom. (Measured @ f_test, Low Signal)", "Inductance Value L [µH] (Min/Typ/Max)", "L [µH] ±Tol%", "Inductance L [nH/µH/mH] (Nom.)", "Induct. L [µH] (Min./Typ./Max., See Test Freq.)", "L [µH] Nominal", "Inductance [nH/µH] Min. Typ. Max."]},
        "possible_units": ["nH", "µH", "mH"],
        "std_unit": "µH",
        "scenarios": [
          {
            "condition": "Test Freq Defined",
            "limits": {
              "Power_Ferrite": [0.1, 0.22, 0.47, 1.0, 2.2, 4.7, 10, 22, 47, 100, 220, 470, 1000],
              "RF_Ceramic": [0.001, 0.0022, 0.0047, 0.01, 0.022, 0.047, 0.1, 0.22, 0.47, 1.0],
              "Common_Mode_Choke": [10, 47, 100, 220, 470, 1000, 2200, 4700, 10000]
            }
          }
        ]
      },
      {
        "key": "inductance_frequency",
        "symbol": "f<sub>TEST</sub>",
        "spec_type": "nominal",
        "column_model": "TYP_ONLY",
        "engineering_class": "NOMINAL_PARAMETER",
        "special_semantics": "NONE",
        "llm_context": {"formal_name": "Inductance Test Frequency", "aliases": ["f_TEST [kHz/MHz] Typ. – Inductance Measurement Frequency", "Test Frequency f_test [kHz] (For L Measurement)", "Measurement Frequency f [MHz] (L Characterization)", "f_test [kHz] Typ. – Standard L Measurement Freq.", "f_TEST = ? kHz (Freq. at Which L is Specified)", "Inductance Test Freq. [kHz] f_TEST (Typ.)", "f_test [MHz] – Frequency for L Measurement", "Measurement Frequency f [kHz] (L & Q Test Condition)", "f_TEST [MHz] Typ. (Test Condition for L Measurement)"]},
        "possible_units": ["kHz", "MHz"],
        "std_unit": "kHz",
        "scenarios": [
          {
            "condition": "Standard",
            "limits": {
              "Power_Ferrite": [100, 250, 1000],
              "RF_Ceramic": [1000, 10000, 100000],
              "Common_Mode_Choke": [100, 1000]
            }
          }
        ]
      },
      {
        "key": "tolerance",
        "symbol": "Tol",
        "spec_type": "nominal",
        "column_model": "TYP_ONLY",
        "engineering_class": "NOMINAL_PARAMETER",
        "special_semantics": "NONE",
        "llm_context": {"formal_name": "Inductance Tolerance", "aliases": ["Tol [%] – Inductance Tolerance (±%)", "L Tolerance [%] (EIA Letter Code, e.g., K=±10%)", "ΔL/L [%] Tolerance", "Inductance Tol. ±[%] (Initial, Before Aging)", "L Accuracy [%] (Nominal, EIA Code: J/K/M)", "Tolerance [%] Inductance (Min/Max from Nominal L)", "L Tol. [%] (Initial; Excl. Temp. & DC Bias Effects)"]},
        "possible_units": ["%"],
        "std_unit": "%",
        "scenarios": [
          {
            "condition": "Standard",
            "limits": {
              "Power_Ferrite": [10, 20, 30],
              "RF_Ceramic": [0.5, 1, 2, 5, 10],
              "Common_Mode_Choke": [20, 30]
            }
          }
        ]
      },
      {
        "key": "dcr",
        "symbol": "DCR",
        "spec_type": "max_limit",
        "column_model": "TYP_MAX",
        "engineering_class": "PERFORMANCE_LIMIT",
        "special_semantics": "NONE",
        "llm_context": {"formal_name": "DC Resistance", "aliases": ["DCR [mΩ/Ω] Typ./Max. – DC Winding Resistance", "DC Resistance R_DC [mΩ] Max.", "DCR [mΩ] Typ. Max. (Winding)", "R_DC [mΩ] Max. – DC Resistance of Winding", "DC Resistance [Ω] Typ./Max. (Winding)", "R_DC Typ./Max. [mΩ] (Series Resistance, DC)", "DCR [Ω] Max. (Measured at DC, Room Temperature)", "Winding DC Resistance R_DC [mΩ] Typ. Max.", "R(DC) [mΩ] Typ. Max. – Winding Resistance (DC)"]},
        "possible_units": ["mΩ", "Ω"],
        "std_unit": "mΩ",
        "scenarios": [
          {
            "condition": "Max at 25°C",
            "limits": {
              "Power_Ferrite": [2, 5, 10, 20, 50, 100, 200, 500],
              "RF_Ceramic": [50, 100, 200, 500, 1000, 2000, 5000],
              "Common_Mode_Choke": [10, 20, 50, 100, 200]
            }
          }
        ]
      },
      {
        "key": "dcr_tolerance",
        "symbol": "ΔR<sub>DC</sub>",
        "spec_type": "nominal",
        "column_model": "TYP_ONLY",
        "engineering_class": "NOMINAL_PARAMETER",
        "special_semantics": "NONE",
        "llm_context": {"formal_name": "DCR Tolerance", "aliases": ["ΔDCR [%] Typ. – DCR Tolerance", "Resistance Tolerance ΔR_DC [%] (Typical)", "DCR Tol. [%] Typ. (DC Resistance, ±%)", "ΔR_DC [%] – DCR Manufacturing Tolerance", "DCR Tolerance [%] Typ. (At Nominal DCR Value)", "R_DC Tolerance [%] (Typical, Manufacturing Spread)", "ΔR(DC) [%] Typ. – Resistance Tolerance", "DCR Tol [%] Typ. (±%, Winding Resistance)", "DC Resistance Accuracy [%] Typ. (±ΔR_DC)"]},
        "possible_units": ["%"],
        "std_unit": "%",
        "scenarios": [
          {
            "condition": "",
            "limits": {
              "Power_Ferrite": [10, 15, 20],
              "RF_Ceramic": [15, 20],
              "Common_Mode_Choke": [10, 20]
            }
          }
        ]
      },
      {
        "key": "srf",
        "symbol": "f<sub>res</sub>",
        "spec_type": "min_limit",
        "column_model": "MIN_TYP_MAX",
        "engineering_class": "PERFORMANCE_LIMIT",
        "special_semantics": "NONE",
        "llm_context": {"formal_name": "Self Resonant Frequency", "aliases": ["f_res [MHz/GHz] Min./Typ. – Self Resonant Frequency", "SRF [MHz] Min. Typ. (L & C_parasitic Dependent)", "f_SRF [MHz] – Self-Resonant Frequency (Typ.)", "SRF [GHz] Typ. (Above = Capacitive Behavior)", "Self-Resonant Freq. f_res [MHz] Min./Typ./Max.", "f_SRF [MHz] (= 1/(2π√(L·C_p)); Use Below SRF Only)", "Self Resonance Frequency [MHz] f_SRF Min. Typ.", "f_res [GHz] – Inductor SRF (Min., Parasitic C Dep.)", "SRF [MHz] Min. Typ. Max. (Measured, Low Signal)"]},
        "possible_units": ["MHz", "GHz"],
        "std_unit": "MHz",
        "scenarios": [
          {
            "condition": "",
            "limits": {
              "Power_Ferrite": [2, 5, 10, 20, 50, 100],
              "RF_Ceramic": [100, 500, 1000, 2000, 5000, 10000],
              "Common_Mode_Choke": [5, 10, 50, 100, 200]
            }
          }
        ]
      },
      {
        "key": "quality_factor",
        "symbol": "Q",
        "spec_type": "min_limit",
        "column_model": "MIN_TYP_MAX",
        "engineering_class": "PERFORMANCE_LIMIT",
        "special_semantics": "NONE",
        "llm_context": {"formal_name": "Quality Factor", "aliases": ["Q [–] Min./Typ. – Quality Factor", "Q Factor [–] Min. Typ.", "Q Typ./Min. – Inductor Q", "Q = ωL / DCR [–] Min. Typ.", "Quality Factor Q [–]", "Q [–] Min. Typ. Max. (At Specified Test Frequency)"]},
        "possible_units": [""],
        "std_unit": "",
        "scenarios": [
          {
            "condition": "At test freq",
            "limits": {
              "Power_Ferrite": [15, 20, 30, 40, 50],
              "RF_Ceramic": [30, 40, 60, 80, 100, 120],
              "Common_Mode_Choke": [5, 10, 20]
            }
          }
        ]
      },
      {
        "key": "impedance",
        "symbol": "Z",
        "spec_type": "nominal",
        "column_model": "MIN_TYP_MAX",
        "engineering_class": "NOMINAL_PARAMETER",
        "special_semantics": "NONE",
        "llm_context": {"formal_name": "Impedance", "aliases": ["Z [Ω/kΩ] Typ. – Impedance", "Impedance |Z| [Ω] Typ.", "Z [Ω] Typ. Min. Max.", "|Z| [Ω] – Total Impedance (Typ.)", "Impedance Z [kΩ] (See Impedance Curve)", "Impedance at Frequency [Ω] Z (Typ.)", "Z [Ω] Typ. (See Z vs. Freq. Characteristic)"]},
        "possible_units": ["Ω", "kΩ"],
        "std_unit": "Ω",
        "scenarios": [
          {
            "condition": "At 100MHz",
            "limits": {
              "Power_Ferrite": [50, 100, 220, 470, 1000],
              "RF_Ceramic": [10, 22, 47, 100, 220],
              "Common_Mode_Choke": [100, 220, 470, 1000, 2200]
            }
          }
        ]
      },
      {
        "key": "parasitic_capacitance",
        "symbol": "C<sub>P</sub>",
        "spec_type": "nominal",
        "column_model": "TYP_MAX",
        "engineering_class": "NOMINAL_PARAMETER",
        "special_semantics": "NONE",
        "llm_context": {"formal_name": "Parasitic Capacitance", "aliases": ["C_P [pF] Typ./Max. – Parasitic / Stray Capacitance", "Stray Capacitance C_P [pF] Typ. (Inter-Winding)", "Self Capacitance C_P [pF] Typ./Max. (Parasitic)", "C_P [pF] – Interwinding / Shunt Capacitance (Typ.)", "Parasitic Cap. C_stray [pF] Typ. Max. (Self)", "C_par [pF] – Shunt Parasitic Capacitance (Typ.)", "Stray / Parasitic C_P [pF] (Typ., From SRF & L)", "Self Capacitance [pF] C_P Typ. Max. (Winding)", "C_P [fF/pF] Typ. Max. – Inter-Turn Capacitance", "Parasitic Winding Cap. C_P [pF] (C_P = 1/(L·ω²_SRF))"]},
        "possible_units": ["pF", "nF"],
        "std_unit": "pF",
        "scenarios": [
          {
            "condition": "",
            "limits": {
              "Power_Ferrite": [5, 10, 20, 50],
              "RF_Ceramic": [0.1, 0.5, 1, 2],
              "Common_Mode_Choke": [10, 20, 50, 100]
            }
          }
        ]
      },
      {
        "key": "leakage_inductance",
        "symbol": "L<sub>leak</sub>",
        "spec_type": "max_limit",
        "column_model": "TYP_MAX",
        "engineering_class": "PERFORMANCE_LIMIT",
        "special_semantics": "NONE",
        "llm_context": {"formal_name": "Leakage Inductance", "aliases": ["L_leak [nH/µH] Typ./Max. – Leakage Inductance", "Stray Inductance L_leak [nH] Typ. Max.", "Lleak [nH] – Leakage Inductance (One Secondary Short)", "L_leak [nH] Typ./Max. (Winding Leakage, Short Test)", "Leakage L [nH] Max. (Secondary Shorted, Typ.)", "L_leakage [nH] Typ. Max. – Stray Coupling (Measured)", "Stray Inductance L_stray [nH] Typ./Max.", "Leakage Induct. L_leak [µH] (Typ., Short-Circuit Test)", "L_leak [nH] – Non-Coupled Inductance Component", "L(leak) [nH] Typ. Max. (Measured: Output Shorted)"]},
        "possible_units": ["nH", "µH"],
        "std_unit": "nH",
        "scenarios": [
          {
            "condition": "",
            "limits": {
              "Power_Ferrite": [10, 50, 100],
              "RF_Ceramic": [1, 5, 10],
              "Common_Mode_Choke": [5, 10, 50]
            }
          }
        ]
      },
      {
        "key": "differential_mode_inductance",
        "symbol": "L<sub>DM</sub>",
        "spec_type": "nominal",
        "column_model": "MIN_TYP_MAX",
        "engineering_class": "NOMINAL_PARAMETER",
        "special_semantics": "NONE",
        "llm_context": {"formal_name": "Differential Mode Inductance", "aliases": ["L_DM [µH/nH] Typ. – Differential Mode Inductance", "DM Inductance L_DM [µH] Min./Typ./Max.", "Ldm [µH] – Differential Mode L", "L_DM [nH] Typ. (Differential, Windings In-Phase)", "Differential Mode L [µH] Min./Typ./Max.", "L_DM [µH] (Measured: Both Windings Series-Aiding)", "DM Inductance [µH] L_DM (Series-Aiding Config.)", "L(DM) [µH] Typ. – Leakage/Differential Mode L", "L_DM Min. Typ. Max. [µH] (Diff. Mode)", "Differential Mode Inductance L_DM [nH] (Typ.)"]},
        "possible_units": ["µH", "nH"],
        "std_unit": "µH",
        "scenarios": [
          {
            "condition": "At test frequency",
            "limits": {
              "Power_Ferrite": [0.1, 0.5, 1],
              "RF_Ceramic": [0.01, 0.05, 0.1],
              "Common_Mode_Choke": [0.5, 1, 5, 10]
            }
          }
        ]
      },
      {
        "key": "common_mode_inductance",
        "symbol": "L<sub>CM</sub>",
        "spec_type": "nominal",
        "column_model": "MIN_TYP_MAX",
        "engineering_class": "NOMINAL_PARAMETER",
        "special_semantics": "NONE",
        "llm_context": {"formal_name": "Common Mode Inductance", "aliases": ["L_CM [µH/mH] Typ. – Common Mode Inductance", "CM Inductance L_CM [µH] Min./Typ./Max.", "Lcm [mH] – Common Mode L (Windings Series-Opposing)", "L_CM [µH] Typ. (Common Mode, Both Windings Summed)", "Common Mode L [µH] Min./Typ./Max.", "L_CM [mH] (Measured: Both Windings Series-Opposing)", "CM Inductance [mH] L_CM (Series-Opposing Config.)", "L(CM) [µH] Typ. – Common Mode Choke Inductance", "L_CM Min. Typ. Max. [µH] (Common Mode)", "Common Mode Inductance L_CM [mH] (Typ.)"]},
        "possible_units": ["µH", "mH"],
        "std_unit": "µH",
        "scenarios": [
          {
            "condition": "At test frequency",
            "limits": {
              "Power_Ferrite": [10, 47, 100],
              "RF_Ceramic": [1, 10, 47],
              "Common_Mode_Choke": [100, 470, 1000, 4700, 10000]
            }
          }
        ]
      },
      {
        "key": "insertion_loss",
        "symbol": "IL",
        "spec_type": "min_limit",
        "column_model": "MIN_TYP",
        "engineering_class": "PERFORMANCE_LIMIT",
        "special_semantics": "NONE",
        "llm_context": {"formal_name": "Insertion Loss", "aliases": ["IL [dB] Min./Typ. – Insertion Loss", "Attenuation IL [dB] Min.", "IL [dB] – Insertion Loss / Attenuation", "Insertion Loss [dB] Min. Typ.", "Attenuation [dB] Min. (See IL Curve)", "IL [dB] Typ./Min. – Signal Attenuation", "Insertion Loss IL [dB]", "IL [dB] (Min.; See Attenuation vs. Freq.)", "Insertion Loss [dB] Min. Typ. (Low-Level)"]},
        "possible_units": ["dB"],
        "std_unit": "dB",
        "scenarios": [
          {
            "condition": "At 100MHz",
            "limits": {
              "Power_Ferrite": [10, 20, 30],
              "RF_Ceramic": [5, 10, 20],
              "Common_Mode_Choke": [20, 30, 40, 60]
            }
          }
        ]
      },
      {
        "key": "inductance_vs_current",
        "symbol": "ΔL/I",
        "spec_type": "max_limit",
        "column_model": "TYP_MAX",
        "engineering_class": "PERFORMANCE_LIMIT",
        "special_semantics": "NONE",
        "llm_context": {"formal_name": "Inductance Change vs DC Current", "aliases": ["ΔL/I [%] – Inductance Change vs. DC Bias Current", "L vs I [%] – Inductance Droop at Rated Current", "Inductance Droop ΔL [%] (At I_R, From L_0)", "ΔL/L [%] vs. I_DC (At Rated Current)", "L Rolloff ΔL [%] – At Rated DC Current", "ΔL/L_0 [%] Max. (At I = I_R, DC Bias)", "Inductance vs. Current [%] Droop (@ I_rated)", "ΔL/I [%] Typ./Max. (L Change at I_DC = I_rated)"]},
        "possible_units": ["%"],
        "std_unit": "%",
        "scenarios": [
          {
            "condition": "At rated current",
            "limits": {
              "Power_Ferrite": [100, 200, 500, 1000, 2000],
              "RF_Ceramic": [10, 50, 100],
              "Common_Mode_Choke": [100, 200, 500]
            }
          }
        ]
      }
    ],
    
    "MAGNETIC_PROPERTIES": [
      {
        "key": "permeability",
        "symbol": "µ<sub>r</sub>",
        "spec_type": "nominal",
        "column_model": "TYP_ONLY",
        "engineering_class": "NOMINAL_PARAMETER",
        "special_semantics": "NONE",
        "llm_context": {"formal_name": "Relative Permeability", "aliases": ["µ_r [–] Typ. – Relative Permeability (Initial)", "Permeability µ_r [–] Typ. (Initial, Low Field)", "µr [–] – Relative Initial Permeability (Typ.)", "Initial Permeability µ_i [–] Typ. (Low AC Field)", "µ_r Typ. – Core Relative Permeability", "Relative Permeability [–] µ_r (Typ., Initial)", "µ_r (Initial) [–] Typ. – Core Material Property", "µ_r Typ. [–] (Relative, Initial Magnetization Curve)", "Initial Relative Permeability µ_r [–] (Core Material)"]},
        "possible_units": [""],
        "std_unit": "",
        "scenarios": [
          {
            "condition": "Initial",
            "limits": {
              "Power_Ferrite": [20, 40, 60, 90, 125],
              "RF_Ceramic": [5, 10, 20],
              "Common_Mode_Choke": [2000, 5000, 10000]
            }
          }
        ]
      },
      {
        "key": "saturation_flux_density",
        "symbol": "B<sub>sat</sub>",
        "spec_type": "nominal",
        "column_model": "TYP_ONLY",
        "engineering_class": "NOMINAL_PARAMETER",
        "special_semantics": "NONE",
        "llm_context": {"formal_name": "Saturation Flux Density", "aliases": ["B_sat [mT/T] Typ. – Saturation Flux Density", "Bsat [T] – Magnetic Saturation Flux (Typ.)", "B_SAT [mT] – Core Saturation Flux Density (Typ.)", "Saturation Flux B_s [mT] Typ. (Core)", "B_sat [T] Typ. – Core Material B_SAT", "Saturation Flux Density [mT] B_sat (Core)"]},
        "possible_units": ["mT", "T", "G"],
        "std_unit": "mT",
        "scenarios": [
          {
            "condition": "At 25°C",
            "limits": {
              "Power_Ferrite": [300, 400, 500],
              "RF_Ceramic": [200, 300],
              "Common_Mode_Choke": [400, 500]
            }
          }
        ]
      },
      {
        "key": "al_value",
        "symbol": "A<sub>L</sub>",
        "spec_type": "nominal",
        "column_model": "MIN_TYP_MAX",
        "engineering_class": "NOMINAL_PARAMETER",
        "special_semantics": "NONE",
        "llm_context": {"formal_name": "Inductance Factor", "aliases": ["A_L [nH/turn²] Typ. – Inductance Factor (AL Value)", "AL Value A_L [nH/N²] Min./Typ./Max.", "A_L [nH/turn²] – Inductance per Turn Squared", "Inductance Factor A_L [µH/turn²] (Per N²)", "A_L [nH/T²] Min. Typ. Max. (Core Geometry)", "AL [nH/N²] – Core Inductance Constant", "A_L Typ. [nH/turn²] (L = A_L × N²)", "Inductance per Turn² A_L [nH/N²] Min./Typ./Max.", "A_L [µH/T²] (AL Value; L = A_L · N²)", "AL Factor [nH/turn²] Typ. – Core AL (Min./Max.)"]},
        "possible_units": ["nH/turn²", "µH/turn²"],
        "std_unit": "nH/turn²",
        "scenarios": [
          {
            "condition": "Per turn squared",
            "limits": {
              "Power_Ferrite": [10, 20, 50, 100, 200, 500],
              "RF_Ceramic": [1, 5, 10, 20],
              "Common_Mode_Choke": [50, 100, 200, 500]
            }
          }
        ]
      },
      {
        "key": "core_loss",
        "symbol": "P<sub>core</sub>",
        "spec_type": "max_limit",
        "column_model": "TYP_MAX",
        "engineering_class": "PERFORMANCE_LIMIT",
        "special_semantics": "NONE",
        "llm_context": {"formal_name": "Core Loss", "aliases": ["P_core [mW/W] Typ./Max. – Core Loss", "Core Power Loss P_core [mW] Max.", "AC Loss P_core [mW] Typ./Max.", "Core Loss [mW] Typ. Max.", "P_CORE Typ./Max. [mW]", "AC Core Loss P_c [mW] Max.", "Core Loss Power [W] Typ. Max."]},
        "possible_units": ["mW", "W"],
        "std_unit": "mW",
        "scenarios": [
          {
            "condition": "At rated current, 100kHz",
            "limits": {
              "Power_Ferrite": [10, 50, 100, 200, 500],
              "RF_Ceramic": [1, 5, 10],
              "Common_Mode_Choke": [20, 100, 200]
            }
          }
        ]
      },
      {
        "key": "core_loss_density",
        "symbol": "P<sub>cv</sub>",
        "spec_type": "max_limit",
        "column_model": "TYP_MAX",
        "engineering_class": "PERFORMANCE_LIMIT",
        "special_semantics": "NONE",
        "llm_context": {"formal_name": "Core Loss Density", "aliases": ["P_cv [mW/cm³] Typ./Max. – Core Loss Density", "Pcv [kW/m³] – Core Loss per Unit Volume (Typ.)", "Core Loss per Volume [mW/cm³] P_cv (Typ.)", "P_CV Typ./Max. [mW/cm³]", "Volumetric Core Loss P_cv [mW/cm³]", "Core Loss Density [kW/m³] P_CV"]},
        "possible_units": ["mW/cm³", "kW/m³"],
        "std_unit": "mW/cm³",
        "scenarios": [
          {
            "condition": "At 100kHz, 100mT",
            "limits": {
              "Power_Ferrite": [100, 200, 500],
              "RF_Ceramic": [50, 100],
              "Common_Mode_Choke": [150, 300]
            }
          }
        ]
      },
      {
        "key": "curie_temperature",
        "symbol": "T<sub>C</sub>",
        "spec_type": "nominal",
        "column_model": "TYP_ONLY",
        "engineering_class": "NOMINAL_PARAMETER",
        "special_semantics": "NONE",
        "llm_context": {"formal_name": "Curie Temperature", "aliases": ["T_C [°C] Typ. – Curie Temperature (Core Material)", "Curie Point T_C [°C] (Core Material Property)", "Tc [°C] – Curie Temp. (Above = No Ferromagnetism)", "T_CURIE [°C] Typ. – Ferrite Curie Temperature", "Curie Temperature T_C [°C] (Typ., Core Material)", "T_C Typ. [°C] – Curie Point (Core Loses Magnetism)", "Curie Temp. T_c [°C] (Core, Above = Non-Magnetic)", "T_CURIE [°C] – Core Material Curie Point", "T_C [°C] Typ. (Above = µ_r Drops to 1)", "Curie Temp. Tc [°C] Typ. (Core Material Specific)"]},
        "possible_units": ["°C"],
        "std_unit": "°C",
        "scenarios": [
          {
            "condition": "Core material",
            "limits": {
              "Power_Ferrite": [130, 200, 240],
              "RF_Ceramic": [200, 300],
              "Common_Mode_Choke": [130, 200]
            }
          }
        ]
      }
    ],
    
    "MECHANICAL_CHAR": [
      {
        "key": "core_volume",
        "symbol": "V<sub>e</sub>",
        "spec_type": "nominal",
        "column_model": "TYP_ONLY",
        "engineering_class": "MECHANICAL",
        "special_semantics": "NONE",
        "llm_context": {"formal_name": "Effective Core Volume", "aliases": ["V_e [mm³/cm³] Typ. – Effective Core Volume", "Core Volume V_e [mm³] Typ. (Effective)", "Ve [mm³] – Effective Core Volume (Typ.)", "V_e [cm³] Typ. (Effective; V_e = A_e × l_e)", "Effective Volume [mm³] V_e (Core Material)", "Ve Typ. [mm³] – Core Effective Volume (A_e × l_e)", "V_e [mm³] (Effective Core Vol.; Used for P_cv Calc.)", "Core Effective Volume V_e [cm³] Typ.", "V(e) [mm³] Typ. – Magnetic Core Volume", "Effective Core Vol. V_e [mm³] (Core Geometry)"]},
        "possible_units": ["mm³", "cm³"],
        "std_unit": "mm³",
        "scenarios": [
          {
            "condition": "Typical",
            "limits": {
              "Power_Ferrite": [5, 10, 50, 100, 500, 1000],
              "RF_Ceramic": [0.5, 1, 5, 10],
              "Common_Mode_Choke": [50, 100, 500]
            }
          }
        ]
      },
      {
        "key": "magnetic_path_length",
        "symbol": "l<sub>e</sub>",
        "spec_type": "nominal",
        "column_model": "TYP_ONLY",
        "engineering_class": "MECHANICAL",
        "special_semantics": "NONE",
        "llm_context": {"formal_name": "Effective Magnetic Path Length", "aliases": ["l_e [mm/cm] Typ. – Effective Magnetic Path Length", "Path Length l_e [mm] Typ. (Effective Magnetic)", "le [mm] – Effective Path Length (Core Geometry)", "l_e [mm] Typ. (Effective; H = N·I / l_e)", "Effective Path Length [mm] l_e (Core Specific)", "le Typ. [mm] – Magnetic Path (l_e, Core Geometry)", "l_e [cm] Typ. (Effective Magnetic Path, Core)", "Magnetic Path l_e [mm] Typ. (Core Geometry)", "l(e) [mm] Typ. – Effective Core Path Length", "Effective Magnetic Path l_e [mm] (Core, Typ.)"]},
        "possible_units": ["mm", "cm"],
        "std_unit": "mm",
        "scenarios": [
          {
            "condition": "Typical",
            "limits": {
              "Power_Ferrite": [5, 10, 20, 30, 50],
              "RF_Ceramic": [1, 2, 5],
              "Common_Mode_Choke": [10, 20, 40]
            }
          }
        ]
      },
      {
        "key": "core_area",
        "symbol": "A<sub>e</sub>",
        "spec_type": "nominal",
        "column_model": "TYP_ONLY",
        "engineering_class": "MECHANICAL",
        "special_semantics": "NONE",
        "llm_context": {"formal_name": "Effective Core Area", "aliases": ["A_e [mm²/cm²] Typ. – Effective Core Area", "Core Area A_e [mm²] Typ. (Effective Cross-Section)", "Ae [mm²] – Effective Core Cross-Sectional Area", "Effective Cross-Section [mm²] A_e (Core)", "Ae Typ. [mm²] – Core Cross-Section (Magnetic)", "A_e [cm²] Typ. (Effective Core Area, Core Geometry)", "Core Cross-Sectional Area A_e [mm²] Typ.", "A(e) [mm²] Typ. – Effective Magnetic Core Area", "Effective Core Area A_e [mm²] (Core Geometry)"]},
        "possible_units": ["mm²", "cm²"],
        "std_unit": "mm²",
        "scenarios": [
          {
            "condition": "Typical",
            "limits": {
              "Power_Ferrite": [1, 2, 5, 10, 20, 50],
              "RF_Ceramic": [0.1, 0.5, 1],
              "Common_Mode_Choke": [5, 10, 20]
            }
          }
        ]
      },
      {
        "key": "wire_gauge",
        "symbol": "AWG",
        "spec_type": "nominal",
        "column_model": "TYP_ONLY",
        "engineering_class": "MECHANICAL",
        "special_semantics": "NONE",
        "llm_context": {"formal_name": "Wire Gauge", "aliases": ["AWG [–] Typ. – Wire Gauge (Winding Wire)", "Wire Size AWG [–] Typ. (Winding Conductor)", "AWG Typ. – American Wire Gauge (Winding)", "Wire Gauge AWG [–] (Winding, Typ.)", "Winding Wire AWG [–] Typ. (Conductor Size)", "AWG [–] Typ. (Wire Diameter: Winding Conductor)", "Wire AWG Typ. [–] – Winding Conductor Size", "AWG Wire Size [–] Typ. (Winding, See DCR Note)", "Conductor Gauge AWG [–] Typ. (Winding)", "Wire Gauge [AWG] Typ. – Coil Winding Wire Size"]},
        "possible_units": [""],
        "std_unit": "",
        "scenarios": [
          {
            "condition": "Typical",
            "limits": {
              "Power_Ferrite": [18, 20, 22, 24, 26, 28, 30],
              "RF_Ceramic": [26, 28, 30, 32, 34],
              "Common_Mode_Choke": [20, 22, 24, 26, 28]
            }
          }
        ]
      },
      {
        "key": "turns_count",
        "symbol": "N",
        "spec_type": "nominal",
        "column_model": "TYP_ONLY",
        "engineering_class": "MECHANICAL",
        "special_semantics": "NONE",
        "llm_context": {"formal_name": "Number of Turns", "aliases": ["N [turns] Typ. – Number of Winding Turns", "Turns N [–] Typ. (Winding, L = A_L × N²)", "Winding Turns N [–] Typ. (Primary / Secondary)", "N [–] Typ. – Turn Count (L = A_L · N²)", "Number of Turns N [–] (Winding, Typ.)", "N_turns [–] Typ. – Winding Turn Count", "Turns Count N Typ. [–] (Coil Turns, Design Value)", "N [–] Typ. (Turns; Affects L, DCR, I_sat)", "Winding Turns N [–] Typ. (Primary)", "N Typ. [–] – Number of Coil Turns (Winding)"]},
        "possible_units": [""],
        "std_unit": "",
        "scenarios": [
          {
            "condition": "Typical",
            "limits": {
              "Power_Ferrite": [5, 10, 15, 20, 30, 50],
              "RF_Ceramic": [2, 3, 5, 10],
              "Common_Mode_Choke": [10, 20, 50, 100]
            }
          }
        ]
      },
      {
        "key": "core_material",
        "symbol": "Material",
        "spec_type": "nominal",
        "column_model": "TYP_ONLY",
        "engineering_class": "MECHANICAL",
        "special_semantics": "NONE",
        "llm_context": {"formal_name": "Core Material Type", "aliases": ["Core Material – Type (e.g., NiZn, MnZn, Ferrite)", "Material Type (e.g., NiZn, MnZn, Iron Powder)", "Core Material (e.g., Sendust, Molypermalloy, NiZn)", "Magnetic Core Material (e.g., MnZn, Nanocrystalline)", "Core Type – Material (e.g., Air Core, Ferrite, NiZn)", "Core Composition (e.g., NiZn Ferrite, Iron Powder)", "Material Code – Core (e.g., NiZn, MnZn, Ceramic)", "Core Mat. Type (NiZn / MnZn / Sendust / Iron_Powder)", "Magnetic Material (e.g., Nanocrystalline, MnZn Ferrite)", "Core Material: NiZn / MnZn / Iron Powder / Sendust"]},
        "possible_units": [""],
        "std_unit": "",
        "scenarios": [
          {
            "condition": "N/A",
            "limits": {
              "Power_Ferrite": ["NiZn", "MnZn", "Iron_Powder", "Sendust", "Molypermalloy"],
              "RF_Ceramic": ["Ceramic", "Air_Core", "Ferrite"],
              "Common_Mode_Choke": ["NiZn", "MnZn", "Nanocrystalline"]
            }
          }
        ]
      },
      {
        "key": "shielding",
        "symbol": "Shielding",
        "spec_type": "nominal",
        "column_model": "TYP_ONLY",
        "engineering_class": "MECHANICAL",
        "special_semantics": "NONE",
        "llm_context": {"formal_name": "Magnetic Shielding", "aliases": ["Shielding – Type (Shielded / Semi-Shielded / Unshielded)", "Magnetic Shielding Type (Shielded or Unshielded)", "Shielding [Shielded / Unshielded] – EMI Containment", "Shielding Type – Shielded / Open / Semi-Shielded", "Magnetic Shield (Shielded = Low Stray Field)", "Shielding Classification (Shielded / Unshielded)", "EMI Shielding (Shielded: Low External H-Field)", "Magnetic Shielding Style: Shielded / Open Core", "Shield Type – Shielded / Unshielded (Inductor)", "Shielding: Shielded / Semi / Unshielded (See Note)"]},
        "possible_units": [""],
        "std_unit": "",
        "scenarios": [
          {
            "condition": "N/A",
            "limits": {
              "Power_Ferrite": ["Shielded", "Semi-Shielded", "Unshielded"],
              "RF_Ceramic": ["Unshielded"],
              "Common_Mode_Choke": ["Shielded", "Unshielded"]
            }
          }
        ]
      },
      {
        "key": "mounting_type",
        "symbol": "Mount",
        "spec_type": "mechanical",
        "column_model": "TYP_ONLY",
        "engineering_class": "MECHANICAL",
        "special_semantics": "NONE",
        "llm_context": {"formal_name": "Mounting Type", "aliases": ["Mount Type – SMD / Through-Hole / Chassis", "Mounting Style (SMD / THT / Chip / PCB)", "Mount [SMD / Through-Hole / Radial / Axial]", "Mounting Type – SMD, Through-Hole, Chassis", "PCB Mounting Style (SMD / THT / Chassis Mount)", "Mounting (SMD=Reflow; THT=Wave/Hand; Chassis=Screw)", "Mount Style – Chip / Radial / Axial / SMD", "Assembly Method – SMD or Through-Hole", "Mounting Category (SMD / THT / PCB Mounted)", "Mount [SMD / THT / Chassis] – PCB Assembly Type"]},
        "possible_units": [""],
        "std_unit": "",
        "scenarios": [
          {
            "condition": "N/A",
            "limits": {
              "Power_Ferrite": ["SMD", "Through-Hole", "Chassis"],
              "RF_Ceramic": ["SMD", "Chip"],
              "Common_Mode_Choke": ["SMD", "Through-Hole", "PCB"]
            }
          }
        ]
      },
      {
        "key": "footprint",
        "symbol": "Footprint",
        "spec_type": "mechanical",
        "column_model": "TYP_ONLY",
        "engineering_class": "MECHANICAL",
        "special_semantics": "NONE",
        "llm_context": {"formal_name": "PCB Footprint", "aliases": ["Footprint [mm²] Typ. – PCB Land Area", "PCB Footprint [mm²] Typ. (Component Land Area)", "Footprint Size [mm²] Typ. (PCB Occupied Area)", "PCB Area [mm²] Typ. – Component Footprint", "Land Area [mm²] Typ. (PCB, Component Body + Pads)", "Footprint [mm²] Typ. (L × W, PCB Occupied)", "PCB Footprint Area [mm²] (Typ., Body + Pads)", "Component Footprint [mm²] Typ. – PCB Area", "Land Pattern Area [mm²] Typ. (PCB Footprint)", "Footprint [mm²] (PCB Area, Typ., Body × Width)"]},
        "possible_units": ["mm²"],
        "std_unit": "mm²",
        "scenarios": [
          {
            "condition": "Typical",
            "limits": {
              "Power_Ferrite": [4, 9, 16, 36, 64, 100],
              "RF_Ceramic": [0.5, 1, 2, 4],
              "Common_Mode_Choke": [9, 16, 36]
            }
          }
        ]
      },
      {
        "key": "height",
        "symbol": "H",
        "spec_type": "mechanical",
        "column_model": "TYP_ONLY",
        "engineering_class": "MECHANICAL",
        "special_semantics": "NONE",
        "llm_context": {"formal_name": "Component Height", "aliases": ["H [mm] Max. – Component Height / Profile", "Height H [mm] Max. (Mounted Profile, Above PCB)", "Profile H [mm] Max. (Component, PCB Mounted)", "H [mm] Max. – Max. Mounted Height (PCB Surface)", "Component Height [mm] Max. (Above Board Surface)", "H Max. [mm] – Height (PCB-to-Top of Component)", "Height H [mm] (Max., Mounted, Body + Stand-off)", "Profile Height [mm] Max. (Above PCB, Mounted)", "H [mm] Max. – Component Standoff + Body Height", "Height [mm] Max. H (Component, PCB Assembly)"]},
        "possible_units": ["mm"],
        "std_unit": "mm",
        "scenarios": [
          {
            "condition": "",
            "limits": {
              "Power_Ferrite": [0.8, 1.0, 1.5, 2.0, 3.0, 4.0, 5.0, 10.0],
              "RF_Ceramic": [0.3, 0.5, 0.6, 0.8, 1.0],
              "Common_Mode_Choke": [1.5, 2.0, 3.0, 5.0, 10.0]
            }
          }
        ]
      },
      {
        "key": "weight",
        "symbol": "W",
        "spec_type": "mechanical",
        "column_model": "TYP_ONLY",
        "engineering_class": "MECHANICAL",
        "special_semantics": "NONE",
        "llm_context": {"formal_name": "Weight", "aliases": ["W [mg/g] Typ. – Component Weight / Mass", "Component Weight [mg] Typ. (Per Piece)", "Mass [g] Typ. – Component (Per Piece, Bare)", "Weight [mg] Typ. (Component, Excl. Packaging)", "W Typ. [mg] – Component Weight (±20% Approx.)", "Mass m [mg] Typ. (Per Component, No Reel)", "Component Mass [g] Typ. (Bare, Pick-and-Place)", "Net Weight [mg] Typ. (Component, Per Piece)", "W [mg] Typ. (Suitable for Pick-and-Place Calc.)", "Weight W [g] Typ. – Component Mass (Per Piece)"]},
        "possible_units": ["mg", "g"],
        "std_unit": "mg",
        "scenarios": [
          {
            "condition": "",
            "limits": {
              "Power_Ferrite": [10, 50, 100, 500, 1000, 5000],
              "RF_Ceramic": [1, 5, 10, 50],
              "Common_Mode_Choke": [100, 500, 1000]
            }
          }
        ]
      }
    ],
    
    "RELIABILITY": [
      {
        "key": "mtbf",
        "symbol": "MTBF",
        "spec_type": "min_limit",
        "column_model": "MIN_ONLY",
        "engineering_class": "NOMINAL_PARAMETER",
        "special_semantics": "NONE",
        "llm_context": {"formal_name": "Mean Time Between Failures", "aliases": ["MTBF [hours] Min. – Mean Time Between Failures", "Reliability MTBF [h] Min. (At Rated Conditions)", "MTBF [h] Min. – Component Reliability (Rated)", "Mean Time Between Failures [h] Min.", "MTBF Min. [hours] – Reliability (Standard Conditions)", "λ = 1/MTBF [FIT] – Failure Rate (MTBF Derived)", "MTBF [h] Min. (Per MIL-HDBK-217 or IEC 62380)", "MTBF [h] Min. (Ref. IEC 62380 / MIL-HDBK-217)", "Mean Time to Failure MTBF [h] Min."]},
        "possible_units": ["hours"],
        "std_unit": "hours",
        "scenarios": [
          {
            "condition": "At rated conditions",
            "limits": {
              "Power_Ferrite": [100000, 500000, 1000000],
              "RF_Ceramic": [1000000],
              "Common_Mode_Choke": [500000, 1000000]
            }
          }
        ]
      },
      {
        "key": "humidity_resistance",
        "symbol": "RH",
        "spec_type": "max_rating",
        "column_model": "MAX_ONLY",
        "engineering_class": "SAFETY_LIMIT",
        "special_semantics": "NONE",
        "llm_context": {"formal_name": "Humidity Resistance", "aliases": ["RH [%RH] Max. – Maximum Operating Humidity", "Max Humidity [%RH] (Operating, Non-Condensing)", "Humidity Resistance RH [%RH] Max. (Operating)", "Max. Relative Humidity [%RH] (Op., Non-Cond.)", "RH [%RH] Max. (Operating, Non-Condensing)", "Operating Humidity [%RH] Max. (Non-Condensing)", "Humidity RH [%RH] Max. – Non-Condensing", "Relative Humidity Max. [%RH] (Non-Condensing, Op.)", "RH Max. [%RH] – Operating Humidity (Non-Cond.)"]},
        "possible_units": ["%RH"],
        "std_unit": "%RH",
        "scenarios": [
          {
            "condition": "Operating",
            "limits": {
              "Power_Ferrite": [85, 95],
              "RF_Ceramic": [85, 95],
              "Common_Mode_Choke": [85, 95]
            }
          }
        ]
      },
      {
        "key": "vibration_resistance",
        "symbol": "Vib",
        "spec_type": "nominal",
        "column_model": "TYP_ONLY",
        "engineering_class": "NOMINAL_PARAMETER",
        "special_semantics": "NONE",
        "llm_context": {"formal_name": "Vibration Resistance", "aliases": ["Vib [G] Typ. – Vibration Resistance", "Vibration Spec [G] (Typ.)", "Vibration Rating [G] Typ. (Sinusoidal)", "Vib Resistance [G] Typ. (Sine Wave)", "Vibration Withstand [G] Typ.", "Mechanical Vibration [G] Typ.", "Vibration Spec [G] (IEC 60068-2-6)", "Vibration Resistance [G] Typ."]},
        "possible_units": ["G"],
        "std_unit": "G",
        "scenarios": [
          {
            "condition": "10-2000Hz",
            "limits": {
              "Power_Ferrite": [10, 20, 50],
              "RF_Ceramic": [20, 50],
              "Common_Mode_Choke": [10, 20]
            }
          }
        ]
      },
      {
        "key": "shock_resistance",
        "symbol": "Shock",
        "spec_type": "nominal",
        "column_model": "TYP_ONLY",
        "engineering_class": "NOMINAL_PARAMETER",
        "special_semantics": "NONE",
        "llm_context": {"formal_name": "Shock Resistance", "aliases": ["Shock [G] Typ. – Shock Resistance (Half-Sine)", "Shock Rating [G] (Half-Sine Pulse, Typ.)", "Mechanical Shock [G] Typ. (Half-Sine)", "Shock Resistance [G] (Half-Sine, Per IEC)", "Shock [G] Typ. (3 Axes)", "Impact Resistance [G] Typ. (Half-Sine)", "Mechanical Shock Rating [G] Typ.", "Shock [G] Typ. – Per IEC 60068-2-27", "Shock Withstand [G] Typ. (Half-Sine)", "Shock Resistance [G] Typ. (Half-Sine Pulse)"]},
        "possible_units": ["G"],
        "std_unit": "G",
        "scenarios": [
          {
            "condition": "Half-sine 11ms",
            "limits": {
              "Power_Ferrite": [50, 100, 500],
              "RF_Ceramic": [100, 500, 1000],
              "Common_Mode_Choke": [50, 100]
            }
          }
        ]
      },
      {
        "key": "solderability",
        "symbol": "Solder",
        "spec_type": "nominal",
        "column_model": "TYP_ONLY",
        "engineering_class": "NOMINAL_PARAMETER",
        "special_semantics": "NONE",
        "llm_context": {"formal_name": "Solderability", "aliases": ["Solder – Solderability (Lead-Free / SnPb / Both)", "Solder Compatibility (Lead-Free Reflow / Wave)", "Reflow Compatible (Lead-Free SAC305 / SnPb)", "Solderability – Reflow Profile (Lead-Free or SnPb)", "Solder Process (Lead-Free Reflow / Wave Solder)", "Soldering Compatibility (LF=Lead-Free, SnPb)", "Reflow Solder (Lead-Free SAC305 Compatible: Yes/No)", "Solder Type (Lead-Free / Leaded / Both Processes)", "Solderability – Per J-STD-002 (Lead-Free / SnPb)"]},
        "possible_units": [""],
        "std_unit": "",
        "scenarios": [
          {
            "condition": "Reflow profile",
            "limits": {
              "Power_Ferrite": ["Lead-Free", "SnPb", "Both"],
              "RF_Ceramic": ["Lead-Free", "SnPb", "Both"],
              "Common_Mode_Choke": ["Lead-Free", "SnPb", "Both"]
            }
          }
        ]
      },
      {
        "key": "msl_rating",
        "symbol": "MSL",
        "spec_type": "nominal",
        "column_model": "TYP_ONLY",
        "engineering_class": "NOMINAL_PARAMETER",
        "special_semantics": "NONE",
        "llm_context": {"formal_name": "Moisture Sensitivity Level", "aliases": ["MSL – Moisture Sensitivity Level (Per JEDEC)", "Moisture Rating MSL [1–6] (J-STD-020)", "MSL [1/2/3] – Per JEDEC J-STD-020", "Moisture Sensitivity MSL (JEDEC J-STD-020E)", "MSL Level – Floor Life (J-STD-020, SMD Only)", "MSL (1=Unlimited / 2=1yr / 3=168h Floor Life)", "Moisture Sensitivity Level – IPC/JEDEC J-STD-020", "MSL Rating Per J-STD-020 (SMD Packages)", "MSL [–] Per JEDEC (MSL1=Unlimited Floor Life)", "Moisture Sensitivity (MSL) J-STD-020 Rev. E"]},
        "possible_units": [""],
        "std_unit": "",
        "scenarios": [
          {
            "condition": "Per JEDEC",
            "limits": {
              "Power_Ferrite": ["MSL1", "MSL2", "MSL3"],
              "RF_Ceramic": ["MSL1"],
              "Common_Mode_Choke": ["MSL1", "MSL2"]
            }
          }
        ]
      }
    ],
    
    "PACKAGE": [
      {
        "key": "package_code",
        "symbol": "PKG",
        "spec_type": "mechanical",
        "column_model": "TYP_ONLY",
        "engineering_class": "MECHANICAL",
        "special_semantics": "NONE",
        "llm_context": {"formal_name": "Size Code", "aliases": ["PKG – Size / Case Code (e.g., 0402, 0805, 1210)", "Package Size (e.g., 0603, 1206, 2520, Radial)", "Case Code (EIA, e.g., 0402, 1008, 3225)", "PKG Code – Chip Size (e.g., 0201, 0805, 5050)", "Size Code [EIA] (e.g., 0402=1.0×0.5mm, 1210=etc.)", "Package / Case (e.g., Radial, Toroid, 0603, 4040)", "Component Size Code (EIA/IEC, e.g., 01005–6060)", "Case Size EIA (e.g., 0805, 1206, Axial, Radial)", "Footprint Code (e.g., 0402, 1210, 2520, Toroid)", "Size Code PKG (e.g., 0603, 1812, Radial, Axial)"]},
        "possible_units": [""],
        "std_unit": "",
        "scenarios": [
          {
            "condition": "N/A",
            "limits": {
              "Power_Ferrite": ["0201", "0402", "0603", "0805", "1008", "1206", "1210", "1812", "2520", "3225", "4040", "5050", "6060", "Radial", "Axial"],
              "RF_Ceramic": ["01005", "0201", "0402", "0603", "0805"],
              "Common_Mode_Choke": ["0805", "1206", "1210", "Radial", "Toroid"]
            }
          }
        ]
      },
      {
        "key": "termination",
        "symbol": "Term",
        "spec_type": "mechanical",
        "column_model": "TYP_ONLY",
        "engineering_class": "MECHANICAL",
        "special_semantics": "NONE",
        "llm_context": {"formal_name": "Termination Type", "aliases": ["Term – Termination / Terminal Finish (e.g., Sn, Ag)", "Terminal Finish (e.g., Sn, Ni/Au, Ag, Bare Cu)", "Termination Material (e.g., Sn, Ag, Ni/Au)", "Lead / Terminal Finish (e.g., Matte Sn, Ag, NiAu)", "Electrode Plating (e.g., Sn, Ag, Ni/Au, Bare Cu)", "Termination Type – Sn / Ag / Ni/Au / Bare Cu", "End Cap / Terminal Material (RoHS: Sn or Ni/Au)", "Terminal Plating (e.g., 100% Sn, Ag, Ni/Au)", "Termination [Sn / Ag / NiAu / BearCu]", "Contact Finish – Terminal (e.g., Sn, Ag, Ni/Au)"]},
        "possible_units": [""],
        "std_unit": "",
        "scenarios": [
          {
            "condition": "N/A",
            "limits": {
              "Power_Ferrite": ["Sn", "Ag", "Ni/Au", "Bare_Cu"],
              "RF_Ceramic": ["Sn", "Ag", "Ni/Au"],
              "Common_Mode_Choke": ["Sn", "Ni/Au"]
            }
          }
        ]
      },
      {
        "key": "pin_count",
        "symbol": "Pins",
        "spec_type": "mechanical",
        "column_model": "TYP_ONLY",
        "engineering_class": "MECHANICAL",
        "special_semantics": "NONE",
        "llm_context": {"formal_name": "Number of Pins/Terminals", "aliases": ["Pins [–] Typ. – Number of Terminals / Pins", "Pin Count [–] (e.g., 2, 4, 6, 8 Terminals)", "Terminals [–] Typ. – Number of Leads/Pads", "Pin / Terminal Count [–] (2=Single; 4+=Multi-Wind.)", "Pins [–] – Terminal Count (2 for Single, 4 for CMC)", "Number of Leads [–] Typ. (2-Pin / 4-Pin / 6-Pin)", "Terminal Count [–] (2-Lead Inductor / 4-Lead CMC)", "Pins/Pads Count [–] (2 = Standard; 4/6/8 = CMC)", "No. of Terminals [–] Typ. – Pin Configuration", "Pin Count [–] (2=2-Terminal; 4/6/8=Multi-Winding)"]},
        "possible_units": [""],
        "std_unit": "",
        "scenarios": [
          {
            "condition": "N/A",
            "limits": {
              "Power_Ferrite": [2],
              "RF_Ceramic": [2],
              "Common_Mode_Choke": [4, 6, 8]
            }
          }
        ]
      }
    ],
    
    "OPERATING_CONDITIONS": [
      {
        "key": "operating_temp_range",
        "symbol": "T<sub>A</sub>",
        "spec_type": "nominal",
        "column_model": "MIN_MAX",
        "engineering_class": "NOMINAL_PARAMETER",
        "special_semantics": "NONE",
        "llm_context": {"formal_name": "Operating Temperature Range", "aliases": ["T_A [°C] Operating Range (Min. to Max.)", "Ambient Temperature Range T_A [°C] (Min/Max)", "T_AMB [°C] Operating (Lower to Upper Limit)", "T_A [°C] Range (Operating, Continuous, Still Air)", "Operating Temperature [°C] T_A (Min./Max.)", "T_A(op) [°C] – Min. to Max. Operating Range", "Ambient Temp. Range T_A [°C] (Continuous, Op.)", "T_OP [°C] Min. Max. – Operating Ambient Range", "Operating Temp. Range [°C] T_A (All Conditions)"]},
        "possible_units": ["°C"],
        "std_unit": "°C",
        "scenarios": [
          {
            "condition": "Standard",
            "limits": {
              "Power_Ferrite": ["-40 to 85", "-40 to 105", "-40 to 125", "-55 to 155"],
              "RF_Ceramic": ["-55 to 125", "-55 to 150"],
              "Common_Mode_Choke": ["-40 to 85", "-40 to 125"]
            }
          }
        ]
      },
      {
        "key": "ambient_pressure",
        "symbol": "P<sub>AMB</sub>",
        "spec_type": "nominal",
        "column_model": "MIN_MAX",
        "engineering_class": "NOMINAL_PARAMETER",
        "special_semantics": "NONE",
        "llm_context": {"formal_name": "Ambient Pressure Range", "aliases": ["P_AMB [kPa] Operating Range (Min. to Max.)", "Operating Pressure P_AMB [kPa] (Min/Max Range)", "Ambient Pressure [kPa] Range", "P_AMB [mmHg] Operating (Min. to Max.)", "Pressure Range [kPa] P_AMB (Operating, Typical)", "Atmospheric Pressure [kPa] Range (Operating)", "P_AMB [kPa] – Operating Pressure Range", "Operating Atmospheric Pressure [kPa] Min./Max."]},
        "possible_units": ["kPa", "mmHg"],
        "std_unit": "kPa",
        "scenarios": [
          {
            "condition": "Operating",
            "limits": {
              "Power_Ferrite": ["70 to 106"],
              "RF_Ceramic": ["70 to 106"],
              "Common_Mode_Choke": ["70 to 106"]
            }
          }
        ]
      }
    ],
    
    "AC_CHARACTERISTICS": [
      {
        "key": "frequency_range",
        "symbol": "f<sub>RANGE</sub>",
        "spec_type": "nominal",
        "column_model": "MIN_MAX",
        "engineering_class": "NOMINAL_PARAMETER",
        "special_semantics": "NONE",
        "llm_context": {"formal_name": "Operating Frequency Range", "aliases": ["f_RANGE [kHz/MHz/GHz] – Operating Frequency Range", "Frequency Range f [kHz] Min. to Max. (Operating)", "Working Frequency [kHz–MHz] Range (Typ.)", "f_RANGE [MHz] (Min/Max, Operating, Typ.)", "Operating Freq. Range [kHz–MHz] f_RANGE", "f [kHz] to f [MHz] – Usable Frequency Range", "Frequency Range [MHz] (Operating, Below SRF)", "f_RANGE [kHz to MHz] – Working Frequency Band", "Useful Frequency Range [kHz–GHz] f_RANGE (Typ.)", "Freq. Range [kHz–MHz] (Operating, Below SRF)"]},
        "possible_units": ["kHz", "MHz", "GHz"],
        "std_unit": "kHz",
        "scenarios": [
          {
            "condition": "Typical",
            "limits": {
              "Power_Ferrite": ["1 to 1000", "10 to 2000"],
              "RF_Ceramic": ["100 to 10000", "1000 to 100000"],
              "Common_Mode_Choke": ["0.1 to 100", "1 to 1000"]
            }
          }
        ]
      },
      {
        "key": "ripple_current",
        "symbol": "ΔI<sub>L</sub>",
        "spec_type": "max_limit",
        "column_model": "MAX_ONLY",
        "engineering_class": "PERFORMANCE_LIMIT",
        "special_semantics": "NONE",
        "llm_context": {"formal_name": "Rated Ripple Current", "aliases": ["ΔI_L [mA/A] Max. – Rated AC Ripple Current", "AC Ripple Current ΔI_L [mA] Max.", "Delta I [A] Max. – Ripple Current Rating", "Ripple Current Rating ΔI [mA] Max.", "I_ripple [A] Max. – AC Superimposed Current", "ΔI_L [mA] Max. (Superimposed AC)", "AC Current ΔI_L [A] Max. (Ripple)", "Rated Ripple I [mA] Max.", "ΔI_L [A] Max. (Peak-to-Peak Ripple)"]},
        "possible_units": ["mA", "A"],
        "std_unit": "mA",
        "scenarios": [
          {
            "condition": "At switching frequency",
            "limits": {
              "Power_Ferrite": [500, 1000, 2000, 5000],
              "RF_Ceramic": [50, 100, 200],
              "Common_Mode_Choke": [200, 500, 1000]
            }
          }
        ]
      },
      {
         "key": "coupling_coefficient",
         "symbol": "k",
         "spec_type": "min_limit",
         "column_model": "MIN_TYP",
         "engineering_class": "PERFORMANCE_LIMIT",
         "special_semantics": "NONE",
         "llm_context": {"formal_name": "Coupling Coefficient", "aliases": ["k [–] Min./Typ. – Coupling Coefficient (Between Windings)", "Magnetic Coupling k [–] Typ. (Winding-to-Winding)", "k Factor [–] Min. Typ. (Coupling, 0 to 1)", "k [–] – Mutual Inductance Coupling (k = M/√(L1·L2))", "Coupling Coefficient k [–] (Min./Typ., Windings)", "k Typ. [–] – Inductive Coupling (0=None, 1=Perfect)", "k [–] Min. (Between Winding 1 & 2; k=M/√L1L2)", "Magnetic Coupling Factor k [–] (Min./Typ.)", "k Factor [–] – Flux Coupling Between Coils (Typ.)", "Coupling Coeff. k Typ. Min. [–] (Winding Mutual)"]},
         "possible_units": [""],
         "std_unit": "",
         "scenarios": [
           {
             "condition": "Between windings",
             "limits": {
               "Power_Ferrite": [0.95, 0.98],
               "RF_Ceramic": [0.90, 0.95],
               "Common_Mode_Choke": [0.90, 0.95, 0.98, 0.99]
             }
           }
         ]
       }
    ],

    "THERMAL_CHAR": [
      {
        "key": "thermal_resistance",
        "symbol": "θ<sub>JA</sub>",
        "spec_type": "nominal",
        "column_model": "TYP_MAX",
        "engineering_class": "NOMINAL_PARAMETER",
        "special_semantics": "NONE",
        "llm_context": {"formal_name": "Thermal Resistance", "aliases": ["θ_JA [°C/W] Typ./Max. – Thermal Resistance to Ambient", "Rth [°C/W] Typ. Max. (Component to Ambient, PCB)", "Thermal Resistance θ_JA [°C/W] (Standard PCB, Still Air)", "R_th [°C/W] Typ./Max. – Inductor Thermal Resistance", "Rth(component-ambient) [°C/W] Typ. Max. (PCB Mount)", "θ_JA [K/W] Typ. Max. – Thermal Res. to Ambient", "Thermal Resistance to Ambient [°C/W] Rth (PCB)", "Rth [°C/W] Typ./Max. (Standard FR4 PCB, Still Air)", "θ(JA) [°C/W] Typ. Max. – Component-to-Ambient", "R_th [°C/W] Max. (PCB Mount, Still Air, Standard)"]},
        "possible_units": ["°C/W"],
        "std_unit": "°C/W",
        "scenarios": [
          {
            "condition": "Standard PCB",
            "limits": {
              "Power_Ferrite": [20, 30, 50, 80],
              "RF_Ceramic": [100, 150, 200],
              "Common_Mode_Choke": [40, 60, 100]
            }
          }
        ]
      },
      {
        "key": "power_dissipation",
        "symbol": "P<sub>D</sub>",
        "spec_type": "max_limit",
        "column_model": "TYP_MAX",
        "engineering_class": "PERFORMANCE_LIMIT",
        "special_semantics": "NONE",
        "llm_context": {"formal_name": "Power Dissipation", "aliases": ["P_D [mW/W] Typ./Max. – Power Dissipation (At I_rated)", "Max Power Loss P_D [mW] Max. (At Rated Current)", "Power Dissipation P_D [W] Typ./Max.", "P_D [mW] Max. (DC Loss + Core Loss)", "Total Loss [mW] Typ./Max. (P_D = I²×DCR + P_core)", "Power Loss P_D [W] Max. (All Sources)", "P_D [mW] Max. – Total Inductor Loss", "Total Power Dissipation [mW] P_D"]},
        "possible_units": ["mW", "W"],
        "std_unit": "mW",
        "scenarios": [
          {
            "condition": "At rated current",
            "limits": {
              "Power_Ferrite": [100, 250, 500, 1000, 2000],
              "RF_Ceramic": [50, 100, 200],
              "Common_Mode_Choke": [100, 300, 500]
            }
          }
        ]
      }
    ],

    "COMPLIANCE": [
      {
        "key": "rohs_status",
        "symbol": "RoHS",
        "spec_type": "nominal",
        "column_model": "TYP_ONLY",
        "engineering_class": "REGULATORY",
        "special_semantics": "BOOLEAN_OR_ENUM",
        "llm_context": {"formal_name": "RoHS Compliance", "aliases": ["RoHS – Compliance Status (Compliant / Non-Compliant)", "Lead Free Status – RoHS (Compliant: Yes/No)", "RoHS Compliance (Compliant / With Exemption)", "RoHS [Compliant / Non-Compliant] – EU Dir. 2011/65", "Lead-Free Status RoHS (Yes=Compliant, Per EU Direc.)", "RoHS Compliant (Yes / With Exemption / No)", "RoHS Status – EU RoHS Directive Compliance", "Lead Free / RoHS Compliant (Compliant: Y/N)", "RoHS (Restriction of Hazardous Substances) Status", "RoHS Compliance Status (EU 2011/65/EU Directive)"]},
        "possible_units": [""],
        "std_unit": "",
        "scenarios": [
          {
            "condition": "N/A",
            "limits": {
              "Power_Ferrite": ["Compliant", "Compliant with Exemption", "Non-Compliant"],
              "RF_Ceramic": ["Compliant"],
              "Common_Mode_Choke": ["Compliant"]
            }
          }
        ]
      },
      {
        "key": "automotive_grade",
        "symbol": "AEC-Q200",
        "spec_type": "nominal",
        "column_model": "TYP_ONLY",
        "engineering_class": "REGULATORY",
        "special_semantics": "BOOLEAN",
        "llm_context": {"formal_name": "AEC-Q200 Qualified", "aliases": ["AEC-Q200 – Automotive Grade Qualification (Yes/No)", "Automotive Grade AEC-Q200 (Qualified: Yes / No)", "AEC-Q200 Qualified (Yes = Automotive Rated)", "AEC-Q200 [Yes / No] – Automotive Passive Qual.", "Automotive Qualified (AEC-Q200: Yes/No)", "AEC-Q200 Qualification Status (Yes / No)", "AEC-Q200 – Passive Component Automotive Std.", "Qualified to AEC-Q200 (Yes = Automotive Grade)", "AEC-Q200 Compliance (Automotive Qualification)", "AEC-Q200 [Y/N] – Automotive Component Qual."]},
        "possible_units": [""],
        "std_unit": "",
        "scenarios": [
          {
            "condition": "N/A",
            "limits": {
              "Power_Ferrite": ["Yes", "No"],
              "RF_Ceramic": ["Yes", "No"],
              "Common_Mode_Choke": ["Yes", "No"]
            }
          }
        ]
      },
      {
        "key": "reach_status",
        "symbol": "REACH",
        "spec_type": "nominal",
        "column_model": "TYP_ONLY",
        "engineering_class": "REGULATORY",
        "special_semantics": "NONE",
        "llm_context": {"formal_name": "REACH Compliance", "aliases": ["REACH – Compliance Status (Compliant / Affected)", "SVHC Free – REACH Status (Compliant: Yes/No)", "REACH Compliance (Compliant / Contains SVHC)", "REACH [Compliant / Affected] – EU SVHC Status", "SVHC Status REACH (Compliant = No SVHC Above 0.1%)", "REACH Status (EU Reg. 1907/2006, SVHC: Yes/No)", "REACH Compliant – SVHC Free (Per Candidate List)", "REACH [Compliant / Affected] (SVHC Declaration)", "REACH Compliance (Restricted Substances: EU)", "SVHC / REACH Compliance [Compliant / Affected]"]},
        "possible_units": [""],
        "std_unit": "",
        "scenarios": [
          {
            "condition": "N/A",
            "limits": {
              "Power_Ferrite": ["Compliant", "Affected"],
              "RF_Ceramic": ["Compliant"],
              "Common_Mode_Choke": ["Compliant"]
            }
          }
        ]
      },
      {
        "key": "halogen_free",
        "symbol": "HF",
        "spec_type": "nominal",
        "column_model": "TYP_ONLY",
        "engineering_class": "REGULATORY",
        "special_semantics": "BOOLEAN",
        "llm_context": {"formal_name": "Halogen Free", "aliases": ["HF – Halogen Free (Yes / No)", "Halogen Free [Yes / No] – Per IEC 61249-2-21", "HF Status (Halogen Free: Yes = No Cl/Br Above 900ppm)", "Halogen Free [Y/N] (IEC 61249-2-21 Compliant)", "Halogen Content – Halogen Free: Yes / No", "HF [Yes / No] – Cl+Br < 900ppm (IEC 61249-2-21)", "Halogen Free (HF: Yes; Per IEC 61249-2-21)", "HF Compliance – Halogen Free (Cl, Br < 900ppm)", "Halogen-Free Status (Yes = No Halogens Above Limit)", "Halogen Free HF [Y/N] – IEC 61249-2-21 Compliant"]},
        "possible_units": [""],
        "std_unit": "",
        "scenarios": [
          {
            "condition": "N/A",
            "limits": {
              "Power_Ferrite": ["Yes", "No"],
              "RF_Ceramic": ["Yes"],
              "Common_Mode_Choke": ["Yes", "No"]
            }
          }
        ]
      }
    ],

    "LOGISTICS": [
      {
        "key": "packaging_type",
        "symbol": "Pkg",
        "spec_type": "mechanical",
        "column_model": "TYP_ONLY",
        "engineering_class": "LOGISTICS",
        "special_semantics": "NONE",
        "llm_context": {"formal_name": "Packaging Type", "aliases": ["Pkg – Packaging Type (Tape & Reel / Tray / Bulk)", "Packing Type (T&R = Tape & Reel; Bulk; Tray)", "Delivery Form – Tape & Reel / Tray / Bulk", "Packaging [Tape & Reel / Paper Tape / Tray / Bulk]", "Pack Type – T&R / Bulk / Tray (Delivery Form)", "Packaging Code (TR=Tape & Reel, T=Tray, B=Bulk)", "Delivery Packaging (Tape & Reel / Tray / Bulk)", "Packing Style – Tape & Reel / Tray / Bulk", "Pkg. Type (e.g., T&R 8mm, Tray, Bulk, Paper Tape)", "Packaging Form (Tape & Reel / Paper Tape / Bulk)"]},
        "possible_units": [""],
        "std_unit": "",
        "scenarios": [
          {
            "condition": "N/A",
            "limits": {
              "Power_Ferrite": ["Tape & Reel", "Tray", "Bulk"],
              "RF_Ceramic": ["Tape & Reel", "Paper Tape"],
              "Common_Mode_Choke": ["Tape & Reel", "Tray"]
            }
          }
        ]
      },
      {
        "key": "reel_quantity",
        "symbol": "Qty",
        "spec_type": "nominal",
        "column_model": "TYP_ONLY",
        "engineering_class": "LOGISTICS",
        "special_semantics": "INTEGER",
        "llm_context": {"formal_name": "Reel Quantity", "aliases": ["Qty [pcs] Typ. – Units per Reel / Pack Quantity", "Pack Qty [pcs] – Units per Reel (Standard)", "Reel Quantity [pcs] Typ. (Units per Standard Reel)", "Qty/Reel [pcs] (Standard Reel, Tape & Reel Pack)", "Units per Reel [pcs] Typ. (T&R, Standard)", "Pack Quantity [pcs] – Per Reel or Tray", "Qty [pcs] – Units per Packaging Unit (Reel/Tray)", "Reel Qty [pcs] (Standard Reel, e.g., 1000 / 3000)", "Packing Qty [pcs] Typ. (Per Standard Reel)", "Units/Reel [pcs] Typ. – Standard Packaging Count"]},
        "possible_units": ["pcs"],
        "std_unit": "pcs",
        "scenarios": [
          {
            "condition": "Standard Reel",
            "limits": {
              "Power_Ferrite": [500, 1000, 2000, 3000],
              "RF_Ceramic": [10000, 15000],
              "Common_Mode_Choke": [500, 1000]
            }
          }
        ]
      },
      {
        "key": "tape_width",
        "symbol": "W<sub>tape</sub>",
        "spec_type": "mechanical",
        "column_model": "TYP_ONLY",
        "engineering_class": "LOGISTICS",
        "special_semantics": "NONE",
        "llm_context": {"formal_name": "Carrier Tape Width", "aliases": ["W_tape [mm] Typ. – Carrier Tape Width", "Tape Width W_tape [mm] (EIA-481, Standard)", "Carrier Tape Width [mm] W_tape (8/12/16/24mm)", "W_tape [mm] Typ. – T&R Carrier Tape Width", "Tape Width [mm] (8mm / 12mm / 16mm / 24mm)", "T&R Tape Width W_tape [mm] (Per EIA-481)", "Carrier Tape W [mm] Typ. (8 / 12 / 16 / 24mm)", "Tape Width W_tape [mm] (Reel Carrier, EIA-481)", "W_tape [mm] – Carrier Tape Width (T&R Packaging)", "Reel Carrier Tape Width [mm] W_tape (Typ.)"]},
        "possible_units": ["mm"],
        "std_unit": "mm",
        "scenarios": [
          {
            "condition": "N/A",
            "limits": {
              "Power_Ferrite": [8, 12, 16, 24],
              "RF_Ceramic": [8],
              "Common_Mode_Choke": [12, 16, 24]
            }
          }
        ]
      }
    ]
  },
    # ==============================================================================
    # 7. BJT - CORRECTED WITH METADATA FIELDS חלק7
    # ==============================================================================
  "BJT": {
    "archetypes": ["Small_Signal", "Power_BJT"],
    
    "ABS_MAX": [
      {
        "key": "vceo",
        "symbol": "V<sub>CEO</sub>",
        "spec_type": "max_rating",
        "column_model": "MAX_ONLY",
        "engineering_class": "SAFETY_LIMIT",
        "special_semantics": "NONE",
        "llm_context": {"formal_name": "Collector-Emitter Voltage", "aliases": ["V_CEO [V] Max. – Collector-Emitter Voltage (Open Base)", "V_CEO [V] Abs. Max. (Base Open, Continuous)", "VCEO [V] Max. – Collector-to-Emitter (Base Open)", "V(CEO) [V] Max. (Open Base, Abs. Max.)", "V_CE(sus) [V] Max. – Sustained (Open Base)", "V_CEO Abs. Max. [V] (C-E, Base = Open Circuit)", "Max. V_CEO [V] (Do Not Exceed, Open Base)", "V(CE) Max. [V] – C-E Voltage, Base Floating"]},
        "possible_units": ["V"],
        "std_unit": "V",
        "scenarios": [
          {
            "condition": "Open Base",
            "limits": {
              "Small_Signal": [15, 20, 30, 40, 45, 60, 80, 100],
              "Power_BJT": [40, 60, 80, 100, 120, 140, 200, 250, 400, 600, 1000, 1500]
            }
          }
        ]
      },
      {
        "key": "vcbo",
        "symbol": "V<sub>CBO</sub>",
        "spec_type": "max_rating",
        "column_model": "MAX_ONLY",
        "engineering_class": "SAFETY_LIMIT",
        "special_semantics": "NONE",
        "llm_context": {"formal_name": "Collector-Base Voltage", "aliases": ["V_CBO [V] Max. – Collector-Base Voltage (Open Emitter)", "V_CBO [V] Abs. Max. (Emitter Open, Continuous)", "VCBO [V] Max. – Collector-to-Base (Emitter Open)", "V(CBO) [V] Max. (Open Emitter, Abs. Max.)", "V_CB Max. [V] – C-B Junction (Emitter Floating)", "V_CBO Abs. Max. [V] (Emitter = Open Circuit)", "Max. V_CBO [V] (Do Not Exceed, Open Emitter)", "V(CB) Max. [V] – Collector-Base, Emitter Open"]},
        "possible_units": ["V"],
        "std_unit": "V",
        "scenarios": [
          {
            "condition": "Open Emitter",
            "limits": {
              "Small_Signal": [20, 30, 40, 60, 80, 100, 120],
              "Power_BJT": [60, 80, 100, 120, 160, 200, 300, 450, 700, 1000, 1700]
            }
          }
        ]
      },
      {
        "key": "vebo",
        "symbol": "V<sub>EBO</sub>",
        "spec_type": "max_rating",
        "column_model": "MAX_ONLY",
        "engineering_class": "SAFETY_LIMIT",
        "special_semantics": "NONE",
        "llm_context": {"formal_name": "Emitter-Base Voltage", "aliases": ["V_EBO [V] Max. – Emitter-Base Voltage (Open Collector)", "V_EBO [V] Abs. Max. (Collector Open, Continuous)", "VEBO [V] Max. – Emitter-to-Base (Collector Open)", "V(EBO) [V] Max. (Open Collector, Abs. Max.)", "V_EB Max. [V] – E-B Junction (Collector Floating)", "V_EBO Abs. Max. [V] (Collector = Open Circuit)", "Max. V_EBO [V] (Do Not Exceed, Open Collector)", "V(EB) Max. [V] – Emitter-Base, Collector Open"]},
        "possible_units": ["V"],
        "std_unit": "V",
        "scenarios": [
          {
            "condition": "Open Collector",
            "limits": {
              "Small_Signal": [5, 6, 7, 8],
              "Power_BJT": [5, 6, 7, 8, 10]
            }
          }
        ]
      },
      {
        "key": "ic_max",
        "symbol": "I<sub>C</sub>",
        "spec_type": "max_rating",
        "column_model": "MAX_ONLY",
        "engineering_class": "SAFETY_LIMIT",
        "special_semantics": "NONE",
        "llm_context": {"formal_name": "Collector Current", "aliases": ["I_C [mA/A] Max. – Continuous Collector Current", "Collector Current I_C [A] Max. (Continuous DC)", "Max Collector Current I_C [mA] (Continuous)", "I_C(max) [A] – Maximum Continuous DC I_C", "Max. I_C [A] – DC Collector Current (Continuous)", "I(C) [mA] Max. – Cont. Collector Current (DC)", "Collector DC Current I_C [A] Max. (Abs.)", "I_C Abs. Max. [mA] (Continuous, No Pulsed Ext.)", "Max. Continuous I_C [A] (Abs. Max., DC)"]},
        "possible_units": ["mA", "A"],
        "std_unit": "mA",
        "scenarios": [
          {
            "condition": "Continuous",
            "limits": {
              "Small_Signal": [50, 100, 200, 500, 800, 1000],
              "Power_BJT": [1000, 2000, 3000, 5000, 8000, 10000, 15000, 20000, 30000, 50000]
            }
          }
        ]
      },
      {
        "key": "ic_peak",
        "symbol": "I<sub>C(peak)</sub>",
        "spec_type": "max_rating",
        "column_model": "MAX_ONLY",
        "engineering_class": "SAFETY_LIMIT",
        "special_semantics": "NONE",
        "llm_context": {"formal_name": "Peak Collector Current", "aliases": ["I_C(peak) [mA/A] Max. – Pulsed Collector Current", "Pulsed Collector Current I_C(pulse) [A] Max.", "IC Peak [A] – Peak / Pulsed I_C (Non-Continuous)", "I_C(pulse) [mA] Max. (Pulsed, Duty Cycle Limited)", "I_C(peak) [A] Abs. Max. – Peak (Pulsed Condition)", "Max. Pulsed I_C [A] (Peak, Short Duration)", "I_C(pulsed) [A] Max. – Peak Collector (Pulse)", "I_C Peak [mA] Max. (Non-Repetitive Pulse)", "Pulsed I_C [A] Max. – Peak Current (Duty Cycle Dep.)"]},
        "possible_units": ["mA", "A"],
        "std_unit": "mA",
        "scenarios": [
          {
            "condition": "Pulsed",
            "limits": {
              "Small_Signal": [200, 500, 1000],
              "Power_BJT": [3000, 6000, 10000, 20000, 40000, 80000]
            }
          }
        ]
      },
      {
        "key": "ib_max",
        "symbol": "I<sub>B</sub>",
        "spec_type": "max_rating",
        "column_model": "MAX_ONLY",
        "engineering_class": "SAFETY_LIMIT",
        "special_semantics": "NONE",
        "llm_context": {"formal_name": "Base Current", "aliases": ["I_B [mA/A] Max. – Continuous Base Current", "Max Base Current I_B [mA] (Continuous)", "IB Max [mA] – Maximum DC Base Current", "I_B(max) [A] – Abs. Max. Continuous I_B", "I_B [mA] Max. (Continuous DC, Abs. Max.)", "Max. I_B [mA] – DC Base Drive Current (Continuous)", "I(B) [mA] Max. – Cont. Base Current", "Base Current I_B [A] Max. (DC, Continuous)", "I_B Abs. Max. [mA] (Continuous Base Drive)", "Max. Continuous I_B [mA] (Abs. Max., DC)"]},
        "possible_units": ["mA", "A"],
        "std_unit": "mA",
        "scenarios": [
          {
            "condition": "Continuous",
            "limits": {
              "Small_Signal": [10, 20, 50, 100],
              "Power_BJT": [100, 200, 500, 1000, 2000, 5000]
            }
          }
        ]
      },
      {
        "key": "power_dissipation",
        "symbol": "P<sub>D</sub>",
        "spec_type": "max_rating",
        "column_model": "MAX_ONLY",
        "engineering_class": "SAFETY_LIMIT",
        "special_semantics": "NONE",
        "llm_context": {"formal_name": "Maximum Power Dissipation", "aliases": ["P_D [W/mW] Max. – Total Power Dissipation", "Total Dissipation P_D [W] Max.", "P_D Abs. Max. [W]", "Max. Power P_D [mW]", "Maximum Allowable P_D [W]"]},
        "possible_units": ["W", "mW"],
        "std_unit": "W",
        "scenarios": [
          {
            "condition": "Tc=25°C",
            "limits": {
              "Small_Signal": [0.15, 0.2, 0.3, 0.35, 0.5, 0.625, 1, 1.5],
              "Power_BJT": [1, 2, 5, 10, 20, 25, 40, 50, 75, 100, 150, 200, 300]
            }
          },
          {
            "condition": "Ta=25°C",
            "limits": {
              "Small_Signal": [0.1, 0.15, 0.2, 0.3, 0.4],
              "Power_BJT": [0.5, 1, 2, 5]
            }
          }
        ]
      },
      {
        "key": "tj_max",
        "symbol": "T<sub>j(max)</sub>",
        "spec_type": "max_rating",
        "column_model": "MAX_ONLY",
        "engineering_class": "SAFETY_LIMIT",
        "special_semantics": "NONE",
        "llm_context": {"formal_name": "Maximum Junction Temperature", "aliases": ["T_j(max) [°C] – Maximum Junction Temperature", "Max Junction Temp. T_J [°C] (Abs. Max.)", "Tj(max) [°C] – Internal Die Temp. Limit", "T_J Max. [°C] (Do Not Exceed, All Conditions)", "Maximum Operating Junction Temp. T_J [°C]", "T_J(max) [°C] – Die Temperature Absolute Limit", "Max. T_J [°C] (Abs. Max., Continuous)", "Junction Temp. Limit T_j [°C] Abs. Max.", "T_JMAX [°C] – Thermal Shutdown Precedes This", "Tj [°C] Max. (Absolute Maximum, Per Thermal Model)"]},
        "possible_units": ["°C"],
        "std_unit": "°C",
        "scenarios": [
          {
            "condition": "",
            "limits": {
              "Small_Signal": [125, 150, 175],
              "Power_BJT": [150, 175, 200]
            }
          }
        ]
      },
      {
        "key": "storage_temp",
        "symbol": "T<sub>STG</sub>",
        "spec_type": "max_rating",
        "column_model": "MIN_MAX",
        "engineering_class": "SAFETY_LIMIT",
        "special_semantics": "NONE",
        "llm_context": {"formal_name": "Storage Temperature Range", "aliases": ["T_STG [°C] Storage Range (Min. to Max.)", "Storage Temp Range T_STG [°C] (Min./Max.)", "T_stg [°C] – Non-Operating Storage Range", "Storage Temp. T_STG [°C] Min. Max. (Non-Op.)", "T_STORAGE [°C] Range (Non-Operating, Device Off)", "Non-Operating Storage Temp. T_STG [°C] Min–Max", "T_STG [°C] – Component Storage (Unpowered)", "Storage Temperature [°C] Min. Max. T_STG"]},
        "possible_units": ["°C"],
        "std_unit": "°C",
        "scenarios": [
          {
            "condition": "Min to Max",
            "limits": {
              "Small_Signal": ["-55 to 150", "-65 to 150"],
              "Power_BJT": ["-55 to 150", "-65 to 175"]
            }
          }
        ]
      },
      {
        "key": "vcex",
        "symbol": "V<sub>CEX</sub>",
        "spec_type": "max_rating",
        "column_model": "MAX_ONLY",
        "engineering_class": "SAFETY_LIMIT",
        "special_semantics": "NONE",
        "llm_context": {"formal_name": "Collector-Emitter Voltage with External Resistor", "aliases": ["V_CEX [V] Max. – V_CE with R_BE Resistor", "VCEX [V] Abs. Max. (With External R_B-E)", "Collector-Emitter with RBE [V] Max. V_CEX", "V_CE(X) Max. [V] – With Base-Emitter Resistor", "VCEX Abs. Max. [V] (R_BE Resistor Across B-E)", "V_CEX [V] Max. (External R_BE; Better Than V_CEO)", "V(CEX) [V] Max. – C-E Voltage with R_BE", "Collector-Emitter Voltage V_CEX [V] (R_B-E Fitted)", "Max. V_CEX [V] (V_CE, Base-Emitter Resistor Applied)"]},
        "possible_units": ["V"],
        "std_unit": "V",
        "scenarios": [
          {
            "condition": "With RBE resistor",
            "limits": {
              "Small_Signal": [20, 30, 45, 60],
              "Power_BJT": [60, 80, 100, 150, 250, 400]
            }
          }
        ]
      },
      {
        "key": "soa_dc",
        "symbol": "SOA",
        "spec_type": "max_rating",
        "column_model": "GRAPH",
        "engineering_class": "SAFETY_LIMIT",
        "special_semantics": "GRAPH_REFERENCE",
        "llm_context": {"formal_name": "Safe Operating Area - DC", "aliases": ["SOA – DC Safe Operating Area (See Graph)", "DC Safe Operating Area – Refer to Figure X", "DC SOA (I_C vs. V_CE, Continuous, See Curve)", "SOA [DC] – Safe Operating Region (Graph Only)", "Safe Operating Area – DC (I_C-V_CE Boundary)", "DC SOA (Bounded by: I_C(max), V_CEO, P_D, T_j)", "SOA DC Operation – Consult Datasheet Figure", "Safe Operating Area (DC) – See Characteristic Curve", "DC SOA Boundary – I_C / V_CE (Refer to Graph)"]},
        "possible_units": [""],
        "std_unit": "",
        "scenarios": [
          {
            "condition": "DC Operation",
            "limits": {
              "Small_Signal": ["See_Graph"],
              "Power_BJT": ["See_Graph"]
            }
          }
        ]
      },
      {
        "key": "soa_pulsed",
        "symbol": "SOA<sub>pulse</sub>",
        "spec_type": "max_rating",
        "column_model": "GRAPH",
        "engineering_class": "SAFETY_LIMIT",
        "special_semantics": "GRAPH_REFERENCE",
        "llm_context": {"formal_name": "Safe Operating Area - Pulsed", "aliases": ["SOA_pulse – Pulsed Safe Operating Area (See Graph)", "Pulsed Safe Operating Area – Refer to Figure X", "Pulsed SOA (I_C vs. V_CE, Duty Cycle Param., Graph)", "SOA [Pulsed] – Extended Region (Pulse Width Dep.)", "Safe Operating Area – Pulsed (I_C-V_CE, Fig.)", "SOA Pulsed Operation – Consult Datasheet Figure", "Safe Operating Area (Pulsed) – See Pulse Curves", "Pulsed SOA Boundary – I_C/V_CE (t_p Dependent)"]},
        "possible_units": [""],
        "std_unit": "",
        "scenarios": [
          {
            "condition": "Pulsed Operation",
            "limits": {
              "Small_Signal": ["See_Graph"],
              "Power_BJT": ["See_Graph"]
            }
          }
        ]
      },
      {
        "key": "secondary_breakdown",
        "symbol": "V<sub>(BR)CES</sub>",
        "spec_type": "max_rating",
        "column_model": "MIN_ONLY",
        "engineering_class": "SAFETY_LIMIT",
        "special_semantics": "NONE",
        "llm_context": {"formal_name": "Secondary Breakdown Voltage", "aliases": ["V_(BR)CES [V] Min. – Secondary Breakdown Voltage", "Second Breakdown V_CEO(sus) [V] Min.", "V_(BR)CES [V] – Secondary (2nd) Breakdown", "Secondary Breakdown [V] Min. (V_(BR)CES)", "VCEO(sus) [V] Min. – Sustained Breakdown Voltage", "2nd Breakdown V_(BR)CES [V] Min. (See SOA Note)", "V_(BR)CES Min. [V] – Safe Operating Boundary", "Secondary Breakdown Limit [V] Min. V(BR)CES", "V_CEO(sus) [V] Min. – Sustaining Breakdown", "2nd-Breakdown V_(BR)CES [V] (Refer to SOA Graph)"]},
        "possible_units": ["V"],
        "std_unit": "V",
        "scenarios": [
          {
            "condition": "At specified conditions",
            "limits": {
              "Small_Signal": [20, 30, 45],
              "Power_BJT": [40, 60, 80, 100, 150]
            }
          }
        ]
      },
      {
        "key": "lead_temp",
        "symbol": "T<sub>LEAD</sub>",
        "spec_type": "max_rating",
        "column_model": "MAX_ONLY",
        "engineering_class": "SAFETY_LIMIT",
        "special_semantics": "NONE",
        "llm_context": {"formal_name": "Lead Temperature (Soldering)", "aliases": ["T_LEAD [°C] Max. – Lead Temperature (Soldering)", "Soldering Temperature T_sol [°C] Max.", "Lead Temp (Soldering) [°C] Max.", "T_LEAD [°C] Max. (Wave/Iron Soldering)", "Lead Temp. [°C] Max. – Solder Point", "T_LEAD Max. [°C] – Iron/Wave Solder", "T_S(solder) [°C] Max.", "Reflow / Hand Solder Peak T_LEAD [°C] Max."]},
        "possible_units": ["°C"],
        "std_unit": "°C",
        "scenarios": [
          {
            "condition": "10 seconds",
            "limits": {
              "Small_Signal": [260, 300],
              "Power_BJT": [260, 300]
            }
          }
        ]
      }
    ],
    
    "ELEC_CHAR": [
      {
        "key": "bvceo",
        "symbol": "BV<sub>CEO</sub>",
        "spec_type": "min_limit",
        "column_model": "MIN_ONLY",
        "engineering_class": "PERFORMANCE_LIMIT",
        "special_semantics": "NONE",
        "llm_context": {"formal_name": "Collector-Emitter Breakdown Voltage", "aliases": ["BV_CEO [V] Min. – C-E Breakdown", "Breakdown Voltage BV_CEO [V] Min. (Open Base)", "V_(BR)CEO [V] Min. – Avalanche Breakdown", "Collector-Emitter Breakdown BV_CEO [V] Min.", "V(BR)CEO [V] Min. – Open-Base Breakdown", "Breakdown V_CEO [V] Min. (Open Base, See Test Cond.)"]},
        "possible_units": ["V"],
        "std_unit": "V",
        "scenarios": [
          {
            "condition": "At IC=1mA to 10mA",
            "limits": {
              "Small_Signal": [20, 30, 45, 60, 80],
              "Power_BJT": [50, 60, 80, 100, 140, 250, 400]
            }
          }
        ]
      },
      {
        "key": "bvcbo",
        "symbol": "BV<sub>CBO</sub>",
        "spec_type": "min_limit",
        "column_model": "MIN_ONLY",
        "engineering_class": "PERFORMANCE_LIMIT",
        "special_semantics": "NONE",
        "llm_context": {"formal_name": "Collector-Base Breakdown Voltage", "aliases": ["BV_CBO [V] Min. – C-B Breakdown", "V_(BR)CBO [V] Min. – Avalanche Breakdown (Emitter Open)", "Collector-Base Breakdown BV_CBO [V] Min.", "V(BR)CBO [V] Min. – Open-Emitter Breakdown", "Breakdown V_CBO [V] Min. (Open Emitter, See Cond.)", "BV_CBO [V] Min. – Collector-Base (Open Emitter)"]},
        "possible_units": ["V"],
        "std_unit": "V",
        "scenarios": [
          {
            "condition": "At IC=10µA to 100µA",
            "limits": {
              "Small_Signal": [30, 40, 60, 80, 100],
              "Power_BJT": [80, 100, 120, 160, 300, 450]
            }
          }
        ]
      },
      {
        "key": "bvebo",
        "symbol": "BV<sub>EBO</sub>",
        "spec_type": "min_limit",
        "column_model": "MIN_ONLY",
        "engineering_class": "PERFORMANCE_LIMIT",
        "special_semantics": "NONE",
        "llm_context": {"formal_name": "Emitter-Base Breakdown Voltage", "aliases": ["BV_EBO [V] Min. – E-B Breakdown", "V_(BR)EBO [V] Min. – Avalanche Breakdown (Coll. Open)", "Emitter-Base Breakdown BV_EBO [V] Min.", "V(BR)EBO [V] Min. – Open-Collector Breakdown", "Breakdown V_EBO [V] Min. (Open Collector, See Cond.)", "BV_EBO [V] Min. – Emitter-Base (Open Collector)"]},
        "possible_units": ["V"],
        "std_unit": "V",
        "scenarios": [
          {
            "condition": "At IE=10µA",
            "limits": {
              "Small_Signal": [5, 6, 7],
              "Power_BJT": [5, 6, 7, 8]
            }
          }
        ]
      },
      {
        "key": "hfe",
        "symbol": "h<sub>FE</sub>",
        "spec_type": "min_limit",
        "column_model": "MIN_TYP_MAX",
        "engineering_class": "PERFORMANCE_LIMIT",
        "special_semantics": "NONE",
        "llm_context": {"formal_name": "DC Current Gain", "aliases": ["h_FE [–] Min./Typ./Max. – DC Current Gain (Beta)", "Current Gain h_FE [–] (Min./Typ./Max., See Cond.)", "Static Forward Current Gain h_FE [–] Min. Typ."]},
        "possible_units": [""],
        "std_unit": "",
        "scenarios": [
          {
            "condition": "VCE=5V, IC=2mA",
            "limits": {
              "Small_Signal": [100, 150, 200, 250, 300, 400, 600],
              "Power_BJT": [10, 20, 30, 40, 50, 60, 100, 150]
            }
          },
          {
            "condition": "VCE=5V, IC=10mA",
            "limits": {
              "Small_Signal": [110, 150, 200, 300, 400],
              "Power_BJT": [15, 25, 40, 60, 100]
            }
          },
          {
            "condition": "VCE=2V, IC=500mA",
            "limits": {
              "Small_Signal": [],
              "Power_BJT": [10, 20, 30, 50, 80]
            }
          }
        ]
      },
      {
        "key": "vce_sat",
        "symbol": "V<sub>CE(sat)</sub>",
        "spec_type": "max_limit",
        "column_model": "TYP_MAX",
        "engineering_class": "PERFORMANCE_LIMIT",
        "special_semantics": "NONE",
        "llm_context": {"formal_name": "Saturation Voltage", "aliases": ["V_CE(sat) [mV/V] Typ./Max. – CE Saturation Voltage", "Collector-Emitter Saturation Voltage V_CE(sat) [V] Max.", "V(CE)(sat) [mV] Max. – CE Sat. (I_C/I_B=10)", "V_CE(SAT) Typ./Max. [V] – C-E Saturation", "Collector-Emitter Sat. Voltage [mV] V_CE(sat) Max."]},
        "possible_units": ["mV", "V"],
        "std_unit": "mV",
        "scenarios": [
          {
            "condition": "IC=10mA, IB=1mA",
            "limits": {
              "Small_Signal": [100, 150, 200, 250, 300],
              "Power_BJT": [200, 300, 500]
            }
          },
          {
            "condition": "IC=500mA, IB=50mA",
            "limits": {
              "Small_Signal": [200, 300, 500],
              "Power_BJT": [500, 800, 1000, 1500, 2000]
            }
          },
          {
            "condition": "IC=3A, IB=300mA",
            "limits": {
              "Small_Signal": [],
              "Power_BJT": [1000, 1500, 2000, 3000]
            }
          }
        ]
      },
      {
        "key": "vbe_sat",
        "symbol": "V<sub>BE(sat)</sub>",
        "spec_type": "max_limit",
        "column_model": "TYP_MAX",
        "engineering_class": "PERFORMANCE_LIMIT",
        "special_semantics": "NONE",
        "llm_context": {"formal_name": "Base-Emitter Saturation Voltage", "aliases": ["V_BE(sat) [V] Typ./Max. – B-E Saturation Voltage", "V(BE)(sat) [V] Max. – B-E Sat. (I_C/I_B=10)", "V_BE Saturation [V] Max. (Forced β Condition)", "VBE(SAT) [V] Typ./Max. – Base-Emitter Saturation", "Base-Emitter Sat. Voltage V_BE(sat) [V] Max."]},
        "possible_units": ["V", "mV"],
        "std_unit": "V",
        "scenarios": [
          {
            "condition": "IC=10mA, IB=1mA",
            "limits": {
              "Small_Signal": [0.7, 0.8, 0.9],
              "Power_BJT": [0.8, 0.9, 1.0]
            }
          },
          {
            "condition": "IC=500mA, IB=50mA",
            "limits": {
              "Small_Signal": [0.8, 0.9, 1.0],
              "Power_BJT": [0.9, 1.0, 1.2, 1.5]
            }
          }
        ]
      },
      {
        "key": "vbe_on",
        "symbol": "V<sub>BE(on)</sub>",
        "spec_type": "nominal",
        "column_model": "MIN_TYP_MAX",
        "engineering_class": "NOMINAL_PARAMETER",
        "special_semantics": "NONE",
        "llm_context": {"formal_name": "Base-Emitter On Voltage", "aliases": ["V_BE(on) [V] – Base-Emitter On Voltage (Active Region)", "Base-Emitter On Voltage V_BE [V] Min./Typ./Max.", "V(BE)(on) [V] – Forward B-E Voltage (Linear Region)", "Base-Emitter Forward Voltage V_BE [V] (Active)"]},
        "possible_units": ["V"],
        "std_unit": "V",
        "scenarios": [
          {
            "condition": "VCE=5V, IC=2mA",
            "limits": {
              "Small_Signal": [0.55, 0.6, 0.65, 0.7, 0.75],
              "Power_BJT": [0.6, 0.65, 0.7, 0.8]
            }
          },
          {
            "condition": "VCE=5V, IC=10mA",
            "limits": {
              "Small_Signal": [0.6, 0.65, 0.7, 0.75, 0.8],
              "Power_BJT": [0.65, 0.7, 0.8, 0.9]
            }
          },
          {
            "condition": "VCE=2V, IC=500mA",
            "limits": {
              "Small_Signal": [],
              "Power_BJT": [0.7, 0.8, 0.9, 1.0, 1.2]
            }
          }
        ]
      },
      {
        "key": "icbo",
        "symbol": "I<sub>CBO</sub>",
        "spec_type": "max_limit",
        "column_model": "MAX_ONLY",
        "engineering_class": "PERFORMANCE_LIMIT",
        "special_semantics": "NONE",
        "llm_context": {"formal_name": "Collector-Base Leakage Current", "aliases": ["I_CBO [nA/µA] Max. – Collector Cutoff Current (C-B)", "I(CBO) [µA] Max. – C-B Reverse Leakage", "I_CBO Max. [nA] – I_C with Open Emitter (V_CB=Spec.)"]},
        "possible_units": ["nA", "µA"],
        "std_unit": "nA",
        "scenarios": [
          {
            "condition": "VCB=30V to 60V, 25°C",
            "limits": {
              "Small_Signal": [10, 50, 100],
              "Power_BJT": [100, 500, 1000, 5000]
            }
          },
          {
            "condition": "VCB=30V to 60V, 150°C",
            "limits": {
              "Small_Signal": [1000, 5000],
              "Power_BJT": [10000, 50000, 100000]
            }
          }
        ]
      },
      {
        "key": "iceo",
        "symbol": "I<sub>CEO</sub>",
        "spec_type": "max_limit",
        "column_model": "MAX_ONLY",
        "engineering_class": "PERFORMANCE_LIMIT",
        "special_semantics": "NONE",
        "llm_context": {"formal_name": "Collector-Emitter Leakage Current", "aliases": ["I_CEO [nA/µA] Max. – Collector-Emitter Leakage", "Collector Cutoff Current I_CEO [nA] Max. (I_B=0)", "I(CEO) [µA] Max. – C-E Leakage (I_B=0)", "I_CEO Max. [µA] – I_C with Open Base (V_CE=Spec.)", "Collector-Emitter Leakage I(CEO) [µA] Max."]},
        "possible_units": ["nA", "µA", "mA"],
        "std_unit": "nA",
        "scenarios": [
          {
            "condition": "VCE=30V to 60V",
            "limits": {
              "Small_Signal": [50, 100, 500, 1000],
              "Power_BJT": [500, 1000, 5000, 10000]
            }
          }
        ]
      },
      {
        "key": "iebo",
        "symbol": "I<sub>EBO</sub>",
        "spec_type": "max_limit",
        "column_model": "MAX_ONLY",
        "engineering_class": "PERFORMANCE_LIMIT",
        "special_semantics": "NONE",
        "llm_context": {"formal_name": "Emitter-Base Leakage Current", "aliases": ["I_EBO [nA/µA] Max. – Emitter-Base Leakage Current", "I(EBO) [nA] Max. – E-B Reverse Leakage (I_C=0)", "I_EBO Max. [nA] – I_E with Open Collector", "Emitter-Base Leakage I(EBO) [nA] Max. (V_EB=5V)"]},
        "possible_units": ["nA", "µA"],
        "std_unit": "nA",
        "scenarios": [
          {
            "condition": "VEB=5V",
            "limits": {
              "Small_Signal": [10, 50, 100],
              "Power_BJT": [100, 500, 1000]
            }
          }
        ]
      },
      {
        "key": "ft",
        "symbol": "f<sub>T</sub>",
        "spec_type": "nominal",
        "column_model": "MIN_TYP_MAX",
        "engineering_class": "NOMINAL_PARAMETER",
        "special_semantics": "NONE",
        "llm_context": {"formal_name": "Transition Frequency", "aliases": ["f_T [MHz/GHz] Typ. – Transition Frequency", "fT [MHz] Typ. – Unity Current Gain Frequency", "Transition Freq. f_T [MHz] (|h_FE|=1 Crossover)", "Transition Frequency f_T [MHz] Min./Typ./Max."]},
        "possible_units": ["MHz", "GHz"],
        "std_unit": "MHz",
        "scenarios": [
          {
            "condition": "VCE=10V, IC=10mA",
            "limits": {
              "Small_Signal": [100, 150, 200, 250, 300, 400, 500, 600],
              "Power_BJT": [1, 3, 5, 10, 20, 30, 50]
            }
          }
        ]
      },
      {
        "key": "cob",
        "symbol": "C<sub>ob</sub>",
        "spec_type": "nominal",
        "column_model": "MIN_TYP_MAX",
        "engineering_class": "NOMINAL_PARAMETER",
        "special_semantics": "NONE",
        "llm_context": {"formal_name": "Output Capacitance", "aliases": ["C_ob [pF] Typ. – Output Capacitance", "Collector Output Capacitance C_ob [pF] Typ./Max.", "C(ob) [pF] – Collector-Base Capacitance", "Collector Output Capacitance [pF] C_ob"]},
        "possible_units": ["pF"],
        "std_unit": "pF",
        "scenarios": [
          {
            "condition": "VCB=10V, f=1MHz",
            "limits": {
              "Small_Signal": [1, 2, 3, 5, 8, 10, 15, 20],
              "Power_BJT": [30, 50, 100, 200, 500, 1000, 2000]
            }
          }
        ]
      },
      {
        "key": "cib",
        "symbol": "C<sub>ib</sub>",
        "spec_type": "nominal",
        "column_model": "TYP_MAX",
        "engineering_class": "NOMINAL_PARAMETER",
        "special_semantics": "NONE",
        "llm_context": {"formal_name": "Input Capacitance", "aliases": ["C_ib [pF] Typ./Max. – Input Capacitance", "Base Input Capacitance C_ib [pF] Typ./Max.", "C(ib) [pF] – Emitter-Base Capacitance", "Base Input Capacitance [pF] C_ib"]},
        "possible_units": ["pF"],
        "std_unit": "pF",
        "scenarios": [
          {
            "condition": "VEB=0.5V, f=1MHz",
            "limits": {
              "Small_Signal": [2, 5, 8, 10, 15],
              "Power_BJT": [50, 100, 200, 500, 1000]
            }
          }
        ]
      },
      {
        "key": "cre",
        "symbol": "C<sub>re</sub>",
        "spec_type": "nominal",
        "column_model": "TYP_MAX",
        "engineering_class": "NOMINAL_PARAMETER",
        "special_semantics": "NONE",
        "llm_context": {"formal_name": "Reverse Transfer Capacitance", "aliases": ["C_re [pF] Typ./Max. – Reverse Transfer Capacitance", "Collector-Base Capacitance C_re [pF] Typ./Max.", "C(re) [pF] – C-B Reverse Transfer Cap.", "Miller Capacitance C_re [pF] Typ.", "Reverse Transfer Cap. C_re [pF] Typ. Max.", "Feedback Capacitance C_re [pF] Typ. (C-B)"]},
        "possible_units": ["pF"],
        "std_unit": "pF",
        "scenarios": [
          {
            "condition": "VCB=10V, f=1MHz",
            "limits": {
              "Small_Signal": [0.5, 1, 1.5, 2, 3],
              "Power_BJT": [5, 10, 20, 50, 100]
            }
          }
        ]
      },
      {
        "key": "hfe_linearity",
        "symbol": "Δh<sub>FE</sub>",
        "spec_type": "max_limit",
        "column_model": "TYP_MAX",
        "engineering_class": "PERFORMANCE_LIMIT",
        "special_semantics": "NONE",
        "llm_context": {"formal_name": "hFE Variation", "aliases": ["Δh_FE [%] Typ./Max. – h_FE / Beta Variation", "Gain Variation Δh_FE [%] (Over I_C Range, Max.)", "Beta Variation [%] Δh_FE (I_C Sweep, Typ./Max.)", "Δh_FE [%] Max. (h_FE Change Over I_C Range)", "h_FE Linearity [%] Max. – Gain Flatness (I_C)", "ΔBeta [%] Max. (Over Specified I_C Range)", "Δh_FE Max. [%] – Gain Roll-Off Across I_C", "h_FE Deviation [%] Max. (Min. to Max. I_C Swing)", "Δh_FE [%] (Gain Variation: Low to High I_C)"]},
        "possible_units": ["%"],
        "std_unit": "%",
        "scenarios": [
          {
            "condition": "Over IC range",
            "limits": {
              "Small_Signal": [10, 20, 30],
              "Power_BJT": [20, 30, 50]
            }
          }
        ]
      },
      {
        "key": "thermal_resistance_jc",
        "symbol": "θ<sub>JC</sub>",
        "spec_type": "nominal",
        "column_model": "TYP_MAX",
        "engineering_class": "NOMINAL_PARAMETER",
        "special_semantics": "NONE",
        "llm_context": {"formal_name": "Thermal Resistance Junction to Case", "aliases": ["θ_JC [°C/W] Typ./Max. – Thermal Resistance J-C", "Rth(j-c) [°C/W] Max. – Junction to Case", "Thermal Res. J-C θ_JC [°C/W] Typ./Max.", "R_TH(JC) [°C/W] Max. (Case = Mounting Surface)", "θ_JC [°C/W] – Junction to Case (Steady State)", "R(θJC) [K/W] Max. (Mounting Tab / Case Ref.)", "Theta JC [°C/W] Typ./Max. – R_θJC", "Rth J→C [°C/W] Max. (Thermal Contact = Case)", "Thermal Res. J-C θ_JC [°C/W] (Typ. Max.)", "θ(JC) [°C/W] Max – See Package Thermal Model"]},
        "possible_units": ["°C/W"],
        "std_unit": "°C/W",
        "scenarios": [
          {
            "condition": "N/A",
            "limits": {
              "Small_Signal": [200, 150, 100, 50],
              "Power_BJT": [5, 3, 2, 1.5, 1, 0.7, 0.5]
            }
          }
        ]
      },
      {
        "key": "thermal_resistance_ja",
        "symbol": "θ<sub>JA</sub>",
        "spec_type": "nominal",
        "column_model": "TYP_MAX",
        "engineering_class": "NOMINAL_PARAMETER",
        "special_semantics": "NONE",
        "llm_context": {"formal_name": "Thermal Resistance Junction to Ambient", "aliases": ["θ_JA [°C/W] Typ./Max. – Thermal Resistance J-A", "Rth(j-a) [°C/W] Max. – Junction to Ambient", "Thermal Res. J-A θ_JA [°C/W] Typ./Max.", "R_TH(JA) [°C/W] Max. (Free Air, No Heat Sink)", "θ_JA [°C/W] – Junction to Ambient (Free Air)", "Theta JA [°C/W] Typ./Max. – R_θJA (Free Air)", "Rth J→A [°C/W] Max. (Free Air, No Forced Cooling)", "Thermal Impedance J-A θ_JA [°C/W] Typ. Max.", "θ(JA) [°C/W] Max – Free Air, Standard PCB"]},
        "possible_units": ["°C/W"],
        "std_unit": "°C/W",
        "scenarios": [
          {
            "condition": "Free air",
            "limits": {
              "Small_Signal": [200, 300, 400, 500],
              "Power_BJT": [40, 50, 62.5, 80, 100]
            }
          }
        ]
      },
      {
        "key": "noise_figure",
      "symbol": "NF",
      "spec_type": "max_limit",
      "column_model": "TYP_MAX",
      "engineering_class": "PERFORMANCE_LIMIT",
      "special_semantics": "NONE",
      "llm_context": {"formal_name": "Noise Figure", "aliases": ["NF [dB] Typ./Max. – Noise Figure", "Spot Noise Figure [dB] NF", "Noise Figure F [dB] Max.", "Spot NF [dB] Max.", "NF Typ. Max. [dB] – BJT Spot Noise"]},
      "possible_units": ["dB"],
      "std_unit": "dB",
      "scenarios": [
        {
          "condition": "f=1kHz, Rg=1kΩ",
          "limits": {
            "Small_Signal": [1, 2, 4, 6, 10],
            "Power_BJT": [] 
          }
        }
      ]
    },
    {
      "key": "delay_time",
      "symbol": "t<sub>d</sub>",
      "spec_type": "nominal",
      "column_model": "TYP_MAX",
      "engineering_class": "DYNAMIC_PARAMETER",
      "special_semantics": "SWITCHING",
      "llm_context": {"formal_name": "Delay Time", "aliases": ["t_d [ns] Typ./Max. – Delay Time (Switching)", "td [ns] – Turn-On Delay (Input to 10% I_C)", "t_delay [ns] Max. – Switching Delay (BJT)", "t_d [µs] Typ./Max. – Input to 10% Output Delay", "Switching Delay t_d [ns] Max. (Resistive Load)", "t_d [ns] Max. – Time: Input Step to 10% I_C"]},
      "possible_units": ["ns", "µs"],
      "std_unit": "ns",
      "scenarios": [
        {
          "condition": "VCC=30V, IC=1A, IB1=-IB2",
          "limits": {
            "Small_Signal": [5, 10, 35],
            "Power_BJT": [10, 50, 100, 200]
          }
        }
      ]
    },
    {
      "key": "rise_time",
      "symbol": "t<sub>r</sub>",
      "spec_type": "nominal",
      "column_model": "TYP_MAX",
      "engineering_class": "DYNAMIC_PARAMETER",
      "special_semantics": "SWITCHING",
      "llm_context": {"formal_name": "Rise Time", "aliases": ["t_r [ns] Typ./Max. – Rise Time (10% to 90% I_C)", "Rise Time t_r [ns] Max. (Resistive Load, Spec. Cond.)", "tr [ns] – Current Rise Time (10% to 90%)", "t_RISE [ns] Max. – Switching Rise (I_C 10→90%)", "t_r [µs] Typ./Max. – 10% to 90% I_C Rise", "Switching t_r [ns] Max. (Resistive Load, V_CC)", "t_r [ns] Max. – Time: 10% to 90% Collector I"]},
      "possible_units": ["ns", "µs"],
      "std_unit": "ns",
      "scenarios": [
        {
          "condition": "Resistive Load",
          "limits": {
            "Small_Signal": [10, 40, 100],
            "Power_BJT": [100, 300, 700, 1500]
          }
        }
      ]
    },
    {
      "key": "storage_time",
      "symbol": "t<sub>s</sub>",
      "spec_type": "nominal",
      "column_model": "TYP_MAX",
      "engineering_class": "DYNAMIC_PARAMETER",
      "special_semantics": "SWITCHING",
      "llm_context": {"formal_name": "Storage Time", "aliases": ["t_s [ns] Typ./Max. – Storage Time (Saturation)", "ts [ns] – Saturation Storage Time (t_s)", "t_storage [ns] Max. – Charge Storage (Saturation)", "t_s [µs] Typ./Max. – Stored Charge Recovery", "t_s [ns] Max. – Time: I_B Removed to 90% I_C"]},
      "possible_units": ["ns", "µs"],
      "std_unit": "ns",
      "scenarios": [
        {
          "condition": "VCC=30V, IC=1A, IB1=-IB2",
          "limits": {
            "Small_Signal": [150, 200, 400],
            "Power_BJT": [500, 1000, 2500, 4000]
          }
        }
      ]
    },
    {
      "key": "fall_time",
      "symbol": "t<sub>f</sub>",
      "spec_type": "nominal",
      "column_model": "TYP_MAX",
      "engineering_class": "DYNAMIC_PARAMETER",
      "special_semantics": "SWITCHING",
      "llm_context": {"formal_name": "Fall Time", "aliases": ["t_f [ns] Typ./Max. – Fall Time (90% to 10% I_C)", "Fall Time t_f [ns] Max. (Resistive Load, Spec. Cond.)", "tf [ns] – Current Fall Time (90% to 10%)", "t_FALL [ns] Max. – Switching Fall (I_C 90→10%)", "t_f [µs] Typ./Max. – 90% to 10% I_C Fall", "Switching t_f [ns] Max. (Resistive Load, V_CC)", "t_f [ns] Max. – Time: 90% to 10% Collector I"]},
      "possible_units": ["ns", "µs"],
      "std_unit": "ns",
      "scenarios": [
        {
          "condition": "Resistive Load",
          "limits": {
            "Small_Signal": [20, 50, 100],
            "Power_BJT": [100, 400, 800, 2000]
          }
        }
      ]
    },
    {
      "key": "input_impedance_hie",
      "symbol": "h<sub>ie</sub>",
      "spec_type": "nominal",
      "column_model": "MIN_TYP_MAX",
      "engineering_class": "SMALL_SIGNAL_PARAMETER",
      "special_semantics": "HYBRID_PARAM",
      "llm_context": {"formal_name": "Input Impedance (Small Signal)", "aliases": ["h_ie [kΩ/Ω] Typ. – Small-Signal Input Impedance", "Input Impedance h_ie [kΩ] Min./Typ./Max.", "hie [kΩ] – h-param Input Z", "Small-Signal h_ie [kΩ] Min. Typ. Max.", "h_ie Typ. [kΩ] – Hybrid Input Parameter", "h(ie) [Ω] Min./Typ./Max. (Active Region)"]},
      "possible_units": ["kΩ", "Ω"],
      "std_unit": "kΩ",
      "scenarios": [
        {
          "condition": "VCE=10V, IC=1mA, f=1kHz",
          "limits": {
            "Small_Signal": [1, 2, 5, 10],
            "Power_BJT": [0.5, 1, 2]
          }
        }
      ]
    },
    {
      "key": "output_admittance_hoe",
      "symbol": "h<sub>oe</sub>",
      "spec_type": "nominal",
      "column_model": "MIN_TYP_MAX",
      "engineering_class": "SMALL_SIGNAL_PARAMETER",
      "special_semantics": "HYBRID_PARAM",
      "llm_context": {"formal_name": "Output Admittance (Small Signal)", "aliases": ["h_oe [µS] Typ. – Small-Signal Output Admittance", "Output Admittance h_oe [µS] Min./Typ./Max.", "hoe [µmhos] – h-param Output Y", "Small-Signal h_oe [µS] Min. Typ. Max.", "h_oe Typ. [µS] – Hybrid Output Admittance", "h(oe) [µmhos] Min./Typ./Max. (Active)"]},
      "possible_units": ["µS", "µmhos"],
      "std_unit": "µS",
      "scenarios": [
        {
          "condition": "VCE=10V, IC=1mA, f=1kHz",
          "limits": {
            "Small_Signal": [5, 10, 30, 50, 100],
            "Power_BJT": [50, 100, 200]
          }
        }
      ]
    },
    {
      "key": "reverse_voltage_ratio_hre",
      "symbol": "h<sub>re</sub>",
      "spec_type": "nominal",
      "column_model": "TYP_MAX",
      "engineering_class": "SMALL_SIGNAL_PARAMETER",
      "special_semantics": "HYBRID_PARAM",
      "llm_context": {"formal_name": "Reverse Voltage Ratio", "aliases": ["h_re [×10⁻⁴] Typ./Max. – Reverse Voltage Feedback Ratio", "Reverse Voltage Feedback Ratio h_re [×10⁻⁴]", "hre [–] – h-param Reverse Voltage", "Small-Signal h_re [×10⁻⁴] Typ. Max.", "Reverse Voltage Ratio h_re [–] Typ./Max.", "h_re Typ. [×10⁻⁴] – Hybrid Reverse Param.", "h(re) [×10⁻⁴] Typ./Max. (Active Region)"]},
      "possible_units": ["x10^-4", ""],
      "std_unit": "x10^-4",
      "scenarios": [
        {
          "condition": "VCE=10V, IC=1mA, f=1kHz",
          "limits": {
            "Small_Signal": [0.1, 1, 2, 5, 10],
            "Power_BJT": [5, 10, 20]
           }
          }
        ]
      }
    ],

    "SWITCHING_CHAR": [
      {
        "key": "switch_td_on",
        "symbol": "t<sub>d(on)</sub>",
        "spec_type": "nominal",
        "column_model": "TYP_MAX",
        "engineering_class": "SWITCHING",
        "special_semantics": "NONE",
        "llm_context": {"formal_name": "Turn-On Delay Time", "aliases": ["t_d(on) [ns] Typ./Max. – Turn-On Delay Time", "Turn-On Delay t_d(on) [ns] (Typ./Max.)", "td(on) [ns] – Delay Time (Turn-On)", "t_DON [ns] Typ./Max. – Switching Delay (On)", "Turn-On Delay [ns] t_d(on) (See Test Cond.)", "t_d(ON) [ns] Max. – Delay: Input to Output Rise", "td(ON) [ns] Typ./Max. – Turn-On Delay (Switching)", "Turn-On Delay Time t_d(on) [ns] (Note: Test Circuit)"]},
        "possible_units": ["ns"],
        "std_unit": "ns",
        "scenarios": [
          {
            "condition": "IC=IC_test, VCC=VCC_test, IB1=IC/10",
            "limits": {
              "Small_Signal": [5, 10, 15, 20, 30, 50],
              "Power_BJT": [20, 40, 80, 150, 300, 600]
            }
          }
        ]
      },
      {
        "key": "switch_tr",
        "symbol": "t<sub>r</sub>",
        "spec_type": "nominal",
        "column_model": "TYP_MAX",
        "engineering_class": "SWITCHING",
        "special_semantics": "NONE",
        "llm_context": {"formal_name": "Rise Time (Switching)", "aliases": ["t_r [ns] Typ./Max. – Rise Time (Switching)", "Rise Time t_r [ns] (10% to 90% Collector Voltage)", "tr [ns] – Rise Time (Switching Characteristics)", "t_R [ns] Typ./Max. – Collector Voltage Rise Time", "Rise Time [ns] t_r (10%→90%, Switching)", "t_r(10–90%) [ns] Typ./Max. – Signal Rise", "Rise Time t_r [ns] (See Switching Test Circuit)", "tr [ns] Typ./Max. – IC Rise to 90% (Turn-On)"]},
        "possible_units": ["ns"],
        "std_unit": "ns",
        "scenarios": [
          {
            "condition": "IC=IC_test, VCC=VCC_test, IB1=IC/10",
            "limits": {
              "Small_Signal": [10, 20, 30, 50, 80, 150],
              "Power_BJT": [30, 60, 120, 200, 400, 800]
            }
          }
        ]
      },
      {
        "key": "switch_ts",
        "symbol": "t<sub>s</sub>",
        "spec_type": "nominal",
        "column_model": "TYP_MAX",
        "engineering_class": "SWITCHING",
        "special_semantics": "NONE",
        "llm_context": {"formal_name": "Storage Time", "aliases": ["t_s [ns] Typ./Max. – Storage Time (Turn-Off)", "Storage Time t_s [ns] (Saturation Recovery)", "ts [ns] – Storage Time (Turn-Off Switching)", "t_S [ns] Typ./Max. – Charge Storage Delay", "Storage Time [ns] t_s (See Turn-Off Test Cond.)", "t_stg [ns] Typ./Max. – Saturation Storage Delay", "Storage Time t_s [ns] (Base Drive Reversal, Sat.)", "ts [ns] Typ./Max. – Collector to 90% Residual (Off)"]},
        "possible_units": ["ns"],
        "std_unit": "ns",
        "scenarios": [
          {
            "condition": "IC=IC_test, VCC=VCC_test, IB2=-IC/10",
            "limits": {
              "Small_Signal": [20, 40, 80, 150, 250, 500],
              "Power_BJT": [100, 200, 500, 1000, 2000, 5000]
            }
          }
        ]
      },
      {
        "key": "switch_tf",
        "symbol": "t<sub>f</sub>",
        "spec_type": "nominal",
        "column_model": "TYP_MAX",
        "engineering_class": "SWITCHING",
        "special_semantics": "NONE",
        "llm_context": {"formal_name": "Fall Time (Switching)", "aliases": ["t_f [ns] Typ./Max. – Fall Time (Switching)", "Fall Time t_f [ns] (90% to 10% Collector Voltage)", "tf [ns] – Fall Time (Switching Characteristics)", "t_F [ns] Typ./Max. – Collector Voltage Fall Time", "Fall Time [ns] t_f (90%→10%, Turn-Off)", "t_f(90–10%) [ns] Typ./Max. – Signal Fall", "Fall Time t_f [ns] (See Switching Test Circuit)", "tf [ns] Typ./Max. – IC Fall to 10% (Turn-Off)"]},
        "possible_units": ["ns"],
        "std_unit": "ns",
        "scenarios": [
          {
            "condition": "IC=IC_test, VCC=VCC_test, IB2=-IC/10",
            "limits": {
              "Small_Signal": [10, 20, 40, 80, 150, 300],
              "Power_BJT": [30, 60, 100, 200, 400, 800]
            }
          }
        ]
      },
      {
        "key": "ton_total",
        "symbol": "t<sub>on</sub>",
        "spec_type": "nominal",
        "column_model": "TYP_MAX",
        "engineering_class": "SWITCHING",
        "special_semantics": "NONE",
        "llm_context": {"formal_name": "Turn-On Time", "aliases": ["t_on [ns] Typ./Max. – Total Turn-On Time", "Turn-On Time t_on [ns] (td(on) + tr)", "ton [ns] – Total Turn-On Switching Time", "t_ON [ns] Typ./Max. (= t_d(on) + t_r)", "Turn-On Time [ns] t_on (Total, Switch-On)", "Total Turn-On t_on [ns] Typ./Max. (See Test Cond.)", "t_ON [ns] Typ./Max. – Turn-On (Delay + Rise)", "ton [ns] Max. – Total Switch-On Time"]},
        "possible_units": ["ns"],
        "std_unit": "ns",
        "scenarios": [
          {
            "condition": "IC=IC_test, VCC=VCC_test",
            "limits": {
              "Small_Signal": [20, 40, 60, 100, 150, 250],
              "Power_BJT": [60, 120, 250, 500, 900, 1500]
            }
          }
        ]
      },
      {
        "key": "toff_total",
        "symbol": "t<sub>off</sub>",
        "spec_type": "nominal",
        "column_model": "TYP_MAX",
        "engineering_class": "SWITCHING",
        "special_semantics": "NONE",
        "llm_context": {"formal_name": "Turn-Off Time", "aliases": ["t_off [ns] Typ./Max. – Total Turn-Off Time", "Turn-Off Time t_off [ns] (ts + tf)", "toff [ns] – Total Turn-Off Switching Time", "t_OFF [ns] Typ./Max. (= t_s + t_f)", "Turn-Off Time [ns] t_off (Total, Switch-Off)", "Total Turn-Off t_off [ns] Typ./Max. (See Test Cond.)", "t_OFF [ns] Typ./Max. – Turn-Off (Storage + Fall)", "toff [ns] Max. – Total Switch-Off Time"]},
        "possible_units": ["ns"],
        "std_unit": "ns",
        "scenarios": [
          {
            "condition": "IC=IC_test, VCC=VCC_test",
            "limits": {
              "Small_Signal": [30, 60, 100, 200, 350, 650],
              "Power_BJT": [150, 300, 700, 1500, 3000, 6000]
            }
          }
        ]
      }
    ],

    "THERMAL_CHAR": [
      {
        "key": "theta_jc_bjt",
        "symbol": "R<sub>θJC</sub>",
        "spec_type": "nominal",
        "column_model": "TYP_MAX",
        "engineering_class": "NOMINAL_PARAMETER",
        "special_semantics": "NONE",
        "llm_context": {"formal_name": "Thermal Resistance Junction-to-Case", "aliases": ["R_θJC [°C/W] Typ./Max. – Junction-to-Case Thermal Resistance", "Thermal Resistance Junction-Case R_θJC [°C/W] Max.", "θ_JC [°C/W] Max. – J-to-C Thermal Resistance", "R(θJC) [°C/W] Max. – Thermal Resist. (J-C)", "Thermal Resistance J-C [°C/W] R_θJC Max.", "R_θJC Typ./Max. [°C/W] – Junction-to-Case (Steady-State)", "Thermal Res. R_θJC [°C/W] Max. (J-to-Case)", "Junction-to-Case Thermal Resistance [°C/W] Typ./Max."]},
        "possible_units": ["°C/W"],
        "std_unit": "°C/W",
        "scenarios": [
          {
            "condition": "DC, Steady-State",
            "limits": {
              "Small_Signal": [100, 150, 200, 300, 500, 800],
              "Power_BJT": [0.4, 0.7, 1, 1.5, 2, 3, 5, 8]
            }
          }
        ]
      },
      {
        "key": "theta_ja_bjt",
        "symbol": "R<sub>θJA</sub>",
        "spec_type": "nominal",
        "column_model": "TYP_MAX",
        "engineering_class": "NOMINAL_PARAMETER",
        "special_semantics": "NONE",
        "llm_context": {"formal_name": "Thermal Resistance Junction-to-Ambient", "aliases": ["R_θJA [°C/W] Typ./Max. – Junction-to-Ambient Thermal Resistance", "Thermal Resistance Junction-Ambient R_θJA [°C/W] Max.", "θ_JA [°C/W] Max. – J-to-A Thermal Resistance", "R(θJA) [°C/W] Max. – Thermal Resist. (J-A)", "Thermal Resistance J-A [°C/W] R_θJA Max.", "R_θJA Typ./Max. [°C/W] – Junction-to-Ambient (No Heatsink)", "Thermal Res. R_θJA [°C/W] Max. (J-to-Ambient)", "Junction-to-Ambient Thermal Resistance [°C/W] (Free Air)"]},
        "possible_units": ["°C/W"],
        "std_unit": "°C/W",
        "scenarios": [
          {
            "condition": "Free Air, No Heatsink",
            "limits": {
              "Small_Signal": [200, 300, 400, 500, 600, 800, 1000],
              "Power_BJT": [5, 8, 10, 15, 20, 30, 40, 60]
            }
          }
        ]
      },
      {
        "key": "pd_tc25",
        "symbol": "P<sub>D</sub>",
        "spec_type": "max_rating",
        "column_model": "MAX_ONLY",
        "engineering_class": "SAFETY_LIMIT",
        "special_semantics": "NONE",
        "llm_context": {"formal_name": "Total Power Dissipation", "aliases": ["P_D [W] Max. – Total Power Dissipation (Tc=25°C)", "Power Dissipation P_D [W] Max. (Case Temp. = 25°C)", "P_TOT [W] Max. at T_C=25°C – Total Dissipation", "Total Power Dissip. P_D [W] Max. (Case=25°C)", "P_D(max) [W] at Tc=25°C – Power Rating", "Max. Power Dissipation [W] P_D (at T_case=25°C)", "P_D [W] Max. – Power Rating at T_C=25°C (Derate Above)", "Total Dissipation P_D [W] Max. (Tc=25°C, No Heatsink)"]},
        "possible_units": ["W", "mW"],
        "std_unit": "W",
        "scenarios": [
          {
            "condition": "Tc=25°C",
            "limits": {
              "Small_Signal": [0.2, 0.3, 0.4, 0.5, 0.6, 0.8, 1.0],
              "Power_BJT": [10, 20, 30, 50, 75, 100, 150, 200, 250]
            }
          }
        ]
      },
      {
        "key": "derating_factor",
        "symbol": "D<sub>F</sub>",
        "spec_type": "nominal",
        "column_model": "TYP_ONLY",
        "engineering_class": "NOMINAL_PARAMETER",
        "special_semantics": "NONE",
        "llm_context": {"formal_name": "Power Derating Factor", "aliases": ["Derating Factor [mW/°C] – Power Derating Above T_C", "Power Derate Factor [mW/°C] (Above 25°C)", "D_F [mW/°C] – Derating Factor (P vs. T_C Slope)", "Power Derating [mW/°C] Above T_case=25°C", "Derate Factor [mW/°C] (P_D Reduction per °C)", "Thermal Derating [mW/°C] (Above T_c Reference)", "Power Derating Factor [mW/°C] – See Derating Curve", "Derate [mW/°C] – Power vs. Case Temperature Slope"]},
        "possible_units": ["mW/°C", "W/°C"],
        "std_unit": "mW/°C",
        "scenarios": [
          {
            "condition": "Above Tc=25°C",
            "limits": {
              "Small_Signal": [2, 3, 4, 5, 6, 8],
              "Power_BJT": [80, 120, 160, 200, 300, 400, 600, 800, 1000]
            }
          }
        ]
      }
    ],

    "DYNAMIC_CHAR": [
      {
        "key": "cibo",
        "symbol": "C<sub>ibo</sub>",
        "spec_type": "max_limit",
        "column_model": "TYP_MAX",
        "engineering_class": "DYNAMIC_PARAMETER",
        "special_semantics": "NONE",
        "llm_context": {"formal_name": "Input Capacitance", "aliases": ["C_ibo [pF] Typ./Max. – Input (E-B) Capacitance, Open Collector", "Input Capacitance C_ibo [pF] Max. (Emitter-Base, OC)", "C_be [pF] Typ./Max. – Base-Emitter Capacitance (Open Coll.)", "C_ibo [pF] – E-B Input Junction Capacitance (Coll. Open)", "Input Cap. C_ibo [pF] Max. (f=1MHz, Open Collector)", "C(ibo) [pF] Typ./Max. – Emitter-Base Capacitance", "C_EB [pF] – Input Capacitance (B-E Junction, Open Coll.)", "Cibo [pF] Max. – Input Junction Cap. (Open Collector)"]},
        "possible_units": ["pF"],
        "std_unit": "pF",
        "scenarios": [
          {
            "condition": "VEB=0.5V, f=1MHz, IC=0",
            "limits": {
              "Small_Signal": [2, 3, 5, 8, 10, 15, 20, 30],
              "Power_BJT": [50, 100, 200, 400, 800, 1500, 3000]
            }
          }
        ]
      },
      {
        "key": "cobo",
        "symbol": "C<sub>obo</sub>",
        "spec_type": "max_limit",
        "column_model": "TYP_MAX",
        "engineering_class": "DYNAMIC_PARAMETER",
        "special_semantics": "NONE",
        "llm_context": {"formal_name": "Output Capacitance", "aliases": ["C_obo [pF] Typ./Max. – Output (C-B) Capacitance, Open Emitter", "Output Capacitance C_obo [pF] Max. (Collector-Base, OE)", "C_cb [pF] Typ./Max. – Collector-Base Capacitance (Open Em.)", "C_obo [pF] – C-B Output Junction Capacitance (Em. Open)", "Output Cap. C_obo [pF] Max. (f=1MHz, Open Emitter)", "C(obo) [pF] Typ./Max. – Collector-Base Capacitance", "C_CB [pF] – Output Capacitance (C-B Junction, Open Em.)", "Cobo [pF] Max. – Output Junction Cap. (Open Emitter)"]},
        "possible_units": ["pF"],
        "std_unit": "pF",
        "scenarios": [
          {
            "condition": "VCB=10V, f=1MHz, IE=0",
            "limits": {
              "Small_Signal": [1, 2, 3, 5, 8, 12, 20],
              "Power_BJT": [20, 40, 80, 150, 300, 600, 1200]
            }
          }
        ]
      },
      {
        "key": "ft_sw",
        "symbol": "f<sub>T</sub>",
        "spec_type": "nominal",
        "column_model": "MIN_TYP",
        "engineering_class": "DYNAMIC_PARAMETER",
        "special_semantics": "NONE",
        "llm_context": {"formal_name": "Current Gain–Bandwidth Product", "aliases": ["f_T [MHz/GHz] Typ./Min. – Gain-Bandwidth Product (Unity h_FE)", "Transition Frequency f_T [MHz] Typ. (|h_fe|=1)", "f_T [MHz] Typ. – Unity-Gain Bandwidth (hFE=1)", "Gain Bandwidth f_T [GHz] Typ. (Short-Circuit h_fe=1)", "f(T) [MHz] Typ./Min. – Transition Frequency", "f_T [MHz] Min./Typ. – Unity-Current-Gain Freq.", "Transit Frequency f_T [MHz] Typ. (hfe=1 crossover)", "fT [MHz] Min./Typ. – GBW Product (h_FE Unity-Gain)"]},
        "possible_units": ["MHz", "GHz"],
        "std_unit": "MHz",
        "scenarios": [
          {
            "condition": "VCE=10V, IC=10mA, f=100MHz",
            "limits": {
              "Small_Signal": [100, 150, 200, 300, 500, 800, 1000, 2000, 4000, 8000],
              "Power_BJT": [3, 5, 8, 10, 20, 30, 50, 80]
            }
          }
        ]
      }
    ]
  },

    # ==============================================================================
    # 8. OPAMP חלק8
    # ==============================================================================
    "OPAMP": {
    "archetypes": ["General_Purpose", "Precision_Zero_Drift", "High_Speed"],

    "ABS_MAX": [
      {
        "key": "supply_voltage",
        "symbol": "V<sub>S</sub>",
        "spec_type": "max_rating",
        "column_model": "MAX_ONLY",
        "engineering_class": "SAFETY_LIMIT",
        "special_semantics": "NONE",
        "llm_context": {
          "formal_name": "Total Supply Voltage",
          "aliases": ["V_S [V] Max. – Total Supply Voltage (V+ - V-)", "Supply Voltage V_S [V] Abs. Max. (V+ minus V-)", "Max Supply Voltage [V] V_S (Total, V+ to V-)", "V_S [V] Abs. Max. (Single or Dual, Total Span)", "Total Supply V_S [V] Max. (V_CC to V_EE)", "V_S = V+ - V- [V] Abs. Max. (Do Not Exceed)", "Supply Voltage V_CC [V] Max. (Total Span, Abs.)", "Max. V_S [V] – Total Span (V+ - V-, Abs. Max.)", "V(S) [V] Max. – Total Supply (V+ to V-)", "Abs. Max. Supply V_S [V] (V+ - V- Combined)"]
        },
        "possible_units": ["V"],
        "std_unit": "V",
        "scenarios": [
          {
            "condition": "Total (V+ - V-)",
            "limits": {
              "General_Purpose": [16, 32, 36, 40, 44],
              "Precision_Zero_Drift": [5.5, 6, 12, 16, 18],
              "High_Speed": [5.5, 6, 12, 15]
            }
          }
        ]
      },
      {
        "key": "differential_input_voltage",
        "symbol": "V<sub>ID</sub>",
        "spec_type": "max_rating",
        "column_model": "MAX_ONLY",
        "engineering_class": "SAFETY_LIMIT",
        "special_semantics": "NONE",
        "llm_context": {
          "formal_name": "Differential Input Voltage",
          "aliases": ["V_ID [V] Max. – Differential Input Voltage (Abs.)", "Max Differential Input V_ID [V] (Abs. Max.)", "Diff. Input Voltage V_ID [V] Max. (V+ - V-)", "V_ID [V] Abs. Max. – Between Input Pins (±)", "Differential Input V_DIFF [V] Max. (Abs.)", "V(ID) [V] Abs. Max. – V(+) to V(-) Input", "V_ID [V] Max. (|V(+) - V(-)| Do Not Exceed)", "Max. V_ID [V] – Differential (Input Pin Voltage)", "Differential Input Rating V_ID [V] (Abs. Max.)", "V_ID Abs. Max. [V] (Input+ to Input-, No Damage)"]
        },
        "possible_units": ["V"],
        "std_unit": "V",
        "scenarios": [
          {
            "condition": "Max",
            "limits": {
              "General_Purpose": [32, 36, 40, 44],
              "Precision_Zero_Drift": [5.5, 6, 12, 16],
              "High_Speed": [5.5, 6, 12]
            }
          }
        ]
      },
      {
        "key": "input_voltage_range",
        "symbol": "V<sub>ICM</sub>",
        "spec_type": "max_rating",
        "column_model": "MIN_MAX",
        "engineering_class": "SAFETY_LIMIT",
        "special_semantics": "NONE",
        "llm_context": {
          "formal_name": "Input Common-Mode Voltage Range",
          "aliases": ["V_ICM [V] – Input Common-Mode Voltage (Abs. Max.)", "Common Mode Input Voltage V_CM [V] (Abs. Max. Range)", "Input Voltage Range V_ICM [V] (Min. to Max.)", "V_ICM [V] Abs. Max.", "Common-Mode Input Range [V] V_ICM (Abs. Max.)", "V_CM [V] (Allowable CM Input, V- to V+)", "Input V_ICM [V] Range (Abs. Max., CM Voltage)", "Common Mode V_ICM [V] – Max. CM Input Range", "V_ICM Abs. Max. [V] (Input Pin, Both ± Rails)"]
        },
        "possible_units": ["V"],
        "std_unit": "V",
        "scenarios": [
          {
            "condition": "Absolute Max",
            "limits": {
              "General_Purpose": ["V- to V+", "V--0.3 to V++0.3"],
              "Precision_Zero_Drift": ["V--0.3 to V++0.3"],
              "High_Speed": ["V- to V+"]
            }
          }
        ]
      },
      {
        "key": "output_short_circuit_duration",
        "symbol": "t<sub>SC</sub>",
        "spec_type": "max_rating",
        "column_model": "MAX_ONLY",
        "engineering_class": "SAFETY_LIMIT",
        "special_semantics": "NONE",
        "llm_context": {
          "formal_name": "Output Short Circuit Duration",
          "aliases": ["t_SC [s] – Output Short Circuit Duration (Max.)", "Short Circuit Duration t_SC [s] (Output, Indefinite)", "Output Short Time t_SC [s] Max. (Cont. or Limited)", "t_SC – Short Circuit at Output (Indefinite / 10s)", "Output Short-Circuit Duration [s] (Indefinite OK)", "t(SC) [s] – Max. Time with V_OUT Shorted to GND", "Short Circuit Time [s] (Output Tolerance: Cont.)", "t_SC Max. [s] – Continuous or Timed Short Circuit", "Output Short Duration t_SC (Indefinite / t=10s)", "Max. Short-Circuit Duration t_SC [s] – Output Pin"]
        },
        "possible_units": ["s"],
        "std_unit": "s",
        "scenarios": [
          {
            "condition": "Continuous",
            "limits": {
              "General_Purpose": ["Indefinite"],
              "Precision_Zero_Drift": ["Indefinite", "10"],
              "High_Speed": ["Indefinite", "10"]
            }
          }
        ]
      },
      {
        "key": "power_dissipation",
        "symbol": "P<sub>D</sub>",
        "spec_type": "max_rating",
        "column_model": "MAX_ONLY",
        "engineering_class": "SAFETY_LIMIT",
        "special_semantics": "NONE",
        "llm_context": {
          "formal_name": "Maximum Power Dissipation",
          "aliases": ["P_D [mW/W] Max. – Power Dissipation", "Power Dissipation P_D [mW] Max.", "Max Power P_D [mW] (See Derating)", "P_D [mW] Abs. Max. (Derate Above)", "Total Dissipation P_D [W] Max.", "P_D(max) [mW] (Derate to T_J(max))", "P_D Abs. Max. [mW] (Fig. X Derating)", "P_tot [mW] Max. (Derate Linearly)"]
        },
        "possible_units": ["mW", "W"],
        "std_unit": "mW",
        "scenarios": [
          {
            "condition": "Ta=25°C",
            "limits": {
              "General_Purpose": [500, 625, 1000, 1250],
              "Precision_Zero_Drift": [300, 500, 625],
              "High_Speed": [500, 1000, 1500]
            }
          }
        ]
      },
      {
        "key": "junction_temperature",
        "symbol": "T<sub>J</sub>",
        "spec_type": "max_rating",
        "column_model": "MAX_ONLY",
        "engineering_class": "SAFETY_LIMIT",
        "special_semantics": "NONE",
        "llm_context": {
          "formal_name": "Maximum Junction Temperature",
          "aliases": ["T_J [°C] Max. – Maximum Junction Temperature", "Max Junction Temp. T_J [°C] (Abs. Max.)", "Tj Max [°C] – Internal Die Temperature Limit", "T_J Max. [°C] (Do Not Exceed, All Conditions)", "T_J(max) [°C] – Absolute Max. Junction Temp.", "Max. T_J [°C] (Abs. Max., Continuous Operation)", "T_JMAX [°C] – Upper Junction Temp. Limit", "Tj [°C] Max. (Per Thermal Model, Abs.)", "Junction Temp. Limit T_J [°C] Max. (Abs.)", "T_J [°C] Abs. Max. (Die Temperature, All Cond.)"]
        },
        "possible_units": ["°C"],
        "std_unit": "°C",
        "scenarios": [
          {
            "condition": "Max",
            "limits": {
              "General_Purpose": [125, 150],
              "Precision_Zero_Drift": [125, 150],
              "High_Speed": [125, 150]
            }
          }
        ]
      },
      {
        "key": "storage_temperature",
        "symbol": "T<sub>STG</sub>",
        "spec_type": "max_rating",
        "column_model": "MIN_MAX",
        "engineering_class": "SAFETY_LIMIT",
        "special_semantics": "NONE",
        "llm_context": {
          "formal_name": "Storage Temperature Range",
          "aliases": ["T_STG [°C] Storage Range (Min. to Max.)", "Storage Temperature T_STG [°C] (Non-Operating)", "T_stg [°C] Range – Non-Op. Storage", "T_STG [°C] (Unpowered)", "Storage Temp. T_STG [°C] Min. Max. (Non-Op.)", "T_STORAGE [°C] (Non-Operating, Device Off)", "Non-Op. Storage T_STG [°C] Min–Max (Unpowered)", "T_STG [°C] – Component Storage Range", "Storage Temperature [°C] Min. Max. T_STG"]
        },
        "possible_units": ["°C"],
        "std_unit": "°C",
        "scenarios": [
          {
            "condition": "Min to Max",
            "limits": {
              "General_Purpose": ["-65 to 150"],
              "Precision_Zero_Drift": ["-65 to 150"],
              "High_Speed": ["-65 to 150"]
            }
          }
        ]
      },
      {
        "key": "esd_rating",
        "symbol": "V<sub>ESD</sub>",
        "spec_type": "max_rating",
        "column_model": "MIN_ONLY",
        "engineering_class": "SAFETY_LIMIT",
        "special_semantics": "NONE",
        "llm_context": {
          "formal_name": "ESD Rating",
          "aliases": ["V_ESD [kV] Min. – ESD Rating (HBM)", "Electrostatic Discharge V_ESD [kV] (HBM, Min.)", "ESD HBM [kV] Min. (ANSI/ESDA/JEDEC JS-001)", "ESD Rating V_ESD [kV] (Human Body Model)", "V_ESD [kV] – HBM ESD (All Pins, Min.)", "ESD HBM Class [kV] – Per JEDEC JESD22-A114", "V(ESD) HBM [kV] Min. (All Pins to GND)", "ESD Rating [kV] Min. (Human Body Model, HBM)", "HBM ESD V_ESD [kV] Min. (Per JS-001)"]
        },
        "possible_units": ["kV"],
        "std_unit": "kV",
        "scenarios": [
          {
            "condition": "Human Body Model",
            "limits": {
              "General_Purpose": [1, 2, 4],
              "Precision_Zero_Drift": [2, 4],
              "High_Speed": [1, 2]
            }
          }
        ]
      },
      {
        "key": "lead_temperature",
        "symbol": "T<sub>LEAD</sub>",
        "spec_type": "max_rating",
        "column_model": "MAX_ONLY",
        "engineering_class": "SAFETY_LIMIT",
        "special_semantics": "NONE",
        "llm_context": {
          "formal_name": "Lead Temperature (Soldering)",
          "aliases": ["T_LEAD [°C] Max. – Lead Temp. (Soldering)", "Soldering Temperature T_sol [°C] Max.", "Lead Temp [°C] Max. – Solder Point", "T_LEAD [°C] Max. (Wave/Iron Soldering)", "Lead Temp. (Soldering) [°C] Max.", "T_LEAD Max. [°C] – Iron/Wave Solder", "T_S(solder) [°C] Max. (Iron or Wave)", "Lead Temp. (Solder Point) [°C] Max.", "Reflow / Hand Solder Peak T_LEAD [°C] Max."]
        },
        "possible_units": ["°C"],
        "std_unit": "°C",
        "scenarios": [
          {
            "condition": "10 seconds",
            "limits": {
              "General_Purpose": [260, 300],
              "Precision_Zero_Drift": [260, 300],
              "High_Speed": [260, 300]
            }
          }
        ]
      }
    ],

    "ELEC_CHAR": [
      {
        "key": "supply_voltage_range",
        "symbol": "V<sub>S</sub>",
        "spec_type": "nominal",
        "column_model": "MIN_MAX",
        "engineering_class": "NOMINAL_PARAMETER",
        "special_semantics": "NONE",
        "llm_context": {
          "formal_name": "Operating Supply Voltage Range",
          "aliases": ["V_S [V] Operating Range (Single/Dual Supply)", "Supply Voltage Range V_S [V] (Min. to Max.)", "Operating Voltage V_S [V] (Single or Dual, Range)", "V_S [V] Min./Max. (Single Supply or ±Dual)", "Supply Range [V] V_S (Operating, All Conditions)", "V_CC [V] Range (Single-Supply Operating, Min–Max)", "V_S [V] (Single: Min to Max; Dual: ±Min to ±Max)", "Operating Supply [V] V_S (Single/Dual, Full Spec.)", "V_S Range [V] (Min/Max, Guaranteed Operation)", "Supply Voltage V_S [V] Operating (Min. to Max.)"]
        },
        "possible_units": ["V"],
        "std_unit": "V",
        "scenarios": [
          {
            "condition": "Single Supply",
            "limits": {
              "General_Purpose": ["3 to 32", "5 to 36"],
              "Precision_Zero_Drift": ["1.8 to 5.5", "2.7 to 5.5", "4.5 to 12"],
              "High_Speed": ["2.7 to 5.5", "4.5 to 12"]
            }
          },
          {
            "condition": "Dual Supply",
            "limits": {
              "General_Purpose": ["±1.5 to ±16", "±2.5 to ±18"],
              "Precision_Zero_Drift": ["±0.9 to ±2.75", "±2.25 to ±6"],
              "High_Speed": ["±1.35 to ±2.75", "±2.25 to ±6"]
            }
          }
        ]
      },
      {
        "key": "offset_voltage",
        "symbol": "V<sub>OS</sub>",
        "spec_type": "max_limit",
        "column_model": "TYP_MAX",
        "engineering_class": "PERFORMANCE_LIMIT",
        "special_semantics": "NONE",
        "llm_context": {
          "formal_name": "Input Offset Voltage",
          "aliases": ["V_OS [µV/mV] Typ./Max. – Input Offset Voltage", "Input Offset Voltage V_OS [µV] Max.", "Vos [mV] Typ./Max. – Input Offset", "Offset Voltage V_OS [µV] Max.", "V_OS [µV] Typ. Max. (Excl. Temp. Drift)", "Input Offset V_OS [mV] Max. (Initial)", "V(OS) [µV] Typ./Max. – Input Referred Offset", "Initial V_OS [mV] Max. (No Trim)", "Offset Voltage [µV] V_OS Typ./Max. (DC)"]
        },
        "possible_units": ["µV", "mV"],
        "std_unit": "µV",
        "scenarios": [
          {
            "condition": "25°C",
            "limits": {
              "General_Purpose": [500, 1000, 2000, 5000, 7000],
              "Precision_Zero_Drift": [1, 5, 10, 25, 50, 100],
              "High_Speed": [200, 500, 1000, 3000, 5000]
            }
          },
          {
            "condition": "Over temperature",
            "limits": {
              "General_Purpose": [1000, 3000, 6000],
              "Precision_Zero_Drift": [5, 15, 50, 150],
              "High_Speed": [500, 2000, 4000]
            }
          }
        ]
      },
      {
        "key": "offset_drift",
        "symbol": "ΔV<sub>OS</sub>/ΔT",
        "spec_type": "max_limit",
        "column_model": "TYP_MAX",
        "engineering_class": "PERFORMANCE_LIMIT",
        "special_semantics": "NONE",
        "llm_context": {
          "formal_name": "Input Offset Voltage Drift",
          "aliases": ["ΔV_OS/ΔT [µV/°C] Typ./Max. – Offset Voltage Drift", "Offset Voltage Drift [nV/°C] Typ./Max.", "TCV ΔV_OS/ΔT [µV/°C] – Temp. Coeff. of V_OS", "Temp Coeff of Vos [µV/°C] Typ./Max. (Drift)", "ΔV_OS/ΔT [nV/°C] Typ. (Over Temp. Range)", "V_OS Drift [µV/°C] Typ./Max. (TC_VOS)", "Offset Drift ΔV_OS/T [nV/°C] Typ. Max.", "TCV [µV/°C] – Input Offset Temp. Coefficient", "V_OS TC [nV/°C] Typ./Max.", "ΔV_OS/ΔT Typ. Max. [µV/°C] – Offset Tempco"]
        },
        "possible_units": ["µV/°C", "nV/°C"],
        "std_unit": "µV/°C",
        "scenarios": [
          {
            "condition": "Typical",
            "limits": {
              "General_Purpose": [1, 5, 10, 15, 20, 30],
              "Precision_Zero_Drift": [0.005, 0.01, 0.02, 0.05, 0.1],
              "High_Speed": [0.5, 1, 2, 5, 10]
            }
          }
        ]
      },
      {
        "key": "input_bias_current",
        "symbol": "I<sub>B</sub>",
        "spec_type": "max_limit",
        "column_model": "TYP_MAX",
        "engineering_class": "PERFORMANCE_LIMIT",
        "special_semantics": "NONE",
        "llm_context": {
          "formal_name": "Input Bias Current",
          "aliases": ["I_B [pA/nA/µA] Typ./Max. – Input Bias Current", "Input Bias Current I_B [nA] Max.", "Bias Current IB [pA] Typ./Max. (Both Inputs)", "I_B [nA] Typ. Max. (Average of I_B+ and I_B-)", "I_BIAS [nA] Max. – Input Pin Bias", "I_B Typ./Max. [pA] (Input Terminal)", "Input Bias I_B [nA] Max. (= (I_B+ + I_B-)/2)", "I(B) [pA] Typ. Max. – Both Input Terminals", "Bias Current [nA] I_B Typ./Max. (Input Pins)"]
        },
        "possible_units": ["pA", "nA", "µA"],
        "std_unit": "nA",
        "scenarios": [
          {
            "condition": "25°C",
            "limits": {
              "General_Purpose": [3, 20, 45, 50, 80, 100, 200, 500],
              "Precision_Zero_Drift": [0.001, 0.005, 0.01, 0.1, 0.5, 1, 5],
              "High_Speed": [0.1, 1, 5, 10, 50, 100]
            }
          },
          {
            "condition": "Over temperature",
            "limits": {
              "General_Purpose": [10, 50, 100, 300, 800],
              "Precision_Zero_Drift": [0.01, 0.1, 1, 10],
              "High_Speed": [1, 10, 50, 200]
            }
          }
        ]
      },
      {
        "key": "input_offset_current",
        "symbol": "I<sub>OS</sub>",
        "spec_type": "max_limit",
        "column_model": "TYP_MAX",
        "engineering_class": "PERFORMANCE_LIMIT",
        "special_semantics": "NONE",
        "llm_context": {
          "formal_name": "Input Offset Current",
          "aliases": ["I_OS [pA/nA] Typ./Max. – Input Offset Current", "Input Offset Current I_OS [nA] Max.", "Offset Current IOS [pA] Typ./Max.", "I_OS [nA] Typ. Max. (= |I_B+ - I_B-|)", "I_OFFSET [pA] Max. – Input Current Mismatch", "I_OS Typ./Max. [pA] (Diff. of Input Bias)", "Input Offset I_OS [nA] Max. (|I_B+ minus I_B-|)", "I(OS) [pA] Typ. Max. – Input Offset (Mismatch)", "Offset Current [pA] I_OS Typ./Max. (Input Pins)"]
        },
        "possible_units": ["pA", "nA"],
        "std_unit": "nA",
        "scenarios": [
          {
            "condition": "25°C",
            "limits": {
              "General_Purpose": [0.5, 3, 5, 10, 20, 50, 100],
              "Precision_Zero_Drift": [0.001, 0.005, 0.01, 0.1, 0.5, 2],
              "High_Speed": [0.1, 1, 5, 10, 20]
            }
          }
        ]
      },
      {
        "key": "input_impedance_diff",
        "symbol": "Z<sub>ID</sub>",
        "spec_type": "min_limit",
        "column_model": "MIN_TYP",
        "engineering_class": "PERFORMANCE_LIMIT",
        "special_semantics": "NONE",
        "llm_context": {
          "formal_name": "Differential Input Impedance",
          "aliases": ["Z_ID [MΩ/GΩ] Min./Typ. – Differential Input Impedance", "Input Impedance Z_ID [MΩ] Typ. (Differential)", "Differential Input Z Z_ID [GΩ] Min./Typ.", "Z_ID [MΩ] – Diff. Input Impedance (V+ to V-)", "Diff. Input Z [MΩ] Typ./Min. (Between Inputs)", "Z_IN(diff) [GΩ] Typ. – Differential Mode Z", "Input Impedance [MΩ] Z_ID (V(+) to V(-), Typ.)", "Z_ID Typ. [GΩ] – Differential Input Resistance", "Differential Z_ID [MΩ] Min. Typ. (DC, Typ.)", "Z(ID) [GΩ] Typ. – Input Diff. Impedance"]
        },
        "possible_units": ["MΩ", "GΩ"],
        "std_unit": "MΩ",
        "scenarios": [
          {
            "condition": "Typical",
            "limits": {
              "General_Purpose": [1, 10, 100, 1000],
              "Precision_Zero_Drift": [100, 1000, 10000],
              "High_Speed": [1, 10, 100]
            }
          }
        ]
      },
      {
        "key": "input_impedance_common",
        "symbol": "Z<sub>IC</sub>",
        "spec_type": "min_limit",
        "column_model": "MIN_TYP",
        "engineering_class": "PERFORMANCE_LIMIT",
        "special_semantics": "NONE",
        "llm_context": {
          "formal_name": "Common-Mode Input Impedance",
          "aliases": ["Z_IC [MΩ/GΩ] Min./Typ. – Common-Mode Input Impedance", "Common Mode Input Z Z_IC [GΩ] Typ.", "Input Z CM Z_IC [MΩ] Min./Typ.", "Z_IC [MΩ] – CM Input Impedance (Each Input to GND)", "Common-Mode Z_IN [GΩ] Typ. (Input to Ground)", "Z_IN(cm) [MΩ] Typ. – Common Mode Input Impedance", "Input Impedance CM [GΩ] Z_IC (Each Pin to GND)", "Z_IC Typ. [MΩ] – Common-Mode Input Z", "Common Mode Z [GΩ] Min. Typ. (Input Pin to GND)", "Z(IC) [MΩ] Typ. – CM Input Impedance (Shunt)"]
        },
        "possible_units": ["MΩ", "GΩ"],
        "std_unit": "MΩ",
        "scenarios": [
          {
            "condition": "Typical",
            "limits": {
              "General_Purpose": [100, 1000, 10000],
              "Precision_Zero_Drift": [1000, 10000],
              "High_Speed": [100, 1000]
            }
          }
        ]
      },
      {
        "key": "input_capacitance",
        "symbol": "C<sub>IN</sub>",
        "spec_type": "nominal",
        "column_model": "TYP_ONLY",
        "engineering_class": "NOMINAL_PARAMETER",
        "special_semantics": "NONE",
        "llm_context": {
          "formal_name": "Input Capacitance",
          "aliases": ["C_IN [pF] Typ. – Input Capacitance", "Input Cap C_IN [pF] Typ. (Differential or CM)", "Cin [pF] Typ. – Input Shunt Capacitance", "C_IN [pF] Typ. (Input Pin to GND, Parasitic)", "Input Capacitance [pF] C_IN (Typ., Diff. Mode)", "C_IN Typ. [pF] – Differential Input Cap.", "Input Cap. C_IN [pF] (Typ., Between Inputs)", "C(IN) [pF] Typ. – Input Shunt Capacitance", "C_IN [pF] Typ. (Input; Affects Noise Gain Roll-Off)", "Input Capacitance Cin [pF] Typ. (Common/Diff.)"]
        },
        "possible_units": ["pF"],
        "std_unit": "pF",
        "scenarios": [
          {
            "condition": "Typical",
            "limits": {
              "General_Purpose": [1, 2, 3, 5, 8],
              "Precision_Zero_Drift": [2, 5, 10],
              "High_Speed": [1, 2, 3, 5]
            }
          }
        ]
      },
      {
        "key": "cmrr",
        "symbol": "CMRR",
        "spec_type": "min_limit",
        "column_model": "MIN_TYP",
        "engineering_class": "PERFORMANCE_LIMIT",
        "special_semantics": "NONE",
        "llm_context": {
          "formal_name": "Common Mode Rejection Ratio",
          "aliases": ["CMRR [dB] Min./Typ. – Common Mode Rejection Ratio", "Common Mode Rejection CMRR [dB] (DC, Min.)", "CMRR [dB] Min. Typ.", "CMR [dB] – CMRR (Min., DC)", "CMRR Min. [dB] (DC; ΔV_OS / ΔV_CM)", "Common-Mode Rejection [dB] CMRR (Min., DC)", "CMRR [dB] Typ./Min. (At DC; See CMRR vs. Freq.)", "CMR Ratio [dB] Min. Typ.", "Common Mode Rejection Ratio [dB] CMRR (DC)"]
        },
        "possible_units": ["dB"],
        "std_unit": "dB",
        "scenarios": [
          {
            "condition": "DC",
            "limits": {
              "General_Purpose": [70, 80, 90, 100, 110],
              "Precision_Zero_Drift": [100, 110, 120, 130, 140, 160],
              "High_Speed": [65, 70, 80, 90]
            }
          },
          {
            "condition": "At 60Hz",
            "limits": {
              "General_Purpose": [70, 80, 90],
              "Precision_Zero_Drift": [90, 100, 120],
              "High_Speed": [60, 70, 80]
            }
          }
        ]
      },
      {
        "key": "psrr",
        "symbol": "PSRR",
        "spec_type": "min_limit",
        "column_model": "MIN_TYP",
        "engineering_class": "PERFORMANCE_LIMIT",
        "special_semantics": "NONE",
        "llm_context": {
          "formal_name": "Power Supply Rejection Ratio",
          "aliases": ["PSRR [dB] Min./Typ. – Power Supply Rejection Ratio", "Supply Rejection Ratio PSRR [dB] (DC, Min.)", "SVRR [dB] Min. Typ. – Supply Voltage Rejection", "PSRR [dB] Min. (DC; ΔV_OS/ΔV_S)", "Power Supply Rejection PSRR [dB] (Min., DC)", "PSR [dB] Typ./Min. (DC)", "PSRR [dB] Min. Typ. (At DC; See PSRR vs. Freq.)", "Supply Rejection [dB] PSRR Min.", "PSRR Min. [dB] (DC; Both Rails, V+ and V-)", "Power Supply Rejection [dB] PSRR (DC, Min.)"]
        },
        "possible_units": ["dB"],
        "std_unit": "dB",
        "scenarios": [
          {
            "condition": "DC, V+ or V-",
            "limits": {
              "General_Purpose": [70, 80, 90, 100, 110],
              "Precision_Zero_Drift": [100, 110, 120, 130, 140],
              "High_Speed": [60, 70, 80, 90]
            }
          },
          {
            "condition": "At 60Hz",
            "limits": {
              "General_Purpose": [70, 80, 90],
              "Precision_Zero_Drift": [90, 100, 110],
              "High_Speed": [60, 70, 80]
            }
          }
        ]
      },
      {
        "key": "open_loop_gain",
        "symbol": "A<sub>OL</sub>",
        "spec_type": "min_limit",
        "column_model": "MIN_TYP",
        "engineering_class": "PERFORMANCE_LIMIT",
        "special_semantics": "NONE",
        "llm_context": {
          "formal_name": "Open Loop Voltage Gain",
          "aliases": ["A_OL [dB/V·mV⁻¹] Min./Typ. – Open Loop Gain", "Open Loop Gain A_OL [dB] Min.", "Large Signal Voltage Gain A_OL [V/mV] (DC)", "AOL [dB] Min. Typ.", "A_OL [dB] – DC Open-Loop Gain (Min.)", "Open-Loop Voltage Gain [dB] A_OL (DC, Min.)", "A_V(OL) [dB] Min. Typ. (DC; ΔV_OUT/ΔV_IN)", "A_OL [V/mV] Min. (= V_OUT Swing / V_ID, DC)", "A_OL Typ. Min. [dB] – DC Open-Loop"]
        },
        "possible_units": ["dB", "V/mV"],
        "std_unit": "dB",
        "scenarios": [
          {
            "condition": "DC, RL=2kΩ",
            "limits": {
              "General_Purpose": [90, 100, 106, 110, 120],
              "Precision_Zero_Drift": [110, 120, 130, 140, 160],
              "High_Speed": [80, 90, 100, 110]
            }
          },
          {
            "condition": "DC, RL=10kΩ",
            "limits": {
              "General_Purpose": [100, 110, 120],
              "Precision_Zero_Drift": [120, 130, 140],
              "High_Speed": [90, 100, 110]
            }
          }
        ]
      },
      {
        "key": "gbw",
        "symbol": "GBW",
        "spec_type": "nominal",
        "column_model": "MIN_TYP_MAX",
        "engineering_class": "NOMINAL_PARAMETER",
        "special_semantics": "NONE",
        "llm_context": {
          "formal_name": "Gain Bandwidth Product",
          "aliases": ["GBW [MHz/kHz/GHz] Typ. – Gain Bandwidth Product", "Gain Bandwidth GBW [MHz] Min./Typ./Max.", "Unity Gain Bandwidth GBW [MHz] (Typ.)", "GBW [MHz] Typ. – Unity-Gain Frequency (0dB)", "Gain-Bandwidth Product [MHz] GBW (Typ.)", "GBP [MHz] Typ. – GBW (f at |A_OL|=0dB)", "GBW Typ. [GHz] – Unity-Gain BW (High-Speed)", "Unity Gain Freq. f_u [MHz] GBW (Typ.)", "GBW [MHz] Min. Typ. Max. (See A_OL vs. Freq.)", "Gain Bandwidth GBW [MHz] (= A_OL × f_–3dB)"]
        },
        "possible_units": ["kHz", "MHz", "GHz"],
        "std_unit": "MHz",
        "scenarios": [
          {
            "condition": "Standard",
            "limits": {
              "General_Purpose": [0.5, 1, 1.2, 3, 4, 10, 18],
              "Precision_Zero_Drift": [0.05, 0.1, 0.5, 1, 2, 5, 10],
              "High_Speed": [10, 50, 100, 200, 500, 1000, 2000, 5000]
            }
          }
        ]
      },
      {
        "key": "phase_margin",
        "symbol": "φ<sub>M</sub>",
        "spec_type": "min_limit",
        "column_model": "MIN_TYP",
        "engineering_class": "PERFORMANCE_LIMIT",
        "special_semantics": "NONE",
        "llm_context": {
          "formal_name": "Phase Margin",
          "aliases": ["φ_M [°] Min./Typ. – Phase Margin (Unity Gain)", "Phase Margin PM [deg] Min. (Unity Gain, G=1)", "φ_M [°] Min. Typ. (G=1)", "PM [deg] Min. – Stability (Phase, At f_u)", "Phase Margin φ_M [°] (Min., Unity Gain Config.)", "φ(M) [°] Typ. Min. (Bode Plot, G=1)", "Phase Margin [°] PM (Min./Typ., Unity Gain)", "φ_M Typ. [°] – Guaranteed Stability (G=1)", "PM [°] Min. Typ. (Measured at GBW Frequency)", "Phase Margin [deg] Typ. Min. (Unity-Gain)"]
        },
        "possible_units": ["deg", "°"],
        "std_unit": "deg",
        "scenarios": [
          {
            "condition": "Unity gain",
            "limits": {
              "General_Purpose": [45, 60, 65, 70],
              "Precision_Zero_Drift": [45, 60, 70],
              "High_Speed": [45, 50, 60]
            }
          }
        ]
      },
      {
        "key": "gain_margin",
        "symbol": "GM",
        "spec_type": "min_limit",
        "column_model": "MIN_TYP",
        "engineering_class": "PERFORMANCE_LIMIT",
        "special_semantics": "NONE",
        "llm_context": {
          "formal_name": "Gain Margin",
          "aliases": ["GM [dB] Min./Typ. – Gain Margin (Unity Gain)", "Gain Margin GM [dB] Min. (G=1, Phase Crossover)", "GM [dB] Typ. Min. (At Phase = -180°, G=1)", "Gain Margin [dB] Min. Typ. (Unity Gain Config.)", "GM [dB] – Gain at Phase = -180° (Min.)", "Gain Margin G_M [dB] Min. (Loop Stability)", "GM Typ. [dB] – Gain Margin (Phase Crossover f)", "G_M [dB] Min. Typ. (Unity Gain, Stability)", "Gain Margin [dB] Min. (G=1, Bode Analysis)", "GM [dB] Typ. Min. (Loop Stability, G=1)"]
        },
        "possible_units": ["dB"],
        "std_unit": "dB",
        "scenarios": [
          {
            "condition": "Unity gain",
            "limits": {
              "General_Purpose": [10, 12, 15],
              "Precision_Zero_Drift": [10, 15],
              "High_Speed": [10, 12]
            }
          }
        ]
      },
      {
        "key": "slew_rate",
        "symbol": "SR",
        "spec_type": "min_limit",
        "column_model": "MIN_TYP",
        "engineering_class": "PERFORMANCE_LIMIT",
        "special_semantics": "NONE",
        "llm_context": {
          "formal_name": "Slew Rate",
          "aliases": ["SR [V/µs] Min./Typ. – Slew Rate (Unity Gain)", "Slew Rate SR [V/µs] Min. (Rising, G=1)", "SR [V/µs] – Output Slew (Rising / Falling, G=1)", "SR Min. [V/µs] (Unity Gain, Rising or Falling)", "Slew Rate [V/µs] Min. Typ. (G=1, Large Signal)", "SR [V/µs] Typ. Min. (dV_OUT/dt, Unity Gain)", "Slew Rate SR [V/µs] – Rising/Falling (Min.)", "Output Slew [V/µs] SR Typ. Min. (G=1)", "Slew Rate [V/µs] SR Typ./Min. (Rising, G=+1)"]
        },
        "possible_units": ["V/µs", "V/ms"],
        "std_unit": "V/µs",
        "scenarios": [
          {
            "condition": "Unity Gain, Rising",
            "limits": {
              "General_Purpose": [0.3, 0.5, 0.6, 1, 3, 10, 13],
              "Precision_Zero_Drift": [0.01, 0.05, 0.1, 0.5, 1, 2],
              "High_Speed": [10, 50, 100, 300, 500, 1000, 2000, 5000]
            }
          },
          {
            "condition": "Unity Gain, Falling",
            "limits": {
              "General_Purpose": [0.3, 0.5, 0.6, 1, 3, 10],
              "Precision_Zero_Drift": [0.01, 0.05, 0.1, 0.5, 1],
              "High_Speed": [10, 50, 100, 300, 500, 1000, 2000]
            }
          }
        ]
      },
      {
        "key": "settling_time",
        "symbol": "t<sub>S</sub>",
        "spec_type": "max_limit",
        "column_model": "TYP_MAX",
        "engineering_class": "PERFORMANCE_LIMIT",
        "special_semantics": "NONE",
        "llm_context": {
          "formal_name": "Settling Time",
          "aliases": ["t_S [µs/ns] Typ./Max. – Settling Time", "Settling Time t_S [µs] Max. (To 0.1%, G=1)", "tS [ns] Typ./Max. – V_OUT Settle (0.1% / 0.01%)", "t_S [µs] Max. (G=1, Step Input, To 0.1%)", "Settling Time [µs] t_S (To 0.1% or 0.01%)", "t_SETTLING [ns] Typ./Max. – To Final ±0.1%", "t_S [ns] Max. (Step → Within ±0.1% of Final)", "t(S) [ns] Typ. Max. – Settle to 0.1% Band", "Output Settling t_S [µs] Max. (To 0.1%, G=1)"]
        },
        "possible_units": ["ns", "µs"],
        "std_unit": "µs",
        "scenarios": [
          {
            "condition": "To 0.1%, G=1",
            "limits": {
              "General_Purpose": [1, 5, 10, 20],
              "Precision_Zero_Drift": [10, 50, 100],
              "High_Speed": [0.05, 0.1, 0.5, 1]
            }
          },
          {
            "condition": "To 0.01%, G=1",
            "limits": {
              "General_Purpose": [5, 10, 30],
              "Precision_Zero_Drift": [50, 100, 200],
              "High_Speed": [0.1, 0.5, 1, 2]
            }
          }
        ]
      },
      {
        "key": "rise_time",
        "symbol": "t<sub>R</sub>",
        "spec_type": "max_limit",
        "column_model": "TYP_MAX",
        "engineering_class": "PERFORMANCE_LIMIT",
        "special_semantics": "NONE",
        "llm_context": {
          "formal_name": "Rise Time",
          "aliases": ["t_R [ns/µs] Typ./Max. – Rise Time (10% to 90%)", "Rise Time t_R [ns] Max. (10% to 90%, G=1)", "tR [ns] Typ./Max. – Output Rise (10→90%)", "t_R [ns] Max. (Small Signal, 10% to 90%)", "Rise Time [ns] t_R (10% to 90%, Resistive Load)", "t_RISE [ns] Typ./Max. – V_OUT Rise (10→90%)", "Output Rise Time t_R [ns] (10–90%, Max.)", "t(R) [ns] Typ. Max. – 10% to 90% Output Rise", "Rise Time [ns] Max. t_R (G=1, Small Signal)"]
        },
        "possible_units": ["ns", "µs"],
        "std_unit": "ns",
        "scenarios": [
          {
            "condition": "10% to 90%",
            "limits": {
              "General_Purpose": [100, 300, 500, 1000],
              "Precision_Zero_Drift": [500, 1000, 5000],
              "High_Speed": [1, 5, 10, 50]
            }
          }
        ]
      },
      {
        "key": "overshoot",
        "symbol": "OS",
        "spec_type": "max_limit",
        "column_model": "TYP_MAX",
        "engineering_class": "PERFORMANCE_LIMIT",
        "special_semantics": "NONE",
        "llm_context": {
          "formal_name": "Overshoot",
          "aliases": ["OS [%] Typ./Max. – Overshoot (Unity Gain)", "Overshoot [%] Max. (G=1, Step Input)", "OS [%] Typ. Max. – V_OUT Overshoot (G=1)", "Output Overshoot [%] OS (Unity Gain, Step)", "OS Typ./Max. [%] – Overshoot (G=1)", "Overshoot OS [%] Max. (G=+1, Resistive Load)", "% Overshoot [%] Typ. Max. (Step, G=1)", "OS [%] – Output Ringing / Overshoot (G=1)", "Output Overshoot OS [%] Max. (Unity Gain)"]
        },
        "possible_units": ["%"],
        "std_unit": "%",
        "scenarios": [
          {
            "condition": "Unity gain",
            "limits": {
              "General_Purpose": [5, 10, 20],
              "Precision_Zero_Drift": [5, 10],
              "High_Speed": [10, 20, 30]
            }
          }
        ]
      },
      {
        "key": "supply_current",
        "symbol": "I<sub>SY</sub>",
        "spec_type": "max_limit",
        "column_model": "TYP_MAX",
        "engineering_class": "PERFORMANCE_LIMIT",
        "special_semantics": "NONE",
        "llm_context": {
          "formal_name": "Supply Current per Amplifier",
          "aliases": ["I_SY [µA/mA] Typ./Max. – Supply Current per Amp", "Supply Current I_SY [mA] Typ./Max. (No Load)", "Quiescent Current per Amp I_SY [µA] (No Load)", "I_Q [µA] Typ./Max. – Quiescent per Amplifier", "I_SY [mA] – Supply Current (Per Channel, No Load)", "Supply Current per Channel I_SY [µA] Max.", "Supply Current [mA] I_SY (Typ., Per Amplifier)"]
        },
        "possible_units": ["µA", "mA"],
        "std_unit": "mA",
        "scenarios": [
          {
            "condition": "No load, VS=5V",
            "limits": {
              "General_Purpose": [0.03, 0.05, 0.3, 0.7, 1, 1.4, 3, 5],
              "Precision_Zero_Drift": [0.045, 0.5, 0.8, 1, 1.7, 2, 3],
              "High_Speed": [2, 5, 7, 10, 15, 20, 25]
            }
          }
        ]
      },
      {
        "key": "shutdown_current",
        "symbol": "I<sub>SD</sub>",
        "spec_type": "max_limit",
        "column_model": "TYP_MAX",
        "engineering_class": "PERFORMANCE_LIMIT",
        "special_semantics": "NONE",
        "llm_context": {
          "formal_name": "Shutdown Supply Current",
          "aliases": ["I_SD [nA/µA] Typ./Max. – Shutdown Supply Current", "Shutdown Current I_SD [µA] Max. (SD Mode)", "ISD [µA] Typ./Max. (Device in Shutdown Mode)", "I_SD [nA] Max. – Current in Shutdown State", "Standby / Shutdown I_SD [µA] Max. (SD=Active)", "Shutdown Mode Current I_SD [µA] Typ./Max.", "I_SD Typ. Max. [nA] (Output Hi-Z)", "Supply Current in Shutdown I_SD [µA] Max.", "I(SD) [µA] Typ. Max. – Shutdown Quiescent"]
        },
        "possible_units": ["nA", "µA"],
        "std_unit": "µA",
        "scenarios": [
          {
            "condition": "Shutdown mode",
            "limits":{
            "General_Purpose": [1, 5, 10],
            "Precision_Zero_Drift": [0.1, 1, 2],
            "High_Speed": [10, 50, 100, 500]
          }
        }
      ]
    },
    {
      "key": "output_voltage_swing_high",
      "symbol": "V<sub>OH</sub>",
      "spec_type": "min_limit",
      "column_model": "MIN_TYP",
      "engineering_class": "PERFORMANCE_LIMIT",
      "special_semantics": "RAIL_TO_RAIL",
      "llm_context": {
        "formal_name": "High Level Output Voltage",
        "aliases": ["V_OH [V/mV] Min./Typ. – High Output Voltage", "Output Voltage Swing High V_OH [mV from V+] (Min.)", "VOH [V] Typ. – Max. Output Voltage (V+ - V_OH)", "V_OH [mV] Min. (Headroom from V+)", "Maximum Output Voltage V_OH [V] (Typ.)", "V_OH (V+ - V_OUT) [mV] Min. (Rail-to-Rail Output)", "Output High V_OH [mV from rail] (Min.)", "V_OH Min. [mV] – Swing from V+", "High-Level Output V_OH [V] Typ./Min.", "V(OH) [mV] Typ. Min. – V+ Rail Headroom"]
      },
      "possible_units": ["V", "mV"],
      "std_unit": "mV",
      "scenarios": [
        {
          "condition": "Output swing from positive rail (V+ - VOH), RL=10kΩ",
          "limits": {
            "General_Purpose": [1000, 1500, 2000],
            "Precision_Zero_Drift": [5, 10, 20, 50],
            "High_Speed": [100, 500, 1000, 1500]
          }
        }
      ]
    },
    {
      "key": "output_voltage_swing_low",
      "symbol": "V<sub>OL</sub>",
      "spec_type": "max_limit",
      "column_model": "TYP_MAX",
      "engineering_class": "PERFORMANCE_LIMIT",
      "special_semantics": "RAIL_TO_RAIL",
      "llm_context": {
        "formal_name": "Low Level Output Voltage",
        "aliases": ["V_OL [V/mV] Typ./Max. – Low Output Voltage", "Output Voltage Swing Low V_OL [mV from V-] (Max.)", "VOL [V] Typ. – Min. Output Voltage (V_OL - V-)", "V_OL [mV] Max. (Headroom from V-)", "Minimum Output Voltage V_OL [V] (Typ.)", "V_OL (V_OUT - V-) [mV] Max. (Rail-to-Rail Output)", "Output Low V_OL [mV from rail] (Max.)", "V_OL Max. [mV] – Swing from V-", "Low-Level Output V_OL [V] Typ./Max.", "V(OL) [mV] Typ. Max. – V- Rail Headroom"]
      },
      "possible_units": ["V", "mV"],
      "std_unit": "mV",
      "scenarios": [
        {
          "condition": "Output swing from negative rail (VOL - V-), RL=10kΩ",
          "limits": {
            "General_Purpose": [500, 1000, 1500],
            "Precision_Zero_Drift": [5, 10, 20, 50],
            "High_Speed": [100, 500, 1000]
          }
        }
      ]
    },
    {
      "key": "output_short_circuit_current",
      "symbol": "I<sub>SC</sub>",
      "spec_type": "min_limit",
      "column_model": "TYP_ONLY",
      "engineering_class": "PERFORMANCE_LIMIT",
      "special_semantics": "NONE",
      "llm_context": {
        "formal_name": "Output Short Circuit Current",
        "aliases": ["I_SC [mA] Typ. – Output Short Circuit Current", "Short Circuit Current I_SC [mA] (Sourcing/Sinking)", "Output Current Capability I_SC [mA] (Typ.)", "Iout [mA] – Short-Circuit Output Current (Typ.)", "I_SC [mA] (Source & Sink)", "Output Drive I_SC [mA] Typ. (Cont. Short Circuit)", "I_SC Typ. [mA] – Sustained Output Current", "Output Short-Circuit I_SC [mA] (Source/Sink, Typ.)", "I_OUT(SC) [mA] Typ. – Peak Output (Shorted)", "Short Circuit I_SC [mA] Typ."]
      },
      "possible_units": ["mA"],
      "std_unit": "mA",
      "scenarios": [
        {
          "condition": "Sourcing/Sinking",
          "limits": {
            "General_Purpose": [10, 20, 30, 40],
            "Precision_Zero_Drift": [10, 20, 30],
            "High_Speed": [50, 80, 100, 150, 200, 400]
          }
        }
      ]
    },
    {
      "key": "voltage_noise_density",
      "symbol": "e<sub>n</sub>",
      "spec_type": "max_limit",
      "column_model": "TYP_MAX",
      "engineering_class": "NOISE_PARAM",
      "special_semantics": "NONE",
      "llm_context": {
        "formal_name": "Input Voltage Noise Density",
        "aliases": ["e_n [nV/√Hz] Typ./Max. – Input Voltage Noise Density", "Voltage Noise e_n [nV/√Hz] Max.", "Input Noise Voltage Density e_n [nV/√Hz]", "Spot Noise e_n [nV/√Hz] Typ./Max.", "e_n [nV/√Hz] Typ. (Voltage Noise)", "Input Referred Noise e_n [nV/√Hz] (Typ.)", "Spot Voltage Noise [nV/√Hz] e_n (Max.)", "e_n [nV/√Hz] – Input Voltage Noise", "Noise Density e_n [nV/√Hz] Typ. Max.", "e(n) [nV/√Hz] Typ./Max. – Spot Noise"]
      },
      "possible_units": ["nV/√Hz"],
      "std_unit": "nV/√Hz",
      "scenarios": [
        {
          "condition": "f=1kHz",
          "limits": {
            "General_Purpose": [20, 30, 40, 50, 80],
            "Precision_Zero_Drift": [3, 5, 10, 15, 22],
            "High_Speed": [1, 2, 5, 8, 12]
          }
        }
      ]
    },
    {
      "key": "current_noise_density",
      "symbol": "i<sub>n</sub>",
      "spec_type": "max_limit",
      "column_model": "TYP_MAX",
      "engineering_class": "NOISE_PARAM",
      "special_semantics": "NONE",
      "llm_context": {
        "formal_name": "Input Current Noise Density",
        "aliases": ["i_n [fA/√Hz / pA/√Hz] Typ./Max. – Current Noise Density", "Current Noise i_n [pA/√Hz] Max.", "Input Noise Current Density i_n [fA/√Hz]", "i_n [fA/√Hz] Typ./Max. (Input Referred)", "Spot Current Noise i_n [pA/√Hz] (Typ.)", "Input Current Noise [fA/√Hz] i_n", "i_n [pA/√Hz] – Input Current Noise Density", "Noise Current Density i_n [fA/√Hz] (Max.)", "i(n) [fA/√Hz] Typ./Max. – Spot Current Noise", "Input Referred Current Noise i_n [pA/√Hz]"]
      },
      "possible_units": ["fA/√Hz", "pA/√Hz"],
      "std_unit": "fA/√Hz",
      "scenarios": [
        {
          "condition": "f=1kHz",
          "limits": {
            "General_Purpose": [500, 1000],
            "Precision_Zero_Drift": [10, 50, 100, 500],
            "High_Speed": [1000, 2000, 5000, 10000]
          }
        }
      ]
    },
    {
      "key": "voltage_noise_pp",
      "symbol": "e<sub>n(p-p)</sub>",
      "spec_type": "max_limit",
      "column_model": "TYP_MAX",
      "engineering_class": "NOISE_PARAM",
      "special_semantics": "LOW_FREQ_NOISE",
      "llm_context": {
        "formal_name": "Low Frequency Noise (0.1Hz to 10Hz)",
        "aliases": ["e_n(p-p) [µVpp] Typ./Max. – 0.1Hz to 10Hz Noise", "0.1Hz to 10Hz Noise [µVpp] Typ./Max. (Peak-to-Peak)", "Peak-to-Peak Noise [nVpp] (BW: 0.1Hz to 10Hz)", "Flicker Noise e_n(p-p) [µVpp] (0.1–10Hz Band)", "Low-Frequency Noise [µVpp] (0.1Hz–10Hz, Typ.)", "e_n(p-p) [µVpp] – 1/f Noise (0.1Hz to 10Hz)", "Peak-to-Peak Voltage Noise [µVpp] (0.1–10Hz)", "0.1–10Hz Input Noise [nVpp] Typ. Max.", "Low-Freq. 1/f Noise [µVpp] (0.1Hz–10Hz Band)", "e_n(p-p) Typ. Max. [µVpp] – Low-Freq. Noise Band"]
      },
      "possible_units": ["µVpp", "nVpp"],
      "std_unit": "µVpp",
      "scenarios": [
        {
          "condition": "0.1Hz to 10Hz",
          "limits": {
            "General_Purpose": [1, 2, 5, 10],
            "Precision_Zero_Drift": [0.1, 0.2, 0.5, 1.5],
            "High_Speed": [5, 10, 20]
          }
        }
      ]
    },
    {
      "key": "thd_plus_n",
      "symbol": "THD+N",
      "spec_type": "max_limit",
      "column_model": "TYP_ONLY",
      "engineering_class": "PERFORMANCE_LIMIT",
      "special_semantics": "AUDIO_PARAM",
      "llm_context": {
        "formal_name": "Total Harmonic Distortion + Noise",
        "aliases": ["THD+N [dB/%] Typ. – Total Harmonic Distortion + Noise", "THD+N [%] Typ.", "THD + Noise [dB] Typ.", "Total Harmonic Distortion [dB] THD+N (Typ.)", "THD+N Typ. [%] – Audio Distortion", "THD + N [%] Typ. – Unity Gain"]
      },
      "possible_units": ["%", "dB"],
      "std_unit": "dB",
      "scenarios": [
        {
          "condition": "f=1kHz, G=1, Vout=2Vpp",
          "limits": {
            "General_Purpose": [-60, -70, -80],
            "Precision_Zero_Drift": [-90, -100, -110, -120],
            "High_Speed": [-70, -80, -90]
          }
        }
      ]
    },
    {
      "key": "channel_separation",
      "symbol": "CS",
      "spec_type": "min_limit",
      "column_model": "TYP_ONLY",
      "engineering_class": "PERFORMANCE_LIMIT",
      "special_semantics": "MULTI_CHANNEL",
      "llm_context": {
        "formal_name": "Channel Separation",
        "aliases": ["CS [dB] Typ. – Channel Separation", "Crosstalk [dB] Typ.", "Channel Isolation CS [dB]", "CS [dB] – Channel-to-Channel Isolation (Typ.)", "Inter-Channel Crosstalk [dB] Typ.", "Channel Separation [dB] CS (Dual/Quad)", "Crosstalk Rejection [dB] Typ.", "CS Typ. [dB] – Channel Isolation (Dual/Quad Amp)", "Isolation [dB] Typ. – Channel-to-Channel"]
      },
      "possible_units": ["dB"],
      "std_unit": "dB",
      "scenarios": [
        {
          "condition": "f=1kHz to 100kHz",
          "limits": {
            "General_Purpose": [90, 100, 110],
            "Precision_Zero_Drift": [120, 130, 140],
            "High_Speed": [60, 70, 80, 100]
          }
        }
        ]
      }
    ],

    "DYNAMIC_CHAR": [
      {
        "key": "phase_margin",
        "symbol": "φ<sub>M</sub>",
        "spec_type": "min_limit",
        "column_model": "TYP_ONLY",
        "engineering_class": "DYNAMIC_PARAMETER",
        "special_semantics": "NONE",
        "llm_context": {
          "formal_name": "Phase Margin",
          "aliases": ["Phase Margin φ_M [°] Typ. – Unity-Gain Configuration", "φ_M [°] Typ. – Phase Margin (G=1, Capacitive Load)", "Phase Margin [°] Typ. (Open-Loop, Unity Gain)", "PM [°] Typ. – Phase Margin at GBW Crossover", "φ_M [degrees] Typ. – Stability Margin (G=1)", "Phase Margin [deg] Typ. – Bode Plot (Unity Gain)", "Phase Margin φ [°] Typ. (at Unity-Gain Bandwidth)", "PM [°] Typ. – Open-Loop Phase at 0 dB Gain Crossing"]
        },
        "possible_units": ["°"],
        "std_unit": "°",
        "scenarios": [
          {
            "condition": "G=1, CL=100pF",
            "limits": {
              "General_Purpose": [45, 50, 55, 60, 65, 70],
              "Precision_Zero_Drift": [45, 50, 55, 60, 65],
              "High_Speed": [40, 45, 50, 55, 60]
            }
          }
        ]
      },
      {
        "key": "full_power_bw",
        "symbol": "BW<sub>P</sub>",
        "spec_type": "nominal",
        "column_model": "MIN_TYP",
        "engineering_class": "DYNAMIC_PARAMETER",
        "special_semantics": "NONE",
        "llm_context": {
          "formal_name": "Full-Power Bandwidth",
          "aliases": ["Full-Power Bandwidth BW_P [MHz/kHz] – Large Signal", "BW_P [MHz] Typ. – Full-Power BW (V_out = V_rated)", "Full Power BW [kHz] Typ. (SR / (2π × V_peak))", "FPBW [MHz] Typ. – Full Output Swing Bandwidth", "Full-Power BW [kHz] (= SR ÷ 2π × V_p)", "Power Bandwidth BW_p [kHz] Typ. – Large Signal", "Full-Output-Swing Bandwidth [kHz] Typ. (FPBW)", "BW_P [MHz] Min./Typ. – Slew-Rate Limited Bandwidth"]
        },
        "possible_units": ["MHz", "kHz"],
        "std_unit": "kHz",
        "scenarios": [
          {
            "condition": "Vout=rated swing, RL=2kΩ",
            "limits": {
              "General_Purpose": [10, 20, 50, 100, 200],
              "Precision_Zero_Drift": [1, 2, 5, 10, 20],
              "High_Speed": [500, 1000, 2000, 5000, 10000, 20000]
            }
          }
        ]
      },
      {
        "key": "output_swing_pos",
        "symbol": "V<sub>OH</sub>",
        "spec_type": "min_limit",
        "column_model": "MIN_TYP",
        "engineering_class": "PERFORMANCE_LIMIT",
        "special_semantics": "NONE",
        "llm_context": {
          "formal_name": "Output Voltage Swing High",
          "aliases": ["V_OH [V] Min./Typ. – Output High Voltage Swing (RL=2kΩ)", "Output High Swing V_OH [V] Min. (from V+, RL=2kΩ)", "V_out(max) [V] Min. – Maximum Output Voltage Swing", "VOH [V] Min./Typ. – Output Voltage High (RL=10kΩ)", "V_OH Min. [V] – Output Swing High (Rail-to-Rail)", "Output Swing High V_OH [V] Typ./Min. (RL=600Ω)", "High Output Level V_OH [V] Min. – Output Range", "V_OH [V] Typ. – Positive Output Swing (RL=2kΩ, G=1)"]
        },
        "possible_units": ["V"],
        "std_unit": "V",
        "scenarios": [
          {
            "condition": "RL=2kΩ, VS=±15V",
            "limits": {
              "General_Purpose": [12, 13, 13.5, 14],
              "Precision_Zero_Drift": [1.4, 1.5, 1.6, 1.8, 2.0],
              "High_Speed": [3.5, 3.8, 4.0, 4.2]
            }
          }
        ]
      },
      {
        "key": "output_swing_neg",
        "symbol": "V<sub>OL</sub>",
        "spec_type": "max_limit",
        "column_model": "TYP_MAX",
        "engineering_class": "PERFORMANCE_LIMIT",
        "special_semantics": "NONE",
        "llm_context": {
          "formal_name": "Output Voltage Swing Low",
          "aliases": ["V_OL [V] Typ./Max. – Output Low Voltage Swing (RL=2kΩ)", "Output Low Swing V_OL [V] Max. (from V-, RL=2kΩ)", "V_out(min) [V] Max. – Minimum Output Voltage Swing", "VOL [V] Typ./Max. – Output Voltage Low (RL=10kΩ)", "V_OL Max. [V] – Output Swing Low (Rail-to-Rail)", "Output Swing Low V_OL [V] Typ./Max. (RL=600Ω)", "Low Output Level V_OL [V] Max. – Output Range", "V_OL [V] Typ. – Negative Output Swing (RL=2kΩ, G=1)"]
        },
        "possible_units": ["V"],
        "std_unit": "V",
        "scenarios": [
          {
            "condition": "RL=2kΩ, VS=±15V",
            "limits": {
              "General_Purpose": [-14, -13.5, -13, -12],
              "Precision_Zero_Drift": [-1.4, -1.5, -1.6, -1.8, -2.0],
              "High_Speed": [-3.5, -3.8, -4.0, -4.2]
            }
          }
        ]
      },
      {
        "key": "capacitive_load",
        "symbol": "C<sub>L</sub>",
        "spec_type": "max_rating",
        "column_model": "MAX_ONLY",
        "engineering_class": "OPERATING_CONDITION",
        "special_semantics": "NONE",
        "llm_context": {
          "formal_name": "Capacitive Load Drive",
          "aliases": ["C_L [pF/nF] Max. – Capacitive Load (Stable Operation)", "Max Capacitive Load C_L [pF] (Stable, No Oscillation)", "Capacitive Load Drive C_L [pF] Max. (G=1)", "C_LOAD [pF] Max. – Stable Output Capacitive Load", "C_L [pF] Max. – Capacitive Load (No Compensation)", "Max Load Capacitance C_L [pF] (Phase Margin ≥45°)", "Capacitive Load C_L [nF] Max. – Stable Drive", "CL [pF] Max. – Output Capacitive Load (Stable, G=1)"]
        },
        "possible_units": ["pF", "nF"],
        "std_unit": "pF",
        "scenarios": [
          {
            "condition": "G=1, Stable Operation",
            "limits": {
              "General_Purpose": [100, 200, 500, 1000, 2000],
              "Precision_Zero_Drift": [100, 200, 500, 1000],
              "High_Speed": [5, 10, 20, 50, 100]
            }
          }
        ]
      }
    ],

    "OPERATING_CONDITIONS": [
      {
        "key": "vs_min_op",
        "symbol": "V<sub>S(min)</sub>",
        "spec_type": "operational_range",
        "column_model": "MIN_ONLY",
        "engineering_class": "OPERATING_CONDITION",
        "special_semantics": "NONE",
        "llm_context": {
          "formal_name": "Minimum Supply Voltage",
          "aliases": ["V_S [V] Min. – Minimum Operating Supply Voltage", "Min. Supply Voltage V_S [V] (Operating Range, Min.)", "V_S(min) [V] – Minimum Recommended Supply", "V_CC(min) [V] – Minimum Single-Supply Voltage", "Supply Voltage Min. [V] V_S (Operating, Not Abs. Max.)", "V_S Min. [V] – Operating (Specified Performance)", "Minimum Operating Supply [V] V_S (Not Startup)", "V(S) Min. [V] – Supply Range Lower Bound (Spec. Perf.)"]
        },
        "possible_units": ["V"],
        "std_unit": "V",
        "scenarios": [
          {
            "condition": "Operating, Specified Performance",
            "limits": {
              "General_Purpose": [3, 4, 5, 6, 8, 10],
              "Precision_Zero_Drift": [1.8, 2.2, 2.5, 3, 4],
              "High_Speed": [3, 4, 5, 6]
            }
          }
        ]
      },
      {
        "key": "vs_max_op",
        "symbol": "V<sub>S(max)</sub>",
        "spec_type": "operational_range",
        "column_model": "MAX_ONLY",
        "engineering_class": "OPERATING_CONDITION",
        "special_semantics": "NONE",
        "llm_context": {
          "formal_name": "Maximum Supply Voltage (Operating)",
          "aliases": ["V_S [V] Max. – Maximum Operating Supply Voltage", "Max. Supply Voltage V_S [V] (Operating Range, Max.)", "V_S(max) [V] – Maximum Recommended Supply", "V_CC(max) [V] – Maximum Single-Supply Voltage", "Supply Voltage Max. [V] V_S (Operating, Not Abs. Max.)", "V_S Max. [V] – Operating (Specified Performance)", "Maximum Operating Supply [V] V_S (Not Abs. Limit)", "V(S) Max. [V] – Supply Range Upper Bound (Spec. Perf.)"]
        },
        "possible_units": ["V"],
        "std_unit": "V",
        "scenarios": [
          {
            "condition": "Operating, Specified Performance",
            "limits": {
              "General_Purpose": [16, 18, 22, 26, 30, 36],
              "Precision_Zero_Drift": [5, 5.5, 6, 8, 12],
              "High_Speed": [5, 6, 10, 12, 15]
            }
          }
        ]
      },
      {
        "key": "vicr_min",
        "symbol": "V<sub>ICR(min)</sub>",
        "spec_type": "operational_range",
        "column_model": "MIN_ONLY",
        "engineering_class": "OPERATING_CONDITION",
        "special_semantics": "NONE",
        "llm_context": {
          "formal_name": "Input Common-Mode Range Low",
          "aliases": ["V_ICR(min) [V] – Input Common-Mode Range (Lower Bound)", "Common-Mode Input Range Min. [V] V_ICR (Operating)", "V_CM(min) [V] – Minimum Input Common-Mode Voltage", "Input Common Mode Min. [V] V_ICR (Operating Range)", "V_ICR Low [V] – Common-Mode Input Voltage Min.", "CM Input Range Min. [V] V_CM (Specified Operation)", "V_ICR Min. [V] – Lower CM Input Boundary (Operating)", "Common-Mode Voltage Min. V_CM [V] (Input Range)"]
        },
        "possible_units": ["V"],
        "std_unit": "V",
        "scenarios": [
          {
            "condition": "Operating, VS=specified",
            "limits": {
              "General_Purpose": [-12, -13, -14, -14.5],
              "Precision_Zero_Drift": [-0.1, 0, 0.1, 0.2],
              "High_Speed": [-3.5, -4, -4.5, -5]
            }
          }
        ]
      },
      {
        "key": "vicr_max",
        "symbol": "V<sub>ICR(max)</sub>",
        "spec_type": "operational_range",
        "column_model": "MAX_ONLY",
        "engineering_class": "OPERATING_CONDITION",
        "special_semantics": "NONE",
        "llm_context": {
          "formal_name": "Input Common-Mode Range High",
          "aliases": ["V_ICR(max) [V] – Input Common-Mode Range (Upper Bound)", "Common-Mode Input Range Max. [V] V_ICR (Operating)", "V_CM(max) [V] – Maximum Input Common-Mode Voltage", "Input Common Mode Max. [V] V_ICR (Operating Range)", "V_ICR High [V] – Common-Mode Input Voltage Max.", "CM Input Range Max. [V] V_CM (Specified Operation)", "V_ICR Max. [V] – Upper CM Input Boundary (Operating)", "Common-Mode Voltage Max. V_CM [V] (Input Range)"]
        },
        "possible_units": ["V"],
        "std_unit": "V",
        "scenarios": [
          {
            "condition": "Operating, VS=specified",
            "limits": {
              "General_Purpose": [12, 13, 14, 14.5],
              "Precision_Zero_Drift": [5.4, 5.5, 5.6, 6.1],
              "High_Speed": [3.5, 4.0, 4.5, 5.0]
            }
          }
        ]
      },
      {
        "key": "ta_range",
        "symbol": "T<sub>A</sub>",
        "spec_type": "operational_range",
        "column_model": "MIN_MAX",
        "engineering_class": "OPERATING_CONDITION",
        "special_semantics": "NONE",
        "llm_context": {
          "formal_name": "Operating Temperature Range",
          "aliases": ["T_A [°C] Min./Max. – Ambient Temperature (Operating)", "Operating Temperature Range T_A [°C] Min. to Max.", "Ambient Temp. T_A [°C] (Operating, Min.–Max.)", "T_A Range [°C] – Specified Operating Temp. Range", "Operating Temp. Range [°C] T_A (Min. to Max.)", "Temperature Range T_A [°C] Min./Max. (Operational)", "T(A) [°C] Min./Max. – Ambient Operating Temperature", "T_A Operating [°C] – Device Specified Temperature Range"]
        },
        "possible_units": ["°C"],
        "std_unit": "°C",
        "scenarios": [
          {
            "condition": "Specified Operating Range",
            "limits": {
              "General_Purpose": [[-40, 85], [-40, 125], [0, 70]],
              "Precision_Zero_Drift": [[-40, 85], [-40, 125], [-55, 125]],
              "High_Speed": [[-40, 85], [-40, 125], [0, 70]]
            }
          }
        ]
      }
    ]
  }
}


