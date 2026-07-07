import random
import json
import html
import re
import copy

from typing import Dict, Any, List, Optional
from dataclasses import dataclass

try:
    from html2image import Html2Image
    _HAS_HTML2IMAGE = True
except ImportError:
    Html2Image = None
    _HAS_HTML2IMAGE = False

from synthetic_pipeline.strategy_utils import (
    apply_final_rounding,
    select_best_display_unit,
    convert_for_display,
)


class BaseDatasheetRenderer:
    """
    מחלקת בסיס המכילה לוגיקה משותפת לכל ה-Renderers.
    מונעת שכפול קוד בפונקציות כמו _format_row.
    """

    SINGLE_VALUE_PARAMS = ["Package Type", "Pin Configuration", "Mounting Type", "Polarization", "Terminal Finish",
                           "Moisture Sensitivity Level"]

    def _get_section_title_variant(self, section_key: str) -> str:
        """
        מחזירה כותרת מגוונת לסקציות השונות בדף הנתונים.
        מבוסס על מינוחים אמיתיים של יצרנים (TI, Vishay, NXP, OnSemi).
        """
        variants = {
            # === Absolute Maximum Ratings ===
            "ABS_MAX": [
                "Absolute Maximum Ratings",
                "Abs. Max. Ratings",
                "Limiting Values",             # נפוץ אצל NXP/Nexperia
                "Maximum Ratings",
                "Absolute Maximums",
                "Stress Ratings"
            ],

            # === Electrical Characteristics ===
            "ELEC_CHAR": [
                "Electrical Characteristics",
                "DC Electrical Characteristics",
                "Electrical Specifications",
                "Static Characteristics",      # נפוץ ב-MOSFETs
                "DC Specifications",
                "Electrical Data"
            ],

            # === Thermal Characteristics ===
            "THERMAL": [
                "Thermal Information",
                "Thermal Characteristics",
                "Thermal Resistance Ratings",
                "Thermal Data",
                "Thermal Specifications"
            ],

            # === Dynamic / AC Characteristics ===
            "DYNAMIC": [
                "Dynamic Characteristics",
                "AC Characteristics",
                "Switching Characteristics",   # נפוץ ברכיבי מיתוג
                "AC Electrical Specifications",
                "Timing Diagrams & Specs"
            ],

            # === Mechanical / Package ===
            "MECHANICAL": [
                "Mechanical Data",
                "Package Dimensions",
                "Physical Specifications",
                "Case Outline",
                "Package Mechanical Data",
                "Mechanical Characteristics"
            ],

            # === Operational ===
            "OPERATING": [
                "Recommended Operating Conditions",
                "Operating Conditions",
                "Recommended Operation",
                "Operating Ratings"
            ]
        }

        # ניקוי המפתח (למקרה שהגיע עם אותיות קטנות או רווחים)
        clean_key = section_key.upper().strip()

        # החזרת וריאציה רנדומלית, או ברירת מחדל יפה אם המפתח לא קיים
        return random.choice(variants.get(clean_key, [clean_key.replace('_', ' ').title()]))

    def _get_possible_units_generic(self, unit: str) -> List[str]:
        """מיפוי משפחות יחידות - תומך בכל הרכיבים"""
        families = [
            ['pF', 'nF', 'µF', 'uF', 'mF', 'F'],  # קיבול
            ['nV', 'µV', 'mV', 'V', 'kV'],  # מתח
            ['nA', 'µA', 'mA', 'A'],  # זרם
            ['mΩ', 'Ω', 'kΩ', 'MΩ'],  # התנגדות
            ['Hz', 'kHz', 'MHz', 'GHz'],  # תדר
            ['ns', 'µs', 'ms', 's'],  # זמן
            ['W', 'mW', 'kW'],  # הספק
            ['°C/W']  # התנגדות תרמית
        ]
        for fam in families:
            if unit in fam:
                return fam
        return [unit]

    def _format_row(self, param) -> Dict:
        """
        ✅ ENHANCED: Random unit formatting variations
        - Sometimes combines value+unit (e.g., "5V")
        - Sometimes separates them (e.g., "5 V")
        - Sometimes omits unit from cell (relies on column header)

        גרסה אוניברסלית ומתוקנת.
        משמשת גם את ה-JSON וגם את ה-HTML.
        """
        # --- תיקון לבאג המשקל (Weight Bug Fix) ---
        if (param.label == "Weight" or param.key == "weight"):
            if param.value_typ is None or (isinstance(param.value_typ, (int, float)) and param.value_typ <= 0):
                param.value_typ = None

        def extract_numeric_value(val):
            """
            מחלץ ערך מספרי יחיד מ-dictionary, list, או מחזיר את הערך כמו שהוא.

            FIX #1: רשימה צריכה להיות ערך יחיד כבר מהמחולל.
            אם הגיעה רשימה — מדפיסים אזהרה ובוחרים את האמצעי (לא הראשון).
            ה-median הוא הבחירה הבטוחה ביותר כי הוא ייצוגי ונמצא בטווח.
            """
            if val is None:
                return None

            if isinstance(val, dict):
                if len(val) > 0:
                    return list(val.values())[0]
                return None

            if isinstance(val, list):
                if len(val) == 0:
                    return None
                # FIX: אזהרה + בחירת אמצעי במקום ראשון
                if len(val) > 1:
                    import warnings
                    warnings.warn(
                        f"[generators.py] extract_numeric_value received a list of {len(val)} "
                        f"values for param '{getattr(param, 'key', '?')}': {val}. "
                        f"Fix the generator to emit a single value. "
                        f"Falling back to median.",
                        stacklevel=4
                    )
                # בחירת האמצעי: sortable values בלבד
                numeric_vals = [v for v in val if isinstance(v, (int, float))]
                if numeric_vals:
                    numeric_vals.sort()
                    return numeric_vals[len(numeric_vals) // 2]
                # אם לא ניתן למיין (רשימת strings) — קח את האמצעי הסדרתי
                return val[len(val) // 2]

            return val

        # חילוץ ערכים בצורה בטוחה
        min_val = extract_numeric_value(param.value_min)
        typ_val = extract_numeric_value(param.value_typ)
        max_val = extract_numeric_value(param.value_max)

        # ==========================================
        # 1. בחירת שם הפרמטר (Alias) ושמירתו בזיכרון
        # ==========================================
        if hasattr(param, '_cached_label'):
            display_label = param._cached_label
        else:
            # FIX Bug 5: normalize merged/underscore labels before using as fallback
            base_label = self._normalize_param_label(param.label)
            display_label = base_label
            aliases = getattr(param, 'aliases', [])

            if not aliases and hasattr(param, 'llm_context') and isinstance(param.llm_context, dict):
                aliases = param.llm_context.get('aliases', [])

            if not aliases:
                from synthetic_pipeline.strategies import UNIFIED_COMPONENT_DB
                for c_name, c_data in UNIFIED_COMPONENT_DB.items():
                    if isinstance(c_data, dict):
                        for sec_name, sec_items in c_data.items():
                            if isinstance(sec_items, list):
                                for item in sec_items:
                                    if isinstance(item, dict) and item.get("key") == param.key:
                                        aliases = item.get("llm_context", {}).get("aliases", [])
                                        break
                                if aliases: break
                    if aliases: break

            if aliases:
                # סינון aliases שמכילים מידע עודף (יחידות, סוגי ערכים, סוגריים)
                _ALIAS_NOISE = re.compile(
                    r'\[.*?\]'           # [uV], [nA], [mhz]
                    r'|Typ\.|Max\.|Min\.' # סוגי ערכים
                    r'|Typ\./Max\.'
                    r'|\(.*?\)'          # (Input Pins), (Typ.)
                    r'|–\s*\w+'          # – Output Ramp Rate
                )
                clean_aliases = [
                    a for a in aliases
                    if not _ALIAS_NOISE.search(a) and len(a.split()) <= 5
                ]
                # אם אחרי הסינון לא נשאר כלום — השתמש בשם המנורמל (FIX Bug 5)
                options = (clean_aliases if clean_aliases else []) + [base_label]
                weights = (
                    [0.85 / len(clean_aliases)] * len(clean_aliases) + [0.15]
                    if clean_aliases else [1.0]
                )
                display_label = random.choices(options, weights=weights)[0]

            param._cached_label = display_label

        # 2. בחירת יחידת תצוגה
        candidate_vals = [v for v in [min_val, typ_val, max_val] if isinstance(v, (int, float))]

        if candidate_vals:
            possible_units = self._get_possible_units_generic(param.unit)
            display_unit = select_best_display_unit(candidate_vals, param.unit, possible_units)
        else:
            display_unit = param.unit

        # ✅ NEW: Decide on unit formatting style (once per row)
        # 30% - combine value+unit (no space): "5V"
        # 40% - separate value and unit: "5 V"
        # 30% - omit unit from value (rely on column header)
        if hasattr(param, '_cached_unit_format'):
            unit_format = param._cached_unit_format
            unit_separator = param._cached_unit_separator
        else:
            format_choice = random.random()

        if format_choice < 0.3:
            unit_format = "combined"    # "5V"
            unit_separator = ""
        elif format_choice < 0.7:
            unit_format = "separated"   # "5 V"
            unit_separator = " "
        else:
            unit_format = "omitted"     # "5" (unit in column header)
            unit_separator = ""

        # 3. פונקציית המרה + פורמט למחרוזת (ללא עיגול!)
        def to_disp(val):
            if val is None:
                return None
            if not isinstance(val, (int, float)):
                return val

            converted = convert_for_display(val, param.unit, display_unit)

            if isinstance(converted, (int, float)):
                f_val = float(converted)

                if 0 < abs(f_val) < 0.05:
                    return f"{f_val:.3g}"

                if abs(f_val - round(f_val)) < 0.05:
                    return str(int(round(f_val)))

                if f_val.is_integer():
                    return str(int(f_val))

                return f"{f_val:.3g}"

            return str(converted)

        # 4. המרת הערכים (כעת הם מחרוזות מעוצבות)
        disp_min = to_disp(min_val)
        disp_typ = to_disp(typ_val)
        disp_max = to_disp(max_val)

        # ✅ NEW: Apply unit formatting based on choice
        def format_with_unit(value_str, is_typ=False):
            """Apply the chosen unit formatting style with safe special characters"""
            if value_str is None:
                return None

            # הזרקת רעש רק אם הערך לא מכיל כבר סימני טולרנס/כיוון
            if is_typ and random.random() < 0.15:
                if not any(char in str(value_str) for char in ['±', '+', '-', '~']):
                    value_str = f"±{value_str}"

            norm_unit = display_unit.strip()

            # ואז שורות 722, 724 — החלף display_unit ב-norm_unit:
            if unit_format == "combined":
                return f"{value_str}{norm_unit}"          # שורה 722
            elif unit_format == "separated":
                return f"{value_str}{unit_separator}{norm_unit}"
            else:  # omitted
                return value_str

        # Apply formatting to all values
        formatted_min = format_with_unit(disp_min) if disp_min else None
        formatted_typ = format_with_unit(disp_typ) if disp_typ else None
        formatted_max = format_with_unit(disp_max) if disp_max else None

        # 5. בניית השורה
        row = {
            "Parameter": display_label,
            "symbol": param.symbol if (hasattr(param, 'symbol') and param.symbol) else "—",
            "Condition": param.condition if param.condition else "",

            "Unit": display_unit if unit_format != "omitted" else display_unit,
            "Min": formatted_min,
            "Typ": formatted_typ,
            "Max": formatted_max,

            "_metadata": {
                "key": param.key,
                "engineering_class": self._get_enum_val(getattr(param, 'engineering_class', 'UNKNOWN')),
                "std_unit": getattr(param, 'std_unit', param.unit),
                "spec_type": self._get_enum_val(getattr(param, 'spec_type', 'UNKNOWN')),
                "unit_format": unit_format,
                "displayed_min": formatted_min,
                "displayed_typ": formatted_typ,
                "displayed_max": formatted_max,
                "displayed_unit": display_unit,
                "formal_name": param.label,
                "raw_min": disp_min,
                "raw_typ": disp_typ,
                "raw_max": disp_max
            }
        }

        # לוגיקה להסתרת Typ אם זה Max Rating
        try:
            spec_val = param.spec_type.value if hasattr(param.spec_type, 'value') else param.spec_type
            if spec_val in ["max_rating", "max_limit"]:
                if not formatted_typ: row["Typ"] = ""
        except:
            pass

        # בדיקה אם להציג ערך בודד (Value)
        if param.key in self.SINGLE_VALUE_PARAMS:
            row["Value"] = formatted_typ if formatted_typ else "—"

        return row

    def _get_enum_val(self, val) -> str:
        if hasattr(val, 'name'):
            return val.name
        if hasattr(val, 'value'):
            return val.value
        return str(val)

    @staticmethod
    def _normalize_param_label(label: str) -> str:
        """
        FIX Bug 5: Convert merged/underscore parameter labels to proper display names.
        Examples: "componentheight" → "Component Height"
                  "input_bias_current" → "Input Bias Current"
                  "RdsOn" → "Rds On"
        """
        if not label or ' ' in label:
            return label
        # snake_case → Title Case
        if '_' in label:
            return label.replace('_', ' ').title()
        # camelCase → Title Case  (e.g. "RdsOn" → "Rds On")
        spaced = re.sub(r'(?<=[a-z])(?=[A-Z])', ' ', label)
        if spaced != label:
            return spaced.title()
        # All-lowercase compound word — insert spaces before known suffixes
        _KNOWN_SUFFIXES = [
            'height', 'width', 'weight', 'length', 'current', 'voltage',
            'power', 'resistance', 'frequency', 'temperature', 'time',
            'ratio', 'range', 'value', 'factor', 'gain', 'noise', 'rate',
        ]
        result = label
        for suffix in _KNOWN_SUFFIXES:
            if result.lower().endswith(suffix) and len(result) > len(suffix):
                prefix = result[:-len(suffix)]
                result = prefix + ' ' + suffix
                break
        return result.title()


class HtmlRenderingConstants:
    """מאגר הסגנונות ומבני הטבלאות"""

    SECTION_TITLES = {
        "ABS_MAX": "Absolute Maximum Ratings",
        "ELEC_CHAR": "Electrical Characteristics",
        "PACKAGE": "Mechanical Information",
        "THERMAL": "Thermal Characteristics"
    }

    TABLE_STRUCTURES = {
        "standard_full": {"name": "Standard Electrical Characteristics",
                          "columns": ["Parameter", "symbol", "Condition", "Min", "Typ", "Max", "Unit"],
                          "merge_limits": False, "show_symbol": True, "split_sections": True},
        "max_ratings_only": {"name": "Absolute Maximum Ratings",
                             "columns": ["Parameter", "symbol", "Condition", "Rating", "Unit"],
                             "merge_limits": "max_only", "show_symbol": True, "split_sections": True},
        "thermal_data": {"name": "Thermal Characteristics",
                         "columns": ["Parameter", "symbol", "Conditions", "Typ", "Max", "Unit"], "merge_limits": False,
                         "show_symbol": True, "split_sections": True},
        "operating_range": {"name": "Recommended Operating Conditions",
                            "columns": ["Parameter", "symbol", "Min", "Max", "Unit"], "merge_limits": False,
                            "show_symbol": True, "split_sections": True},
        "compact_commercial": {"name": "Mechanical / General Information",
                               "columns": ["Parameter", "Condition", "Value", "Unit"], "merge_limits": "typ_preferred",
                               "show_symbol": False, "split_sections": True},
        "reliability_specs": {"name": "Reliability & Test Specifications",
                              "columns": ["Test Item", "Test Conditions", "Duration", "Performance / Limit"],
                              "merge_limits": "custom_text", "show_symbol": False, "split_sections": True},
        "legacy_databook": {"name": "Legacy Databook Style",
                            "columns": ["Characteristic", "symbol", "Min", "Typ", "Max", "Unit"], "merge_limits": False,
                            "show_symbol": True, "condition_in_name": True}
    }

    VISUAL_STYLES = {
        "classic_standard": {"name": "Classic Standard (TI Style)",
                             "css": "body { font-family: Arial, Helvetica, sans-serif; color: #333; line-height: 1.4; } h1 { color: #003366; border-bottom: 2px solid #003366; } table { width: 100%; border-collapse: collapse; margin-bottom: 20px; font-size: 13px; } th { background-color: #003366; color: white; text-align: left; padding: 8px; } td { border-bottom: 1px solid #ddd; padding: 6px; } tr:nth-child(even) { background-color: #f2f2f2; }"},
        "vintage_databook": {"name": "Vintage Databook (80s Style)",
                             "css": "body { font-family: 'Courier New', Courier, monospace; color: #000; } h1 { text-transform: uppercase; text-decoration: underline; } table { width: 100%; border: 2px solid #000; border-collapse: collapse; margin-bottom: 25px; } th { border-bottom: 2px solid #000; border-right: 1px solid #000; padding: 5px; text-transform: uppercase; } td { border-right: 1px solid #000; border-bottom: 1px solid #000; padding: 5px; }"},
        "modern_tech": {"name": "Modern Tech (IoT Style)",
                        "css": "body { font-family: 'Segoe UI', Roboto, sans-serif; color: #444; background: #fcfcfc; } h1 { color: #00BCD4; font-weight: 300; letter-spacing: 1px; } table { width: 100%; border-collapse: separate; border-spacing: 0; box-shadow: 0 2px 15px rgba(0,0,0,0.05); border-radius: 8px; overflow: hidden; } th { background-color: #f8f9fa; color: #555; font-weight: 600; padding: 12px; border-bottom: 2px solid #00BCD4; } td { padding: 12px; border-bottom: 1px solid #eee; }"},
        "industrial_heavy": {"name": "Industrial Heavy",
                             "css": "body { font-family: Verdana, sans-serif; color: #222; } h1 { background-color: #FF5722; color: white; padding: 10px; font-family: Impact, sans-serif; } table { width: 100%; border: 3px solid #444; border-collapse: collapse; } th { background-color: #444; color: #FF5722; padding: 10px; border: 1px solid #666; } td { border: 1px solid #999; padding: 8px; font-weight: bold; }"},
        "scientific_precision": {"name": "Scientific Precision",
                                 "css": "body { font-family: 'Times New Roman', Times, serif; color: #111; } h1 { font-style: italic; border-bottom: 1px solid #000; } table { width: 100%; border-top: 2px solid #000; border-bottom: 2px solid #000; border-collapse: collapse; } th { border-bottom: 1px solid #000; padding: 4px; font-style: italic; } td { padding: 4px; border-right: 1px dotted #ccc; } td:last-child { border-right: none; }"},
        "compact_japanese": {"name": "Compact Japanese",
                             "css": "body { font-family: Tahoma, sans-serif; font-size: 11px; color: #000033; } h1 { font-size: 16px; color: #000080; border-left: 5px solid #000080; padding-left: 10px; } table { width: 100%; border-collapse: collapse; border: 1px solid #999; } th { background-color: #e6e6ff; color: #000080; padding: 3px; border: 1px solid #999; font-size: 10px; } td { border: 1px solid #ccc; padding: 2px 4px; }"},
        "euro_minimalist": {"name": "Euro Minimalist",
                            "css": "body { font-family: 'Helvetica Neue', Helvetica, sans-serif; color: #2c3e50; } h1 { color: #c0392b; font-size: 24px; margin-bottom: 30px; } table { width: 100%; border-collapse: collapse; } th { text-align: left; padding: 15px 5px; border-bottom: 2px solid #c0392b; color: #7f8c8d; font-weight: normal; } td { padding: 10px 5px; border-bottom: 1px solid #ecf0f1; }"},
        "high_contrast_print": {"name": "High Contrast (Print)",
                                "css": "body { font-family: Arial, sans-serif; color: #000; background: #fff; } h1 { background: #000; color: #fff; padding: 5px 10px; } table { width: 100%; border: 4px solid #000; border-collapse: collapse; } th { background: #000; color: #fff; padding: 10px; font-weight: bold; border: 1px solid #fff; } td { border: 1px solid #000; padding: 8px; font-weight: bold; }"},
        "dark_mode_dev": {"name": "Dark Mode (Developer)",
                          "css": "body { font-family: 'Consolas', 'Monaco', monospace; background-color: #1e1e1e; color: #d4d4d4; } h1 { color: #569cd6; } table { width: 100%; border-collapse: collapse; } th { color: #4ec9b0; text-align: left; padding: 10px; border-bottom: 1px solid #333; } td { padding: 10px; border-bottom: 1px solid #2d2d2d; color: #ce9178; } tr:hover { background-color: #2a2d2e; }"},
        "eco_green": {"name": "Eco Green",
                      "css": "body { font-family: 'Trebuchet MS', sans-serif; color: #2e7d32; } h1 { color: #1b5e20; } table { width: 100%; border-collapse: separate; border-spacing: 0; border: 1px solid #a5d6a7; border-radius: 10px; } th { background-color: #e8f5e9; color: #1b5e20; padding: 10px; first-child: border-top-left-radius: 10px; } td { padding: 8px; border-top: 1px solid #a5d6a7; }"}
    }


@dataclass
class RenderingConfig:
    """
    מכיל את כל ההחלטות הרנדומליות שנעשות פעם אחת ומשותפות לכל ה-Renderers
    """
    # Feature 1: Needle in a Haystack
    injected_param_keys: List[str]  # Which parameters were moved to text

    # Feature 2: Structural Sparsity
    hidden_columns: List[str]  # Which columns to hide globally (e.g., ['Min', 'Typ'])
    transposed_sections: List[str]  # Which sections use horizontal layout

    # Feature 3: Context Disconnection
    long_condition_threshold: int = 20  # Move conditions longer than this to footnotes

    @classmethod
    def generate_random(cls, all_parameters: List) -> 'RenderingConfig':
        """
        יוצר קונפיגורציה רנדומלית פעם אחת בתחילת התהליך
        """
        # Feature 1: Select 1-2 parameters to inject into text
        num_victims = min(random.randint(1, 2), len(all_parameters))
        victim_indices = random.sample(range(len(all_parameters)), num_victims)
        injected_keys = [all_parameters[idx].key for idx in victim_indices]

        # Feature 2A: Decide which columns to hide (30% chance each)
        optional_columns = ['Min', 'Typ', 'Max']
        hidden_columns = [col for col in optional_columns if random.random() < 0.3]

        # Feature 2B: Decide which sections to transpose (not predetermined)
        transposed_sections = []  # Will be decided per-section during rendering

        return cls(
            injected_param_keys=injected_keys,
            hidden_columns=hidden_columns,
            transposed_sections=transposed_sections
        )
