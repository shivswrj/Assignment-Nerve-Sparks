import whisper
from sentence_transformers import SentenceTransformer
import chromadb
from pyannote.audio import Pipeline
from config import HF_TOKEN, WHISPER_MODEL, EMBEDDING_MODEL, VECTOR_DB_NAME
import os

# ====== MODE TOGGLE ======
# If True → Loads existing ChromaDB index from chroma_index/ (NO re‑index needed)
# If False → Creates new index (used only if building fresh data)
USE_PREINDEXED = True

# ====== Model Loading ======
asr_model = whisper.load_model(WHISPER_MODEL)
embed_model = SentenceTransformer(EMBEDDING_MODEL)
pipeline = Pipeline.from_pretrained("pyannote/speaker-diarization",
                                    use_auth_token=HF_TOKEN)

# ====== Vector DB Setup ======
if USE_PREINDEXED and os.path.exists("chroma_index"):
    print("🔹 Loading pre‑indexed ChromaDB...")
    client = chromadb.PersistentClient(path="chroma_index")
    collection = client.get_collection(name=VECTOR_DB_NAME)
else:
    print("🔹 Creating fresh ChromaDB collection...")
    client = chromadb.PersistentClient(path="chroma_index")
    try:
        collection = client.create_collection(name=VECTOR_DB_NAME)
    except:
        collection = client.get_collection(name=VECTOR_DB_NAME)

# ====== Functions ======
def transcribe_and_diarize(audio_path):
    """Transcribe audio with Whisper and match with diarization."""
    result = asr_model.transcribe(audio_path)
    transcription_segments = result["segments"]

    diarization = pipeline(audio_path)
    speaker_segments = [
        {"start": turn.start, "end": turn.end, "speaker": speaker}
        for turn, _, speaker in diarization.itertracks(yield_label=True)
    ]

    enriched_segments = []
    for seg in transcription_segments:
        matched_speaker = "Unknown"
        for spk in speaker_segments:
            if seg["start"] >= spk["start"] and seg["end"] <= spk["end"]:
                matched_speaker = spk["speaker"]
                break
        enriched_segments.append({
            "text": seg["text"],
            "start": seg["start"],
            "end": seg["end"],
            "speaker": matched_speaker
        })
    return enriched_segments

def index_transcript(segments, episode_id):
    """Add episode transcript segments to ChromaDB."""
    for idx, seg in enumerate(segments):
        vector = embed_model.encode(seg["text"]).tolist()
        collection.add(
            embeddings=[vector],
            documents=[seg["text"]],
            metadatas=[{
                "episode": episode_id,
                "start": seg["start"],
                "end": seg["end"],
                "speaker": seg["speaker"]
            }],
            ids=[f"{episode_id}_{idx}"]
        )

def search_query(query, top_k=5):
    """Search ChromaDB for top_k results."""
    qvec = embed_model.encode(query).tolist()
    results = collection.query(query_embeddings=[qvec], n_results=top_k)
    return results
