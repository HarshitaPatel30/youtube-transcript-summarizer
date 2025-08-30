# 🎬 YouTube Transcript Summarizer

A clean Streamlit app that fetches a YouTube video’s transcript (English or Hindi), optionally translates it to English, and generates a readable summary using Hugging Face Transformers.

<p align="left">
  <a href="https://www.python.org/"><img alt="Python" src="https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white"></a>
  <a href="https://streamlit.io/"><img alt="Streamlit" src="https://img.shields.io/badge/Streamlit-App-FF4B4B?logo=streamlit&logoColor=white"></a>
  <a href="https://huggingface.co/"><img alt="Transformers" src="https://img.shields.io/badge/HuggingFace-Transformers-F0BF42?logo=huggingface&logoColor=white"></a>
  <a href="./LICENSE"><img alt="License" src="https://img.shields.io/badge/License-MIT-green"></a>
</p>

---

## ✨ Features
- 🔎 Extracts transcript by video URL/ID (via `youtube-transcript-api`)
- 🌐 Language handling: **English**, **Hindi → English (auto-translate)**, or **Auto (en first, hi fallback)**
- 🧠 Summarization with `facebook/bart-large-cnn` (Hugging Face)
- 🖥️ Modern Streamlit UI: sticky input bar, scrollable summary preview, **Download .txt**
- ⚠️ Clear error handling for: disabled transcripts, missing captions, network issues

---

## 🚀 Quick Start

```bash
# 1) Clone
git clone https://github.com/HarshitaPatel30/youtube-transcript-summarizer.git
cd youtube-transcript-summarizer

# 2) (Recommended) Create venv
python -m venv venv
# Windows (Git Bash):
source venv/Scripts/activate

# 3) Install dependencies
pip install -r requirements.txt

# 4) (CPU installs of PyTorch if needed)
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu

# 5) (Optional) Extra tokenizer dependency suggested by Transformers
pip install sacremoses

# 6) Run the app
streamlit run app.py
