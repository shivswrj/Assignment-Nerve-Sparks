# 🎙️ Podcast Audio-to-Text RAG Search
**With Speaker Diarization & Timestamped Playback**

---

## 📌 Overview

This project is a **Retrieval-Augmented Generation (RAG) system** for searching across multiple podcast episodes with advanced audio processing capabilities.

**Key capabilities:**
- 🎧 Convert podcast audio to text (**OpenAI Whisper**)
- 🗣 Identify speakers in transcripts (**Pyannote Audio**)
- 🔍 Search semantically across episodes (**SentenceTransformers + ChromaDB**)
- ⏱ Show timestamped results with episode info
- ▶️ Play exact audio snippets inline
- ⚡ Run in **Fresh Mode** (process from scratch) or **Instant Demo Mode** (use pre-indexed DB)

---

## ✨ Features

- **High accuracy** transcription with Whisper
- **Speaker diarization** — see who spoke each line
- **Multi-episode search** across your entire podcast library
- **Timestamps & snippet playback** in results
- **Pre-indexed mode** for instant demo retrieval
- **Clean Streamlit UI** for upload, indexing, and searching
- **Semantic search** using advanced embedding models
- **Audio snippet extraction** with precise timing

---

## 📂 Project Structure

```
podcast_rag/
├── app.py                 # Streamlit UI
├── backend.py             # Transcription, diarization, retrieval
├── utils.py               # Audio slicing helper
├── config.py              # Model & token configuration
├── requirements.txt       # Python dependencies
├── README.md              # This file
├── sample_data/           # Example audio files
└── chroma_index/          # Prebuilt DB for demo mode
```

---

## 🛠 Installation

### 1️⃣ **Clone Repository**
```bash
git clone <your_repo_url>
cd podcast_rag
```

### 2️⃣ **(Optional) Create Python Virtual Environment**
```bash
python -m venv .venv
.venv\Scripts\activate     # Windows
source .venv/bin/activate  # Mac/Linux
```

### 3️⃣ **Install Dependencies**
```bash
pip install -r requirements.txt
```

### 4️⃣ **Install FFmpeg** (Required by pydub)
- **Download:** [FFmpeg Builds](https://www.gyan.dev/ffmpeg/builds/)
- **Windows:** Extract to `C:\ffmpeg`, add `C:\ffmpeg\bin` to PATH
- **Mac:** `brew install ffmpeg`
- **Linux:** `sudo apt install ffmpeg`
- **Test installation:**
```bash
ffmpeg -version
```

### 5️⃣ **Get HuggingFace Token** (Required for Pyannote)
1. Sign up at [HuggingFace](https://huggingface.co/)
2. Generate an Access Token in your profile settings
3. Accept the Pyannote diarization model license conditions
4. Keep your token ready for the next step

### 6️⃣ **Configure Settings**
Edit `config.py` with your preferences:
```python
HF_TOKEN = "your_hf_token_here"
WHISPER_MODEL = "base"              # Options: base, small, medium, large
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
VECTOR_DB_NAME = "podcasts"
```

---

## 🚀 Modes of Operation

### **Mode 1: Fresh Mode (Build Index from Scratch)**

1. **Configure backend.py:**
```python
USE_PREINDEXED = False
```

2. **Launch application:**
```bash
streamlit run app.py
```

3. **Index your episodes:**
   - Select **"Upload & Index Episode"**
   - Upload audio files (.mp3, .wav, .m4a)
   - Assign unique Episode IDs
   - Wait for transcription and diarization to complete
   - Repeat for additional episodes

### **Mode 2: Instant Demo Mode (Use Pre-indexed Data)**

1. **First, create index using Fresh Mode** (run at least once to generate `chroma_index/`)

2. **Configure backend.py:**
```python
USE_PREINDEXED = True
```

3. **Launch application:**
```bash
streamlit run app.py
```

4. **Start searching immediately** - go directly to **"Search Episodes"**

---

## 🔎 Usage Guide

### **Indexing Episodes**
1. Navigate to **"Upload & Index Episode"** in the sidebar
2. Choose your audio file (supported formats: MP3, WAV, M4A)
3. Enter a unique Episode ID for identification
4. Click "Process Episode"
5. Wait for transcription and speaker diarization to complete
6. Repeat process for additional episodes

### **Searching Episodes**
1. Navigate to **"Search Episodes"** in the sidebar
2. Enter your search query (e.g., "climate change", "AI technology", "investment strategies")
3. Review results showing:
   - **Relevant text snippets**
   - **Speaker identification**
   - **Precise timestamps**
   - **Episode information**
   - **Audio playback controls**

### **Understanding Results**
Each search result includes:
- **Snippet Text:** The relevant portion of the transcript
- **Speaker:** Who spoke this segment (Speaker 1, Speaker 2, etc.)
- **Timestamp:** Exact time in the episode
- **Episode ID:** Which podcast episode contains this content
- **Playback Controls:** Listen to the exact audio segment

---

## ⚙️ Configuration Options

### **Whisper Model Selection**
- `tiny`: Fastest, lowest accuracy
- `base`: Good balance (default)
- `small`: Better accuracy, slower
- `medium`: High accuracy, much slower
- `large`: Best accuracy, very slow

### **Embedding Model Options**
- `all-MiniLM-L6-v2`: Fast, good quality (default)
- `all-mpnet-base-v2`: Better quality, slower
- `sentence-transformers/all-MiniLM-L12-v2`: Larger model, better performance

---

## 🗂️ Dependencies

**Core Libraries:**
- `streamlit` - Web interface
- `openai-whisper` - Audio transcription
- `pyannote.audio` - Speaker diarization
- `sentence-transformers` - Text embeddings
- `chromadb` - Vector database
- `pydub` - Audio processing
- `torch` - Deep learning framework

**Audio Processing:**
- `ffmpeg-python` - Audio format conversion
- `librosa` - Audio analysis
- `scipy` - Scientific computing

**See `requirements.txt` for complete dependency list**

---

## 🚨 Troubleshooting

### **Common Issues:**

**FFmpeg not found:**
- Ensure FFmpeg is installed and in your system PATH
- Restart terminal after PATH modification

**HuggingFace Token Issues:**
- Verify token is correct in `config.py`
- Accept model license agreements on HuggingFace
- Check internet connection for model downloads

**Memory Issues with Large Files:**
- Use smaller Whisper models for large audio files
- Process episodes one at a time
- Consider splitting very long episodes

**Slow Processing:**
- Use GPU if available (CUDA-compatible)
- Choose smaller Whisper models
- Process during off-peak hours

---

## 📊 Performance Notes

**Processing Time Estimates:**
- **10-minute episode:** ~2-5 minutes (base model)
- **1-hour episode:** ~15-30 minutes (base model)
- **GPU acceleration:** 3-5x faster than CPU

**Storage Requirements:**
- **Index data:** ~1MB per hour of audio
- **Audio files:** Original size maintained
- **Models:** ~1-3GB total download

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

---

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 🙋‍♀️ Support

For issues and questions:
1. Check the troubleshooting section above
2. Search existing GitHub issues
3. Create a new issue with detailed information
4. Include error logs and system information

---

## 🔮 Future Enhancements

- [ ] Multi-language support
- [ ] Advanced speaker identification
- [ ] Episode recommendations
- [ ] Export search results
- [ ] API endpoints
- [ ] Batch processing capabilities
- [ ] Custom embedding models
- [ ] Advanced filtering options

---

**Happy podcasting! 🎧**
