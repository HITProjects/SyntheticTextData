"""generators.py — thin orchestrator. All classes moved to separate modules."""
import random
import json
import re
import html
import copy

from typing import Dict, Any, List, Optional, TYPE_CHECKING
from dataclasses import asdict

from synthetic_pipeline.package_characterizer import PackageCharacterizer
from synthetic_pipeline.base_renderer import BaseDatasheetRenderer, HtmlRenderingConstants, RenderingConfig
from synthetic_pipeline.marketing_generator import MarketingSentenceBuilder, MarketingGenerator
from synthetic_pipeline.augmentors import TextDegradationAugmentor, ScanAugmentor, RandomChartGenerator
from synthetic_pipeline.html_renderer import DatasheetHtmlRenderer
from synthetic_pipeline.json_renderer import DatasheetJSONRenderer

if TYPE_CHECKING:
    from synthetic_pipeline.data_types import DatasheetResult


def _generate_nlg_for_params(params: List) -> str:
    """
    ✅ UNIFIED & ENHANCED:
    1. Maximum diversity with 40+ sentence templates (Context Aware).
    2. Varied unit formatting ("5 V", "5V", "5 of volts", etc.).
    3. Full HTML tagging for BIO training.
    """
    sentences = []
    base_renderer = BaseDatasheetRenderer()

    # === רכיבי בניית משפטים מודולריים ===

    OPENERS = [
        "The device features",
        "This component specifies",
        "The datasheet indicates",
        "Critical to performance is",
        "Notably,",
        "Of particular importance,",
        "Key specifications include",
        "Engineering requirements define",
        "The component exhibits",
        "Design parameters specify",
        "Operating characteristics include",
        "Electrical specifications confirm",
        "Functional requirements establish",
        "Performance metrics show",
        "Technical documentation states",
    ]

    VERBS_PRESENT = [
        "features", "specifies", "provides", "delivers",
        "exhibits", "maintains", "guarantees", "ensures",
        "demonstrates", "achieves", "supports", "offers"
    ]

    VERBS_RATED = [
        "rated at", "specified at", "measured at", "characterized by",
        "defined as", "established at", "set at", "calibrated to",
        "verified at", "tested at", "qualified for"
    ]

    CONNECTORS = [
        "of", "at", "with", "measuring", "reaching", "achieving"
    ]

    QUALIFIERS = [
        "", "a nominal", "an operating", "a typical", "a maximum",
        "a specified", "a guaranteed", "a measured", "an optimal"
    ]

    # === פונקציות עזר לזיהוי טיפוס פרמטר ===

    def is_voltage(param_name: str) -> bool:
        """זיהוי פרמטרי מתח"""
        voltage_keywords = ['voltage', 'vdd', 'vcc', 'vgs', 'vds', 'vbe', 'supply', 'vce']
        return any(kw in param_name.lower() for kw in voltage_keywords)

    def is_current(param_name: str) -> bool:
        """זיהוי פרמטרי זרם"""
        current_keywords = ['current', 'idd', 'icc', 'iq', 'id', 'ib', 'ic', 'drain', 'collector']
        return any(kw in param_name.lower() for kw in current_keywords)

    def is_resistance(param_name: str) -> bool:
        """זיהוי פרמטרי התנגדות"""
        resistance_keywords = ['resistance', 'impedance', 'rds', 'ron', 'rth', 'thermal']
        return any(kw in param_name.lower() for kw in resistance_keywords)

    def is_timing(param_name: str) -> bool:
        """זיהוי פרמטרי זמן"""
        timing_keywords = ['time', 'delay', 'rise', 'fall', 'propagation', 'setup', 'hold', 'period']
        return any(kw in param_name.lower() for kw in timing_keywords)

    def is_frequency(param_name: str) -> bool:
        """זיהוי פרמטרי תדר"""
        freq_keywords = ['frequency', 'bandwidth', 'rate', 'clock', 'speed']
        return any(kw in param_name.lower() for kw in freq_keywords)

    # === לולאת עיבוד הפרמטרים ===

    for param in params:
        row_data = base_renderer._format_row(param)
        metadata = row_data.get("_metadata", {})

        param_name = row_data["Parameter"]
        value = row_data.get("Typ") or row_data.get("Max") or row_data.get("Min") or "—"

        unit = row_data.get("Unit", "")
        param_key = metadata.get("key", "unknown")

        # Determine which column the value came from
        value_col = "typ" if row_data.get("Typ") else ("max" if row_data.get("Max") else "min")
        raw_value = metadata.get(f"raw_{value_col}") or value

        # ==========================================
        # ✅ FIX: Noise Injection (Broken Words & Special Chars)
        # ==========================================
        # 1. שבירת מילים עם מקף (Volt- age) ב-10% מהמקרים
        if random.random() < 0.10 and len(param_name) > 5:
            split_idx = len(param_name) // 2
            param_name = param_name[:split_idx] + "- " + param_name[split_idx:]

        # 2. הוספת תווים יווניים מיוחדים לשמות (כמו RθJC)
        if "Thermal" in param_name or "Resistance" in param_name:
            if random.random() < 0.3:
                param_name = param_name.replace("th", "θ").replace("Thermal", "Rθ")

        # ==========================================
        # ✅ FIX: Unit Formatting & Concatenation (Entity Bleeding)
        # ==========================================
        unit_style = random.random()
        value_unit_phrase = ""
        unit_connector = ""

        # יצירת תגים (שומר על ה-BIO)
        tagged_value = f'<span class="nlg-val" data-label="{param_key}_{value_col}">{html.escape(str(raw_value))}</span>'

        tagged_unit = f'<span class="nlg-unit" data-label="{param_key}_unit">{html.escape(str(unit))}</span>'
        tagged_param = f'<span class="nlg-param" data-label="PARAMETER">{html.escape(param_name)}</span>'


        if unit_style < 0.20:
            # הכל דבוק לגמרי ללא רווחים (VoltageMin.55V)
            value_unit_phrase = f"{tagged_value}{tagged_unit}"
            tagged_param = f"{tagged_param}{random.choice(['.', ':', ''])}"
            connector_space = ""
        elif unit_style < 0.50:
            # ערך ויחידה דבוקים (55V)
            value_unit_phrase = f"{tagged_value}{tagged_unit}"
            connector_space = " "
        elif unit_style < 0.75:
            # טווחים עם טילדה (2.0 ~ 4.0 V)
            if row_data.get("Min") and row_data.get("Max"):
                t_min = f'<span class="nlg-val" data-label="{param_key}_min">{html.escape(str(row_data["Min"]))}</span>'
                t_max = f'<span class="nlg-val" data-label="{param_key}_max">{html.escape(str(row_data["Max"]))}</span>'
                value_unit_phrase = f"{t_min} ~ {t_max} {tagged_unit}"
            else:
                value_unit_phrase = f"{tagged_value} {tagged_unit}"
            connector_space = " "
        else:
            value_unit_phrase = tagged_value
            unit_connector = f" in {tagged_unit}"
            connector_space = " "

        # ==========================================
        # ✅ FIX: Table Header Bleeding Templates
        # ==========================================
        table_flat_templates = [
            f"{tagged_param} Min Typ Max {row_data.get('Min') or '-'} {row_data.get('Typ') or '-'} {row_data.get('Max') or '-'} {tagged_unit}",
            f"{tagged_param} {row_data.get('Min') or ''} {row_data.get('Typ') or ''} {row_data.get('Max') or ''} {tagged_unit}".replace("  ", " ").strip()
        ]

        # === בחירת תבנית משפט (Input 2 Logic) ===
        # משתמשים ב-value_unit_phrase ו-unit_connector שיצרנו למעלה

        context_specific_templates = []

        if is_voltage(param_name):
            context_specific_templates = [
                f"The {tagged_param} is maintained at {value_unit_phrase}{unit_connector}.",
                f"Operating {tagged_param} measures {value_unit_phrase}{unit_connector}.",
                f"Supply conditions specify {tagged_param} of {value_unit_phrase}{unit_connector}.",
                f"Voltage specifications establish {tagged_param} at {value_unit_phrase}{unit_connector}.",
            ]

        elif is_current(param_name):
            context_specific_templates = [
                f"Current consumption is characterized by {tagged_param} of {value_unit_phrase}{unit_connector}.",
                f"The {tagged_param} draws {value_unit_phrase}{unit_connector} under typical conditions.",
                f"Electrical specifications define {tagged_param} as {value_unit_phrase}{unit_connector}.",
                f"Operating {tagged_param} measures {value_unit_phrase}{unit_connector}.",
            ]

        elif is_resistance(param_name):
            context_specific_templates = [
                f"The component exhibits {tagged_param} of {value_unit_phrase}{unit_connector}.",
                f"Impedance characteristics show {tagged_param} measuring {value_unit_phrase}{unit_connector}.",
                f"Thermal specifications indicate {tagged_param} of {value_unit_phrase}{unit_connector}.",
                f"On-state {tagged_param} achieves {value_unit_phrase}{unit_connector}.",
            ]

        elif is_timing(param_name):
            context_specific_templates = [
                f"Timing specifications establish {tagged_param} at {value_unit_phrase}{unit_connector}.",
                f"The {tagged_param} measures {value_unit_phrase}{unit_connector} under test conditions.",
                f"Propagation characteristics indicate {tagged_param} of {value_unit_phrase}{unit_connector}.",
                f"Switching performance features {tagged_param} of {value_unit_phrase}{unit_connector}.",
            ]

        elif is_frequency(param_name):
            context_specific_templates = [
                f"The device supports {tagged_param} up to {value_unit_phrase}{unit_connector}.",
                f"Frequency specifications define {tagged_param} of {value_unit_phrase}{unit_connector}.",
                f"Operating bandwidth achieves {tagged_param} of {value_unit_phrase}{unit_connector}.",
                f"Clock performance reaches {tagged_param} of {value_unit_phrase}{unit_connector}.",
            ]

        # === תבניות כלליות (Fallback) ===

        general_templates = [
            # Classic formats
            f"The device features {random.choice(QUALIFIERS)} {tagged_param} of {value_unit_phrase}{unit_connector}.",
            f"This component specifies {tagged_param} at {value_unit_phrase}{unit_connector}.",
            f"Notably, the {tagged_param} is rated at {value_unit_phrase}{unit_connector}.",
            f"Critical to performance is the {tagged_param} of {value_unit_phrase}{unit_connector}.",

            # Technical variants
            f"Engineering specifications define {tagged_param} as {value_unit_phrase}{unit_connector}.",
            f"The datasheet indicates {tagged_param} measuring {value_unit_phrase}{unit_connector}.",
            f"Performance metrics show {tagged_param} of {value_unit_phrase}{unit_connector}.",
            f"Technical documentation establishes {tagged_param} at {value_unit_phrase}{unit_connector}.",

            # Active voice variants
            f"The component {random.choice(VERBS_PRESENT)} {tagged_param} of {value_unit_phrase}{unit_connector}.",
            f"Operating parameters specify {tagged_param} {random.choice(CONNECTORS)} {value_unit_phrase}{unit_connector}.",
            f"Design requirements establish {tagged_param} at {value_unit_phrase}{unit_connector}.",
            f"Functional specifications confirm {tagged_param} of {value_unit_phrase}{unit_connector}.",

            # Passive/measured variants
            f"The {tagged_param} is {random.choice(VERBS_RATED)} {value_unit_phrase}{unit_connector}.",
            f"Measured {tagged_param} achieves {value_unit_phrase}{unit_connector}.",
            f"Specified {tagged_param} reaches {value_unit_phrase}{unit_connector}.",
            f"Tested {tagged_param} demonstrates {value_unit_phrase}{unit_connector}.",

            # With openers
            f"{random.choice(OPENERS)} {tagged_param} of {value_unit_phrase}{unit_connector}.",
            f"{random.choice(OPENERS)} the {tagged_param} at {value_unit_phrase}{unit_connector}.",

            # Comparative/qualified variants
            f"Under standard conditions, {tagged_param} measures {value_unit_phrase}{unit_connector}.",
            f"At nominal operation, the {tagged_param} is {value_unit_phrase}{unit_connector}.",
            f"Typical {tagged_param} performance yields {value_unit_phrase}{unit_connector}.",
            f"Expected {tagged_param} ranges to {value_unit_phrase}{unit_connector}.",

            f"{tagged_param}{connector_space}{value_unit_phrase}{unit_connector}",
            f"{tagged_param} = {value_unit_phrase}{unit_connector}",
        ]

        # 15% סיכוי להשתמש בתבנית שמשטחת טבלה (Header Bleeding)
        if random.random() < 0.15:
            sentences.append(random.choice(table_flat_templates))
        else:
            if context_specific_templates and random.random() < 0.6:
                templates = context_specific_templates + general_templates
            else:
                templates = general_templates
            sentences.append(random.choice(templates))

    return " ".join(sentences)


