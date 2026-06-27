## 2025-05-15 - In-memory NumPy audio pipeline
**Learning:** Transitioning from disk-based WAV chunking to an in-memory NumPy pipeline with FFmpeg pipes significantly reduces I/O overhead and redundant FFmpeg process spawns. For a 600s audio file, this yielded a ~1.77x speedup in the pre-transcription phase.
**Action:** Use `ffmpeg -f f32le -` to pipe raw PCM data to stdout and read into NumPy via `np.frombuffer(out, np.float32).copy()` for efficient in-memory audio processing in Whisper pipelines.
