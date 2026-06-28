## 2026-06-28 - [In-memory NumPy audio pipeline]
**Learning:** Transitioning from disk-based FFmpeg chunking to an in-memory NumPy pipeline reduces FFmpeg process spawns from N+2 to 1 and eliminates redundant disk I/O, providing a significant speedup for the pre-transcription phase.
**Action:** Use `ffmpeg -f s16le -` to pipe raw PCM data to stdout and read into NumPy via `np.frombuffer` for efficient in-memory audio processing in Whisper-based applications.
