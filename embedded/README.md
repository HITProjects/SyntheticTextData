# Automated Datasheet Extraction using Synthetic Data & GenAI
### A data-centric pipeline for parsing electronic component specifications from PDF to structured JSON.
**Niv Saban**

---

## Overview

This project addresses a core challenge in the electronics industry: extracting structured, machine-readable specifications from unstructured PDF datasheets at scale — without manual annotation.

The approach is fully data-centric: a **Synthetic Data Factory** generates realistic training datasheets with perfect ground-truth labels. A fine-tuned **DeBERTa** model then performs joint Named Entity Recognition and Relation Extraction. At inference time, a rule-based PDF preprocessing stage feeds into the trained model, producing structured JSON output.

<img width="1408" height="768" alt="pipeline_overview" src="https://github.com/user-attachments/assets/a7a0e36b-7fa4-466e-b27e-53dc66088721" />

---

## Pipeline

### Step 1 — Synthetic Data Generation

<img width="2816" height="1504" alt="synthetic_pipeline" src="https://github.com/user-attachments/assets/a1cf2684-f4c8-4d4e-beec-ac861dc6b42d" />

A physics constraints engine generates realistic electronic component datasheets. For each document, a central coordinator applies randomised structural rules (hidden columns, transposed tables, footnote injection), then feeds the configured data into two synchronised renderers:

- **HTML Renderer** — produces the visual datasheet with randomised CSS themes and layout noise.
- **JSON Renderer** — produces the 100%-accurate ground-truth labels (BIO entity tags + relation triples), deterministically derived from the same configuration.

This guarantees zero annotation noise: every generated document comes with a perfectly aligned label file.

**Tech stack:** Python · Ollama (`qwen2.5:1.5b`) · Physics constraints engine · wkhtmltopdf

**Output:** 11,400 synthetic HTML datasheets + aligned JSONL ground truth across 8 component types.

| Component Type | Samples | Ratio |
| :--- | :--- | :--- |
| RESISTOR | 1,800 | 15.8% |
| CAPACITOR | 1,800 | 15.8% |
| INDUCTOR | 1,800 | 15.8% |
| DIODE | 1,200 | 10.5% |
| MOSFET | 1,200 | 10.5% |
| BJT | 1,200 | 10.5% |
| OPAMP | 1,200 | 10.5% |
| VOLTAGE_REGULATOR | 1,200 | 10.5% |

<img width="802" height="454" alt="template_engine" src="https://github.com/user-attachments/assets/cd066f2b-d6fa-4389-b04d-291a1f9c9419" />

---

### Step 2 — Preprocessing & Token Alignment

<img width="2816" height="1536" alt="preprocessing_pipeline" src="https://github.com/user-attachments/assets/0efcd442-a03c-4cd0-ae63-5813ddb5cc37" />

The generated HTML and JSONL are preprocessed into token sequences suitable for DeBERTa. The key challenge is sub-word tokenisation: a single engineering term (e.g. `VCE(sat)`) may be split into multiple sub-tokens. To maintain label fidelity, only the first sub-token of each word receives the original BIO tag; the rest are masked with `-100` so the loss function ignores them.

Two training formats are produced per document:
- **Standard** — 512-token sliding window over the full HTML (50-token overlap, BIO boundary repair at splits).
- **Table-only (`_tbl`)** — short 20–150 token sequences containing only the structured table, matching the inference-time input format.

**Tech stack:** Python · HuggingFace Tokenizers · PyTorch

**Output:** 22,762 training samples (11,381 standard + 11,381 `_tbl`) · 80/20 train/validation split.

<img width="786" height="675" alt="json_output" src="https://github.com/user-attachments/assets/2f8b007a-9926-456e-b67a-c67e07119623" />

---

### Step 3 — Model Training (Joint NER + RE)

**Model choice:** The pipeline converts HTML structure into a flat token sequence, making it a pure text classification problem. Document-layout models such as LayoutLM or MarkupLM require 2D spatial coordinates or DOM-tree inputs that are not reliably available from `pdfplumber` output. DeBERTa-v3-base was selected among text-only encoders for its disentangled attention mechanism, which improves handling of long sequences and rare engineering tokens compared to BERT or RoBERTa.

A **DeBERTa-v3-base** shared encoder drives two parallel task heads:

1. **NER head** — token-level classification across 13 BIO classes: `O`, `B/I-PARAMETER`, `B/I-MIN`, `B/I-MAX`, `B/I-TYP`, `B/I-UNIT`, `B/I-CONDITION`.
2. **RE head** — span-pooled pairwise classification across 5 relation types: `has_min`, `has_max`, `has_typ`, `has_unit`, `has_condition`. Span representations are obtained via mean-pooling over sub-tokens and concatenated before classification.

