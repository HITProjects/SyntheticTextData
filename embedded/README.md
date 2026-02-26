# Automated Datasheet Extraction using Synthetic Data & GenAI 📄⚡
## A data-centric pipeline for parsing electronic component specifications from HTML to structured JSON.
### Niv Saban

## 🚀 Executive Summary
This project tackles one of the most persistent challenges in the electronics industry: transforming unstructured PDF datasheets into accessible, accurate digital intelligence.

While standard OCR solutions fail to interpret dense engineering tables and complex technical terminology, I developed a unique Data-Centric approach: instead of manually labeling thousands of documents, I engineered a Synthetic Data Factory that automatically generates realistic training documents paired with perfect Ground Truth labels. By combining a "Physics-Aware" engine with GenAI, the generated data accurately simulates real-world electrical correlations and diverse narrative styles.

Beyond generation, the pipeline meticulously prepares this data for deep learning by parsing structural HTML as rich text and applying advanced sub-word token alignment (using PyTorch's masking techniques for BIO tags). Finally, this 100% accurate ground truth is used to fine-tune a DeBERTa model for Joint Entity & Relation Extraction, enabling it to semantically map complex hardware specifications without a single manual annotation.

<img width="1408" height="768" alt="Gemini_Generated_Image_h0alkhh0alkhh0al" src="https://github.com/user-attachments/assets/a7a0e36b-7fa4-466e-b27e-53dc66088721" />

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

# ✨ Key Features

⚛️ **Physics-Aware Data Generation**: Standard random generators fail in engineering. This engine implements an electrical constraints solver, ensuring that generated parameters obey physical laws. The data is engineeringly valid, not just syntactically correct.

    From the field: If the system generates a TO-220 package, the Physics Engine hard-codes the Thermal Resistance ($R_{\theta JC}$) to a realistic 0.5-2.0 °C/W.      The LLM is then mathematically locked to these facts, preventing it from hallucinating a physically impossible 50 °C/W for a high-power package.

🤖 **GenAI-Powered Text Enrichment**
Integrates Local LLMs (via Ollama) to generate context-aware descriptive text, footnotes, and marketing disclaimers. This simulates the narrative variance found in real datasheets (e.g., TI vs. Vishay vs. ON Semi styles).

🎯 **Perfect Label Alignment (Zero Annotation Noise)**
Eliminates manual annotation. The pipeline generates synthetic HTML alongside perfectly structured BIO (Begin, Inside, Outside) tags and semantic relations. The labeling is handled deterministically by the generation script, guaranteeing zero noise in the Ground Truth.

🧠 **Joint Entity & Relation Extraction (DeBERTa)**
Moves beyond visual models by parsing HTML structure as rich text. The pipeline trains a DeBERTa-based model to simultaneously identify engineering entities and the explicit relationships between them (e.g., mapping a specific voltage to its exact test condition).

⚙️ **Advanced Token Alignment**
Utilizes PyTorch's -100 index masking trick to perfectly align word-level BIO tags with DeBERTa's sub-word tokenization, ensuring clean and efficient loss calculation during training.

🔌 **Extensible Component Architecture**
Built on a modular Object-Oriented Design (OOD). Adding a new electronic component (e.g., moving from MOSFETs to IGBTs) only requires defining a new configuration class, making the system highly scalable to the entire electronics catalog.

---

## 🧩 System Architecture

### 1. The Synthetic Data Pipeline

<img width="2816" height="1504" alt="Gemini_Generated_Image_kr0z7nkr0z7nkr0z" src="https://github.com/user-attachments/assets/a1cf2684-f4c8-4d4e-beec-ac861dc6b42d" />

The generation pipeline ensures strict synchronization between the visual output and the Ground Truth. For each generated datasheet, a central coordinator executes the following sequence:

**Dynamic Configuration (RenderingConfig):** Applies randomized structural rules across the document, such as hiding specific columns, transposing tables, or shifting long test conditions to footnotes.

**Adversarial Partitioning & NLG:** Randomly extracts certain parameters from tables and injects them into natural language paragraphs ("Needle in a Haystack"). This forces the model to learn extraction from both structured tables and unstructured text.

**Synchronized Dual Rendering:** The configured data is simultaneously processed by two engines:

   DatasheetHtmlRenderer: Generates the visual HTML document, incorporating dynamic CSS themes, generated engineering charts, and hidden structural BIO tags.

   DatasheetJSONRenderer: Produces the 100% accurate training JSON. It outputs both entity-centric labels for NER and relation-centric triples (Subject-Predicate-    Object) to train the DeBERTa model on complex semantic relationships.

   ## Dynamic Template Generation Engine

<img width="802" height="454" alt="image" src="https://github.com/user-attachments/assets/cd066f2b-d6fa-4389-b04d-291a1f9c9419" />

The rendering engine generates diverse HTML DOM structures for a single component. By randomizing table layouts, hiding columns, transposing sections, and injecting adversarial structural noise, the pipeline simulates the true chaos of real-world datasheets, preventing the DeBERTa model from overfitting to specific templates.


## 📊 Outputs: From Unstructured HTML to Hierarchical JSON


<img width="786" height="675" alt="image" src="https://github.com/user-attachments/assets/2f8b007a-9926-456e-b67a-c67e07119623" />

Unlike standard OCR tools that produce flat text, the pipeline generates a perfectly matched JSONL Ground Truth. By atomizing parameters into granular attributes (Min/Typ/Max, Units, Conditions), it provides the rich hierarchical structure needed for Deep Learning models to understand physical correlations, going far beyond simple text recognition.


 ### 2.⚙️ Data Preprocessing & Token Alignment
 
 <img width="2816" height="1536" alt="Preprocessing _Pipeline" src="https://github.com/user-attachments/assets/0efcd442-a03c-4cd0-ae63-5813ddb5cc37" />
Before feeding the generated data into the network, the raw HTML and JSONL undergo a rigorous preprocessing pipeline. The structural HTML is parsed into a continuous token stream while preserving its inherent layout context. The most critical step here is **Sub-word Token Alignment**. Because DeBERTa uses a sub-word tokenizer, a single engineering term might be split into multiple tokens. To maintain perfect label fidelity, the pipeline applies PyTorch's `-100` index masking trick: only the first sub-word receives the original BIO tag, while the rest are masked. This ensures the model learns precise entity boundaries without the loss function penalizing tokenization artifacts.

### 🔬 Technical Deep-Dive & Architecture

The pipeline utilizes robust NLP engineering practices to ensure high fidelity during tokenization, alignment, and joint extraction.

* **Structural Preservation:** Table structures are preserved using explicit structural tokens (`\t`, `\n`), enabling the model to learn cross-cell relationships without relying on heavy visual layout models.
* **Overlapping Sliding Windows:** To handle long HTML documents that exceed standard transformer limits, the pipeline implements overlapping sliding windows (512 tokens, 50-token overlap). Crucially, it includes a **BIO boundary repair mechanism** (converting `I-` to `B-` at splits) to ensure valid entity sequences across segment boundaries.
* **Relation Grounding:** Relations are grounded via normalized phrase matching and proximity-based disambiguation based on token indices, rather than fragile character offsets.

#### 🧠 Joint Network Architecture
The extraction engine is powered by a **DeBERTa-v3-base** shared encoder with two parallel heads:
1. **Token-level classification head** for BIO-based Named Entity Recognition (NER).
2. **Span-pooled pairwise classification head** for Relation Extraction (RE). For each candidate entity pair, span representations are obtained via mean pooling over subword tokens and concatenated before classification.

The joint loss is optimized with a heavier weight on NER to ensure stable relation extraction:
$L=\alpha\cdot L_{NER}+\beta\cdot L_{RE}$ (where $\alpha=1.0$, $\beta=0.5$).

---

### 📊 Dataset & Training Statistics

To prevent class imbalance—a notorious issue in relation extraction—**relation negative sampling is explicitly controlled with a 1:1 positive-to-negative ratio**.

#### 📈 Dataset Scale & Complexity
*(Note: Metrics based on a standard generation run of 8,000 components)*

| Metric | Count / Details | Why it matters |
| :--- | :--- | :--- |
| **Total Generated Documents** | `8000` | Demonstrates pipeline scalability across diverse templates. |
| **Avg. Tokens per Document** | `~X,XXX` | Exceeds standard 512-token limit, necessitating the sliding window mechanism. |
| **Total Annotated Entities** | `~X.X Million` | Covers 7 semantic categories (e.g., PARAMETER, VALUE). |
| **Total Semantic Relations** | `~X.X Million` | Covers 6 relation types (e.g., `has_value`, `has_condition`). |

#### ⚙️ Hyperparameters & Training Strategy
A seeded 90/10 train-validation split is used, with best checkpoint selection based on validation loss. We employ a **Differential Learning Rate strategy**, fine-tuning the base encoder carefully while training the task-specific heads more aggressively.

| Parameter | Value | Parameter | Value |
| :--- | :--- | :--- | :--- |
| **Model** | `microsoft/deberta-v3-base` | **Max Sequence Length** | 512 |
| **Effective Batch Size**| 8 | **Epochs** | 3 |
| **Encoder LR** | 2e-5 | **Head LR** | 1e-4 (5× Encoder LR) |
| **Weight Decay** | 0.01 | **Gradient Clipping** | 1.0 (FP16 Enabled) |

## 🔮 Roadmap & Future Scope (must edit)

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
