from pydub import AudioSegment

def get_audio_slice(audio_path, start, end):
    """Extract a snippet of audio from start to end seconds."""
    audio = AudioSegment.from_file(audio_path)
    snippet = audio[start * 1000:end * 1000]  # pydub works in milliseconds
    out_path = f"snippet_{int(start)}s_{int(end)}s.mp3"
    snippet.export(out_path, format="mp3")
    return out_path
