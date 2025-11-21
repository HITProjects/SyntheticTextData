# 🛡️ Cyber Domain Synthetic Log Datasets

## 🚀 Project Overview: Addressing the Data Gap

The core challenge in cybersecurity machine learning (ML) is the severe lack of high-quality, labeled training data. Real-world cyber event logs are often confidential, sensitive, or scarce, making it difficult to develop and validate robust defense models.

**Our Solution:** This project utilizes Generative AI (LLMs) to **synthesize** diverse and labeled cyber log datasets, providing a clean, accessible, and scalable resource for the research community.

## 🎯 Task Definition & Focus

**Domain:** Cyber Security (Web Application Defense).

**Current Focus:** **SQL Injection (SQLi) Log Classification**. We aim to build a foundational dataset to train models to distinguish between normal web traffic and malicious SQLi attack payloads.

| Feature | Description |
| :---: | :--- |
| **Input** | HTTP Request Log (`request_log`) |
| **Output** | Binary Label (`label`: CLEAN or ATTACK) |

## ⚙️ Data Generation Process Summary

The synthetic data generation pipeline is fully programmatic and follows these steps:

1.  **Recipe Design:** Structured prompts are engineered to instruct the LLM on how to simulate both legitimate and malicious HTTP requests, based on domain knowledge.
2.  **LLM Generation:** A Python script (via the LLM API) executes the prompts iteratively to produce a large, diverse collection of labeled logs.
3.  **Benchmarking:** Simple ML models (e.g., Logistic Regression, Decision Tree) are trained on the generated data to establish baseline performance metrics (such as Accuracy, Precision, and Recall), thereby validating the quality and utility of the dataset.

## 📂 Repository Structure

* **`generate_logs.py`**: Script for generating the synthetic data using the LLM API.
* **`synthetic_datasets/`**: Directory containing the 10 generated CSV files.
* **`Data_Analysis.ipynb`**: Jupyter notebook for analysis and benchmarking.