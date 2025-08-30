import streamlit as st
from summarizer import get_transcript, summarize_text, translate_to_english

st.title("🎬 YouTube Transcript Summarizer")
st.write("Easily summarize YouTube videos using AI")

video_url = st.text_input("Enter YouTube Video URL:")

lang_option = st.selectbox(
    "Choose transcript language:",
    ["Auto", "English Only", "Hindi (Translate to English)"]
)

if st.button("Summarize"):
    if not video_url:
        st.error("Please enter a YouTube video URL")
    else:
        try:
            # Determine language
            if lang_option == "English Only":
                lang = 'en'
                transcript = get_transcript(video_url, lang)
            elif lang_option == "Hindi (Translate to English)":
                lang = 'hi'
                transcript = get_transcript(video_url, lang)
                transcript = translate_to_english(transcript)
            else:
                # Auto: Try English, fallback Hindi->English
                try:
                    transcript = get_transcript(video_url, 'en')
                except:
                    transcript = get_transcript(video_url, 'hi')
                    transcript = translate_to_english(transcript)

            st.subheader("Transcript:")
            st.write(transcript[:2000] + ("..." if len(transcript) > 2000 else ""))

            summary = summarize_text(transcript)
            st.subheader("Summary:")
            st.write(summary)

        except Exception as e:
            st.error(f"❌ Failed to fetch transcript: {e}")
