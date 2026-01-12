from youtube_transcript_api import (
    YouTubeTranscriptApi,
    TranscriptsDisabled,
    NoTranscriptFound
)
from transformers import pipeline
import whisper
import yt_dlp
import tempfile
import os
import re

# =====================================================
# Load models ONCE (important for performance)
# =====================================================
summarizer = pipeline(
    "summarization",
    model="facebook/bart-large-cnn"
)

whisper_model = whisper.load_model("base")  # CPU-safe


# =====================================================
# Utility
# =====================================================
def get_video_id(url: str) -> str:
    match = re.search(r"(?:v=|youtu\.be/)([\w-]+)", url)
    if not match:
        raise ValueError("Invalid YouTube URL")
    return match.group(1)


# =====================================================
# Video Metadata (UI Preview)
# =====================================================
def get_video_metadata(url: str) -> dict:
    ydl_opts = {
        "quiet": True,
        "skip_download": True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)

    return {
        "title": info.get("title"),
        "channel": info.get("uploader"),
        "thumbnail": info.get("thumbnail"),
        "duration": info.get("duration"),
    }


# =====================================================
# Transcript Layer (Captions → Whisper fallback)
# =====================================================
def get_transcript(url: str) -> str:
    video_id = get_video_id(url)

    # 1️⃣ Try YouTube captions
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        text = " ".join([t["text"] for t in transcript]).strip()
        if text:
            return text
    except (TranscriptsDisabled, NoTranscriptFound):
        pass
    except Exception:
        pass

    # 2️⃣ Fallback to Whisper
    return whisper_transcribe(url)


# =====================================================
# Whisper Audio Transcription
# =====================================================
def whisper_transcribe(url: str) -> str:
    with tempfile.TemporaryDirectory() as tmpdir:

        ydl_opts = {
            "format": "bestaudio/best",
            "outtmpl": os.path.join(tmpdir, "audio.%(ext)s"),
            "quiet": True,
            "postprocessors": [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
            }],
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        # Find generated mp3
        audio_file = None
        for f in os.listdir(tmpdir):
            if f.endswith(".mp3"):
                audio_file = os.path.join(tmpdir, f)
                break

        if not audio_file:
            raise ValueError("Audio could not be extracted from the video.")

        result = whisper_model.transcribe(audio_file)
        text = result.get("text", "").strip()

        if not text:
            raise ValueError(
                "Audio transcription produced no usable text (music/silent video)."
            )

        return text


# =====================================================
# Chunking (Long Video Support)
# =====================================================
def chunk_text(text: str, chunk_size: int = 800):
    words = text.split()
    return [
        " ".join(words[i:i + chunk_size])
        for i in range(0, len(words), chunk_size)
    ]


# =====================================================
# SAFE Summarization (Tensor Error FIXED)
# =====================================================
def summarize_text(text: str, summary_type: str = "medium") -> str:
    words = text.split()

    # 🚨 HARD GUARD (prevents tensor reshape error)
    if len(words) < 50:
        raise ValueError(
            "Transcript is too short or low-signal to generate a meaningful summary."
        )

    length_map = {
        "short": (80, 30),
        "medium": (150, 40),
        "detailed": (250, 80),
    }

    max_len, min_len = length_map.get(summary_type, (150, 40))

    chunks = chunk_text(text)

    partial_summaries = []

    for chunk in chunks:
        # Skip tiny / empty chunks
        if len(chunk.split()) < 30:
            continue

        result = summarizer(
            chunk,
            max_length=max_len,
            min_length=min_len,
            do_sample=False
        )
        partial_summaries.append(result[0]["summary_text"])

    # 🚨 FINAL SAFETY CHECK
    if not partial_summaries:
        raise ValueError(
            "Unable to generate summary. Video may be music-only or contain very little speech."
        )

    combined = " ".join(partial_summaries)

    final_summary = summarizer(
        combined,
        max_length=max_len,
        min_length=min_len,
        do_sample=False
    )

    return final_summary[0]["summary_text"]
