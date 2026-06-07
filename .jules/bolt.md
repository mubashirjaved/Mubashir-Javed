## 2025-06-25 - [In-memory Audio Processing]
**Learning:** Moving from disk-based intermediate files to FFmpeg pipes and in-memory NumPy slicing provides a massive speedup (~4.5x for 60s files) and simplifies logic by removing temporary directory management.
**Action:** Use FFmpeg's `f32le` format for direct PCM-to-NumPy ingestion to eliminate disk I/O in audio processing pipelines.

## 2025-06-25 - [Dynamic Chunk Offsets]
**Learning:** Hardcoding segment offsets (e.g., 180s) leads to incorrect timestamps if the user changes the chunk size.
**Action:** Always calculate offsets dynamically based on the actual `chunk_seconds` parameter.
