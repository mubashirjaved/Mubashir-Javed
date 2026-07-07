## 2025-05-15 - In-memory NumPy audio pipeline speedup
**Learning:** Moving from disk-based WAV chunking (multiple FFmpeg calls) to a single in-memory FFmpeg pipe with NumPy slicing reduced preprocessing/chunking time by ~50% for 600s files. NumPy slicing is essentially O(1) compared to O(N) disk writes.
**Action:** Always use in-memory pipes and NumPy slicing for Whisper preprocessing to avoid I/O bottlenecks and redundant subprocess overhead.
