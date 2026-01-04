# Automated Datasheet Extraction using Synthetic Data & GenAI 📄⚡
## A data-centric pipeline for parsing electronic component specifications from PDFs to structured JSON.
### Niv Saban

## 🚀 Executive Summary
This project tackles one of the most persistent challenges in the electronics industry: transforming unstructured PDF datasheets into accessible, accurate digital intelligence.

While standard OCR solutions fail to interpret dense engineering tables and complex technical terminology, I developed a unique Data-Centric approach: instead of manually labeling thousands of documents, I engineered a Synthetic Data Factory that automatically generates realistic training documents paired with perfect Ground Truth labels.

At its core, the system utilizes a hybrid "Physics-Aware" engine. Unlike simple random generators, it enforces strict electrical correlations (e.g., relating $V_{DS}$ to $R_{DS(on)}$ in MOSFETs) to ensure engineering validity. This structured data is then enriched by Local LLMs (GenAI) to simulate the varied, unstructured narrative styles found in real-world documentation, creating a robust dataset for training state-of-the-art extraction models.

---

## Dynamic Template Generation Engine

<img width="802" height="454" alt="image" src="https://github.com/user-attachments/assets/cd066f2b-d6fa-4389-b04d-291a1f9c9419" />
Visual heterogeneity in action. The system creates diverse HTML/PDF representations for a single component ID, simulating the real-world chaos of unstructured datasheets.


# ✨ Key Features

⚛️ **Physics-Aware Data Generation**
Unlike standard random generators, this engine implements an electrical constraints solver. It ensures that generated parameters obey physical laws (e.g., calculating $P = V \times I$ or correlating $R_{DS(on)}$ with breakdown voltage), creating data that is engineeringly valid, not just syntactically correct.

🤖 **GenAI-Powered Text Enrichment**
Integrates Local LLMs (via Ollama) to generate context-aware descriptive text, footnotes, and marketing disclaimers. This simulates the unstructured narrative variance found in real datasheets (e.g., TI vs. Vishay vs. ON Semi styles).

🎯 **Zero-Shot Ground Truth Labeling**
Eliminates the need for manual annotation. The pipeline generates the visual PDF/HTML alongside a perfectly structured JSON Ground Truth file, guaranteeing 100% label accuracy for training Deep Learning models.

🎨 **Dynamic Layout & Noise Injection**
Simulates real-world data heterogeneity by randomizing HTML/CSS templates (Single/Dual column, varying font families) and injecting synthetic "scan noise" (blur, rotation, artifacts) to ensure model robustness against low-quality inputs.

🔌 **Extensible Component Architecture**
Built on a modular Object-Oriented Design (OOD). Adding a new electronic component (e.g., moving from MOSFETs to IGBTs) only requires defining a new configuration class, making the system highly scalable to the entire electronics catalog.

---

## 👥 Target Use Cases
1. Hardware Engineers & R&D Teams:
   Accelerating R&D cycles by transforming static PDFs into a queryable component database, allowing engineers to focus on innovation rather than manual data         entry.

2. Procurement & Supply Chain Managers:
   Ensuring supply chain resilience through automated cross-referencing, instantly identifying cost-effective, drop-in replacements to mitigate shortages and         optimize BOM costs.

3. Component Distributors & EDA Tool Providers:
   Powering the next generation of parametric search engines by ingesting and structuring manufacturer data at scale with zero manual overhead.

4. QA & Compliance Officers:
   Enhancing quality assurance by automatically validating component specifications against design requirements, minimizing integration risks before mass             production.
  
---

## 📉 The Bottleneck: Why Models Fail in Electronics

While Document Understanding models (like LayoutLM and Donut) have revolutionized generic document processing, they remain ineffective in the electronics domain due to a critical Data Scarcity. There are simply no public, large-scale, annotated datasets for component datasheets.
The resulting "Cold Start" problem forces companies to rely on fragile RegEx scripts or manual entry. This project flips the paradigm: instead of tweaking model architectures to handle low-resource tasks, we solve the root cause by engineering an infinite stream of high-quality, domain-specific training data, effectively unlocking the potential of State-of-the-Art Transformers for hardware engineering.

---

## 🧩 System Architecture

<img width="1024" height="559" alt="image" src="https://github.com/user-attachments/assets/07218bf7-5035-418c-ad93-182636bb022f" />


---

## 📊 Outputs: From Unstructured PDF to Hierarchical JSON


<img width="1024" height="559" alt="image" src="https://github.com/user-attachments/assets/786c769f-79da-4de6-bf9f-9080db82b15a" />


For every visually generated datasheet, the pipeline simultaneously produces a perfectly matched Ground Truth JSON with 100% label accuracy.

Unlike standard OCR tools that output flat, unstructured text, this system enforces a strict Engineering Data Structure. As demonstrated in the sample below, the JSON preserves the component's complex taxonomy, atomizing each parameter into its granular attributes:

Hierarchical Context: Clearly distinguishes between parent categories (e.g., Power Rating vs. Dissipation Factor).

Granular Parsing: Deconstructs values into Min/Typ/Max, Units, and Test Conditions.

Physics-Aware Training: This rich semantic structure enables Deep Learning models to go beyond simple text recognition, allowing them to "understand" the underlying physical correlations within the data without requiring manual annotation.

## 🔮 Roadmap & Future Scope

This project represents the **Data-Centric** foundation of a larger Document Understanding pipeline. While the current release focuses on the generation of high-fidelity synthetic data, the immediate roadmap involves leveraging this asset for downstream tasks:

1.  **Model Training (LayoutLMv3 / Donut):**
    Fine-tuning multimodal Transformer models on the generated dataset. Since the data includes perfect bounding boxes and semantic labels, we can train models to perform **Information Extraction (IE)** and **Question Answering (QA)** on technical documents with zero manual annotation.

2.  **Sim2Real Adaptation:**
    Validating the model's performance on a "Gold Set" of real-world scanned datasheets. We plan to employ domain adaptation techniques to bridge the gap between our synthetic styles and the noisy, real-world scans found in legacy archives.

3.  **Benchmarking & Physics Validation:**
    Comparing the *Physics-Aware* approach against standard random-data baselines. We aim to quantify how maintaining engineering consistency in the training data improves the model's ability to hallucinate less and detect numerical anomalies in real inference scenarios.

## 🛠️ Getting Started

### Prerequisites
* **Python 3.8+**
* **Ollama** (Required for local LLM inference).
    * *Installation:* [Download Ollama](https://ollama.com/) and pull the base model:
        ```bash
        ollama pull qwen2.5:1.5b
        ```
* **wkhtmltopdf** (Required for rendering visual artifacts).

### Installation

```bash
# 1. Clone the repository
git clone [https://github.com/HITProjects/SyntheticTextData.git](https://github.com/HITProjects/SyntheticTextData.git)

# 2. Navigate to the project directory
cd SyntheticTextData/embedded

# 3. Install Python dependencies
pip install -r requirements.txt
