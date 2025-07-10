import os
import json
import logging
from datetime import datetime
import requests
from dotenv import load_dotenv

# Load env vars
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
PROMPT_PATH = os.getenv("PROMPT_PATH")
MODEL_PATH = os.getenv("MODEL_CONFIG_PATH")
OUTPUT_PATH = os.getenv("OUTPUT_PATH")
LOG_PATH = os.getenv("LOG_PATH")
HEADERS = {"Authorization": f"Bearer {GROQ_API_KEY}"}

# --- Setup logging ---
os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOG_PATH, encoding="utf-8"),
        logging.StreamHandler()
    ]
)

def load_jsonl(path):
    with open(path, "r", encoding="utf-8") as f:
        return [json.loads(line) for line in f]

def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def call_groq_model(prompt, model_id):
    url = "https://api.groq.com/openai/v1/chat/completions"
    payload = {
        "model": model_id,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 512,
        "temperature": 0.7
    }
    response = requests.post(url, headers=HEADERS, json=payload)
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]

def main():
    logging.info("Loading prompts and model config...")
    prompts = load_jsonl(PROMPT_PATH)
    models = load_json(MODEL_PATH)

    os.makedirs(OUTPUT_PATH, exist_ok=True)
    output_file = os.path.join(
        OUTPUT_PATH,
        f"responses_{datetime.now().strftime('%Y%m%d_%H%M')}.jsonl"
    )

    with open(output_file, "w", encoding="utf-8") as f_out:
        for i, entry in enumerate(prompts, 1):
            logging.info(f"Prompt {i}/{len(prompts)}: {entry['category']}")
            for model_name, model_info in models.items():
                try:
                    output = call_groq_model(entry["prompt"], model_info["model"])
                    result = {
                        "timestamp": datetime.now().replace(microsecond=0).isoformat(),
                        "model": model_name,
                        "model_id": model_info["model"],
                        "prompt": entry["prompt"],
                        "category": entry["category"],
                        "note": entry.get("note", ""),
                        "response": output.strip()
                    }
                    f_out.write(json.dumps(result, ensure_ascii=False) + "\n")
                    logging.info(f"✅ {model_name} responded.")
                except Exception as e:
                    logging.error(f"❌ {model_name} failed: {e}")

    logging.info(f"🎉 Done! Results saved to {output_file}")

if __name__ == "__main__":
    main()