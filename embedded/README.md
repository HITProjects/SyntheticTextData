# Automated Datasheet Extraction using Synthetic Data & GenAI 📄⚡
# A data-centric pipeline for parsing electronic component specifications from PDFs to structured JSON.

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

# 🎯 Motivation: Bridging the Data Gap in Electronics
In the modern electronics industry, datasheets serve as the authoritative source of truth for design, procurement, and manufacturing. However, extracting critical intelligence from these documents remains a manual, labor-intensive, and error-prone process, creating significant bottlenecks in supply chain and development workflows.

The core challenge is technological: standard OCR tools and generic NLP models fail to interpret the complex structure of engineering tables, variable units of measurement, and precise numerical values found in technical documents. Furthermore, the most critical barrier is the complete absence of a high-quality, labeled Dataset specific to the electronics domain, which makes it impossible to train advanced Document Understanding models (such as LayoutLM) effectively.

Our solution addresses this gap through a Data-Centric AI approach. Instead of relying on expensive and limited manual labeling, we developed a Synthetic Data Factory. This system procedurally generates realistic datasheets complete with visual noise, diverse layouts, and physical consistency constraints. Crucially, every generated document is automatically paired with Perfect Ground Truth in JSON format. This enables, for the first time, the large-scale training of Deep Learning models capable of automating component comparison, BOM optimization, and intelligent supply chain management.

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
