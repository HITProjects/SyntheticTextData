import random
import json
import re

from typing import Dict, Any, List

try:
    import requests
    _HAS_REQUESTS = True
except ImportError:
    requests = None
    _HAS_REQUESTS = False

from synthetic_pipeline.package_characterizer import PackageCharacterizer


class MarketingSentenceBuilder:
    """
    מנוע בניית משפטים מודולרי לייצור מיליוני וריאציות של תיאורים.
    """

    # === אוצר מילים דינמי ===

    OPENERS = [
        "The {name} from {mfr}",
        "Designed by {mfr}, the {name}",
        "{mfr} introduces the {name}, which",
        "Representing a leap in {tech} technology, the {name}",
        "The {name} is a {quality} {comp_type} that",
        "Engineered for {application}, the {name}",
        "{mfr}'s {name} sets a new standard as a",
        "Featuring advanced {tech} architecture, the {name}"
    ]

    VERBS = [
        "integrates", "combines", "features", "utilizes",
        "incorporates", "leverages", "delivers", "provides",
        "employs", "harnesses"
    ]

    # מילים לחיבור בין הטכנולוגיה לאריזה
    CONNECTORS = [
        "within a", "housed in a", "encapsulated in a",
        "delivered in a standard", "packaged in a robust",
        "assembled in a space-saving", "offered in a"
    ]

    # תיאורים טכנולוגיים לפי סוג רכיב
    TECH_DESCRIPTORS = {
        "OPAMP": [
            "advanced low-noise architecture", "precision rail-to-rail topology",
            "high-bandwidth amplification circuitry", "ultra-stable input stage design",
            "drift-compensated internal reference"
        ],
        "BJT": [
            "robust planar bipolar technology", "high-gain epitaxial structure",
            "optimized saturation characteristics", "fast-switching silicon lattice",
            "low-leakage junction design"
        ],
        "MOSFET": [
            "trench-gate field effect technology", "ultra-low Rdson lattice structure",
            "high-speed switching topology", "avalanche-rugged cell design",
            "charge-balanced structure"
        ],
        "DIODE": [
            "low-forward-drop junction", "fast-recovery epitaxial design",
            "controlled-avalanche structure", "high-surge capability die"
        ],
        "RESISTOR": [
            "precision thin-film element", "high-stability thick-film composition",
            "pulse-withstanding resistive material", "low-inductance element design"
        ],
        "CAPACITOR": [
            "multi-layer dielectric structure", "low-ESR electrode configuration",
            "high-stability dielectric formulation", "self-healing film technology"
        ],
        "INDUCTOR": [
            "high-permeability core material", "low-loss wire winding",
            "shielded magnetic construction", "saturation-resistant core design"
        ],
        "VOLTAGE_REGULATOR": [
            "fast-transient response architecture", "low-dropout pass element",
            "precision bandgap reference", "high-efficiency control loop"
        ],
        "generic": [
            "industry-proven semiconductor technology", "cutting-edge reliable architecture",
            "high-performance solid-state design", "optimized internal circuitry"
        ]
    }

    # משפטי סיום (Value Proposition)
    CLOSERS = [
        "ensuring consistent performance over lifetime.",
        "making it ideal for demanding modern designs.",
        "offering reliable operation in harsh conditions.",
        "optimized for cost-sensitive and high-volume applications.",
        "delivering superior linearity and stability.",
        "guaranteeing minimal signal degradation.",
        "providing a perfect balance of performance and efficiency.",
        "enabling next-generation power density.",
        "simplifying thermal management in compact systems."
    ]

    @classmethod
    def generate(cls, context, manufacturer: str, product_name: str, package_desc: str) -> str:
        """
        בונה פסקה מלאה המורכבת מ-2-3 משפטים מודולריים.
        """
        # 1. חילוץ נתונים
        comp_type = context.component_type.upper()
        # מנרמל את שם הרכיב למפתח במילון (למשל POWER_BJT -> BJT)
        tech_key = "generic"
        for key in cls.TECH_DESCRIPTORS.keys():
            if key in comp_type:
                tech_key = key
                break

        # 2. בחירת רכיבי המשפט הראשון
        tech_desc = random.choice(cls.TECH_DESCRIPTORS[tech_key])

        # בחירת Application רנדומלית כדי לגוון את הפתיחה
        apps = ["industrial systems", "automotive electronics", "portable devices",
                "power management", "signal processing", "telecom infrastructure"]

        opener = random.choice(cls.OPENERS).format(
            name=product_name,
            mfr=manufacturer,
            tech=tech_key.lower().replace("_", " "),
            quality=random.choice(["high-performance", "precision", "industrial-grade", "reliable", "rugged"]),
            comp_type=context.component_type.replace("_", " ").lower(),
            application=random.choice(apps)
        )

        verb = random.choice(cls.VERBS)
        connector = random.choice(cls.CONNECTORS)

        # משפט 1: הזהות והאריזה
        # "The Ultra-BJT from Apex integrates robust planar technology within a TO-220 package."
        sentence_1 = f"{opener} {verb} {tech_desc} {connector} {context.package} package."

        # משפט 2: התיאור הפיזיקלי (מגיע מ-PackageCharacterizer)
        # "This component provides superior thermal coupling..."
        # מוודאים שמתחיל באות גדולה
        package_desc = package_desc[0].upper() + package_desc[
                                                 1:] if package_desc else "It offers standard mounting capabilities"

        # גיוון בפתיחת המשפט השני
        s2_openers = ["This component", "The device", "It", "The specific package design"]
        sentence_2 = f"{random.choice(s2_openers)} {package_desc}"

        if not sentence_2.strip().endswith('.'):
            sentence_2 += "."

        # משפט 3: סגירה
        closer = random.choice(cls.CLOSERS)
        # לפעמים נחבר את הסגירה למשפט השני, ולפעמים היא תהיה נפרדת
        sentence_3 = closer[0].upper() + closer[1:]

        # === הרכבה סופית (וריאציות מבנה) ===
        structure_type = random.randint(1, 3)

        if structure_type == 1:
            # שלושה משפטים נפרדים (קלאסי)
            return f"{sentence_1} {sentence_2} {sentence_3}"

        elif structure_type == 2:
            # חיבור משפט 1 ו-3, ואז הפיזיקלי
            # "The X uses Y technology, making it ideal for Z. It features..."
            combined_1_3 = sentence_1.rstrip('.') + ", " + closer.replace(closer[0].upper(), closer[0].lower())
            return f"{combined_1_3} {sentence_2}"

        else:
            # משפט פיזיקלי באמצע עם מילת קישור
            # "The X uses Y technology. Furthermore, it features..., ensuring..."
            transition = random.choice(["Furthermore,", "Moreover,", "Additionally,", "In addition,"])
            return f"{sentence_1} {transition} {sentence_2} {sentence_3}"


