import os, json, requests, time, random
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv
from utils.logger import setup_logger
from utils.loaders import load_json, load_jsonl

# Load env vars
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
JUDGE_CONFIG_PATH = os.getenv("CONFIG_PATH") + '/judge.json'
OUTPUT_PATH = os.getenv("OUTPUT_PATH") 
LOG_PATH = os.getenv("LOG_PATH") + '/llm_judge.log'
URL = "https://api.groq.com/openai/v1/chat/completions"
HEADERS = {"Authorization": f"Bearer {GROQ_API_KEY}"}

# Setup logging
logger = setup_logger("llm_judge", LOG_PATH)

# Load the most recent response file
def load_responses():
    try:
        output_dir = Path(OUTPUT_PATH)
        output_files = sorted(output_dir.glob("responses_*.jsonl"), reverse = True)
        output_path = output_files[0] if output_files else None

        if output_path is None:
            raise FileNotFoundError("No output files found in /outputs.")

        logger.info(f"📂 Loaded file: {output_path.name}")

        # Load all model responses
        rows = load_jsonl(output_path)
        return rows
    except FileNotFoundError:
        logger.error("❌ Error: {e}")
        exit(1)

# LLM judge to get a scoring from a prompt and a answer
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
            r = requests.post(URL, headers = HEADERS, json = payload, timeout = 60)
            r.raise_for_status()
            text = r.json()["choices"][0]["message"]["content"]
            return json.loads(text.strip())
        except requests.exceptions.RequestException as e:
            if r.status_code == 429:
                logger.warning(f"⚠️ Rate limited (429). Retrying in {backoff}s...")
            else:
                logger.warning(f"⚠️ Request error: {e}. Retrying in {backoff}s...")
            if attempt == retries:
                logger.error("❌ Max retries reached. Skipping.")
                raise
            sleep_time = backoff * (2 ** (attempt - 1)) + random.uniform(0, 1)
            time.sleep(sleep_time)

# Grade every response & write new file
def grade_responses():
    ts = datetime.now().strftime("%Y%m%d_%H%M")
    out_path = f"outputs/scored_{ts}.jsonl"
    judge_config = load_json(JUDGE_CONFIG_PATH)
    rows = load_responses()
    with open(out_path, "w", encoding = "utf-8") as fout:
        for row in rows:
            try:
                score = ask_judge(row["prompt"], row["response"], judge_config)
                row.update({"score": score})
                log_str = f"{row['model']} ✓ " + " ".join(
                    f"{k[0].upper()}{score.get(k)}" for k in judge_config['score_fields'] if k in score
                )
                logger.info(log_str)
            except Exception as e:
                logger.error(f"Judge error → {e}")
                row.update({"score": None})
            fout.write(json.dumps(row, ensure_ascii=False) + "\n")

    logger.info(f"🏁 All done. Scored file saved to {out_path}")

if __name__ == "__main__":
    grade_responses()