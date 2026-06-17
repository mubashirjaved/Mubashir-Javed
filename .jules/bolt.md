## 2025-05-15 - [In-Memory Audio Processing]
**Learning:** Moving from disk-based chunking with FFmpeg to in-memory processing with NumPy slicing provides a ~5.8x speedup for the preprocessing/chunking phase (for 60s audio).
**Action:** Use FFmpeg pipes to load audio into NumPy arrays for high-performance audio processing tasks to avoid redundant Disk I/O and subprocess overhead.
