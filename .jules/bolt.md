## 2025-05-14 - [In-memory NumPy Pipeline for Whisper]
**Learning:** Transitioning from disk-based FFmpeg chunking to an in-memory NumPy pipeline (using pipes and slicing) significantly reduces pre-transcription overhead. For a 600s audio file, preprocessing and chunking time was reduced from ~1.14s to ~0.45s (2.5x speedup), and chunking itself became an O(1) operation (0.0000s measured).
**Action:** Always prefer piping raw PCM data to NumPy (`-f f32le`) and using array slicing for chunking in audio pipelines to eliminate redundant disk I/O and process spawns.
