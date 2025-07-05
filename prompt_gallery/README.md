# 🧠 Prompt Gallery (WIP)

A work-in-progress project exploring how different LLMs behave across handcrafted prompts designed for diverse tasks.

## 🧾 Overview

This project focuses on:
- Designing structured prompts by categories
- Running them through multiple free-access LLMs
- Comparing outputs for insights into reasoning, verbosity, tone, etc.

## 📁 Structure

```
llm-playground/
└── prompt_gallery/             # 🧠 Prompt testing & evaluation module
    ├── prompts/                # 📝 Handcrafted prompts (.jsonl)
    ├── scripts/                # ⚙️ Scripts to query LLM APIs
    ├── results/                # 📊 Model outputs  
    ├── notebooks/              # 📓 Jupyter notebooks for analysis & comparison
    └── README.md               # 📄 Project documentation
```


## 🚧 Current Status

- [x] Project folder initialized
- [ ] Initial prompt set in JSONL
- [ ] Hugging Face script for model calls
- [ ] Output comparison notebook

## 🔜 Next Steps

- Write `prompts.jsonl` with 20+ curated entries
- Run prompts through free models via Hugging Face API
- Create a notebook to compare outputs and annotate findings