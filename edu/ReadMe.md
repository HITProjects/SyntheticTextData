# ABSA-Synthetic-Student-Reviews

## What is this project?
A project for generating a **synthetic dataset of student course reviews** (Computer Science courses), where each review is labeled with:
- **Aspects** (e.g., difficulty, clarity, exam_fairness, etc.)
- **Sentiment per aspect** (positive / neutral / negative)

The dataset is saved in **JSONL** format (one JSON object per line) and is designed for tasks such as **Aspect-Based Sentiment Analysis (ABSA)**.

---

## Motivation | Why is this needed?
Most available student-review datasets provide, at best, an **overall sentiment** (good/bad/neutral), but do not include aspect-level labels.

Aspect-level labeling makes it possible to understand *what exactly* the student is referring to:
- Is the issue the workload?
- Lack of support (TA/office hours)?
- Lecturer quality?
- Exam fairness?

In addition, synthetic data allows control over the amount of data and the variety of writing styles.

---

## Problem Definition
Build a pipeline that generates JSONL examples where each line includes:
- Course / lecturer metadata
- Grade
- Writing style
- An aspects →ive-dictionary (aspect → sentiment)
- A natural-sounding review text that matches the labels

---

## Dataset Format
Each line is a JSON object. Example:

```json
{
  "course_name": "Computer Networks",
  "lecturer": "Prof. Klein",
  "grade": "D (Barely passed)",
  "style": "Confused Student (Unsure about things, asks rhetorical questions)",
  "aspects": { "workload": "neutral" },
  "review_text": "so s this course worth it? workload's okay i guess"
}
```
---
## Fields
- `course_name` (string)
- `lecturer` (string)
- `grade` (categorical string): A/B/C/D/F
- `style` (categorical string): one of the predefined styles
- `aspects` (dict): aspect_name → sentiment
- `review_text` (string)

---

## Model
The text is generated using a locally running LLM via **Ollama**:

- **Model:** `llama3`
- **Provider:** `ollama`
- **Base URL:** `http://localhost:11434`

> The code also supports OpenAI (`gpt-4o-mini`), but the project currently uses Ollama.

---

## Generation Process
The generator (`RobustDataGenerator`) produces each example in several steps:

### 1) Sampling
For each example, the generator samples:
- A course from a predefined list (with a short description)
- A lecturer from a predefined list
- Student year: Freshman / Sophomore / Junior / Senior
- Course state: Currently taking / Completed recently / Took it a while ago  
  *(sometimes “Retaking” depending on the generator version)*
- Grade: A/B/C/D/F
- Number of aspects: randomly between **1 and 3**
- Sentiment for each selected aspect: **positive / neutral / negative**, with basic logical constraints  
  *(e.g., low grades limit some aspects from being positive)*

### 2) Prompt Construction
The prompt includes:
- Writing style + length constraint based on the selected style
- A list of forbidden phrases (`FORBIDDEN_PHRASES`) to avoid “robotic/academic” wording
- The labels (`aspects → sentiment`)
- Aspect-specific keyword guidance (`ASPECT_KEYWORDS`) to encourage alignment between the text and the labels
- Context: course, lecturer, student year, course state, grade

The model is instructed to output **ONLY** the review text (no preamble/meta).

### 3) Two-pass generation (Generation + Refinement)
The system performs:
- Initial generation (`_build_gen_prompt`)
- A refinement / rewrite step (`_build_refiner_prompt`) to better match the style and labels

### 4) Cleaning + Human-like noise
Post-processing steps include:
- Removing preambles, quotes, notes, unwanted endings, etc.
- Fixing truncated starts (e.g., `'s` → `It's`)
- Adding informal writing features for relevant styles (lowercase, abbreviations, `"2"` instead of `"to"`, etc.)
- Occasionally adding small noise (dropping a character / removing a space after punctuation)
- Enforcing strict length constraints per style

---

## Styles
The generator uses **6 predefined writing styles**:
- **Casual** (Texting style: lowercase, no punctuation, slang like `tbh`, `idk`, `tho`, fragments)
- **Simple & Direct** (Use only common words. No academic jargon. Like talking to a friend)
- **Rant/Rave** (Emotional, very subjective, lots of punctuation `!!!` or `...`)
- **Short** (Max 10–15 words. Fragments allowed)
- **Analytic but Simple** (Explains “why” but uses simple language)
- **Confused Student** (Unsure about things, asks rhetorical questions)

---

## Aspects
The system labels from a fixed list of **10 aspects**:
- `difficulty`, `clarity`, `workload`, `lecturer_quality`
- `exam_fairness`, `relevance`, `interest`, `support`
- `materials`, `overall_experience`

Each aspect receives a sentiment from: `positive` / `neutral` / `negative`.

---

## Current Results
- **Dataset file:** `final_student_reviews.jsonl`
- **Number of examples:** 6000 (final for now)
- **Aspects per review:** 1–3 (as defined in the code)


---

## Balancing Update (Improved Version)
In an additional generator version, grade sampling was adjusted to balance the dataset:
- Generate only **A/B/C** using weighted sampling
- Prevent generating **D/F** (weights = 0) to fill missing higher/mid grades

Goal: achieve a more balanced grade distribution in the final dataset.

---

## How to Run

### Requirements
- **Ollama** running locally at: `http://localhost:11434`
- The model installed in Ollama: `llama3`
- Python + libraries: `requests`  
  *(and optionally `openai` if using the OpenAI provider)*

### Generating and saving JSONL
The code supports batch generation and appending to a JSONL file:
- **Output file:** `final_student_reviews.jsonl`
- **Target size:** 6000
- **Batch size:** 50

*(The run is performed from the notebook/script that contains the generator and `generate_dataset_in_batches`.)*

---

## Repository Contents
- `final_student_reviews.jsonl` — final dataset (6000 examples)
- `dataset_generator.ipynb` / `dataset_generator_balanced.ipynb` — notebooks containing the generator and dataset generation runs

---

## Author
Guy Yogev
