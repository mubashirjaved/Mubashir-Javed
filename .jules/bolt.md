## 2025-05-15 - In-memory Audio Processing Pipeline
**Learning:** Transitioning from disk-based audio preprocessing and chunking to an in-memory pipeline using FFmpeg pipes and NumPy arrays significantly reduces I/O overhead. In benchmarks, preprocessing and chunking for a 10-minute audio file improved from ~0.80s to ~0.48s (a ~1.67x speedup for that phase).
**Action:** Always prefer piping raw PCM data from FFmpeg to memory (e.g., via `f32le` and `np.frombuffer`) for audio processing tasks to avoid redundant disk writes and reads.
