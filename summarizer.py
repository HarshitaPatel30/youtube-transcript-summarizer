from youtube_transcript_api import YouTubeTranscriptApi
from transformers import pipeline
import re

# Initialize summarization and translation models
summarizer_model = pipeline("summarization", model="facebook/bart-large-cnn")
translator_model = pipeline("translation", model="Helsinki-NLP/opus-mt-hi-en")  # Hindi -> English

def get_video_id(url):
    """Extract the video ID from a YouTube URL"""
    match = re.search(r"(?:v=|youtu\.be/)([\w-]+)", url)
    return match.group(1) if match else None

def get_transcript(video_url, lang='en'):
    video_id = get_video_id(video_url)
    if not video_id:
        raise ValueError("Invalid YouTube URL")

    # Fetch transcript
    transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
    
    # Try requested language first
    try:
        transcript = transcript_list.find_transcript([lang])
    except:
        # fallback to English
        transcript = transcript_list.find_transcript(['en'])
    
    return " ".join([t['text'] for t in transcript.fetch()])

def summarize_text(text, max_len=150):
    summary = summarizer_model(text, max_length=max_len, min_length=30, do_sample=False)
    return summary[0]['summary_text']

def translate_to_english(text):
    translated = translator_model(text)
    return translated[0]['translation_text']