class MarketingGenerator:
    # ... (קוד MarketingGenerator נשאר זהה לקוד המקורי שלך, ללא שינוי) ...
    MANUFACTURER_PREFIXES = ["Quantum", "Apex", "Vector", "Zenith", "Nova", "Flux", "Nexus", "Pulse", "Prime", "Ultra",
                             "Mega", "Omni", "Precision", "Advanced", "Elite", "Summit", "Vertex", "Titan", "Sigma",
                             "Delta", "Vortex"]
    MANUFACTURER_SUFFIXES = ["Silicon", "Dynamics", "Technologies", "Semiconductor", "Electronics", "Systems", "Micro",
                             "Components", "Devices", "Solutions", "Labs", "Circuits", "Innovations", "Foundry",
                             "Manufacturing", "Power"]
    PRODUCT_PREFIXES = ["Ultra", "Hyper", "Max", "Pro", "Elite", "Prime", "Precision", "Advanced", "High-Speed",
                        "Low-Noise", "Compact", "Enhanced", "Smart", "Intelligent", "Adaptive", "Optimized", "Next-Gen"]
    APPLICATIONS = ["automotive power management", "industrial control systems", "telecommunications infrastructure",
                    "medical instrumentation", "aerospace applications", "consumer electronics", "IoT devices",
                    "battery management systems", "motor control", "LED lighting", "server power supplies",
                    "renewable energy systems", "precision measurement equipment", "high-frequency switching",
                    "portable devices", "ruggedized equipment"]
    PACKAGE_BENEFITS = {
        "thermal": ["provides superior thermal coupling to the PCB for efficient heat dissipation",
                    "features enhanced thermal management capabilities with low junction-to-ambient resistance",
                    "offers excellent heat spreading characteristics for high-power applications",
                    "ensures optimal thermal performance in thermally constrained environments"],
        "space": ["enables high-density PCB layouts with its compact footprint",
                  "maximizes board space utilization in space-critical designs",
                  "allows for miniaturized system designs without compromising performance",
                  "provides industry-leading power density in a small form factor"],
        "mechanical": ["delivers robust mechanical stability under high-vibration conditions",
                       "ensures reliable performance in demanding mechanical environments",
                       "features reinforced lead structure for enhanced durability",
                       "provides superior mechanical strength for harsh operating conditions"],
        "reliability": ["guarantees long-term reliability with industry-proven construction",
                        "meets stringent automotive qualification standards",
                        "ensures consistent performance across wide temperature ranges",
                        "provides exceptional reliability in mission-critical applications"]
    }
    DESCRIPTION_TEMPLATES = [
        "{product_name} from {manufacturer} represents cutting-edge {component_type} technology designed for {application}. {package_benefit_1}. {package_benefit_2}. This component delivers {performance_trait} with {key_feature}, making it ideal for demanding applications requiring {package_strength}.",

        "Designed by {manufacturer}, the {product_name} integrates advanced {technology} within a {package_description}. {package_benefit_1}, allowing for efficient operation in {environment}. {package_benefit_2}, ensuring {reliability_aspect} across the operating range.",

        "{manufacturer} introduces the {product_name}, a high-performance {component_type} engineered for {application}. {package_benefit_1} while {package_benefit_2}. The {package_form_factor} design emphasizes {design_focus}, delivering {performance_outcome} in space-critical applications.",

        "The {product_name} by {manufacturer} combines {technology} with proven reliability for {application}. {package_benefit_1}. The {package_mounting_type} construction {package_benefit_2}, making it suitable for {environment} where {package_strength} is essential."
    ]
    TECHNOLOGIES = ["trench MOSFET technology", "advanced planar architecture", "super-junction design",
                    "precision analog circuitry", "low-noise amplification", "high-speed switching topology",
                    "wide-bandgap semiconductor technology", "integrated protection features"]
    PERFORMANCE_TRAITS = ["exceptional efficiency", "industry-leading performance", "superior linearity",
                          "minimal conduction losses", "ultra-low on-resistance", "excellent thermal stability",
                          "high switching speeds", "low electromagnetic interference", "outstanding precision"]
    KEY_FEATURES = ["low-side current sensing", "integrated gate drive", "thermal shutdown protection",
                    "ESD-hardened inputs", "wide supply voltage range", "true shutdown capability",
                    "over-current protection", "adaptive dead-time control"]
    ENVIRONMENTS = ["automotive", "industrial", "high-temperature", "outdoor", "mission-critical", "space-constrained",
                    "noise-sensitive", "high-reliability"]
    RELIABILITY_ASPECTS = ["long-term stability", "minimal drift", "consistent operation", "predictable behavior",
                           "robust protection"]
    DESIGN_FOCUS = ["thermal efficiency", "power density", "signal integrity", "ease of integration",
                    "cost optimization"]
    PERFORMANCE_OUTCOMES = ["reduced system complexity", "improved power efficiency", "enhanced signal fidelity",
                            "superior thermal performance", "optimized size-to-performance ratio"]
    FEATURES_POOL = ["Low quiescent current for extended battery life",
                     "Wide operating temperature range (-55°C to +150°C)",
                     "Built-in overcurrent and thermal protection", "High precision voltage reference (±1% tolerance)",
                     "Fast transient response (<10µs settling time)",
                     "Low noise operation suitable for audio applications",
                     "Integrated soft-start to reduce inrush current", "ESD protection up to 2kV (HBM)",
                     "High PSRR (>60dB at 1kHz) for improved noise immunity",
                     "Industry-standard pinout for easy migration", "RoHS compliant and halogen-free",
                     "Automotive-grade qualification (AEC-Q100)"]
    SECTION_INTRO_TEMPLATES = {
        "abs_max": [
            "The following ratings are absolute maximum values that must not be exceeded to prevent permanent device damage.",
            "Stress beyond the limits specified may cause irreversible harm to the component.",
            "These ratings define the upper bounds of safe operation; continuous operation at maximum ratings is not recommended."],
        "electrical": [
            "The electrical specifications below represent typical performance under standard test conditions unless otherwise noted.",
            "These parameters characterize the component's behavior across its recommended operating range.",
            "Electrical characteristics are guaranteed over the specified temperature and voltage ranges."],
        "thermal": ["Thermal performance is critical for ensuring long-term reliability and optimal operation.",
                    "The thermal parameters below define heat transfer characteristics from junction to ambient.",
                    "Proper thermal management is essential; exceeding thermal limits may degrade performance or cause failure."],
        "dynamic": ["Dynamic characteristics define the component's transient and switching behavior.",
                    "These parameters are measured under specific load and frequency conditions as detailed in the test setup.",
                    "Switching performance may vary with layout parasitics and external component selection."],
        "mechanical": [
            "Mechanical specifications provide dimensional and packaging information for PCB layout and assembly.",
            "All dimensions are in millimeters unless otherwise specified; tolerances are per JEDEC standards.",
            "Package outlines conform to industry-standard footprints for compatibility with automated assembly."],
        "reliability": ["Reliability data represents performance under accelerated stress testing conditions.",
                        "These metrics ensure the component meets industry standards for quality and longevity.",
                        "Testing methodologies comply with JEDEC and military specifications where applicable."],
        "default": ["The specifications below define key operating parameters for this component.",
                    "All values are measured under standard test conditions unless otherwise indicated.",
                    "Performance is guaranteed across the specified operating range."]
    }

    def __init__(self, mode: str = 'fast', model: str = 'ollama'):
        """
        ✅ תיקון תאימות לאחור (Backward Compatibility Fix)

        Args:
            mode: 'fast' (template-based) or 'high_quality' (LLM-based with locked facts)
            model: 'ollama' or other LLM backend (only used in high_quality mode)
        """
        self.mode = mode
        self.model = model
        self.package_characterizer = PackageCharacterizer()

    def generate(self, context, package_specs: dict = None) -> Dict[str, Any]:
        """
        יוצר תוכן שיווקי - תומך בשני מצבים:
        1. fast: תבניות בלבד (ללא LLM)
        2. high_quality: LLM עם עובדות נעולות (מונע הזיות)
        """
        manufacturer = self._generate_manufacturer_name()
        product_name = self._generate_product_name(context)

        # יצירת תיאור - תלוי במצב
        if self.mode == 'high_quality' and package_specs:
            # מצב LLM - עם נעילת עובדות
            description = self._generate_description_with_llm(context, manufacturer, product_name, package_specs)
        else:
            # מצב מהיר - תבניות בלבד
            if package_specs:
                package_desc = self.package_characterizer.get_package_benefit(context.package, package_specs)
                description = MarketingSentenceBuilder.generate(context, manufacturer, product_name, package_desc)
            else:
                description = self._generate_description(context, manufacturer, product_name)

        # הגדלת מגוון ב-features
        features = random.sample(self.FEATURES_POOL, random.randint(4, 7))
        applications = random.sample(self.APPLICATIONS, random.randint(3, 5))

        # Section Intros (נוצרות לפי הצורך בזמן ה-Rendering)
        sections_present = ["ELECTRICAL_CHARACTERISTICS", "ABS_MAX", "THERMAL"]
        section_intros = self._generate_section_intros(sections_present)

        footnotes = self._generate_footnotes(context)

        return {
            "marketing_name": product_name,
            "manufacturer": manufacturer,
            "description": description,
            "section_intros": section_intros,
            "footnotes": footnotes,
            "key_features": features,
            "typical_applications": applications
        }

    def _generate_description_with_llm(self, context, manufacturer: str, product_name: str, package_specs: dict) -> str:
        """
        🆕 יצירת תיאור באמצעות LLM - עם נעילת עובדות (Locked Facts)

        הפרומפט מספק את כל העובדות הקשיחות (מידות, Rth, פינים)
        ומבקש מה-LLM רק לנסח אותן בצורה שיווקית ללא תוספות.
        """
        # חילוץ עובדות קשיחות מה-package_specs
        pkg_info = self.package_characterizer.get_package_info(context.package)
        limits = package_specs.get("limits", {})
        dims = package_specs.get("dimensions", [])

        # בניית מחרוזת עובדות
        facts = []
        facts.append(f"Package: {context.package}")
        facts.append(f"Form Factor: {pkg_info['form_factor']}")
        facts.append(f"Component Type: {context.component_type}")

        if dims and len(dims) >= 2:
            facts.append(f"Physical Dimensions: {dims[0]}×{dims[1]} mm")

        if "rth_jc" in limits and limits["rth_jc"]:
            facts.append(f"Junction-to-Case Thermal Resistance: {limits['rth_jc']} °C/W")

        if "rth_ja" in limits and limits["rth_ja"]:
            facts.append(f"Junction-to-Ambient Thermal Resistance: {limits['rth_ja']} °C/W")

        facts_text = "\n".join([f"- {fact}" for fact in facts])

        # בניית הפרומפט הנעול
        prompt = f"""You are a technical marketing writer for semiconductor datasheets.

STRICT RULES:
1. Use ONLY the facts provided below - do not add any numbers, dimensions, or specifications
2. Write a concise 2-3 sentence product description
3. Focus on applications and benefits, not on inventing technical specs
4. Do not mention specific pin counts, lead counts, or physical measurements unless explicitly provided

GIVEN FACTS:
{facts_text}

Product Name: {product_name}
Manufacturer: {manufacturer}

Write a professional marketing description following the rules above. Output only the description text, no preamble."""

        _MAX_RETRIES = 3
        _RETRY_DELAY = 2  # seconds
        for _attempt in range(_MAX_RETRIES):
            try:
                if self.model == 'ollama':
                    # קריאה ל-Ollama API
                    response = requests.post(
                        'http://localhost:11434/api/generate',
                        json={
                            'model': 'llama2',  # או כל מודל אחר שמותקן
                            'prompt': prompt,
                            'stream': False
                        },
                        timeout=30
                    )

                    if response.status_code == 200:
                        result = response.json()
                        description = result.get('response', '').strip()

                        # ניקוי והסרת פרמבולים אפשריים
                        description = self._sanitize_text(description)

                        # אימות שהתיאור לא ריק
                        if description and len(description) > 20:
                            return description
                    break  # non-transient HTTP error — don't retry

            except (requests.Timeout, requests.ConnectionError) as e:
                if _attempt < _MAX_RETRIES - 1:
                    import time
                    time.sleep(_RETRY_DELAY)
                else:
                    print(f"⚠️ LLM failed after {_MAX_RETRIES} attempts: {e}, falling back to templates")
            except Exception as e:
                print(f"⚠️ LLM failed: {e}, falling back to templates")
                break

        # Fallback: אם ה-LLM נכשל, נשתמש בתבניות
        package_desc = self.package_characterizer.get_package_benefit(context.package, package_specs)
        return MarketingSentenceBuilder.generate(context, manufacturer, product_name, package_desc)

    def _generate_description_package_aware(self, context, manufacturer: str, product_name: str,
                                            package_specs: dict) -> str:
        """🆕 יוצר תיאור המותאם למאפייני ה-package"""

        template = random.choice(self.DESCRIPTION_TEMPLATES)

        # קבלת מידע על package
        pkg_info = self.package_characterizer.get_package_info(context.package)

        # יצירת שני benefits שונים
        benefit_1 = self.package_characterizer.get_package_benefit(context.package, package_specs)

        # Benefit 2 - מקטגוריה משנית
        secondary_categories = ["thermal", "space", "mechanical", "reliability"]
        secondary_categories.remove(pkg_info["primary_benefit"])
        secondary_benefit = random.choice(secondary_categories)

        benefit_2_templates = PackageCharacterizer.PACKAGE_BENEFIT_TEMPLATES.get(secondary_benefit, {})
        benefit_2 = random.choice(benefit_2_templates.get("default", ["ensures reliable operation"]))

        # Capitalize first letter of benefit_2
        if benefit_2 and not benefit_2[0].isupper():
            benefit_2 = benefit_2[0].upper() + benefit_2[1:]

        # תיאורים ספציפיים לpackage
        package_descriptions = {
            "through_hole": f"{context.package} through-hole package",
            "surface_mount": f"industry-standard {context.package} surface-mount package",
            "specialized": f"{context.package} specialized package"
        }

        mounting_descriptions = {
            "screw_mount": "bolt-down",
            "smd_reflow": "surface-mount",
            "isolated_mount": "electrically isolated",
            "flange_bolt": "flange-mounted"
        }

        package_strengths = {
            "thermal": "superior thermal management",
            "space": "compact footprint and high power density",
            "mechanical": "mechanical robustness and vibration resistance",
            "reliability": "proven long-term reliability"
        }

        description = template.format(
            product_name=product_name,
            manufacturer=manufacturer,
            component_type=context.component_type,
            package_benefit_1=benefit_1,
            package_benefit_2=benefit_2,
            package_description=package_descriptions.get(pkg_info["form_factor"], f"{context.package} package"),
            package_form_factor=pkg_info["form_factor"].replace("_", "-"),
            package_mounting_type=mounting_descriptions.get(pkg_info["mounting"], "standard"),
            package_strength=package_strengths.get(pkg_info["primary_benefit"], "reliability"),
            application=random.choice(self.APPLICATIONS),
            technology=random.choice(self.TECHNOLOGIES),
            performance_trait=random.choice(self.PERFORMANCE_TRAITS),
            key_feature=random.choice(self.KEY_FEATURES),
            environment=random.choice(self.ENVIRONMENTS),
            reliability_aspect=random.choice(self.RELIABILITY_ASPECTS),
            design_focus=random.choice(self.DESIGN_FOCUS),
            performance_outcome=random.choice(self.PERFORMANCE_OUTCOMES)
        )

        return self._sanitize_text(description)

    def _generate_manufacturer_name(self) -> str:
        prefix = random.choice(self.MANUFACTURER_PREFIXES)
        suffix = random.choice(self.MANUFACTURER_SUFFIXES)
        return f"{prefix}{suffix}" if random.random() < 0.7 else f"{prefix} {suffix}"

    def _generate_product_name(self, context) -> str:
        prefix = random.choice(self.PRODUCT_PREFIXES)
        comp_type = context.component_type.upper()
        patterns = [f"{prefix}-{comp_type[:3]}{random.randint(100, 999)}",
                    f"{prefix}{comp_type[:4]}-{random.choice(['TX', 'RX', 'MX', 'LX', 'HX'])}{random.randint(1, 99)}",
                    f"{comp_type[:2]}{random.randint(1000, 9999)}{random.choice(['A', 'B', 'C', 'X', 'P'])}",
                    f"{prefix} {comp_type} Series {random.randint(1000, 9999)}"]
        return random.choice(patterns)

    def _generate_description(self, context, manufacturer: str, product_name: str) -> str:
        """
        פונקציית יצירת תיאור סטנדרטית (ללא package_specs מפורטים).
        ממלאת את כל המשתנים הנדרשים לתבניות באמצעות נתונים בסיסיים.
        """
        template = random.choice(self.DESCRIPTION_TEMPLATES)

        # 1. שליפת מידע בסיסי על המארז (למניעת KeyError)
        pkg_info = self.package_characterizer.get_package_info(context.package)

        # 2. חישוב Benefits רנדומליים (כמו בקוד המקורי)
        benefit_categories = random.sample(list(self.PACKAGE_BENEFITS.keys()), 2)
        package_benefit_1 = random.choice(self.PACKAGE_BENEFITS[benefit_categories[0]])
        package_benefit_2 = random.choice(self.PACKAGE_BENEFITS[benefit_categories[1]])
        if not package_benefit_2[0].isupper():
            package_benefit_2 = package_benefit_2[0].upper() + package_benefit_2[1:]

        # 3. הגדרת המיפויים החסרים (הסיבה לקריסה הקודמת!)
        package_descriptions = {
            "through_hole": f"{context.package} through-hole package",
            "surface_mount": f"industry-standard {context.package} surface-mount package",
            "specialized": f"{context.package} specialized package"
        }
        mounting_descriptions = {
            "screw_mount": "bolt-down",
            "smd_reflow": "surface-mount",
            "isolated_mount": "electrically isolated",
            "flange_bolt": "flange-mounted"
        }
        package_strengths = {
            "thermal": "superior thermal management",
            "space": "compact footprint and high power density",
            "mechanical": "mechanical robustness and vibration resistance",
            "reliability": "proven long-term reliability"
        }

        # 4. הרכבת מילון הארגומנטים המלא
        args = {
            "product_name": product_name,
            "manufacturer": manufacturer,
            "component_type": context.component_type,
            "package": context.package,
            "application": random.choice(self.APPLICATIONS),
            "package_benefit_1": package_benefit_1,
            "package_benefit_2": package_benefit_2,
            "technology": random.choice(self.TECHNOLOGIES),
            "performance_trait": random.choice(self.PERFORMANCE_TRAITS),
            "key_feature": random.choice(self.KEY_FEATURES),
            "environment": random.choice(self.ENVIRONMENTS),
            "reliability_aspect": random.choice(self.RELIABILITY_ASPECTS),
            "design_focus": random.choice(self.DESIGN_FOCUS),
            "performance_outcome": random.choice(self.PERFORMANCE_OUTCOMES),

            # --- התיקון: מילוי השדות שהיו חסרים ---
            "package_description": package_descriptions.get(pkg_info["form_factor"], f"{context.package} package"),
            "package_form_factor": pkg_info["form_factor"].replace("_", "-"),
            "package_mounting_type": mounting_descriptions.get(pkg_info["mounting"], "standard"),
            "package_strength": package_strengths.get(pkg_info["primary_benefit"], "reliability")
        }

        # 5. יצירת הטקסט
        try:
            description = template.format(**args)
        except KeyError as e:
            # Fallback חירום למקרה שמשהו עדיין חסר
            print(f"⚠️ Template formatting error: {e}, using simple fallback.")
            description = f"The {product_name} is a reliable {context.component_type} in a {context.package} package."

        return self._sanitize_text(description)

    def _generate_section_intros(self, sections_present: List[str]) -> Dict[str, str]:
        section_intros = {}
        for section in sections_present:
            section_upper = section.upper()
            if any(keyword in section_upper for keyword in ['ABS', 'MAX', 'ABSOLUTE']):
                category = 'abs_max'
            elif any(keyword in section_upper for keyword in ['THERM', 'THERMAL']):
                category = 'thermal'
            elif any(keyword in section_upper for keyword in ['DYN', 'SWITCH', 'AC']):
                category = 'dynamic'
            elif any(keyword in section_upper for keyword in ['MECH', 'PKG']):
                category = 'mechanical'
            elif any(keyword in section_upper for keyword in ['REL', 'QUALITY']):
                category = 'reliability'
            elif any(keyword in section_upper for keyword in ['ELEC', 'DC']):
                category = 'electrical'
            else:
                category = 'default'
            section_intros[section] = random.choice(self.SECTION_INTRO_TEMPLATES[category])
        return section_intros

    def _generate_footnotes(self, context) -> List[str]:
        footnote_pool = ["All specifications measured at 25°C ambient temperature.",
                         "Pulse width limited by safe operating area.",
                         "Thermal resistance values based on standard JEDEC test board.",
                         "Production tested parameters are 100% verified.",
                         "Specifications subject to change without notice.", "RoHS compliant and halogen-free."]
        return random.sample(footnote_pool, random.randint(1, 3))

    def _parse_json(self, text: str, context) -> Dict[str, Any]:
        try:
            clean_text = text.replace("```json", "").replace("```", "").strip()
            return json.loads(clean_text)
        except:
            try:
                match = re.search(r'\{.*\}', text, re.DOTALL)
                if match: return json.loads(match.group())
            except:
                pass
        return self._get_fallback_data(context)

    def _get_fallback_data(self, context) -> Dict[str, Any]:
        if context is None: return {"marketing_name": "GEN-1000", "manufacturer": "Standard Semi",
                                    "description": "Generic comp.", "section_intros": {}, "footnotes": []}
        print("⚠️ LLM failed, using template-based fallback")
        return self._generate_with_templates(context, [])

    def _sanitize_text(self, text: str) -> str:
        replacements = {'generic comp': 'specialized component', 'generic component': 'high-performance device',
                        'standard part': 'precision device', 'basic device': 'engineered solution',
                        'simple component': 'optimized component', 'null': 'N/A', 'undefined': 'specified', '###': '',
                        'ERROR': 'nominal', 'FAILED': 'tested'}
        result = text
        for old, new in replacements.items():
            result = result.replace(old, new)
            result = result.replace(old.upper(), new.upper())
            result = result.replace(old.lower(), new.lower())
        return result
