## 2025-05-15 - [In-memory audio pipeline]
**Learning:** Transitioning from disk-based WAV chunking to an in-memory NumPy pipeline using FFmpeg's `f32le` pipe significantly reduces pre-transcription overhead. For a 600s audio file, I achieved a ~1.6x speedup by eliminating redundant disk I/O and FFmpeg process spawns for each chunk.
**Action:** Use `ffmpeg -f f32le -` to pipe raw PCM data to stdout and read into NumPy via `np.frombuffer` for efficient in-memory audio processing in Whisper-based applications.
