## 2026-05-16 - [In-memory Audio Processing]
**Learning:** Moving from disk-based temporary files to in-memory NumPy arrays via FFmpeg pipes significantly reduces I/O overhead and avoids filesystem pollution. For a 10-minute audio file, the preprocessing and chunking phase saw a ~2.1x speedup (1.19s -> 0.55s).
**Action:** Use `ffmpeg ... -f f32le pipe:1` and `np.frombuffer(stdout, dtype=np.float32)` for high-performance audio ingestion in Python.
