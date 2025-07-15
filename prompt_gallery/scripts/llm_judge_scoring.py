import os, json, logging, requests
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv
import time
import random

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
JUDGE_CONFIG_PATH = os.getenv("JUDGE_CONFIG_PATH")
HEADERS = {"Authorization": f"Bearer {GROQ_API_KEY}"}
URL = "https://api.groq.com/openai/v1/chat/completions"
OUTPUT_PATH = os.getenv("OUTPUT_PATH") 
LOG_PATH = os.getenv("LOG_PATH") + '/llm_judge.log'

# Setup logging
os.makedirs(os.path.dirname(LOG_PATH), exist_ok = True)
logging.basicConfig(
    level = logging.INFO,
    format = "%(asctime)s [%(levelname)s] %(message)s",
    handlers = [
        logging.FileHandler(LOG_PATH, encoding="utf-8"),
        logging.StreamHandler()
    ]
)

# Locate the most recent response file
def load_responses():
    output_dir = Path("./outputs")
    output_files = sorted(output_dir.glob("responses_*.jsonl"), reverse=True)
    output_path = output_files[0] if output_files else None
    logging.info(f"📂 Loaded file: {output_path.name}")

    # Load all model responses
    rows = [json.loads(line) for line in open(output_path, "r", encoding = "utf-8")]
    return rows

def load_judge_config(path = JUDGE_CONFIG_PATH):
    with open(path, encoding="utf-8") as f:
        return json.load(f)

def ask_judge(prompt, answer, judge_config, retries=3, backoff=2):
    messages = [
        {"role": "system", "content": judge_config['system_prompt']},
        {"role": "user", "content": f"PROMPT:\n{prompt}\n\nANSWER:\n{answer}"}
    ]
    payload = {
        "model": judge_config['model'],
        "messages": messages,
        "max_tokens": judge_config['max_tokens'],
        "temperature": judge_config['temperature']
    }
    
    for attempt in range(1, retries + 1):
        try:
            r = requests.post(URL, headers=HEADERS, json=payload, timeout=60)
            r.raise_for_status()
            text = r.json()["choices"][0]["message"]["content"]
            return json.loads(text.strip())
        except requests.exceptions.RequestException as e:
            if r.status_code == 429:
                logging.warning(f"⚠️ Rate limited (429). Retrying in {backoff}s...")
            else:
                logging.warning(f"⚠️ Request error: {e}. Retrying in {backoff}s...")
            if attempt == retries:
                logging.error("❌ Max retries reached. Skipping.")
                raise
            sleep_time = backoff * (2 ** (attempt - 1)) + random.uniform(0, 1)
            time.sleep(sleep_time)

# Grade every row & write new file
def main():
    ts = datetime.now().strftime("%Y%m%d_%H%M")
    out_path = f"outputs/scored_{ts}.jsonl"
    judge_config = load_judge_config()
    rows = load_responses()
    with open(out_path, "w", encoding="utf-8") as fout:
        for row in rows:
            try:
                score = ask_judge(row["prompt"], row["response"], judge_config)
                row.update({"score": score})
                log_str = f"{row['model']} ✓ " + " ".join(
                    f"{k[0].upper()}{score.get(k)}" for k in judge_config['score_fields'] if k in score
                )
                logging.info(log_str)
            except Exception as e:
                logging.error(f"Judge error → {e}")
                row.update({"score": None})
            fout.write(json.dumps(row, ensure_ascii=False) + "\n")

    logging.info(f"🏁 All done. Scored file saved to {out_path}")


if __name__ == "__main__":
    main()