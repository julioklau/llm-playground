import os, json, requests
from datetime import datetime
from dotenv import load_dotenv
from utils.logger import setup_logger
from utils.loaders import load_json, load_jsonl

# Load env vars
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
PROMPT_PATH = os.getenv("PROMPT_PATH")
MODEL_CONFIG_PATH = os.getenv("CONFIG_PATH") + '/models.json'
OUTPUT_PATH = os.getenv("OUTPUT_PATH")
LOG_PATH = os.getenv("LOG_PATH") + '/run_prompts.log'
URL = "https://api.groq.com/openai/v1/chat/completions"
HEADERS = {"Authorization": f"Bearer {GROQ_API_KEY}"}

# Function to intertact with groq models by api
def call_groq_model(prompt: str, model_id: str) -> str:
    payload = {
        "model": model_id,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 512,
        "temperature": 0.7
    }

    try:
        response = requests.post(URL, headers = HEADERS, json = payload, timeout = 20)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        raise RuntimeError(f"Request failed: {e}")

def generate_responses():
    # Setup logging
    logger = setup_logger("run_prompts", LOG_PATH)
    logger.info("Loading prompts and model config...")
    prompts = load_jsonl(PROMPT_PATH)
    models = load_json(MODEL_CONFIG_PATH)

    # Create response file
    os.makedirs(OUTPUT_PATH, exist_ok=True)
    output_file = os.path.join(
        OUTPUT_PATH,
        f"responses_{datetime.now().strftime('%Y%m%d_%H%M')}.jsonl"
    )

    # Generate responses for each prompt
    with open(output_file, "w", encoding = "utf-8") as out:
        for i, entry in enumerate(prompts, 1):
            logger.info(f"Prompt {i}/{len(prompts)}: {entry['category']}")
            for model_name, model_info in models.items():
                try:
                    output = call_groq_model(entry["prompt"], model_info["model"])
                    result = {
                        "timestamp": datetime.now().replace(microsecond = 0).isoformat(),
                        "model": model_name,
                        "model_id": model_info["model"],
                        "prompt": entry["prompt"],
                        "category": entry["category"],
                        "note": entry.get("note", ""),
                        "response": output.strip()
                    }
                    out.write(json.dumps(result, ensure_ascii = False) + "\n")
                    logger.info(f"✅ {model_name} responded.")
                except Exception as e:
                    logger.error(f"❌ {model_name} failed: {e}")

    logger.info(f"🎉 Done! Results saved to {output_file}")

if __name__ == "__main__":
    generate_responses()