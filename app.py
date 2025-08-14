import streamlit as st
import os
from backend import transcribe_and_diarize, index_transcript, search_query
from utils import get_audio_slice

st.set_page_config(page_title="Podcast RAG Search", layout="wide")
st.title("🎙️ Podcast RAG with Speaker Diarization & Playback")

option = st.radio("Choose Action", ["Upload & Index Episode", "Search Episodes"])

if option == "Upload & Index Episode":
    audio_file = st.file_uploader("Upload Podcast Audio", type=["mp3", "wav", "m4a"])
    episode_id = st.text_input("Episode ID (unique identifier)")

    if audio_file and episode_id and st.button("Process & Index"):
        temp_path = f"temp_{episode_id}.mp3"
        with open(temp_path, "wb") as f:
            f.write(audio_file.read())

        st.info("Transcribing and diarizing... This may take a moment ⏳")
        segments = transcribe_and_diarize(temp_path)
        index_transcript(segments, episode_id)
        st.success(f"Episode '{episode_id}' indexed successfully with {len(segments)} segments.")

elif option == "Search Episodes":
    query = st.text_input("Enter search query:")
    top_k = st.slider("Number of results", 1, 10, 5)
    if query and st.button("Search"):
        results = search_query(query, top_k)
        for doc, meta in zip(results["documents"][0], results["metadatas"][0]):
            st.markdown(f"**{doc}**")
            st.markdown(f"🗣 **Speaker:** {meta.get('speaker','Unknown')} | ⏱ {meta['start']}s → {meta['end']}s | 🎧 Episode: {meta['episode']}")

            audio_path = f"temp_{meta['episode']}.mp3"
            if os.path.exists(audio_path):
                snippet_path = get_audio_slice(audio_path, int(meta['start']), int(meta['end']))
                with open(snippet_path, "rb") as af:
                    st.audio(af.read(), format="audio/mp3")
