# 🎥 AI YouTube Transcript Summarizer

An AI-powered web application that extracts transcripts from YouTube videos
and generates clear, concise summaries using modern NLP techniques.

The app supports automatic captions and includes a Whisper AI fallback
to transcribe videos that do not provide subtitles.

🔗 Live Demo:
https://huggingface.co/spaces/HarshitaPatel30/youtube-transcript-summarizer

---

## ✨ Key Features

- Paste any YouTube video URL
- Automatic transcript extraction
- Whisper AI fallback for videos without captions
- AI-generated summaries (short / detailed)
- View full transcript
- Download transcript and summary
- Clean dark-themed UI
- Deployed on Hugging Face Spaces

---

## 🧠 How It Works

1. User enters a YouTube video URL
2. App tries to fetch captions from YouTube
3. If captions are missing:
   - Audio is extracted
   - Whisper AI converts speech to text
4. Transcript is summarized using NLP models
5. Summary and transcript are displayed to the user

---

## 🛠 Tech Stack

Frontend:
- Streamlit

Backend / AI:
- Python
- OpenAI Whisper
- Hugging Face Transformers
- YouTube Transcript API

Deployment:
- Hugging Face Spaces

---

## 📂 Project Structure

youtube-transcript-summarizer/
│
├── app.py
├── summarizer.py
├── requirements.txt
├── README.md
└── .streamlit/
    └── config.toml

---

## ⚙️ Run Locally

git clone https://github.com/HarshitaPatel30/youtube-transcript-summarizer.git
cd youtube-transcript-summarizer

python -m venv venv
venv\Scripts\activate

pip install -r requirements.txt
streamlit run app.py

Open browser:
http://localhost:8501

---

## 🚀 Future Enhancements

- Timestamp-based summaries
- Multi-language support
- Key points extraction
- Backend separation using FastAPI

---

## 👩‍💻 Author

Harshita Patel  
B.Tech CSE | AI & ML Enthusiast

GitHub:
https://github.com/HarshitaPatel30

Hugging Face:
https://huggingface.co/HarshitaPatel30

---


