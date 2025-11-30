# Datasheet Extraction: Synthetic Data Generation Design Space

## Overview
This document defines the **Design Space** for the synthetic data generation pipeline. It outlines the **Prompt Attributes** (input parameters for the generator) and the **Label Space** (the extraction schema) used to train the Document AI model (e.g., LayoutLM, Donut).

The project architecture follows a **"Deep & Wide" strategy** to demonstrate model generalization:
1.  **Deep:** Deep handling of **Complex Active Components** (MOSFETs, LDOs) with multi-condition tables.
2.  **Wide:** Broad coverage of **Simple Passive Components** (Resistors, Capacitors) with varied structures.
3.  **Universal:** Common metadata extraction across all component types.

---

## 1. Prompt Attributes (Input Design Space)
These parameters serve as the "knobs" for the synthetic generator. Randomizing these attributes ensures high coverage and model robustness against real-world variability.

### A. Content & Domain (The "What")
Controls the technical content, terminology, and measurement units.

#### 1. Component Families
* **Family A: Complex Active Components**
    * **MOSFET:** Includes $V_{DS}$, $I_D$, $R_{DS(on)}$ tables with varying test conditions ($V_{GS}$, $I_D$).
    * **LDO (Voltage Regulator):** Includes Dropout Voltage, Input/Output ranges, and quiescent current.
* **Family B: Simple Passive Components**
    * **Capacitor:** Dielectric types (X7R, C0G), Tolerance, Voltage ratings.
    * **Resistor:** Power ratings, Resistance values, Tolerance codes.

#### 2. Technical Depth
* **Minimalist:** Basic specifications only (Summary sheets).
* **Standard:** Full electrical characteristic tables.
* **Professional/High-Rel:** Includes absolute maximum ratings, extensive footnotes, and derating info.

#### 3. Test Conditions & Behavior
* **Single Condition:** Standard ambient ($25^\circ C$).
* **Multi-Condition:** Dual temperature ($25^\circ C$, $125^\circ C$).
* **Full Range:** Industrial/Automotive ranges ($-40^\circ C \dots 125^\circ C$).

### B. Structure & Layout (The "How")
Controls the visual presentation to train the model's spatial understanding.

#### 4. Document Structure
* **Classic:** Features $\rightarrow$ Description $\rightarrow$ Tables.
* **One-Pager:** Condensed summary format.
* **Hybrid:** Datasheet combined with application notes.

#### 5. Parameter Presentation Style
* **Standard Tables:** Grid lines with headers.
* **Minimalist Tables:** No vertical lines, sparse spacing.
* **Merged Cells:** Tables with grouped conditions using `rowspan`/`colspan`.
* **Embedded Units:** Values containing units (e.g., "50V") inside the cell vs. separate "Unit" columns.

#### 6. Visual Noise & Distractors
* **Graphical Elements:** Circuit schematics, package blueprints, V-I curve graphs.
* **Distractor Text:** Marketing text, "Confidential" watermarks, legal disclaimers.

### C. Noise & Robustness (Real-World Simulation)
Simulates scanning artifacts and varying document quality.

#### 7. Data Density
* **High Density:** Small fonts ($<9pt$), zero padding, compact line height, multi-column layout.
* **Low Density:** Large fonts, generous padding, whitespace, single-column layout.

#### 8. Artifact Injection
* **OCR Noise:** Character confusion (0 vs O, 1 vs l), broken glyphs.
* **Scan Quality:** Skew/Rotation ($\pm 2^\circ$), salt-and-pepper noise, blur, low resolution.

---

## 2. Label Space (Output Extraction Schema)
Defines the target JSON structure for the extraction model.

### Key Architectural Decision:
To handle complex engineering data, parameters are extracted as **Lists of Objects** rather than single values. This allows capturing values alongside their specific **Test Conditions**.

**JSON Structure Example:**
```json
"Rds_on": [
    {
        "value": 0.030,
        "unit": "Ω",
        "condition": "Vgs=10V, Id=20A"
    },
    {
        "value": 0.045,
        "unit": "Ω",
        "condition": "Vgs=4.5V, Id=15A"
    }
]

### 
class DataGenerationPipeline:
    def __init__(self):
        self.sampler = AttributeSampler()      # Stage 1
        self.generator = ContentGenerator()    # Stage 2
        self.renderer = HTMLRenderer()         # Stage 3
        self.augmentor = ArtifactAugmentor()   # Stage 4

    def run(self, num_samples):
        for _ in range(num_samples):
            # 1. Config
            config = self.sampler.sample_config()
            
            # 2. Content (Ground Truth)
            ground_truth = self.generator.create_data(config)
            
            # 3. Render (HTML)
            html_raw = self.renderer.render(ground_truth, config)
            
            # 4. Augment (Final Artifact)
            final_image = self.augmentor.process(html_raw, config.noise_level)
            
            # 5. Save
            self.save_pair(final_image, ground_truth)