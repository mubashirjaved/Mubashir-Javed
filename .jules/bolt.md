## 2026-07-05 - [In-Memory Audio Pipeline Optimization]
**Learning:** Transitioning from disk-based audio chunking (using FFmpeg to write WAV files) to an in-memory NumPy pipeline (using FFmpeg pipes and NumPy slicing) significantly reduces pre-transcription overhead. For a 600s audio file, the preprocessing and chunking phase saw a ~2.3x speedup.
**Action:** Always prefer in-memory data pipelines for intermediate processing steps in audio/video applications to eliminate disk I/O bottlenecks.
