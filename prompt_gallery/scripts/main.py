from scripts.run_prompts import generate_responses
from scripts.llm_judge_scoring import grade_responses

def main():
    generate_responses()
    grade_responses()

if __name__ == "__main__":
    main()
