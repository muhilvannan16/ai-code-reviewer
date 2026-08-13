# 🤖 AI Code Reviewer — AI-Powered Git Diff Analysis

**AI Code Reviewer** is a CLI tool that reviews your staged git changes before you commit — catching bugs, unsafe patterns, and logic errors using an LLM, with built-in hallucination filtering so you only see findings that actually correspond to real lines in your diff.

[![PyPI](https://img.shields.io/pypi/v/ai-code-reviewer-cli?style=flat&logo=pypi&logoColor=white)](https://pypi.org/project/ai-code-reviewer-cli/)
[![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![Groq](https://img.shields.io/badge/Groq-F55036?style=flat&logo=groq&logoColor=white)](https://groq.com/)
[![Publish](https://github.com/muhilvannan16/ai-code-reviewer/actions/workflows/publish.yml/badge.svg)](https://github.com/muhilvannan16/ai-code-reviewer/actions/workflows/publish.yml)

---

## ✨ Key Features

- **Reviews staged changes automatically** — parses `git diff --staged` down to exact added lines and line numbers, not just raw diff text
- **Hallucination-checked output** — every AI-generated comment is cross-validated against the real diff before being shown, so you never get a "bug" pointing at a line that doesn't exist
- **Severity-ranked, color-coded terminal output** — critical issues in red, warnings in yellow, info in cyan, powered by `rich`
- **Pre-commit hook integration** — can block a commit outright when a critical issue is found, enforced at the git level regardless of whether you commit from the terminal, VS Code, or any other tool
- **Fails safe** — network errors or malformed AI responses never crash your workflow or silently block a commit

---

## 📦 Installation

```bash
pip install ai-code-reviewer-cli
```

You'll need a free [Groq API key](https://console.groq.com/keys). Set it as a **persistent environment variable** (not a `.env` file — this needs to work from any project directory, not just one folder):

**Windows:**

setx GROQ_API_KEY "your-key-here"


**macOS/Linux:**
```bash
echo 'export GROQ_API_KEY="your-key-here"' >> ~/.zshrc  # or ~/.bashrc
```

---

## 🚀 Usage

```bash
git add your_file.py
ai-review
```

Example output:

[app.py:12] CRITICAL: Mutable default argument 'items=[]' can retain state across calls.
[app.py:24] WARNING: Using 'is' for string comparison instead of '=='.


---

## 🔒 Pre-commit Hook (optional)

To block commits automatically when a critical issue is found, add a `pre-commit` hook to any repo that calls this tool's review pipeline and exits non-zero on critical findings. See [`hooks/pre_commit_check.py`](hooks/pre_commit_check.py) in this repo for a working example.

---

## 🛠️ Built With

- **Python** — core CLI and diff-parsing logic
- **Groq** (`openai/gpt-oss-120b`) — LLM-powered review generation
- **Rich** — colored terminal output
- **python-dotenv** — local development configuration
- **GitHub Actions + PyPI Trusted Publishing** — fully automated, secretless release pipeline

---

## 📄 License

MIT

---

## 👤 Author

**Muhil** ([@muhilvannan16](https://github.com/muhilvannan16))
