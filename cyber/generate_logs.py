import os
import json
import re
import pandas as pd
from openai import OpenAI
from requests.exceptions import ConnectionError
import time

# --- הגדרות Ollama (מודל חזק) ---
# שימוש ב-llama3:8b לדיוק גבוה יותר ב-JSON
OLLAMA_MODEL = "llama3:8b"
# כתובת ה-API המקומית
OLLAMA_API_URL = 'http://localhost:11434/v1'
# זמן המתנה מוגדל (3 דקות)
REQUEST_TIMEOUT = 180
RECORDS_PER_BATCH = 10  # 10 רשומות בכל קובץ
NUM_BATCHES = 10  # 10 קבצים (סה"כ 100 רשומות)

# 1. הגדרת ה-Prompt המובנה (Generator)
LOG_GENERATION_PROMPT = f"""
You are a sophisticated Security Analyst model. Your task is to generate exactly {RECORDS_PER_BATCH} synthetic Web Server Access Log records.
The output MUST be a single, valid JSON object containing a key named 'logs', and its value must be a JSON array of the {RECORDS_PER_BATCH} log records.

RULES:
1. 5 records must simulate normal user activity (e.g., viewing public products). Set 'is_malicious' to false.
2. 5 records must simulate SQL Injection (SQLi) attempts. Embed typical SQL attack payloads (e.g., 'OR 1=1 --', 'UNION SELECT table_name') within the 'query_params' field. Set 'is_malicious' to true.
3. The timestamp must be sequential for all {RECORDS_PER_BATCH} records.

Each log record must adhere strictly to the following JSON structure:
{{
  "timestamp": "YYYY-MM-DDTHH:MM:SSZ",
  "source_ip": "A.B.C.D",
  "http_method": "GET",
  "requested_url": "/api/v1/product/view",
  "query_params": "product_id=...", 
  "is_malicious": true/false
}}
"""


def generate_and_validate_logs(batch_number, client):
    """מייצרת ומאמתת דאטה-סט יחיד."""
    print(f"\n--- Generating Batch {batch_number + 1} of {NUM_BATCHES} using {OLLAMA_MODEL} ---")

    try:
        # 2. קריאה ל-API
        response = client.chat.completions.create(
            model=OLLAMA_MODEL,
            response_format={"type": "json_object"},
            messages=[
                {"role": "system",
                 "content": "You are a professional security log generator. Always output ONLY the valid JSON structure under the key 'logs'."},
                {"role": "user", "content": LOG_GENERATION_PROMPT}
            ],
            temperature=0.7
        )

        # 3. ניתוח הפלט הגמיש (Flexi-Parse)
        json_output = response.choices[0].message.content.strip()

        try:
            data = json.loads(json_output)
        except json.JSONDecodeError:
            print("Warning: Direct JSON parse failed. Attempting cleanup...")
            json_match = re.search(r'\{.*\}', json_output, re.DOTALL)
            if json_match:
                data = json.loads(json_match.group(0))
            else:
                raise ValueError("Could not find a valid JSON object in the model's output.")

        # 4. אימות מבנה ומציאת המערך logs (גמישות)
        log_array = None
        if 'logs' in data and isinstance(data['logs'], list):
            log_array = data['logs']
        elif isinstance(data, list):
            log_array = data  # אם המודל החזיר מערך ישירות

        if log_array is None:
            raise ValueError(
                "Final JSON structure missing the required log array (neither direct array nor 'logs' key found).")

        # 5. טעינה ל-Pandas ושמירה
        df = pd.DataFrame(log_array)

        # אימות ספירה וסוג הנתונים
        df['is_malicious'] = df['is_malicious'].astype(str).str.lower().str.strip()
        malicious_count = df[df['is_malicious'] == 'true'].shape[0]

        print(f"Total records generated: {len(df)}")
        print(f"Malicious records found: {malicious_count} (Expected: {RECORDS_PER_BATCH // 2})")

        # שמירה כקובץ CSV
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        filename = f"synthetic_logs_batch_{batch_number + 1}_{timestamp}.csv"

        df.to_csv(filename, index=False)
        print(f"SUCCESS: Data saved to {filename}")

    except Exception as e:
        print(f"An error occurred during Batch {batch_number + 1}: {e}")
        print("Moving to next batch...")


def main_generator_loop():
    print(f"--- Attempting connection to Ollama API at {OLLAMA_API_URL} ---")

    try:
        # בדיקת חיבור ואימות מודל
        client = OpenAI(
            api_key='ollama',
            base_url=OLLAMA_API_URL,
            timeout=REQUEST_TIMEOUT
        )
        client.models.list()
        print(f"--- Successfully connected. Running {NUM_BATCHES} Batches ---")

        # הלולאה שמריצה את יצירת הדאטה-סט 10 פעמים
        for i in range(NUM_BATCHES):
            # זמן מנוחה קצר בין קריאות למניעת עומס
            if i > 0:
                time.sleep(5)
            generate_and_validate_logs(i, client)

        print("\n--- All 10 Batches Attempted. Check your project folder for CSV files. ---")

    except ConnectionError:
        print("\nFATAL ERROR: Could not connect to Ollama server.")
        print("Please ensure 'ollama serve' is running in a separate terminal.")
    except Exception as e:
        print(f"\nFATAL ERROR: Initialization failed: {e}")


if __name__ == "__main__":
    main_generator_loop()