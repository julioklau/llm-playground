# 🧠 Prompt Gallery

This project explores how different large language models (LLMs) respond to structured prompts across varied task categories. It enables automated prompt testing and output collection using multiple free-access models.

## 🚀 Highlights

- Compare outputs of different LLMs using structured, category-based prompts
- Automate prompt runs across multiple free-access APIs (Groq)
- Score model responses using an LLM-based judge for qualitative evaluation
- Output everything to JSONL and logs for reproducibility and future benchmarking
- Modular folder structure, easy to extend with new models or prompt sets

## 🧾 Overview

This project focuses on:
- Designing structured prompts by categories
- Running them through multiple free-access LLMs
- Comparing outputs for insights into reasoning, verbosity, tone, etc.
- Scoring the outputs using an automated LLM-based judge

## 📁 Structure

```
llm-playground/
└── prompt_gallery/             # 🧠 Prompt testing & evaluation module
    ├── config/                 # 🤖 Model config and wrappers
    ├── logs/                   # 📂 Runtime logs (ignored by Git)
    ├── notebooks/              # 📓 Analysis notebooks to compare outputs    
    ├── outputs/                # 📊 Model outputs and scores
    ├── prompts/                # 📝 Prompt sets (.jsonl)
    ├── scripts/                # ⚙️ Scripts to run prompts and call models
    ├── utils/                  # 🔧 Helpers and shared utilities 
    └── README.md               # 📄 Project documentation
```

## 🔧 Tech Stack

- **Python 3.12** – Core language
- **LLM APIs** – Groq (Gemma 7B, LLaMA 3 8B, LLaMA 3 70B)
- **dotenv** – For managing `.env` configuration
- **Jupyter Notebooks** – For qualitative analysis of outputs
- **Logging** – Runtime information and prompt traceability
- **pipreqs** – For auto-generating `requirements.txt`
- **JSONL** – Structured prompt and response formats

## ⚙️ Setup

This project uses a `.env` file for managing paths and API keys.


### 🔑 Step 1: Get you Groq API Key
1. Visit [https://console.groq.com/keys](https://console.groq.com/keys)
2. Log in or sign up (use Google or email).
3. Click **"Create API Key"**
4. Copy and paste the generated key

### 🧪 Step 2: Set Up the `.env` File
Copy the example file name as .env.example:
```bash
cp .env.example .env
```
Fill in values:
```env
GROQ_API_KEY=your_groq_api_key_here
PROMPT_PATH=prompts/prompts.jsonl
CONFIG_PATH=config
OUTPUT_PATH=outputs
LOG_PATH=logs
```
### 📦 Step 3: Installation

Make sure you’re using Python 3.8+ (preferably 3.12). Then, install dependencies using pip:
```bash
pip install -r requirements.txt
```

### 🚀 Step 4: Usage
Run all prompts and automatically evaluate responses using an LLM-based judge:
```bash
python -m scripts.main
```

## 🚧 Current Status

- [x] Project folder initialized
- [x] Initial prompt set in JSONL
- [x] Prompt runner script connected to two LLMs
- [x] Output generation working
- [x] Output comparison notebook
- [x] LLM judge script to evaluate outputs
- [x] Structured prompt pipeline
- [x] Logging, output, and evaluation setup

## 🎯 Goals

- Understand how models differ in reasoning and expression
- Identify patterns in hallucination, verbosity, and reasoning style
- Gain insights into model-specific response behaviors and styles

## 📄 License
This project is covered under the [Apache 2.0 License](../LICENSE), as specified in the root of this repository.

## 🤝 Contact

Created by [julioklau](https://github.com/julioklau) — feel free to reach out if you have questions or feedback!
- GitHub: [julioklau](https://github.com/julioklau)
- LinkedIn: [Julio Lau](https://linkedin.com/in/julio-lau)
- Email: julioklau97@gmail.com