# Synthetic Data Generation for Electronics Datasheets 📄⚡

## 📌 Project Overview
This project presents an End-to-End pipeline for the procedural generation of synthetic electronics datasheets. The system generates high-fidelity visual documents (HTML/PDF) paired with structured JSON Ground Truth.

The primary goal is to solve the **data scarcity** problem in the electronics domain and enable the training of **State-of-the-Art (SOTA)** Document Understanding models for automated specification analysis.

---

## 🎯 Motivation
Training AI models for document extraction (such as LayoutLM, Donut) requires thousands of labeled examples. In the electronics domain, this presents a dual challenge:
1.  **Data Complexity:** Datasheets contain complex multi-condition tables, diverse units of measurement, and technical diagrams that are difficult to label manually.
2.  **Labeling Cost:** Manual annotation of thousands of technical documents is expensive, slow, and prone to human error.

Our system allows for the generation of **infinite** perfect training examples with zero human intervention, accelerating R&D in Automated Specification Analysis.

---

## 👥 Target Use Cases
- Training document-understanding models (LayoutLM, Donut, Pix2Struct)
- Benchmarking OCR & table extraction pipelines
- Rapid prototyping of spec-mining systems in electronics R&D

---

## ❓ Problem Definition
The core problem is the lack of a high-quality, labeled public dataset for electronic datasheets that captures real-world diversity.
A synthetic dataset must address:
* **Visual Diversity:** Various design styles (Vintage, Modern, Industrial).
* **Physical Consistency:** Data must be physically plausible (e.g., high voltage in a MOSFET implies higher $R_{DS(on)}$).
* **Natural Language:** Integration of textual descriptions and footnotes that mimic human engineering writing.

---

## 🧩 System Architecture
Component DB → Physical Correlation Engine → LLM Enrichment → HTML Renderer → JSON + HTML Outputs

---

## ⚙️ Methodology & Process

The system is built on a "Deep & Wide" architecture covering both complex active components and standardized passive components.

### 1. Unified Component Database
A hierarchical database defining physical boundaries, units, and operating conditions for a wide range of components (Resistors, Capacitors, MOSFETs, Diodes, Voltage Regulators, etc.).

### 2. Physical Correlation Engine (PCE) 🧠
A logic engine ensuring generated data maintains **physical plausibility**.
* **Example:** The engine ensures that as Capacitance ($C$) increases, ESR decreases, or that larger Packages correlate with higher Power Dissipation ratings.

### 3. LLM Enrichment Layer (Ollama & Qwen) 🤖
To simulate human-written documents, the pipeline utilizes a locally running Large Language Model (LLM):
* **Model:** `qwen2.5:3b` (via Ollama).
* **Role:** Generates creative metadata—marketing names, persuasive product descriptions, technical footnotes, and section intros. This ensures every datasheet looks unique and non-templated.

### 4. Visual Rendering Engine 🎨
An engine that converts structured data into HTML using dynamic CSS themes. Supported styles include:
* *Legacy Databook* (80s style).
* *Modern Tech* (Clean, IoT style).
* *Industrial Heavy* (High contrast).

---

## 📊 Results

For every generated sample, the system produces two outputs:

1.  **JSON Ground Truth:** A structured file containing all technical values hierarchically (Min/Typ/Max, Conditions, Units). This serves as the perfect label for training.
2.  **HTML Datasheet:** A visual file simulating a real datasheet, which can be rendered into an image or PDF (input for Vision models).

**Sample Output Generation:**
* **Component:** High Power MOSFET
* **Correlation Applied:** High $V_{DSS}$ $\to$ Adjusted $R_{DS(on)}$.
* **LLM Output:** "Optimized for high-efficiency synchronous rectification applications..."
