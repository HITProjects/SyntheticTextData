import random
import re
import io

try:
    import numpy as np
    _HAS_NP = True
except ImportError:
    np = None
    _HAS_NP = False

try:
    import cv2
    _HAS_CV2 = True
except ImportError:
    cv2 = None
    _HAS_CV2 = False

try:
    import matplotlib
    matplotlib.use('Agg')  # non-GUI backend — safe in worker threads
    import matplotlib.pyplot as plt
    _HAS_MPL = True
except ImportError:
    plt = None
    _HAS_MPL = False


class TextDegradationAugmentor:
    """
    מוסיף רעש ריאליסטי של PDF דיגיטלי ל-HTML הסינטטי.
    פועל על תוכן ה-span בלבד — התגיות עצמן לא משתנות.
    ה-JSON (ground truth) נשאר נקי לחלוטין.

    Args:
        intensity: עוצמת הרעש בין 0.0 ל-1.0. מומלץ: 0.5.
    """

    COLUMN_ABBREVIATIONS = {
        "Typical":   ["Typ.", "Typ", "Nom.", "Nom", "Avg.", "Avg"],
        "typical":   ["typ.", "typ", "nom.", "nom", "avg.", "avg"],
        "Minimum":   ["Min.", "Min", "Lower Limit", "From"],
        "minimum":   ["min.", "min"],
        "Maximum":   ["Max.", "Max", "Upper Limit", "Limit", "To"],
        "maximum":   ["max.", "max"],
        "Parameter": ["Param.", "Param", "Characteristic", "Spec."],
        "parameter": ["param.", "param"],
        "Condition": ["Cond.", "Cond", "Test Cond.", "@ Cond."],
        "condition": ["cond.", "cond"],
    }

    SPECIAL_CHAR_REPLACEMENTS = [
        (r'µ',   ['u', 'μ'],        0.6),
        (r'°C',  ['degC', 'oC'],    0.5),
        (r'±',   ['+/-'],           0.5),
        (r'Ω',   ['Ohm', 'ohm'],    0.4),
        (r'≤',   ['<='],            0.4),
        (r'≥',   ['>='],            0.4),
    ]

    _NUMBER_UNIT_PATTERN = re.compile(
        r'(\d+\.?\d*)\s+'
        r'(m?V|mA|µA|uA|nA|A|'
        r'mΩ|Ohm|kΩ|MΩ|Ω|'
        r'pF|nF|µF|uF|mF|'
        r'ns|µs|us|ms|'
        r'MHz|kHz|GHz|Hz|'
        r'mW|kW|W|'
        r'degC|°C|oC|'
        r'%|ppm|dB)'
    )

    def __init__(self, intensity: float = 0.5):
        self.intensity = max(0.0, min(1.0, intensity))

    def degrade(self, html_content: str) -> str:
        """מחיל רעש על כל span ב-HTML."""
        if self.intensity == 0.0:
            return html_content
        return re.sub(
            r'(<span[^>]*>)(.*?)(</span>)',
            self._degrade_span,
            html_content,
            flags=re.DOTALL
        )

    def _degrade_span(self, match: re.Match) -> str:
        open_tag  = match.group(1)
        content   = match.group(2)
        close_tag = match.group(3)

        if not content.strip() or content.strip() in ('—', '-', ''):
            return match.group(0)
        if '<' in content:
            return match.group(0)

        degraded = content
        degraded = self._apply_column_abbreviations(degraded)
        degraded = self._apply_number_unit_merge(degraded)
        degraded = self._apply_special_chars(degraded)
        degraded = self._apply_line_breaks(degraded)
        degraded = self._apply_word_merging(degraded)   # ← חדש
        return f"{open_tag}{degraded}{close_tag}"

    def _apply_column_abbreviations(self, text: str) -> str:
        if random.random() > 0.35 * self.intensity:
            return text
        for full_name, abbreviations in self.COLUMN_ABBREVIATIONS.items():
            if full_name in text:
                text = text.replace(full_name, random.choice(abbreviations), 1)
                break
        return text

    def _apply_number_unit_merge(self, text: str) -> str:
        if random.random() > 0.45 * self.intensity:
            return text
        return self._NUMBER_UNIT_PATTERN.sub(
            lambda m: f"{m.group(1)}{m.group(2)}", text
        )

    def _apply_special_chars(self, text: str) -> str:
        for pattern, replacements, base_prob in self.SPECIAL_CHAR_REPLACEMENTS:
            if random.random() < base_prob * self.intensity:
                text = re.sub(pattern, random.choice(replacements), text)
        return text

    def _apply_line_breaks(self, text: str) -> str:
        if random.random() > 0.20 * self.intensity:
            return text
        words = text.split()
        if len(words) < 3:
            return text
        split_idx = len(words) // 2
        return ' '.join(words[:split_idx]) + '\n' + ' '.join(words[split_idx:])

    def _apply_word_merging(self, text: str) -> str:
        if random.random() > 0.15 * self.intensity:
            return text
        words = text.split()
        if len(words) < 2:
            return text
        i = random.randint(0, len(words) - 2)
        words[i] = words[i].lower() + words[i + 1].lower()
        words.pop(i + 1)
        return ' '.join(words)

    # ------------------------------------------------------------------
    # NER window noise — applied to parts[] before text assembly
    # ------------------------------------------------------------------

    _NER_SEP_SUBS = {
        "Parameter: ":     ["Param: ", "PARAM ", "Spec: "],
        " | Min: ":        ["\tMin\t", " min ", " MIN "],
        " | Typ: ":        ["\tTyp\t", " typ ", " NOM "],
        " | Max: ":        ["\tMax\t", " max ", " LIM "],
        " | Conditions: ": ["\t", " @ ", " ; Cond: "],
        " min ":           [" Min. ", " minimum ", " MIN "],
        " typ ":           [" Typ. ", " nom. ", " NOM "],
        " max ":           [" Max. ", " maximum ", " LIM "],
        " @ ":             [" ; ", " at ", " (@ "],
        " ; ":             [" @ ", " | "],
        "[Param] ":        ["[P] ", "PARAM: "],
        " [Min] ":         ["\t", " min ", " [MIN] "],
        " [Typ] ":         ["\t", " typ ", " [TYP] "],
        " [Max] ":         ["\t", " max ", " [MAX] "],
        " [Cond] ":        [" @ ", " ; ", "\t"],
    }

    _UNIT_SUBS = [
        ("mΩ", ["mOhm", "mohm", "mΩ"],  0.50),
        ("kΩ", ["kOhm", "kohm", "kΩ"],  0.40),
        ("MΩ", ["MOhm", "Mohm", "MΩ"],  0.40),
        ("Ω",  ["Ohm",  "ohm",  "Ω"],   0.40),
        ("µA", ["uA",   "µA"],           0.50),
        ("µV", ["uV",   "µV"],           0.50),
        ("µs", ["us",   "µs"],           0.50),
        ("µF", ["uF",   "µF"],           0.50),
        ("°C", ["degC", "C",    "°C"],   0.45),
    ]

    def degrade_ner_parts(self, parts: list) -> list:
        """
        Apply realistic noise to NER window parts before text assembly.
        Only connector/separator text (label=None) and UNIT tokens are modified —
        MIN/TYP/MAX/PARAMETER/CONDITION values stay clean as ground truth.
        """
        if self.intensity == 0.0:
            return parts
        result = []
        for content, label in parts:
            if content is None or str(content).strip() == '':
                result.append((content, label))
                continue
            s = str(content)
            if label is None:
                s = self._degrade_ner_separator(s)
            elif label == "UNIT":
                s = self._degrade_unit(s)
            result.append((s, label))
        return result

    def _degrade_ner_separator(self, text: str) -> str:
        for key, variants in self._NER_SEP_SUBS.items():
            if key in text and random.random() < 0.35 * self.intensity:
                text = text.replace(key, random.choice(variants), 1)
        return text

    def _degrade_unit(self, text: str) -> str:
        for original, variants, prob in self._UNIT_SUBS:
            if original in text and random.random() < prob * self.intensity:
                return text.replace(original, random.choice(variants), 1)
        return text


