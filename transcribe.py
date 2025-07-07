import whisperx

# Load model (base, CPU, int8 for faster inference)
model = whisperx.load_model("medium", device="cpu", compute_type="float32")

# Load audio file
audio = whisperx.load_audio("adio.ogg")

# Transcribe with language hint (English)
result = model.transcribe(audio, language="en")

# --- Save plain text transcript ---
with open("transcription.txt", "w", encoding="utf-8") as f:
    for seg in result["segments"]:
        f.write(f"[{seg['start']:.2f}s - {seg['end']:.2f}s] {seg['text']}\n")

# --- Save SRT subtitles ---
def format_srt_timestamp(seconds):
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    ms = int((seconds - int(seconds)) * 1000)
    return f"{h:02}:{m:02}:{s:02},{ms:03}"

with open("transcription.srt", "w", encoding="utf-8") as f:
    for i, seg in enumerate(result["segments"], 1):
        f.write(f"{i}\n")
        f.write(f"{format_srt_timestamp(seg['start'])} --> {format_srt_timestamp(seg['end'])}\n")
        f.write(f"{seg['text'].strip()}\n\n")
