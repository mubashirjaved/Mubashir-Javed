## 2025-05-22 - Full in-memory audio processing pipeline
**Learning:** Moving from disk-based preprocessing and chunking (WAV files) to in-memory NumPy slicing provides a ~5x speedup for 60s files and significantly higher gains for larger files by eliminating redundant FFmpeg calls and disk I/O.
**Action:** Prefer streaming FFmpeg output to NumPy for batch processing pipelines. Always update timestamp logic when chunking dynamically.
