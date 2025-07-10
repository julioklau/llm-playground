# 🧠 Prompt Gallery (WIP)

This project explores how different large language models (LLMs) respond to structured prompts across varied task categories. It enables automated prompt testing and output collection using multiple free-access models.

## 🧾 Overview

This project focuses on:
- Designing structured prompts by categories
- Running them through multiple free-access LLMs
- Comparing outputs for insights into reasoning, verbosity, tone, etc.

## 📁 Structure

```
llm-playground/
└── prompt_gallery/             # 🧠 Prompt testing & evaluation module
    ├── logs/                   # 📂 Logs of model responses and runtime info (ignored by Git, generated at runtime)
    ├── models/                 # 🤖 Model wrappers or config files
    ├── notebooks/              # 📓 Analysis notebooks to compare outputs
    ├── outputs/                # 📊 Generated model outputs per prompt
    ├── prompts/                # 📝 Curated prompt sets (.jsonl)
    ├── scripts/                # ⚙️ Scripts to run prompts and call models
    └── README.md               # 📄 Project documentation
```
## ⚙️ Configuration

This project uses a `.env` file to manage environment variables (API keys, model settings, output paths, etc.).


### 🔑 Step 1: Get you groq API Key
1. Visit [https://console.groq.com/keys](https://console.groq.com/keys)
2. Log in or sign up (use Google or email).
3. Click **"Create API Key"**
4. Copy and paste the generated key

### 🧪 Step 2: Set Up the `.env` File
1. Copy the example file name as .env.example:
   ```bash
   cp .env.example .env
2. Fill in your actual values:
    ```env
    GROQ_API_KEY=your_groq_api_key_here
    PROMPT_PATH=prompts/prompts.jsonl
    MODEL_CONFIG_PATH=models/models.json
    OUTPUT_PATH=outputs
    LOG_PATH=logs/run_prompts.log
## 🚧 Current Status

- [x] Project folder initialized
- [x] Initial prompt set in JSONL
- [x] Prompt runner script connected to two LLMs
- [x] Output generation working
- [ ] Output comparison notebook

## 🔜 Next Steps

- Develop an evaluation notebook to compare output structure and tone
- Explore qualitative metrics and annotation tagging

## 🎯 Goals

- Understand how different models interpret the same task
- Identify patterns in hallucination, verbosity, and reasoning style