class ScanAugmentor:
    """
    מחלקה להוספת אפקטים של סריקה ובלייה לתמונות דפי נתונים.
    גרסה מתוקנת: מתמקדת רק בעיבוד תמונה (OpenCV) ללא תלות ב-Html2Image.
    """

    def __init__(self):
        # ✅ תיקון: הסרנו את האתחול של Html2Image מכאן.
        # המחלקה הזו מקבלת תמונה מוכנה ומלכלכת אותה.
        pass

    def apply_rotation(self, image, max_angle=2.0):
        """סיבוב קל המדמה הנחה עקומה בסורק"""
        if image is None: return None
        angle = random.uniform(-max_angle, max_angle)
        h, w = image.shape[:2]
        center = (w // 2, h // 2)

        # מטריצת הסיבוב
        M = cv2.getRotationMatrix2D(center, angle, 1.0)
        # מילוי הרקע בלבן כדי שלא יהיו שוליים שחורים
        rotated = cv2.warpAffine(image, M, (w, h), borderValue=(255, 255, 255))
        return rotated

    def apply_blur(self, image):
        """טשטוש המדמה פוקוס לא מושלם בסורק"""
        if image is None: return None
        if random.random() < 0.5:
            # Gaussian Blur קל
            return cv2.GaussianBlur(image, (3, 3), 0)
        else:
            # טשטוש תנועה קל (Motion Blur)
            kernel_size = 3
            kernel = np.zeros((kernel_size, kernel_size))
            kernel[int((kernel_size - 1) / 2), :] = np.ones(kernel_size)
            kernel /= kernel_size
            return cv2.filter2D(image, -1, kernel)

    def apply_salt_and_pepper(self, image, prob=0.002):
        """רעש מלח-פלפל המדמה לכלוך על הזכוכית או אבק"""
        if image is None: return None
        output = np.copy(image)

        # רעש שחור (Pepper)
        num_pepper = np.ceil(prob * image.size * 0.5)
        coords = [np.random.randint(0, i - 1, int(num_pepper)) for i in image.shape]
        output[coords[0], coords[1], :] = 0

        # רעש לבן (Salt) - פחות קריטי על רקע לבן אבל קיים
        num_salt = np.ceil(prob * image.size * 0.5)
        coords = [np.random.randint(0, i - 1, int(num_salt)) for i in image.shape]
        output[coords[0], coords[1], :] = 255

        return output

    def apply_scan_artifacts(self, image):
        """הוספת הצללות או פסים של סורק (Scanner lines)"""
        if image is None: return None
        # הוספת "צל" הדרגתי (Vignette עדין)
        rows, cols = image.shape[:2]
        X_resultant_kernel = cv2.getGaussianKernel(cols, cols / 2)
        Y_resultant_kernel = cv2.getGaussianKernel(rows, rows / 2)
        kernel = Y_resultant_kernel * X_resultant_kernel.T
        mask = 255 * kernel / np.linalg.norm(kernel)

        # הפיכת המסכה שתהיה בהירה באמצע וכהה בקצוות
        mask = cv2.resize(mask, (cols, rows))
        mask = (mask - mask.min()) / (mask.max() - mask.min())
        mask = 0.8 + 0.2 * mask  # שומר על הבהירות, רק מכהה קצוות בקטנה

        # החלה על כל הערוצים
        if len(image.shape) == 3:
            mask = mask[:, :, np.newaxis]

        return (image * mask).astype(np.uint8)

    def degrade_quality(self, image, quality=85):
        """שמירה כ-JPEG איכות נמוכה וטעינה מחדש (Compression Artifacts)"""
        if image is None: return None
        encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), quality]
        result, encimg = cv2.imencode('.jpg', image, encode_param)
        decimg = cv2.imdecode(encimg, 1)
        return decimg


