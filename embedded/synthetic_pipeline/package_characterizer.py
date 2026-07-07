import random


class PackageCharacterizer:
    """
    מאפיין כל package לפי תכונות פיזיקליות אמיתיות.
    מאפשר יצירת תיאורים מדויקים ורלוונטיים.
    """

    PACKAGE_CATEGORIES = {
        # === Through-Hole (THT) ===
        "TO-220": {
            "form_factor": "through_hole",
            "size_class": "medium_power",
            "primary_benefit": "thermal",
            "mounting": "screw_mount",
            "key_features": ["heatsink_tab", "high_power", "traditional"]
        },
        "TO-220AB": {
            "form_factor": "through_hole",
            "size_class": "medium_power",
            "primary_benefit": "thermal",
            "mounting": "screw_mount",
            "key_features": ["heatsink_tab", "high_power", "traditional"]
        },
        "TO-247": {
            "form_factor": "through_hole",
            "size_class": "high_power",
            "primary_benefit": "thermal",
            "mounting": "screw_mount",
            "key_features": ["heatsink_tab", "ultra_high_power", "industrial_grade"]
        },
        "TO-247-3": {
            "form_factor": "through_hole",
            "size_class": "high_power",
            "primary_benefit": "thermal",
            "mounting": "screw_mount",
            "key_features": ["heatsink_tab", "ultra_high_power", "sic_optimized"]
        },
        "TO-247-4": {
            "form_factor": "through_hole",
            "size_class": "high_power",
            "primary_benefit": "thermal",
            "mounting": "screw_mount",
            "key_features": ["kelvin_source", "ultra_high_power", "low_inductance"]
        },
        "TO-3P": {
            "form_factor": "through_hole",
            "size_class": "high_power",
            "primary_benefit": "thermal",
            "mounting": "screw_mount",
            "key_features": ["heatsink_tab", "high_power", "legacy_compatible"]
        },
        "TO-264": {
            "form_factor": "through_hole",
            "size_class": "ultra_high_power",
            "primary_benefit": "thermal",
            "mounting": "screw_mount",
            "key_features": ["heatsink_tab", "extreme_power", "industrial"]
        },
        "ITO-220": {
            "form_factor": "through_hole",
            "size_class": "medium_power",
            "primary_benefit": "reliability",
            "mounting": "isolated_mount",
            "key_features": ["electrical_isolation", "safety", "high_voltage"]
        },
        "TO-220FP": {
            "form_factor": "through_hole",
            "size_class": "medium_power",
            "primary_benefit": "reliability",
            "mounting": "isolated_mount",
            "key_features": ["full_pack", "electrical_isolation", "high_voltage"]
        },

        # === Surface Mount - Power ===
        "DPAK(TO-252)": {
            "form_factor": "surface_mount",
            "size_class": "medium_power_smd",
            "primary_benefit": "space",
            "mounting": "smd_reflow",
            "key_features": ["compact", "automated_assembly", "cost_effective"]
        },
        "TO-252": {
            "form_factor": "surface_mount",
            "size_class": "medium_power_smd",
            "primary_benefit": "space",
            "mounting": "smd_reflow",
            "key_features": ["compact", "automated_assembly", "cost_effective"]
        },
        "D2PAK(TO-263)": {
            "form_factor": "surface_mount",
            "size_class": "high_power_smd",
            "primary_benefit": "thermal",
            "mounting": "smd_reflow",
            "key_features": ["large_pad", "high_power_smd", "excellent_thermal"]
        },
        "TO-263-7": {
            "form_factor": "surface_mount",
            "size_class": "high_power_smd",
            "primary_benefit": "thermal",
            "mounting": "smd_reflow",
            "key_features": ["kelvin_connection", "high_power_smd", "precision_sensing"]
        },
        "D2PAK-7L": {
            "form_factor": "surface_mount",
            "size_class": "high_power_smd",
            "primary_benefit": "thermal",
            "mounting": "smd_reflow",
            "key_features": ["kelvin_connection", "high_power_smd", "low_inductance"]
        },
        "PowerPAK_SO-8": {
            "form_factor": "surface_mount",
            "size_class": "medium_power_smd",
            "primary_benefit": "space",
            "mounting": "smd_reflow",
            "key_features": ["low_profile", "dual_cool", "optimized_footprint"]
        },
        "PQFN_5x6": {
            "form_factor": "surface_mount",
            "size_class": "small_power_smd",
            "primary_benefit": "space",
            "mounting": "smd_reflow",
            "key_features": ["ultra_compact", "land_grid", "low_profile"]
        },
        "DFN_5x6": {
            "form_factor": "surface_mount",
            "size_class": "small_power_smd",
            "primary_benefit": "space",
            "mounting": "smd_reflow",
            "key_features": ["ultra_compact", "exposed_pad", "thermal_efficient"]
        },
        "DFN_8x8": {
            "form_factor": "surface_mount",
            "size_class": "medium_power_smd",
            "primary_benefit": "thermal",
            "mounting": "smd_reflow",
            "key_features": ["gan_optimized", "exposed_pad", "high_frequency"]
        },
        "TOLL": {
            "form_factor": "surface_mount",
            "size_class": "high_power_smd",
            "primary_benefit": "thermal",
            "mounting": "smd_reflow",
            "key_features": ["leadless", "ultra_low_inductance", "high_current"]
        },
        "DirectFET": {
            "form_factor": "surface_mount",
            "size_class": "small_power_smd",
            "primary_benefit": "space",
            "mounting": "smd_reflow",
            "key_features": ["top_cool", "bottom_cool", "ultra_compact"]
        },

        # === Surface Mount - Small Signal ===
        "SOT-23": {
            "form_factor": "surface_mount",
            "size_class": "small_signal",
            "primary_benefit": "space",
            "mounting": "smd_reflow",
            "key_features": ["ultra_compact", "low_cost", "high_density"]
        },
        "SOT-23-3": {
            "form_factor": "surface_mount",
            "size_class": "small_signal",
            "primary_benefit": "space",
            "mounting": "smd_reflow",
            "key_features": ["ultra_compact", "low_cost", "high_density"]
        },
        "SOT-23-5": {
            "form_factor": "surface_mount",
            "size_class": "small_signal",
            "primary_benefit": "space",
            "mounting": "smd_reflow",
            "key_features": ["ultra_compact", "low_cost", "high_density"]
        },
        "SOT-23-6": {
            "form_factor": "surface_mount",
            "size_class": "small_signal",
            "primary_benefit": "space",
            "mounting": "smd_reflow",
            "key_features": ["ultra_compact", "low_cost", "high_density"]
        },
        "SOT-89": {
            "form_factor": "surface_mount",
            "size_class": "small_signal",
            "primary_benefit": "space",
            "mounting": "smd_reflow",
            "key_features": ["compact", "thermal_tab", "standard"]
        },
        "SOT-223": {
            "form_factor": "surface_mount",
            "size_class": "small_signal",
            "primary_benefit": "thermal",
            "mounting": "smd_reflow",
            "key_features": ["thermal_tab", "medium_power", "standard"]
        },
        "SOD-123": {
            "form_factor": "surface_mount",
            "size_class": "small_signal",
            "primary_benefit": "space",
            "mounting": "smd_reflow",
            "key_features": ["ultra_compact", "diode_package", "standard"]
        },
        "DO-214": {
            "form_factor": "surface_mount",
            "size_class": "small_signal",
            "primary_benefit": "space",
            "mounting": "smd_reflow",
            "key_features": ["compact", "diode_package", "standard"]
        },

        # === Passive Components (Resistors, Capacitors, Inductors) ===
        "0201": {
            "form_factor": "surface_mount",
            "size_class": "ultra_small",
            "primary_benefit": "space",
            "mounting": "smd_reflow",
            "key_features": ["ultra_compact", "high_density", "miniature"]
        },
        "0402": {
            "form_factor": "surface_mount",
            "size_class": "very_small",
            "primary_benefit": "space",
            "mounting": "smd_reflow",
            "key_features": ["compact", "high_density", "standard"]
        },
        "0603": {
            "form_factor": "surface_mount",
            "size_class": "small",
            "primary_benefit": "space",
            "mounting": "smd_reflow",
            "key_features": ["compact", "standard", "versatile"]
        },
        "0805": {
            "form_factor": "surface_mount",
            "size_class": "small",
            "primary_benefit": "space",
            "mounting": "smd_reflow",
            "key_features": ["standard", "easy_handling", "versatile"]
        },
        "1206": {
            "form_factor": "surface_mount",
            "size_class": "medium",
            "primary_benefit": "mechanical",
            "mounting": "smd_reflow",
            "key_features": ["standard", "robust", "easy_handling"]
        },
        "1210": {
            "form_factor": "surface_mount",
            "size_class": "medium",
            "primary_benefit": "mechanical",
            "mounting": "smd_reflow",
            "key_features": ["robust", "higher_power", "standard"]
        },
        "1812": {
            "form_factor": "surface_mount",
            "size_class": "large",
            "primary_benefit": "mechanical",
            "mounting": "smd_reflow",
            "key_features": ["robust", "high_power", "large_footprint"]
        },
        "2010": {
            "form_factor": "surface_mount",
            "size_class": "large",
            "primary_benefit": "mechanical",
            "mounting": "smd_reflow",
            "key_features": ["robust", "high_power", "large_footprint"]
        },
        "2512": {
            "form_factor": "surface_mount",
            "size_class": "large",
            "primary_benefit": "thermal",
            "mounting": "smd_reflow",
            "key_features": ["high_power", "thermal_mass", "industrial"]
        }
    }

    # תבניות משפטים לפי קטגוריית Benefit
    PACKAGE_BENEFIT_TEMPLATES = {
        "thermal": {
            "heatsink_tab": [
                "provides superior thermal coupling to the PCB via an integrated heatsink tab, achieving junction-to-ambient thermal resistance (Rθ_JA) of {rth_ja} °C/W",
                "features a large metal tab for direct heatsink mounting, delivering junction-to-case thermal resistance (Rθ_JC) as low as {rth_jc} °C/W",
                "ensures efficient heat dissipation through a dedicated thermal pad that transfers heat directly to external cooling solutions"
            ],
            "exposed_pad": [
                "utilizes an exposed thermal pad on the bottom for direct heat transfer to the PCB, minimizing thermal resistance",
                "incorporates a large exposed die pad that enables low-impedance thermal paths to ground planes"
            ],
            "large_pad": [
                "features an expansive thermal pad designed for maximum heat spreading across the PCB copper area"
            ],
            "default": [
                "provides reliable thermal performance suitable for standard operating conditions",
                "ensures adequate heat dissipation for typical application requirements"
            ]
        },
        "space": {
            "ultra_compact": [
                "measures just {dimensions} mm, enabling ultra-high component density on space-constrained PCBs",
                "offers a miniature footprint of {dimensions} mm for applications demanding minimal board area"
            ],
            "compact": [
                "features a compact {dimensions} mm footprint, balancing size with ease of assembly",
                "provides space-efficient design in a {dimensions} mm package suitable for automated pick-and-place"
            ],
            "default": [
                "optimizes board space utilization without compromising manufacturability",
                "delivers a practical form factor for modern high-density layouts"
            ]
        },
        "mechanical": {
            "robust": [
                "delivers robust mechanical stability with reinforced terminations that withstand vibration and thermal cycling",
                "features strengthened solder joints and body construction for harsh industrial environments"
            ],
            "default": [
                "ensures reliable mechanical performance in standard operating conditions",
                "provides adequate mechanical strength for typical assembly processes"
            ]
        },
        "reliability": {
            "electrical_isolation": [
                "incorporates electrical isolation between the die and the mounting tab, enabling safe chassis grounding without insulating pads",
                "features an isolated mounting surface that eliminates the need for additional thermal interface insulators"
            ],
            "default": [
                "meets industry-standard reliability specifications for long-term operation",
                "ensures consistent performance across rated environmental conditions"
            ]
        }
    }

    @classmethod
    def get_package_info(cls, package_name: str) -> dict:
        """מחזיר מידע על package או fallback אם לא נמצא"""
        return cls.PACKAGE_CATEGORIES.get(
            package_name,
            {
                "form_factor": "surface_mount",
                "size_class": "generic",
                "primary_benefit": "space",
                "mounting": "smd_reflow",
                "key_features": ["standard"]
            }
        )

    @classmethod
    def get_package_benefit(cls, package_name: str, package_specs: dict) -> str:
        """
        מייצר תיאור benefit ספציפי לpackage בהתבסס על מאפייניו האמיתיים
        עם הגנה מפני ערכים חסרים (N/A)
        """
        pkg_info = cls.get_package_info(package_name)
        benefit_category = pkg_info["primary_benefit"]
        key_features = pkg_info["key_features"]

        # חילוץ נתונים מתוך ה-specs
        limits = package_specs.get("limits", {})
        dims = package_specs.get("dimensions", [])

        # הכנת המשתנים להזרקה
        rth_jc_val = limits.get("rth_jc")
        rth_ja_val = limits.get("rth_ja")

        # פירמוט מידות בצורה בטוחה
        dim_str = "generic"
        if dims and isinstance(dims, list) and len(dims) >= 2:
            dim_str = f"{dims[0]}×{dims[1]}"

        # בחירת קטגוריית תבניות
        templates = cls.PACKAGE_BENEFIT_TEMPLATES.get(benefit_category, {})

        # סינון תבניות: נשתמש רק בתבניות שאנחנו יכולים למלא את הנתונים שלהן!
        valid_templates = []

        # 1. נסה למצוא תבניות ספציפיות לפי key_features
        potential_templates = []
        for feature in key_features:
            if feature in templates:
                potential_templates.extend(templates[feature])

        # אם לא מצאנו לפי פיצ'ר, נלך לדיפולט של הקטגוריה
        if not potential_templates:
            potential_templates = templates.get("default", [])

        # 2. בדיקת היתכנות (האם יש לי את הנתון הדרוש לתבנית?)
        for t in potential_templates:
            if "{rth_jc}" in t and not rth_jc_val:
                continue  # דלג על תבנית שדורשת נתון חסר
            if "{rth_ja}" in t and not rth_ja_val:
                continue
            if "{dimensions}" in t and dim_str == "generic":
                continue

            valid_templates.append(t)

        # אם סיננו את הכל (למשל חסרים נתונים), נשתמש ב-Generic Fallback מוחלט
        if not valid_templates:
            valid_templates = [
                "designed for optimal performance in standard applications",
                "offers a robust solution for modern circuit designs",
                f"utilizes industry-standard {package_name} packaging"
            ]

        # בחירה והחלפה
        selected_template = random.choice(valid_templates)

        # ביצוע ההחלפה (רק אם הערכים קיימים, אחרת זה לא היה נבחר)
        if rth_jc_val:
            selected_template = selected_template.replace("{rth_jc}", str(rth_jc_val))
        if rth_ja_val:
            selected_template = selected_template.replace("{rth_ja}", str(rth_ja_val))

        selected_template = selected_template.replace("{dimensions}", dim_str)

        return selected_template