Joint loss: $L = \alpha \cdot L_{NER} + \beta \cdot L_{RE}$ ($\alpha=1.0$, $\beta=0.5$).

Relation negative sampling is fixed at a 1:1 positive-to-negative ratio to prevent class imbalance.

**Tech stack:** `microsoft/deberta-v3-base` · PyTorch · HuggingFace Transformers · Google Colab T4 (FP16)

**Hyperparameters:**

| Parameter | Value | Parameter | Value |
| :--- | :--- | :--- | :--- |
| **Max Sequence Length** | 512 | **Epochs** | 3 |
| **Effective Batch Size** | 8 | **Encoder LR** | 2e-5 |
| **Head LR** | 1e-4 | **Weight Decay** | 0.01 |
| **Gradient Clipping** | 1.0 | **Mixed Precision** | FP16 |

**Results (synthetic held-out set, ~4,550 samples):**

| Entity | F1-Score |
|---|---|
| PARAMETER | 1.000 |
| CONDITION | 1.000 |
| UNIT | 0.9997 |
| TYP | 0.998 |
| MIN / MAX | > 0.990 |
| **Overall NER F1** | **0.982** |

---

### Step 4 — PDF Extraction Pipeline

At inference time, PDFs go through a multi-stage rule-based preprocessing stage before reaching the model:

1. **PDF → HTML** — `pdfplumber` extracts tables and text with layout preservation.
2. **Page filtering** — pages without electrical specification tables are discarded.
3. **Table cleaning** — multi-format parser handles standard Min/Typ/Max tables, key-value tables, catalog tables, and condition-column tables (where column headers are physical values such as rated voltages or frequencies).
4. **NER filter** — the trained DeBERTa model scores each extracted parameter row; rows it does not recognise as electrical parameters are dropped. Original preprocessor values are always preserved for accepted rows.
5. **Deduplication** — duplicate parameters across Absolute Maximum and Electrical Characteristics tables are merged, keeping the entry with the most populated fields.

**Tech stack:** pdfplumber · BeautifulSoup · HuggingFace Transformers · Python

---

## Benchmark Results

Evaluated against 7 manually annotated real-world datasheets spanning all major component types.

| Component | Type | T1 — Discovery | T2 — Value Accuracy (±10%) | T3 — Full Match |
|---|---|---|---|---|
| 1662528 | DIODE | 0.917 | 0.917 | 0.917 |
| 2SC5994-D | BJT | 0.667 | 0.571 | 0.571 |
| IRF3205 (Infineon) | MOSFET | 0.690 | 0.618 | 0.618 |
| LM741 | OPAMP | 0.571 | 0.462 | 0.462 |
| e-hd | CAPACITOR | 0.667 | 0.667 | 0.667 |
| GP-1671375 | RESISTOR | 0.667 | 0.667 | 0.667 |
| TPS7A02 | VOLTAGE_REGULATOR | 0.314 | 0.208 | 0.208 |
| **Overall** | | **0.642** | **0.587** | **0.587** |

**Evaluation tiers:**
- **T1 — Discovery:** Parameter name found (word-overlap ≥ 60%).
- **T2 — Value Accuracy:** Name found + numeric value within ±10% of gold.
- **T3 — Full Match:** Name + value + unit all correct.

**Ablation — contribution of the NER filter:**

| System | T2-F1 (avg) |
|---|---|
| Rule-based preprocessing only | 0.579 |
| + NER inclusion filter | **0.587** |

**On the synthetic-to-real gap:** The model achieves NER F1 = 0.982 on synthetic data and T2-F1 = 0.587 on real PDFs. The gap reflects domain shift: real PDFs are processed through `pdfplumber`, which introduces merged cells, irregular spacing, and multi-level headers absent from the synthetic training distribution. The rule-based preprocessing stage and NER filter partially bridge this gap.

---

## Getting Started

### Prerequisites
- Python 3.8+
- [Ollama](https://ollama.com/) with `qwen2.5:1.5b` (for data generation)
- `wkhtmltopdf` (for rendering synthetic HTML to PDF)

```bash
ollama pull qwen2.5:1.5b
```

### Installation

```bash
git clone https://github.com/HITProjects/SyntheticTextData.git
cd SyntheticTextData/embedded
pip install -r requirements.txt
```

### Usage

```bash
# Generate synthetic training data
python synthetic_pipeline/main.py

# Run extraction on benchmark PDFs
python run_benchmark_pipeline.py

# Evaluate results
python benchmark/evaluate_benchmark.py
```
