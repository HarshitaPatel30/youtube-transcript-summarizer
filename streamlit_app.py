import streamlit as st
from summarizer import (
    get_transcript,
    summarize_text,
    get_video_metadata
)

# ===================== Page Config =====================
st.set_page_config(
    page_title="AI YouTube Summarizer",
    layout="wide"
)

# ===================== Sidebar =====================
with st.sidebar:
    st.header("ℹ️ How it works")
    st.markdown("""
1. Paste a YouTube video URL  
2. Captions are fetched (or Whisper transcribes audio)  
3. AI generates a concise summary
""")

    st.header("🔗 Example URL")
    st.code("https://www.youtube.com/watch?v=9bZkp7q19f0")

    st.header("🛠 Tech Stack")
    st.markdown("""
- Python  
- Streamlit  
- Whisper  
- Hugging Face Transformers  
- yt-dlp + FFmpeg
""")

# ===================== Main Header =====================
st.title("🎬 AI YouTube Video Summarizer")
st.caption(
    "Summarize any YouTube video using AI-powered transcription & NLP. "
    "Supports captions with Whisper audio fallback."
)

# ===================== Inputs =====================
url = st.text_input("🔗 Enter YouTube Video URL")

summary_type = st.selectbox(
    "📏 Summary Length",
    ["short", "medium", "detailed"]
)

# ===================== Video Preview =====================
if url:
    try:
        metadata = get_video_metadata(url)

        st.markdown("### 📺 Video Preview")
        col1, col2 = st.columns([1, 2])

        with col1:
            st.image(metadata["thumbnail"], use_container_width=True)

        with col2:
            st.markdown(f"**Title:** {metadata['title']}")
            st.markdown(f"**Channel:** {metadata['channel']}")

            if metadata["duration"]:
                m = metadata["duration"] // 60
                s = metadata["duration"] % 60
                st.markdown(f"**Duration:** {m}:{s:02d}")

    except Exception:
        st.warning("Unable to load video preview.")

# ===================== Action =====================
if st.button("🚀 Summarize Video"):
    if not url:
        st.error("Please enter a YouTube URL.")
    else:
        status = st.status("Processing video…", expanded=True)

        try:
            # ---- Stage 1 ----
            status.write("📄 Fetching transcript (captions / audio)…")
            transcript = get_transcript(url)

            # ---- Stage 2 ----
            status.write("🧠 Generating AI summary…")
            summary = summarize_text(transcript, summary_type)

            status.update(label="✅ Done", state="complete")

            # ===================== Tabs =====================
            tab1, tab2, tab3 = st.tabs(
                ["📝 Summary", "📜 Transcript", "ℹ️ About"]
            )

            # -------- Summary Tab --------
            with tab1:
                st.subheader("Summary")
                st.write(summary)

                st.markdown(
                    f"**Word count:** {len(summary.split())}"
                )

                st.download_button(
                    label="⬇ Download Summary (.txt)",
                    data=summary,
                    file_name="youtube_summary.txt",
                    mime="text/plain"
                )

            # -------- Transcript Tab --------
            with tab2:
                st.subheader("Full Transcript")

                st.markdown(
                    f"**Word count:** {len(transcript.split())}"
                )

                st.text_area(
                    label="Transcript",
                    value=transcript,
                    height=300
                )

                st.download_button(
                    label="⬇ Download Transcript (.txt)",
                    data=transcript,
                    file_name="youtube_transcript.txt",
                    mime="text/plain"
                )

            # -------- About Tab --------
            with tab3:
                st.markdown("""
### 🔍 How this application works

1. Attempts to fetch YouTube captions  
2. Falls back to Whisper-based audio transcription  
3. Splits long transcripts into chunks  
4. Uses transformer-based abstractive summarization  
5. Merges partial summaries into a coherent result  

**Built for real-world usage, not demos.**
""")

        except Exception as e:
            status.update(label="❌ Failed", state="error")
            st.error(str(e))
