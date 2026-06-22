## 2026-06-22 - In-memory NumPy audio pipeline
**Learning:** Transitioning from disk-based WAV chunking to an in-memory NumPy pipeline with FFmpeg pipes achieved a ~4x speedup for 600s audio files by eliminating redundant disk I/O and subprocess overhead.
**Action:** Use FFmpeg pipes to stream audio directly into NumPy arrays for high-performance audio processing tasks.
