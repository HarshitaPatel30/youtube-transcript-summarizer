import streamlit as st
from summarizer import (
    get_transcript,
    summarize_text,
    get_video_metadata
)

st.set_page_config(
    page_title="AI YouTube Summarizer",
    layout="wide"
)

st.title("🎬 AI YouTube Video Summarizer")
st.caption(
    "Summarize YouTube videos using AI — captions first, Whisper audio fallback if needed."
)

# ===================== Inputs =====================
url = st.text_input("Enter YouTube Video URL")

summary_type = st.selectbox(
    "Summary Length",
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
if st.button("Summarize"):
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

                1. Attempts to fetch YouTube captions using the official transcript API  
                2. If captions are unavailable, downloads audio and transcribes it using **Whisper**  
                3. Splits long transcripts into manageable chunks  
                4. Applies **Transformer-based abstractive summarization**  
                5. Combines partial summaries into a final coherent result  

                **Tech Stack**
                - Python
                - Streamlit
                - Whisper (Speech-to-Text)
                - Hugging Face Transformers
                - yt-dlp + FFmpeg
                """)

        except Exception as e:
            status.update(label="❌ Failed", state="error")
            st.error(str(e))