def generate_datasheet_sample(result: 'DatasheetResult', seed: Optional[int] = None) -> Dict[str, Any]:
    """
    🆕 מתאם ראשי - יוצר את הקונפיגורציה פעם אחת ומעביר לכולם
    """
    if seed is not None:
        random.seed(seed)

    # Step 1: Generate marketing content
    marketing_gen = MarketingGenerator(mode='fast')
    marketing_data = marketing_gen.generate(result.context)

    # Step 2: Create unified rendering configuration
    config = RenderingConfig.generate_random(result.parameters)

    # Step 3: Inject parameters into text BEFORE rendering
    injected_params = []
    remaining_params = []

    for param in result.parameters:
        if param.key in config.injected_param_keys:
            injected_params.append(param)
        else:
            remaining_params.append(param)

    # Generate NLG for injected params
    injected_text = _generate_nlg_for_params(injected_params)
    if random.random() < 0.5:
        marketing_data["description"] += " " + injected_text
    else:
        marketing_data.setdefault("key_features", []).append(injected_text)

    # Step 4: Update result with remaining params
    result_copy = copy.copy(result)
    result_copy.parameters = remaining_params

    # Step 5: Render HTML with the config
    html_renderer = DatasheetHtmlRenderer()
    html_output = html_renderer.render(result_copy, marketing_data, config)

    # Step 5.5: Apply realistic PDF degradation noise  ← חדש
    degrader = TextDegradationAugmentor(intensity=0.5)
    html_output = degrader.degrade(html_output)

    # Step 6: Render JSON with THE SAME config
    json_renderer = DatasheetJSONRenderer()
    json_output = json_renderer.render(
        result_copy,
        marketing_data,
        config,
        injected_param_keys=config.injected_param_keys
    )

    return {
        "html": html_output,
        "json": json_output,
        "config": asdict(config)  # For debugging/verification
    }
