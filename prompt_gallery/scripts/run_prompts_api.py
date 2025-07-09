import os
import json
import logging
from time import sleep
from dotenv import load_dotenv
import requests

# --- Load environment variables ---
load_dotenv()

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# --- Logging setup ---
os.makedirs("logs", exist_ok=True)
logging.basicConfig(
    filename="logs/run_prompts_api.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

# --- Load models from single JSON file ---
with open("models/models.json", "r", encoding="utf-8") as f:
    model_config = json.load(f)

# --- Load prompts ---
with open("prompts/prompts.jsonl", "r", encoding="utf-8") as f:
    prompts = [json.loads(line) for line in f]

# --- Anthropic (Claude) ---
def call_anthropic(model, prompt):
    url = "https://api.anthropic.com/v1/messages"
    headers = {
        "x-api-key": ANTHROPIC_API_KEY,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json"
    }
    data = {
        "model": model,
        "max_tokens": 512,
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    return response.json()["content"][0]["text"]

# --- Groq (Mixtral) ---
def call_groq(model, prompt):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}"
    }
    data = {
        "model": model,
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 512,
        "temperature": 0.7
    }
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]

# --- Run prompts for each model ---
for model_name, config in model_config.items():
    provider = config["provider"]
    model_id = config["model"]
    logging.info(f"Starting: {model_name} ({provider})")

    results = []
    for entry in prompts:
        prompt_text = entry["prompt"]
        logging.info(f"[{model_name}] → {prompt_text[:60]}...")

        try:
            if provider == "anthropic":
                response = call_anthropic(model_id, prompt_text)
            elif provider == "groq":
                response = call_groq(model_id, prompt_text)
            else:
                raise ValueError(f"Unsupported provider: {provider}")

        except Exception as e:
            logging.error(f"Error in {model_name}: {e}")
            response = f"ERROR: {str(e)}"

        results.append({
            "model": model_name,
            "provider": provider,
            "prompt": prompt_text,
            "response": response,
            "category": entry.get("category"),
            "note": entry.get("note")
        })

        sleep(1.2)  # To avoid rate limit

    # --- Save results ---
    os.makedirs("results", exist_ok=True)
    output_path = f"results/{model_name}_output.jsonl"
    with open(output_path, "w", encoding="utf-8") as f:
        for r in results:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

    logging.info(f"✔ Finished: {model_name}, saved to {output_path}")
