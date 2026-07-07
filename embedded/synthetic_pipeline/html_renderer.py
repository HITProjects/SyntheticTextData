import random
import html
import re

from typing import Dict, Any, List

from synthetic_pipeline.base_renderer import BaseDatasheetRenderer, HtmlRenderingConstants, RenderingConfig
from synthetic_pipeline.augmentors import RandomChartGenerator


class DatasheetHtmlRenderer(BaseDatasheetRenderer):
    """
    Renders the final HTML with features like:
    - Dynamic header structures (Classic/Modern/Minimalist)
    - Page layouts (Standard/Two-Col/Grid)
    - Visual Noise (Watermarks, Image Placeholders)

    ✅ FIX #2 APPLIED: HTML renderer now ONLY uses data from result.parameters
    ✅ FIX #3 APPLIED: Graph placement limited to ELECTRICAL_CHARACTERISTICS section
    """

    HEADER_STRUCTURES = {
        "classic": {
            "template": "<div class='header header-classic'><div class='header-meta'><span class='meta-id'>Document ID: {sample_id}</span><span class='meta-manufacturer'>{manufacturer}</span></div><h1 class='product-title'>{marketing_name}</h1><div class='product-description'><p><strong>Description:</strong> {description}</p></div><div class='technical-info'><span>Package: {package}</span> | <span>Technology: {archetype}</span></div></div>",
            "css_class": "header-classic"},
        "modern": {
            "template": "<div class='header header-modern'><div class='header-brand'><h2>{manufacturer}</h2></div><div class='header-content-centered'><h1>{marketing_name}</h1><p class='lead-description'>{description}</p><div class='spec-badges'><span class='badge'>{package}</span><span class='badge'>{archetype}</span><span class='badge-id'>{sample_id}</span></div></div></div>",
            "css_class": "header-modern"},
        "minimalist": {
            "template": "<div class='header header-minimalist'><div class='header-row'><div class='header-left'><small class='text-muted'>{manufacturer}</small><h1>{marketing_name}</h1></div><div class='header-right'><code>{sample_id}</code></div></div><p class='description-minimalist'>{description}</p><hr class='divider'><small class='tech-specs'>{package} • {archetype}</small></div>",
            "css_class": "header-minimalist"}
    }

    LAYOUT_CLASSES = ["layout-standard", "layout-two-column", "layout-grid"]
    WATERMARKS = ["DRAFT", "CONFIDENTIAL", "PRELIMINARY", "INTERNAL USE ONLY", None, None, None]

    TABLE_STRUCTURES = {
        "max_ratings_only": {"columns": ["Parameter", "symbol", "Value", "Unit", "Condition"]},
        "thermal_data": {"columns": ["Parameter", "symbol", "Typ", "Max", "Unit", "Condition"]},
        "compact_commercial": {"columns": ["Parameter", "Value", "Unit"]},
        "standard_full": {"columns": ["Parameter", "symbol", "Min", "Typ", "Max", "Unit", "Condition"]}
    }

    # ── Fix #7: class-level constant — was being rebuilt inside the column loop ──
    _STRUCTURAL_CONDITIONS = frozenset({
        "Max", "Min", "Typ", "Maximum", "Minimum", "Typical",
        "Nom", "Nominal", "Value", "Rating", "Limit",
    })

    _NOTE_TEXTS = [
        # Thermal / test condition footnotes
        "Note 1: Unless otherwise specified, all limits guaranteed at TJ = 25°C.",
        "All typical values at TA = 25°C unless otherwise noted.",
        "* All specifications apply over the full operating temperature range.",
        "Specifications are measured with VS = ±15V unless otherwise noted.",
        "(a) Stresses beyond those listed may cause permanent damage to the device.",
        # Pulse / measurement footnotes
        "(1) Measured with device mounted on 1 in² FR4 PCB, copper area 1 in².",
        "* Pulse test: PW ≤ 300 µs, duty cycle ≤ 2%.",
        "† Guaranteed by design, not 100% production tested.",
        "(2) For additional information refer to the application note.",
        "§ Applies to commercial temperature range only.",
        "(3) Short-circuit duration must not exceed one second.",
        "* Measured at TA = 25°C with no load and VS = 5V.",
        "† Measured under pulsed conditions; duty cycle ≤ 1%.",
        "(4) Body diode characteristics apply to the intrinsic diode only.",
        "* 100% production tested at TA = 25°C.",
        # PCB / mounting footnotes
        "Thermal resistance depends on PCB layout, copper area, and airflow.",
        "(5) TJ = TA + (PD × θJA). See thermal model in application note.",
        "† Limits apply to device operating in free air without heatsink.",
        "* See AN-1112 for recommended PCB layout and decoupling.",
        "(6) ESD sensitivity class 2 per JESD22-A114. Handle with appropriate precautions.",
        # Safety / ratings footnotes
        "CAUTION: Do not exceed absolute maximum ratings.",
        "† Exceeding maximum ratings may cause permanent device failure.",
        "* Stress ratings only. Functional operation above rated conditions is not implied.",
        "(7) Applies only to commercial-grade (0°C to 70°C) devices.",
        "† AEC-Q101 qualified. Suitable for automotive applications.",
        # Noise / AC / frequency footnotes
        "(8) Noise performance measured with 10 Ω source resistance at f = 1 kHz.",
        "* Gain-bandwidth product specified at unity gain configuration.",
        "† Input-referred noise measured in 1 Hz bandwidth, f = 10 Hz to 10 kHz.",
        "(9) Settling time measured to 0.01% of final value with 10 V step input.",
        "* Measured with capacitive load CL = 10 pF on output.",
        # Process / production / revision footnotes
        "This document contains information on products in the design phase of development.",
        "† Data is based on characterization and is not 100% tested in production.",
        "* Engineering samples available; contact factory for pricing and lead time.",
        "(10) For soldering profile, refer to JEDEC J-STD-020D.",
        "† Lead-free (Pb-free) package. RoHS compliant. MSL = 1 per IPC/JEDEC J-STD-020.",
    ]

    def __init__(self):
        """Initialize footnotes list for Feature 3"""
        self.footnotes = []

    def _render_transposed_table(self, parameters: List[Any]) -> str:
        """
        ✅ FIXED: Tags values in transposed tables WITHOUT label injection.
        ✅ FEATURE 2B: Helper method for transposed table layout.

        FIX #3: מסיר "Min: ", "Typ: ", "Max: " מתוך ה-span.
        הסיבה: ה-aligner.py מחלץ את תוכן ה-span כ-BIO entity.
        אם הspan מכיל "Min: 0.8 mm" — המודל לומד שה-MIN entity כולל
        את המילה "Min". זהו data-leakage זהה לבעיה המקורית שתוקנה.
        """
        if not parameters:
            return ""

        # Build parameter names as column headers
        html_output = "<table><thead><tr>"
        html_output += "<th>Parameter</th>"
        for param in parameters:
            row_data = self._format_row(param)
            html_output += f"<th>{html.escape(row_data['Parameter'])}</th>"
        html_output += "</tr></thead><tbody>"

        # Add value row with tagging — FIX: ערך בלבד בתוך ה-span
        html_output += "<tr><td><strong>Value</strong></td>"
        for param in parameters:
            row_data = self._format_row(param)
            metadata = row_data.get("_metadata", {})
            param_key = metadata.get("key", "unknown")

            value_parts = []
            if row_data.get("Min"):
                # FIX: ה-span מכיל רק את הערך, ללא "Min: "
                tagged = (
                    f'<span class="val-tag" data-label="{param_key}_min">'
                    f'{html.escape(str(row_data["Min"]))}'
                    f'</span>'
                )
                value_parts.append(tagged)
            if row_data.get("Typ"):
                tagged = (
                    f'<span class="val-tag" data-label="{param_key}_typ">'
                    f'{html.escape(str(row_data["Typ"]))}'
                    f'</span>'
                )
                value_parts.append(tagged)
            if row_data.get("Max"):
                tagged = (
                    f'<span class="val-tag" data-label="{param_key}_max">'
                    f'{html.escape(str(row_data["Max"]))}'
                    f'</span>'
                )
                value_parts.append(tagged)

            value_str = "<br>".join(value_parts) if value_parts else "—"
            html_output += f"<td>{value_str}</td>"
        html_output += "</tr>"

        # Add unit row with tagging
        html_output += "<tr><td><strong>Unit</strong></td>"
        for param in parameters:
            row_data = self._format_row(param)
            metadata = row_data.get("_metadata", {})
            param_key = metadata.get("key", "unknown")

            unit = row_data.get("Unit", "—")
            if unit and unit != "—":
                tagged_unit = (
                    f'<span class="unit-tag" data-label="{param_key}_unit">'
                    f'{html.escape(str(unit))}'
                    f'</span>'
                )
                html_output += f"<td>{tagged_unit}</td>"
            else:
                html_output += f"<td>—</td>"
        html_output += "</tr>"

        # Add condition row if any parameter has conditions
        has_conditions = any(self._format_row(p).get("Condition") for p in parameters)
        if has_conditions:
            html_output += "<tr><td><strong>Conditions</strong></td>"
            for param in parameters:
                row_data = self._format_row(param)
                metadata = row_data.get("_metadata", {})
                param_key = metadata.get("key", "unknown")

                condition = row_data.get("Condition", "")
                if condition and condition != "—":
                    tagged_condition = (
                        f'<span class="condition-tag" data-label="{param_key}_condition">'
                        f'{html.escape(str(condition))}'
                        f'</span>'
                    )
                    html_output += f"<td>{tagged_condition}</td>"
                else:
                    html_output += f"<td>—</td>"
            html_output += "</tr>"

        html_output += "</tbody></table>"
        return html_output

    def _render_footnotes_section(self) -> str:
        if not self.footnotes:
            return ""

        html_output = '<div class="notes-section" style="margin-top: 30px; padding: 20px; background: #fff9e6; border-left: 4px solid #ffc107; border-radius: 4px;">'
        html_output += '<h3 style="margin-top: 0; color: #f57c00;">Notes</h3>'
        html_output += '<ol style="margin: 10px 0; padding-left: 20px;">'

        for i, note in enumerate(self.footnotes, 1):
            # ✅ FIXED: Don't escape if already contains tags!
            if '<span' in note:
                # Already tagged, use as-is
                html_output += f'<li style="margin: 8px 0; line-height: 1.6;">{note}</li>'
            else:
                # Not tagged, escape it
                html_output += f'<li style="margin: 8px 0; line-height: 1.6;">{html.escape(note)}</li>'

        html_output += '</ol>'
        html_output += '</div>'
        return html_output

    def _format_display_value(self, val: Any) -> str:
        """
        ✅ פונקציה מינימלית - רק HTML escaping, ללא שום עיבוד
        כל הערכים כבר עובדו ב-_format_row ונשמרו ב-JSON
        """
        if val is None or val == "" or val == "—":
            return "—"

        # המרה פשוטה למחרוזת + HTML escaping
        return html.escape(str(val))

    def _get_enhanced_css(self, watermark: str = None, font: str = "'Segoe UI', sans-serif",
                         table_style: str = "standard", theme: str = "standard") -> str:
        """
        Generate enhanced CSS with customizable visual elements.
        ✅ MERGED: Supports Watermarks + Fonts + Table Styles + Themes
        """
        # Define theme color palettes
        themes = {
            'legacy': {'header_bg': '#000000', 'header_text': '#ffffff', 'border_color': '#000000', 'text_color': '#000000', 'accent': '#000000'},
            'infineon': {'header_bg': '#820000', 'header_text': '#ffffff', 'border_color': '#820000', 'text_color': '#333333', 'accent': '#820000'},
            'onsemi': {'header_bg': '#1a5e1a', 'header_text': '#ffffff', 'border_color': '#1a5e1a', 'text_color': '#333333', 'accent': '#1a5e1a'},
            'onsemi_navy': {'header_bg': '#003366', 'header_text': '#ffffff', 'border_color': '#003366', 'text_color': '#333333', 'accent': '#003366'},
            'standard': {'header_bg': '#f8f9fa', 'header_text': '#555', 'border_color': '#ddd', 'text_color': '#333', 'accent': '#3498db'}
        }

        colors = themes.get(theme, themes['standard'])

        # Watermark CSS
        watermark_css = ""
        if watermark:
            watermark_css = f"body::before {{ content: '{watermark}'; position: fixed; top: 50%; left: 50%; transform: translate(-50%, -50%) rotate(-45deg); font-size: 120px; color: rgba(200, 200, 200, 0.15); font-weight: bold; z-index: 9999; pointer-events: none; }}"

        # Base CSS
        css = f"""
            body {{ font-family: {font}; background-color: white; margin: 20px; line-height: 1.6; color: {colors['text_color']}; }}
            {watermark_css}

            /* Layout Classes */
            .layout-standard {{ max-width: 1200px; margin: 0 auto; }}
            .layout-two-column {{ max-width: 1400px; margin: 0 auto; }}
            .layout-two-column .sections-container {{ display: grid; grid-template-columns: 1fr 1fr; gap: 30px; margin-top: 20px; }}
            .layout-grid {{ max-width: 1600px; margin: 0 auto; }}
            .layout-grid .sections-container {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(500px, 1fr)); gap: 25px; margin-top: 20px; }}

            /* Headers */
            .header {{ margin-bottom: 30px; padding: 20px; border-bottom: 2px solid {colors['border_color']}; }}
            .section-title {{ font-size: 20px; margin-bottom: 15px; border-bottom: 2px solid {colors['accent']}; padding-bottom: 8px; color: {colors['accent']}; }}

            /* General Table Settings */
            table {{ width: 100%; border-collapse: collapse; margin: 15px 0; font-size: 13px; }}
        """

        # Table Styles Logic
        if table_style == 'minimalist':
            css += f"""
                th {{ background-color: {colors['header_bg']}; color: {colors['header_text']}; padding: 12px 15px; text-align: left; font-weight: bold; border-bottom: 2px solid {colors['border_color']}; }}
                td {{ padding: 10px 15px; border-bottom: 1px solid #e0e0e0; }}
            """
        elif table_style == 'grid':
            css += f"""
                table {{ border: 2px solid {colors['border_color']}; }}
                th {{ background-color: {colors['header_bg']}; color: {colors['header_text']}; padding: 10px 12px; border: 1px solid {colors['border_color']}; font-weight: bold; }}
                td {{ padding: 8px 12px; border: 1px solid {colors['border_color']}; }}
            """
        elif table_style == 'striped':
            css += f"""
                th {{ background-color: {colors['header_bg']}; color: {colors['header_text']}; padding: 10px 12px; text-align: left; border: 1px solid {colors['border_color']}; }}
                td {{ padding: 8px 12px; border: 1px solid {colors['border_color']}; }}
                tr:nth-child(even) {{ background-color: #f8f8f8; }}
            """
        elif table_style == 'dense':
            css += f"""
                table {{ font-size: 11px; }}
                th {{ background-color: {colors['header_bg']}; color: {colors['header_text']}; padding: 4px 6px; border: 1px solid {colors['border_color']}; }}
                td {{ padding: 2px 4px; border: 1px solid {colors['border_color']}; }}
            """
        else: # Standard fallback
            css += f"""
                th, td {{ padding: 10px; text-align: left; border: 1px solid {colors['border_color']}; }}
                th {{ background-color: {colors['header_bg']}; color: {colors['header_text']}; font-weight: 600; }}
                tr:nth-child(even) {{ background-color: #f9f9f9; }}
            """

        # Additional Utilities (Tags, Notes, etc.)
        css += f"""
            .subheader td {{ background-color: #e8e8e8 !important; font-weight: bold; }}
            .features-apps {{ display: grid; grid-template-columns: 1fr 1fr; gap: 30px; margin: 30px 0; }}
            .features-apps ul {{ list-style: disc; padding-left: 20px; }}
            .footer-notes {{ margin-top: 40px; padding: 20px; background: #f8f9fa; border-radius: 4px; }}
            sub, sup {{ font-size: 75%; line-height: 0; position: relative; vertical-align: baseline; }}
            sup {{ top: -0.5em; }} sub {{ bottom: -0.25em; }}
            .val-tag, .unit-tag, .nlg-val, .nlg-unit, .condition-tag {{ display: inline; }}
            .note-ref {{ color: {colors['accent']}; font-size: 0.9em; vertical-align: super; font-weight: bold; }}
        """

        return css

    def _render_features_and_apps(self, marketing_data: Dict) -> str:
        features = marketing_data.get("key_features", [])
        applications = marketing_data.get("typical_applications", [])
        if not features and not applications: return ""
        html_output = '<div class="features-apps">'
        if features:
            html_output += '<div class="features-section"><h3>Key Features</h3><ul>'
            for feature in features:
                # NLG-generated features already contain raw <span data-label="..."> markup.
                # Escaping destroys those attributes and makes them invisible to the aligner.
                content = feature if ('<span' in feature and 'data-label' in feature) else html.escape(feature)
                html_output += f'<li>{content}</li>'
            html_output += '</ul></div>'
        if applications:
            html_output += '<div class="apps-section"><h3>Typical Applications</h3><ul>'
            for app in applications: html_output += f'<li>{html.escape(app)}</li>'
            html_output += '</ul></div>'
        html_output += '</div>'
        return html_output

    def _get_random_image_placeholder(self, result_context) -> str:
        """
        ✅ FIX #3: Now accepts result.context to determine component type
        """
        # 30% סיכוי שלא יהיה גרף בכלל (כדי לשמור על גיוון בדאטה)
        if random.random() < 0.3:
            return ""

        # יצירת תמונת הגרף האקראית (Base64 HTML)
        try:
            component_type = result_context.component_type if result_context else None
            chart_html = RandomChartGenerator.generate_chart_image(component_type)
        except Exception as e:
            print(f"⚠️ Error generating chart: {e}")
            return ""

        # בחירת כותרת מתאימה לגרף
        caption = "Figure 1: Typical Performance Characteristics"

        # החזרת ה-HTML המלא עם התמונה והכותרת
        return f"""
        <div class="graph-container" style="margin: 25px auto; width: 80%; text-align: center; page-break-inside: avoid;">
            {chart_html}
            <div style="font-size: 13px; color: #555; margin-top: 8px; font-style: italic; font-family: sans-serif;">
                {caption}
            </div>
        </div>
        """

    def render(self, result: 'DatasheetResult', marketing_data: Dict,
               config: 'RenderingConfig') -> str:
        """
        ✅ FIXED: Fully synchronized render using pre-computed config and varied titles.
        ✅ ENHANCED: Now supports diverse visual themes, fonts, and table styles.
        """
        self.footnotes = []
        self.config = config  # Store for use in helper methods

        # 1. Visual Style Decisions (Randomized)
        watermark = random.choice(self.WATERMARKS)
        layout_class = random.choice(self.LAYOUT_CLASSES)

        # --- NEW VISUAL DIVERSITY ---
        fonts = [
            "'Times New Roman', serif", "'Courier New', monospace",
            "'Arial', sans-serif", "'Segoe UI', sans-serif", "'Helvetica', sans-serif"
        ]
        table_styles = ['minimalist', 'grid', 'striped', 'dense', 'standard']
        themes = ['legacy', 'infineon', 'onsemi', 'onsemi_navy', 'standard']

        selected_font = random.choice(fonts)
        selected_table_style = random.choice(table_styles)
        selected_theme = random.choice(themes)

        # Generate CSS with all parameters
        css_content = self._get_enhanced_css(
            watermark=watermark,
            font=selected_font,
            table_style=selected_table_style,
            theme=selected_theme
        )
        # ---------------------------

        # 3. Group Parameters by Section
        sections = {}
        for param in result.parameters:
            if param.section not in sections:
                sections[param.section] = []
            sections[param.section].append(param)

        # 4. Start Building HTML Body
        body_content = ""

        # Render Header & Features
        body_content += self._render_header(result, marketing_data)
        body_content += self._render_features_and_apps(marketing_data)

        # 5. Render Sections Loop
        sections_html = '<div class="sections-container">'

        section_struct_map = {
            "ABS_MAX": "max_ratings_only",
            "THERMAL": "thermal_data",
            "PACKAGE": "compact_commercial",
            "RELIABILITY": "standard_full"
        }

        # SUPER-HEADER POOL — שמות סקציה אמיתיים מ-datasheets (Vishay, Infineon, TI, OnSemi)
        # הוספת super-header ב-50% מהמקרים מדמה את מבנה ה-datasheets האמיתיים
        # שבהם row[0] = "ABSOLUTE MAXIMUM RATINGS (TC = 25°C)" ו-row[1] = "PARAMETER | SYMBOL | ..."
        _SUPER_HEADER_VARIANTS = {
            "ABS_MAX": [
                "Absolute Maximum Ratings (TC = 25 °C, unless otherwise noted)",
                "Absolute Maximum Ratings",
                "Abs. Max. Ratings (TA = 25 °C)",
                "Maximum Ratings (TC = 25 °C)",
                "Limiting Values",
            ],
            "THERMAL": [
                "Thermal Resistance Ratings",
                "Thermal Characteristics",
                "Thermal Data",
                "Thermal Information",
            ],
            "ELECTRICAL_CHARACTERISTICS": [
                "Electrical Characteristics (TJ = 25 °C, unless otherwise noted)",
                "Specifications (TJ = 25 °C, unless otherwise noted)",
                "DC Electrical Characteristics",
                "Static and Dynamic Characteristics",
            ],
        }

        # B6: probability of key-value format per component type
        _KV_PROBS = {"CAPACITOR": 0.40, "INDUCTOR": 0.30, "RESISTOR": 0.15}
        _comp_type = getattr(result.context, "component_type", "")

        for section_name, parameters in sections.items():
            # A. Determine table structure
            struct_key = section_struct_map.get(section_name, "standard_full")

            # B6: passives sometimes use key-value layout for electrical sections
            _ELEC_SECTIONS = {"ELEC_CHAR", "ELECTRICAL_CHARACTERISTICS", "DYNAMIC_CHAR", "STATIC_CHAR"}
            if (section_name in _ELEC_SECTIONS
                    and random.random() < _KV_PROBS.get(_comp_type, 0.0)):
                struct_key = "key_value"

            # Fresh random layout per section — each section gets independent augmentation flags
            layout_config = {
                "swap_symbol_position":  random.random() < 0.30,
                "merge_min_typ_max":     random.random() < 0.20,
                "use_alt_column_names":  random.random() < 0.40,
                "use_subheaders":        random.random() < 0.20,
                # קטגוריה 1 — מבנה טבלה "מלוכלך" כמו PDF אמיתי
                "use_super_header":      random.random() < 0.25,  # 1.3: כותרת-על ממוזגת
                "use_two_row_header":    random.random() < 0.20,  # 1.2: כותרת דו-שורתית (Value → Min/Typ/Max)
                "use_continuation_rows": random.random() < 0.25,  # 1.4: שורות המשך עם PARAMETER ריק
                "use_variant_columns":   random.random() < 0.10,  # 1.1: עמודות וריאנט (1N5817/18/19)
                # קטגוריה 2 — מיזוג תאים
                "use_merged_sub_rows":   random.random() < 0.15,  # 2.1: שני תת-פרמטרים בתא ערך אחד
                "use_merged_conditions": random.random() < 0.15,  # 2.2: שתי תנאות ממוזגות לשם פרמטר
                "use_symbol_prefix":     random.random() < 0.20,  # 2.3: סימבול לפני שם הפרמטר
                # קטגוריה 3 — עיצוב טקסט
                "use_unicode_subs":      random.random() < 0.25,  # 3.1: µ→u, °→deg, ±→+/-, Ω→ohm
                "use_symbol_flatten":    random.random() < 0.30,  # 3.2: V_DS → VDS / V DS
                "use_number_variants":   random.random() < 0.20,  # 3.3: 1000 → 1 000 / 1,000
                "use_condition_variants":random.random() < 0.25,  # 3.4: T_C=25°C → T_C = 25 °C
                # קטגוריה 4 — קידוד תווים והפניות
                "use_inline_linebreaks": random.random() < 0.20,  # 4.1: <br> באמצע שם פרמטר/תנאי ארוך
                "use_dash_variants":     random.random() < 0.30,  # 4.2: - → – או − (en-dash / minus)
                "use_footnote_markers":  random.random() < 0.20,  # 4.3: † *(1) ¹ אחרי ערכים
                # קטגוריה 5 — פורמטי ערכים
                "use_qualifier_labels":  random.random() < 0.25,  # 5.1: (typ) (nom) (max) אחרי ערך
                "use_inequality_prefix": random.random() < 0.15,  # 5.2: ≤ ≥ < > לפני ערך
                "use_tolerance_suffix":  random.random() < 0.15,  # 5.3: ±5% ±10% אחרי ערך
                "use_range_in_cell":     random.random() < 0.15,  # 5.4: "X to Y" בתא Max, Min ריק
                # קטגוריה 6 — שורות רעש
                "use_repeated_header":   random.random() < 0.15,  # 6.1: כותרת חוזרת באמצע הטבלה
                "use_note_rows":         random.random() < 0.25,  # 6.2: שורות הערה/הגבלה בין שורות
                "use_empty_sep_rows":    random.random() < 0.20,  # 6.3: שורות ריקות כמפרידים
                "use_continued_marker":  random.random() < 0.10,  # 6.4: שורת (Continued) בשבר עמוד
            }

            # B. Render the Table (using self.config internally)
            table_html = self._render_table(parameters, struct_key, layout_config, section_name)

            # ── Super-header injection (50% probability) ──────────────────
            # מדמה את מבנה ה-datasheets האמיתיים שבהם שורת הכותרות מקדימה
            # על ידי שורת super-header ממוזגת (כמו ב-Vishay, Infineon, TI).
            # ה-Aligner ו-Preprocessor כבר מטפלים בזה ב-inference —
            # כאן אנחנו מוסיפים אותו לנתוני האימון הסינתטיים.
            if random.random() < 0.5:
                variants = _SUPER_HEADER_VARIANTS.get(section_name)
                if variants:
                    super_title = random.choice(variants)
                    # חישוב מספר העמודות מה-table_html שנוצר
                    first_tr = re.search(r'<tr[^>]*>(.*?)</tr>', table_html, re.DOTALL)
                    n_cols = len(re.findall(r'<t[hd][^>]*>', first_tr.group(1))) if first_tr else 7
                    super_row = (
                        f"<tr class='super-header'>"
                        f"<th colspan='{n_cols}' style='text-align:left;font-weight:bold;'>"
                        f"{html.escape(super_title)}"
                        f"</th></tr>"
                    )
                    # הכנס את ה-super-header לפני השורה הראשונה של הטבלה
                    table_html = table_html.replace(
                        "<table><thead><tr>", f"<table><thead>{super_row}<tr>", 1
                    )

            # C. Get Section Intro Text
            intro = marketing_data.get("section_intros", {}).get(section_name, "")
            intro_html = f"<p><em>{html.escape(intro)}</em></p>" if intro else ""

            # D. Generate Graph/Chart
            graph_html = ""
            if any(x in section_name.upper() for x in ["ELEC", "CHAR", "TYPICAL", "PERFORMANCE"]):
                if hasattr(self, '_get_random_chart'):
                    graph_html = self._get_random_chart(result.context)
                else:
                    graph_html = self._get_random_image_placeholder(result.context)

            # E. Varied Section Title
            display_title = self._get_section_title_variant(section_name)

            # F. Assemble Section HTML
            sections_html += (
                f"<div class='section'>"
                f"<h2 class='section-title'>{html.escape(display_title)}</h2>"
                f"{intro_html}"
                f"{table_html}"
                f"{graph_html}"
                f"</div>"
            )

        sections_html += '</div>'
        body_content += sections_html

        # 6. Render Footnotes & Footer
        if self.footnotes:
            body_content += self._render_footnotes_section()

        body_content += self._render_footer(marketing_data)

        # 7. Final HTML Assembly
        return (
            f"<!DOCTYPE html>"
            f"<html>"
            f"<head>"
            f"<meta charset='UTF-8'>"
            f"<style>{css_content}</style>"
            f"</head>"
            f"<body class='{layout_class}'>"
            f"{body_content}"
            f"</body>"
            f"</html>"
        )

    def _render_header(self, result, marketing) -> str:
        header_type = random.choice(list(self.HEADER_STRUCTURES.keys()))
        config = self.HEADER_STRUCTURES[header_type]
        desc = marketing['description']
        desc_html = desc if ('<span' in desc and 'data-label' in desc) else html.escape(desc)
        data = {"sample_id": html.escape(result.context.sample_id),
                "manufacturer": html.escape(marketing['manufacturer']),
                "marketing_name": html.escape(marketing['marketing_name']),
                "description": desc_html, "package": html.escape(result.context.package),
                "archetype": html.escape(result.context.archetype)}
        return config["template"].format(**data)

    def _get_column_name_variant(self, base_name: str, use_alt: bool) -> str:
        if not use_alt: return base_name
        alternatives = {
            "Parameter": [
                "Characteristic", "Item", "Description", "Specification", "Spec.",
                "Parameter Name", "Feature", "Property", "Characteristics", "Param."
            ],
            "symbol": [
                "Sym.", "Symbol", "Notation", "Sym", "Ref.", "Code", "Designator"
            ],
            "Condition": [
                "Test Conditions", "Notes", "Conditions", "Remarks", "Comments",
                "Test Criteria", "Note", "Measurement Conditions", "@ Conditions"
            ],
            "Unit": [
                "Units", "Unit", "UoM", "Dimension", "Scale"
            ],
            "Min": [
                "Minimum", "Min.", "Min Limit", "Lower Limit", "Guaranteed Min.", "From"
            ],
            "Typ": [
                "Typical", "Typ.", "Nominal", "Nom.", "Typ. Val.", "Average", "Avg."
            ],
            "Max": [
                "Maximum", "Max.", "Max Limit", "Upper Limit", "Limit", "To", "Guaranteed Max."
            ],
            "Value": [
                "Rating", "Limit", "Value", "Spec Value", "Level", "Amount", "Data"
            ]
        }
        return random.choice(alternatives.get(base_name, [base_name]))

    def _render_table(self, parameters: List[Any], structure_key: str, layout_config: Dict, section_name: str = "") -> str:
        # B6: key-value table (capacitor/inductor/resistor style) — highest priority dispatch
        if structure_key == "key_value":
            return self._render_key_value_table(parameters)

        # Fix 1.1: טבלת וריאנטים — ענף נפרד
        if layout_config.get("use_variant_columns"):
            return self._render_variant_table(parameters, layout_config, section_name)

        # טבלה טרנספוזית — ענף נפרד
        if self.config and section_name in self.config.transposed_sections:
            return self._render_transposed_table(parameters)

        cols = list(self.TABLE_STRUCTURES.get(
            structure_key,
            {"columns": ["Parameter", "symbol", "Min", "Typ", "Max", "Unit", "Condition"]}
        )["columns"])

        if self.config and self.config.hidden_columns:
            cols = [c for c in cols if c not in self.config.hidden_columns]

        if layout_config.get("swap_symbol_position") and "symbol" in cols and "Parameter" in cols:
            try:
                p_idx, s_idx = cols.index("Parameter"), cols.index("symbol")
                cols[p_idx], cols[s_idx] = cols[s_idx], cols[p_idx]
            except ValueError:
                pass

        if layout_config.get("merge_min_typ_max") and all(c in cols for c in ["Min", "Typ", "Max"]):
            cols = [c for c in cols if c not in ["Min", "Typ", "Max"]]
            target_idx = cols.index("Unit") if "Unit" in cols else len(cols)
            cols.insert(target_idx, "Min/Typ/Max")

        display_cols = [
            (col, self._get_column_name_variant(col, layout_config.get("use_alt_column_names")))
            for col in cols
        ]

        n_cols = len(display_cols)

        # Fix 1.3: כותרת-על ממוזגת (Super-header) — שורה שכוללת את שם הסקציה לפני עמודות
        if layout_config.get("use_super_header") and section_name:
            html_output = (
                f"<table><thead>"
                f"<tr><th colspan='{n_cols}'>{html.escape(section_name)}</th></tr>"
                f"<tr>"
            )
        else:
            html_output = "<table><thead><tr>"

        # Fix 1.2: כותרת דו-שורתית — שורה 1: "Value" כולל colspan על Min/Typ/Max,
        #           שורה 2: שמות עמודות בפועל. מדמה את דפוס 2SC5994 / ON Semi.
        _has_mtm = all(c in [col for col, _ in display_cols] for c in ["Min", "Typ", "Max"])
        if layout_config.get("use_two_row_header") and _has_mtm:
            # שורה 1
            for col, name in display_cols:
                if col == "Min":
                    html_output += "<th colspan='3'>Value</th>"
                elif col in ("Typ", "Max"):
                    continue
                else:
                    html_output += f"<th>{html.escape(name)}</th>"
            html_output += "</tr><tr>"
            # שורה 2 — כל עמודה בנפרד
            for _, name in display_cols:
                html_output += f"<th>{html.escape(name)}</th>"
        else:
            for _, name in display_cols:
                html_output += f"<th>{html.escape(name)}</th>"

        html_output += "</tr></thead><tbody>"

        prev_cat = None
        prev_param_name = ""   # Fix 1.4: מעקב אחר שם הפרמטר הקודם לשורות המשך
        _n, _i = len(parameters), 0
        while _i < _n:
            param      = parameters[_i]
            next_param = parameters[_i + 1] if _i + 1 < _n else None

            # Fix 2.1: שני תת-פרמטרים (שמות זהים, סמלים שונים) → שורה אחת עם שני ערכים
            if (layout_config.get("use_merged_sub_rows")
                    and next_param is not None
                    and getattr(param, "label", None) == getattr(next_param, "label", None)
                    and str(getattr(param, "symbol", "")) != str(getattr(next_param, "symbol", ""))
                    and random.random() < 0.35):
                html_output += self._render_merged_sub_row(param, next_param, display_cols)
                prev_param_name = str(getattr(param, "label", ""))
                _i += 2
                continue

            # Fix 2.2: שתי שורות עם אותו מפתח ותנאות שונות → שם פרמטר ממוזג
            if (layout_config.get("use_merged_conditions")
                    and next_param is not None
                    and getattr(param, "key", None) == getattr(next_param, "key", None)
                    and getattr(param, "condition", "") and getattr(next_param, "condition", "")
                    and getattr(param, "condition", "") != getattr(next_param, "condition", "")
                    and random.random() < 0.25):
                html_output += self._render_merged_conditions_row(param, next_param, display_cols)
                prev_param_name = str(getattr(param, "label", ""))
                _i += 2
                continue

            if layout_config.get("use_subheaders"):
                curr_cat = getattr(param, 'category', None) or getattr(param, 'section', None)
                if curr_cat and curr_cat != prev_cat:
                    html_output += (
                        f"<tr class='subheader'>"
                        f"<td colspan='{len(cols)}'>"
                        f"{html.escape(curr_cat.replace('_', ' ').title())}"
                        f"</td></tr>"
                    )
                    prev_cat = curr_cat

            row_data = self._format_row(param)
            metadata = row_data.get("_metadata", {})
            unit_format = metadata.get("unit_format", "separated")
            param_key = metadata.get("key", "")
            _symbol_val = str(row_data.get("symbol") or "")  # Fix 2.3

            # Fix 1.4: שורת המשך — PARAMETER ריק כשהפרמטר זהה לשורה הקודמת
            curr_param_name = str(row_data.get("Parameter") or "")
            use_empty_param = (
                layout_config.get("use_continuation_rows")
                and bool(prev_param_name)
                and curr_param_name == prev_param_name
            )
            prev_param_name = curr_param_name

            # Fix 5.4: row-level decision — merge Min+Max into range cell
            _use_range_this_row = (
                layout_config.get("use_range_in_cell")
                and any(c == "Min" for c, _ in display_cols)
                and any(c == "Max" for c, _ in display_cols)
                and metadata.get("raw_min") is not None
                and metadata.get("raw_max") is not None
                and random.random() < 0.30
            )

            # Fix Cat 6: noise rows before this parameter row
            html_output += self._cat6_noise_rows(
                _i, _n, param,
                parameters[_i - 1] if _i > 0 else None,
                display_cols, layout_config,
            )

            html_output += (
                f'<tr data-key="{param_key}" '
                f'data-class="{metadata.get("engineering_class", "")}" '
                f'data-unit-format="{unit_format}">'
            )

            for logical_col, _ in display_cols:
                # --- 1. מציאת הערך הרלוונטי ---
                if logical_col == "Min/Typ/Max":
                    min_str = row_data.get('Min') or "—"
                    typ_str = row_data.get('Typ') or "—"
                    max_str = row_data.get('Max') or "—"
                    val = f"{min_str} / {typ_str} / {max_str}"
                elif logical_col == "Value":
                    val = row_data.get("Value") or row_data.get("Max") or row_data.get("Typ") or "—"
                else:
                    val = row_data.get(logical_col)

                # נרמול הגנה: הפיכת ערך ריק למקף
                if val is None or str(val).strip() == "":
                    val = "—"

                # --- 2. מקרים מיוחדים (יוצאים עם continue) ---
                # FIX Bug 4: structural column-header words must not appear as CONDITION entities.
                # "Max", "Typical" etc. come from compact_commercial column-model encoding —
                # they are NOT test conditions and should not be tagged or stored as such.
                if val != "—":
                    if logical_col == "Condition":
                        if str(val) in self._STRUCTURAL_CONDITIONS:
                            # Emit as plain untagged text so the model doesn't learn
                            # column-header words as valid CONDITION entities
                            html_output += f"<td>{html.escape(str(val))}</td>"
                            continue
                        elif len(str(val)) > getattr(self.config, 'long_condition_threshold', 50):
                            tagged = f'<span data-label="{param_key}_condition">{html.escape(str(val))}</span>'
                            self.footnotes.append(tagged)
                            html_output += f"<td><span class='note-ref'>(Note {len(self.footnotes)})</span></td>"
                        else:
                            _dc3 = self._cat3_dirty(str(val), "condition", layout_config)
                            _dc4, _cfm = self._cat4_dirty(_dc3, "condition", layout_config)
                            html_output += f'<td><span data-label="{param_key}_condition">{_dc4}</span>{_cfm}</td>'
                        continue

                    elif logical_col == "Unit" and unit_format == "combined":
                        # FIX: When unit_format=combined the unit is already
                        # embedded inside the value cell (e.g. "0.25mW").
                        # Rendering it AGAIN here with a separate unit-tag span
                        # causes the aligner to see the same string twice — once
                        # as part of the VALUE entity and once as a standalone
                        # UNIT entity — which corrupts BIO training.
                        # Solution: emit only the tagged span, no duplicate.
                        _du = self._cat3_dirty(str(val), "unit", layout_config)
                        html_output += (
                            f'<td>'
                            f'<span class="unit-tag" data-label="{param_key}_unit">{html.escape(_du)}</span>'
                            f'</td>'
                        )
                        continue

                    elif logical_col in ["Min", "Typ", "Max"]:
                        col_lower = logical_col.lower()

                        # Fix 5.4: Range in cell — Min→"—", Max→"minVal sep maxVal"
                        if _use_range_this_row:
                            if logical_col == "Min":
                                html_output += "<td>—</td>"
                                continue
                            elif logical_col == "Max":
                                _rm = metadata.get("raw_min")
                                _rx = metadata.get("raw_max")
                                _sep = random.choice([' to ', ' ~ ', ' / ', '–'])
                                _dm3 = self._cat3_dirty(str(_rm), "value", layout_config)
                                _dm4, _ = self._cat4_dirty(_dm3, "value", layout_config)
                                _dx3 = self._cat3_dirty(str(_rx), "value", layout_config)
                                _dx4, _xfm = self._cat4_dirty(_dx3, "value", layout_config)
                                html_output += (
                                    f'<td>'
                                    f'<span class="val-tag" data-label="{param_key}_min">{_dm4}</span>'
                                    f'{html.escape(_sep)}'
                                    f'<span class="val-tag" data-label="{param_key}_max">{_dx4}</span>{_xfm}'
                                    f'</td>'
                                )
                                continue

                        raw_val = metadata.get(f"raw_{col_lower}")
                        if raw_val and str(raw_val) in str(val):
                            unique_id = f"{param_key}_{col_lower}"
                            _dv3 = self._cat3_dirty(str(raw_val), "value", layout_config)
                            _dv4, _vfm = self._cat4_dirty(_dv3, "value", layout_config)

                            # Fix 5.2: Inequality prefix for limit values
                            _ineq = ''
                            if layout_config.get("use_inequality_prefix") and random.random() < 0.30:
                                if col_lower == "max":
                                    _ineq = random.choice(['≤ ', html.escape('< '), 'max '])
                                elif col_lower == "min":
                                    _ineq = random.choice(['≥ ', html.escape('> '), 'min '])

                            # Fix 5.3: Tolerance suffix
                            _tol = ''
                            if layout_config.get("use_tolerance_suffix") and random.random() < 0.25:
                                _tol = random.choice([' ±1%', ' ±5%', ' ±10%', ' ±15%'])

                            # Fix 5.1: Qualifier label
                            _qual = ''
                            if layout_config.get("use_qualifier_labels") and random.random() < 0.30:
                                if col_lower == "typ":
                                    _qual = random.choice([' (typ)', ' (nom)', ' (typical)'])
                                elif col_lower == "min":
                                    _qual = random.choice([' (min)', ' (min.)'])
                                elif col_lower == "max":
                                    _qual = random.choice([' (max)', ' (max.)'])

                            html_output += (
                                f'<td>'
                                f'{_ineq}'
                                f'<span class="val-tag" data-label="{unique_id}">{_dv4}</span>'
                                f'{_tol}{_qual}{_vfm}'
                                f'</td>'
                            )
                            continue

                # --- 3. זרימה רגילה לכל שאר המקרים ---
                if val == "—":
                    html_output += "<td>—</td>"
                    continue

                # Fix Cat 3: text-formatting artifacts on symbol and unit columns
                _val_str = str(val)
                if logical_col == "symbol":
                    _val_str = self._cat3_dirty(_val_str, "symbol", layout_config)
                elif logical_col == "Unit":
                    _val_str = self._cat3_dirty(_val_str, "unit", layout_config)
                display_val = _val_str if logical_col == "symbol" else html.escape(_val_str)

                if logical_col == "Parameter":
                    # Fix 1.4: שורת המשך — תא ריק כשהפרמטר זהה לשורה הקודמת
                    if use_empty_param:
                        html_output += "<td></td>"
                    else:
                        # Fix Cat 4.1: inline line break in long parameter names
                        _p4, _ = self._cat4_dirty(str(val), "parameter", layout_config)
                        if layout_config.get("use_symbol_prefix") and _symbol_val:
                            # Fix 2.3: סמבול לא-מתויג לפני שם הפרמטר
                            html_output += (
                                f'<td>{html.escape(_symbol_val)} '
                                f'<span data-label="PARAMETER">{_p4}</span></td>'
                            )
                        else:
                            html_output += f'<td><span data-label="PARAMETER">{_p4}</span></td>'
                elif logical_col == "symbol":
                    html_output += f'<td><span data-label="{param_key}_symbol">{html.escape(str(val))}</span></td>'
                elif logical_col in ["Min", "Typ", "Max", "Value", "Min/Typ/Max"]:
                    clean_col = logical_col.lower().replace("/", "_")
                    html_output += f'<td><span class="val-tag" data-label="{param_key}_{clean_col}">{display_val}</span></td>'
                elif logical_col == "Unit":
                    html_output += f'<td><span class="unit-tag" data-label="{param_key}_unit">{display_val}</span></td>'
                else:
                    html_output += f"<td>{display_val}</td>"

            html_output += "</tr>"
            _i += 1

        return html_output + "</tbody></table>"


    @staticmethod
    def _cat6_noise_rows(i: int, n: int, param, prev_param, display_cols: list, lc: dict) -> str:
        """Cat 6: noise rows inserted before parameter row i (repeated headers, notes, separators)."""
        noise = ''
        n_cols = len(display_cols)

        # 6.3: Empty separator — between different sections, or occasionally at random
        if lc.get("use_empty_sep_rows"):
            prev_sec = getattr(prev_param, 'section', None) if prev_param else None
            curr_sec = getattr(param,      'section', None)
            if prev_sec and prev_sec != curr_sec and random.random() < 0.55:
                noise += '<tr>' + '<td></td>' * n_cols + '</tr>'
            elif i > 0 and random.random() < 0.05:
                noise += '<tr>' + '<td></td>' * n_cols + '</tr>'

        # 6.1: Repeated header row at table midpoint (fires once)
        if lc.get("use_repeated_header") and i == max(1, n // 2) and random.random() < 0.65:
            hrow = '<tr class="repeat-header">'
            for _, col_name in display_cols:
                hrow += f'<th>{html.escape(col_name)}</th>'
            hrow += '</tr>'
            noise += hrow

        # 6.2: Note/footnote row — sparse, any inter-row position
        if lc.get("use_note_rows") and i > 0 and random.random() < 0.08:
            noise += (
                f'<tr class="note-row">'
                f'<td colspan="{n_cols}">'
                f'{html.escape(random.choice(DatasheetHtmlRenderer._NOTE_TEXTS))}</td>'
                f'</tr>'
            )

        # 6.4: "(Continued)" marker fires once near 65% of the table
        if lc.get("use_continued_marker") and i == max(1, int(n * 0.65)) and random.random() < 0.60:
            noise += (
                f'<tr class="continued-row">'
                f'<td colspan="{n_cols}">(Continued)</td>'
                f'</tr>'
            )

        return noise

    @staticmethod
    def _cat4_dirty(text: str, ttype: str, lc: dict) -> tuple:
        """Cat 4: PDF encoding & reference artifacts. Returns (html_content, footnote_suffix)."""
        s = str(text)

        # 4.2 Dash/hyphen variants — apply BEFORE html.escape so the char itself gets escaped
        if ttype in ("value", "condition") and lc.get("use_dash_variants"):
            if '-' in s and random.random() < 0.55:
                s = s.replace('-', random.choice(['–', '−', '-']), 1)

        s = html.escape(s)

        # 4.1 Inline line break — apply AFTER html.escape so <br> is not escaped
        if ttype in ("parameter", "condition") and lc.get("use_inline_linebreaks"):
            if len(s) > 15 and random.random() < 0.40:
                mid = len(s) // 2
                sp = s.find(' ', max(0, mid - 8))
                if sp > 0:
                    s = s[:sp] + '<br>' + s[sp + 1:]

        # 4.3 Footnote marker — appended outside the span by the caller
        footnote = ''
        if lc.get("use_footnote_markers") and random.random() < 0.22:
            if ttype == "value":
                footnote = random.choice(['†', ' *', '<sup>(1)</sup>', '¹'])
            elif ttype == "condition":
                footnote = random.choice([' (1)', ' *', '†'])

        return s, footnote

    @staticmethod
    def _cat3_dirty(text: str, ttype: str, lc: dict) -> str:
        """Cat 3: apply realistic text-formatting artifacts to visible span content."""
        s = text

        # 3.1 Unicode substitutions — units, symbols, conditions
        if ttype in ("unit", "symbol", "condition") and lc.get("use_unicode_subs"):
            _SUBS = [
                ('µ', ['u', 'μ', 'u']),
                ('°', ['deg ', 'deg', '°']),
                ('±', ['+/-', '+/-', '±']),
                ('Ω', ['ohm', 'Ohm', 'R']),
                ('×', ['x', 'X']),
                ('θ', ['th', 'theta', 'θ']),
            ]
            for orig, choices in _SUBS:
                if orig in s and random.random() < 0.70:
                    s = s.replace(orig, random.choice(choices))

        # 3.2 Subscript flattening — symbol cells only
        if ttype == "symbol" and lc.get("use_symbol_flatten") and random.random() < 0.65:
            sep = random.choice(['', ' '])
            s = re.sub(r'_([A-Za-z0-9]+)', sep + r'\1', s)

        # 3.3 Number format variants — value cells
        if ttype == "value" and lc.get("use_number_variants") and random.random() < 0.55:
            try:
                f = float(s)
                if f >= 1000 and '.' not in s and 'e' not in s.lower():
                    tsep = random.choice([' ', ','])
                    s = format(int(f), ',').replace(',', tsep)
                elif abs(f) < 0.001 and f != 0:
                    s = random.choice([f'{f:.2e}', f'{f:.2E}', f'{f:.3e}'])
            except ValueError:
                pass

        # 3.4 Condition text variants — spacing and case around "="
        if ttype == "condition" and lc.get("use_condition_variants"):
            if '=' in s and random.random() < 0.55:
                s = re.sub(r'\s*=\s*', random.choice([' = ', '= ', ' =']), s)
            if random.random() < 0.40:
                s = re.sub(r'T_([A-Z])', lambda m: random.choice([
                    f'T_{m.group(1)}', f'T{m.group(1)}', f't{m.group(1).lower()}'
                ]), s)

        return s

    def _render_merged_sub_row(self, p1, p2, display_cols):
        """Fix 2.1: שני תת-פרמטרים (Rθ JA / Rθ JC) → שורה אחת, ערכים ממוזגים בתא."""
        rd1, rd2 = self._format_row(p1), self._format_row(p2)
        m1,  m2  = rd1.get("_metadata", {}), rd2.get("_metadata", {})
        pk1, pk2 = m1.get("key", ""), m2.get("key", "")
        param_name = str(rd1.get("Parameter") or "—")
        symbol     = f"{rd1.get('symbol', '—')} {rd2.get('symbol', '—')}"
        unit       = str(rd1.get("Unit") or rd2.get("Unit") or "—")
        v1 = m1.get("raw_max") or m1.get("raw_typ") or m1.get("raw_min") or "—"
        v2 = m2.get("raw_max") or m2.get("raw_typ") or m2.get("raw_min") or "—"
        row_html = f'<tr data-key="{pk1}">'
        for col, _ in display_cols:
            if col == "Parameter":
                row_html += f'<td><span data-label="PARAMETER">{html.escape(param_name)}</span></td>'
            elif col == "symbol":
                row_html += f'<td><span data-label="{pk1}_symbol">{html.escape(symbol)}</span></td>'
            elif col == "Max":
                s1 = (f'<span class="val-tag" data-label="{pk1}_max">{html.escape(str(v1))}</span>'
                      if v1 != "—" else "—")
                s2 = (f'<span class="val-tag" data-label="{pk2}_max">{html.escape(str(v2))}</span>'
                      if v2 != "—" else "—")
                row_html += f"<td>{s1} {s2}</td>"
            elif col in ("Min", "Typ", "Condition"):
                row_html += "<td>—</td>"
            elif col == "Unit":
                row_html += (
                    f'<td><span class="unit-tag" data-label="{pk1}_unit">'
                    f'{html.escape(unit)}</span></td>'
                )
            else:
                row_html += "<td>—</td>"
        return row_html + "</tr>"

    def _render_merged_conditions_row(self, p1, p2, display_cols):
        """Fix 2.2: שתי תנאות ממוזגות לשם הפרמטר (כמו 'I_D T_C=25°C T_C=100°C')."""
        rd1 = self._format_row(p1)
        m1  = rd1.get("_metadata", {})
        pk1 = m1.get("key", "")
        param_name = str(rd1.get("Parameter") or "—")
        cond1 = str(rd1.get("Condition") or "")
        cond2 = str(self._format_row(p2).get("Condition") or "")
        merged_name = f"{param_name} {cond1} {cond2}".strip()
        unit = str(rd1.get("Unit") or "—")
        v1   = m1.get("raw_max") or m1.get("raw_typ") or m1.get("raw_min")
        row_html = f'<tr data-key="{pk1}">'
        for col, _ in display_cols:
            if col == "Parameter":
                row_html += f'<td><span data-label="PARAMETER">{html.escape(merged_name)}</span></td>'
            elif col == "symbol":
                row_html += f'<td>{html.escape(str(rd1.get("symbol", "—")))}</td>'
            elif col == "Max":
                if v1:
                    row_html += (
                        f'<td><span class="val-tag" data-label="{pk1}_max">'
                        f'{html.escape(str(v1))}</span></td>'
                    )
                else:
                    row_html += "<td>—</td>"
            elif col in ("Min", "Typ", "Condition"):
                row_html += "<td></td>"
            elif col == "Unit":
                row_html += (
                    f'<td><span class="unit-tag" data-label="{pk1}_unit">'
                    f'{html.escape(unit)}</span></td>'
                )
            else:
                row_html += "<td>—</td>"
        return row_html + "</tr>"

    def _render_variant_table(self, parameters: List[Any], layout_config: Dict, section_name: str = "") -> str:
        """
        Fix 1.1: טבלת וריאנטים — עמודות מספרי חלק במקום MIN/TYP/MAX.
        מדמה datasheets כמו 1N5817/1N5818/1N5819 של Vishay.
        """
        _VARIANT_FAMILIES = [
            ["1N5817", "1N5818", "1N5819"],
            ["BC546",  "BC547",  "BC548"],
            ["TL071",  "TL072",  "TL074"],
            ["LM358",  "LM358A", "LM358B"],
            ["BAS16",  "BAS17",  "BAS18"],
            ["2N3903", "2N3904", "2N3905"],
            ["BAV99",  "BAV99A"],
            ["TL431A", "TL431B"],
        ]
        _MULTS_2 = [0.67, 1.00]
        _MULTS_3 = [0.60, 1.00, 1.50]

        family     = random.choice(_VARIANT_FAMILIES)
        n_variants = min(len(family), random.choice([2, 3]))
        variants   = family[:n_variants]
        mults      = _MULTS_2 if n_variants == 2 else _MULTS_3
        tag_roles  = ["min", "max"] if n_variants == 2 else ["min", "typ", "max"]

        cols_display = ["Parameter", "Symbol"] + variants + ["Unit"]
        n_cols       = len(cols_display)

        # Fix 1.3 יכול לשלב גם עם 1.1
        if layout_config.get("use_super_header") and section_name:
            html_output = (
                f"<table><thead>"
                f"<tr><th colspan='{n_cols}'>{html.escape(section_name)}</th></tr>"
                f"<tr>"
            )
        else:
            html_output = "<table><thead><tr>"

        for col in cols_display:
            html_output += f"<th>{html.escape(col)}</th>"
        html_output += "</tr></thead><tbody>"

        prev_param_name = ""
        for param in parameters:
            row_data  = self._format_row(param)
            metadata  = row_data.get("_metadata", {})
            param_key = metadata.get("key", "")

            param_name = str(row_data.get("Parameter") or "—")
            symbol     = str(row_data.get("symbol")    or "—")
            unit_val   = str(row_data.get("Unit")      or "—")

            base_str = (
                metadata.get("raw_max") or
                metadata.get("raw_typ") or
                metadata.get("raw_min")
            )

            # Fix 1.4 אפשרי גם בתוך טבלת וריאנטים
            use_empty_param = (
                layout_config.get("use_continuation_rows")
                and bool(prev_param_name)
                and param_name == prev_param_name
            )
            prev_param_name = param_name

            html_output += f'<tr data-key="{param_key}">'

            # עמודת Parameter
            if use_empty_param:
                html_output += "<td></td>"
            else:
                html_output += (
                    f'<td><span data-label="PARAMETER">'
                    f'{html.escape(param_name)}</span></td>'
                )

            # עמודת Symbol
            html_output += (
                f'<td><span data-label="{param_key}_symbol">'
                f'{html.escape(symbol)}</span></td>'
            )

            # עמודות וריאנט
            for vi, (vname, mult, role) in enumerate(zip(variants, mults, tag_roles)):
                if base_str:
                    try:
                        base_f   = float(base_str)
                        var_f    = base_f * mult
                        decimals = len(base_str.split(".")[-1]) if "." in base_str else 0
                        var_str  = str(round(var_f, decimals)) if decimals else str(int(round(var_f)))
                    except (ValueError, TypeError):
                        var_str = base_str
                else:
                    var_str = "—"

                if var_str != "—":
                    html_output += (
                        f'<td><span class="val-tag" data-label="{param_key}_{role}">'
                        f'{html.escape(var_str)}</span></td>'
                    )
                else:
                    html_output += "<td>—</td>"

            # עמודת Unit
            if unit_val != "—":
                html_output += (
                    f'<td><span class="unit-tag" data-label="{param_key}_unit">'
                    f'{html.escape(unit_val)}</span></td>'
                )
            else:
                html_output += "<td>—</td>"

            html_output += "</tr>"

        return html_output + "</tbody></table>"


    # =========================================================================
    # B6 — Key-value table renderer (capacitor / inductor / resistor style)
    # =========================================================================

    def _build_kv_value_cell(self, param_key: str, raw_min, raw_typ, raw_max, unit: str) -> str:
        """Build an inline value+unit string with data-label spans for a key-value cell."""
        def span(val, role):
            return f'<span data-label="{param_key}_{role}">{html.escape(str(val))}</span>'

        unit_span = span(unit, "unit") if unit and str(unit).strip() else ""

        if raw_min is not None and raw_max is not None:
            sep = random.choice([" to ", " ~ ", " – ", "–"])
            if random.random() < 0.70:
                return f"{span(raw_min, 'min')}{sep}{span(raw_max, 'max')}{unit_span}"
            else:
                u = html.escape(str(unit))
                return f"{span(raw_min, 'min')}{u}{sep}{span(raw_max, 'max')}{unit_span}"

        if raw_typ is not None:
            return f"{span(raw_typ, 'typ')}{(' ' if unit_span else '')}{unit_span}"

        if raw_max is not None:
            prefix = random.choice(["", "≤ ", "Max. "])
            return f"{prefix}{span(raw_max, 'max')}{(' ' if unit_span else '')}{unit_span}"

        if raw_min is not None:
            prefix = random.choice(["", "≥ ", "Min. "])
            return f"{prefix}{span(raw_min, 'min')}{(' ' if unit_span else '')}{unit_span}"

        return "—"

    def _render_key_value_table(self, parameters: List[Any]) -> str:
        """B6: 2-column key-value table common in capacitor/inductor datasheets.

        Generates rows like:
          Item                    | Performance Characteristics
          Temperature Range       | -40 to +105°C
          Rated Voltage Range     | 6.3 to 50V

        Embeds MIN/TYP/MAX/UNIT data-label spans inside the value cell so the
        NER model learns to parse inline range strings rather than discrete columns.
        """
        _COL1_NAMES = ["Item", "Parameter", "Characteristic", "Specification", "Property"]
        _COL2_NAMES = [
            "Performance Characteristics", "Specifications", "Rated Value",
            "Specification Value", "Rated Specifications", "Performance Spec.",
        ]
        col1 = random.choice(_COL1_NAMES)
        col2 = random.choice(_COL2_NAMES)

        if random.random() < 0.50:
            super_titles = [
                "General Specifications", "Electrical Specifications",
                "Performance Characteristics", "Rated Specifications",
            ]
            super_title = random.choice(super_titles)
            html_output = (
                f"<table><thead>"
                f"<tr><th colspan='2'>{html.escape(super_title)}</th></tr>"
                f"<tr><th>{html.escape(col1)}</th><th>{html.escape(col2)}</th></tr>"
                f"</thead><tbody>"
            )
        else:
            html_output = (
                f"<table><thead>"
                f"<tr><th>{html.escape(col1)}</th><th>{html.escape(col2)}</th></tr>"
                f"</thead><tbody>"
            )

        for param in parameters:
            row_data  = self._format_row(param)
            metadata  = row_data.get("_metadata", {})
            param_key = metadata.get("key", "")

            param_name = str(row_data.get("Parameter") or "—")
            unit_val   = str(row_data.get("Unit") or "")
            raw_min    = metadata.get("raw_min")
            raw_typ    = metadata.get("raw_typ")
            raw_max    = metadata.get("raw_max")

            value_cell = self._build_kv_value_cell(
                param_key, raw_min, raw_typ, raw_max, unit_val
            )

            html_output += (
                f"<tr>"
                f'<td><span data-label="PARAMETER">{html.escape(param_name)}</span></td>'
                f"<td>{value_cell}</td>"
                f"</tr>"
            )

        return html_output + "</tbody></table>"

    def _render_footer(self, marketing):
        notes = "".join([f"<li>{html.escape(n)}</li>" for n in marketing.get('footnotes', [])])
        return f"<div class='footer-notes'><h3>Notes:</h3><ul>{notes}</ul></div>"
