## 2026-05-15 - In-Memory Audio Processing Pipeline
**Learning:** Moving from disk-based temporary WAV files to an in-memory NumPy pipeline with FFmpeg piping (`f32le`) reduces preprocessing and chunking overhead by ~2.5x and eliminates disk I/O.
**Action:** Use `ffmpeg ... -f f32le pipe:1` and `np.frombuffer(proc.stdout, dtype=np.float32).copy()` for efficient audio loading. Ensure `threading` and other essential imports are preserved even if `tempfile` is removed.