class RandomChartGenerator:
    """
    מייצר גרפים הנדסיים גנריים (ללא קשר לנתונים) כדי למלא את המקום ויזואלית

    ✅ FIX #3 APPLIED: Now accepts component_type and forces Linear plots for Resistors
    """

    STYLES = ['seaborn-v0_8-darkgrid', 'bmh', 'ggplot', 'classic']
    LABELS = [
        ('Voltage (V)', 'Current (A)'),
        ('Frequency (Hz)', 'Gain (dB)'),
        ('Temperature (°C)', 'Power Dissipation (W)'),
        ('Time (µs)', 'Voltage (V)'),
        ('Load Current (mA)', 'Dropout Voltage (mV)')
    ]

    @staticmethod
    def generate_chart_image(component_type: str = None) -> str:
        """
        מייצר גרף ומחזיר אותו כ-HTML Base64 Image

        ✅ FIX #3: If component_type is RESISTOR, force linear IV curve
        """
        if not _HAS_MPL or not _HAS_NP:
            return ""
        import base64

        # בחירת סגנון אקראי
        try:
            plt.style.use(random.choice(RandomChartGenerator.STYLES))
        except:
            plt.style.use('ggplot')

        # שינוי 1: הקטנת הפרופורציות (במקור היה 5, 3.5)
        # זה גורם לפונטים להיראות גדולים יותר יחסית לגרף, שזה טוב להקטנה
        fig, ax = plt.subplots(figsize=(4.5, 3), dpi=100)

        # יצירת דאטה פיקטיבי
        x = np.linspace(0, 10, 100)

        # ✅ FIX #3: Force linear chart for resistors
        if component_type and "RESISTOR" in component_type.upper():
            chart_type = 'linear'
        else:
            chart_type = random.choice(['linear', 'exp', 'log', 'saturation'])

        if chart_type == 'linear':
            y = random.uniform(0.1, 2) * x + random.uniform(0, 5)
        elif chart_type == 'exp':
            y = np.exp(x / random.uniform(2, 5))
        elif chart_type == 'log':
            y = np.log(x + 1) * random.uniform(1, 5)
        else:  # saturation
            y = 10 * (1 - np.exp(-x))

        # הוספת רעש קל
        y = y + np.random.normal(0, 0.2, len(x))

        ax.plot(x, y, linewidth=2)

        # עיצוב
        labels = random.choice(RandomChartGenerator.LABELS)
        ax.set_xlabel(labels[0], fontsize=9)
        ax.set_ylabel(labels[1], fontsize=9)
        # הקטנת הכותרת
        ax.set_title(f"Typical Characteristics", fontsize=10)
        ax.grid(True, linestyle='--', alpha=0.7)

        # שמירה לזיכרון
        buf = io.BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight')
        plt.close(fig)

        # המרה ל-Base64
        data = base64.b64encode(buf.getvalue()).decode('utf-8')

        # שינוי 2: CSS מגביל רוחב (max-width) וממרכז (margin: 0 auto)
        # הוספתי div עוטף כדי להבטיח מרכוז
        return f"""
        <div style="text-align: center; width: 100%; margin: 10px 0;">
            <img src="data:image/png;base64,{data}"
                 style="max-width: 60%; height: auto; border: 1px solid #ccc; box-shadow: 2px 2px 5px rgba(0,0,0,0.05);">
        </div>
        """
