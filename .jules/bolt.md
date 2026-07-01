## 2026-07-01 - [In-memory NumPy Pipeline for Whisper]
**Learning:** Transitioning from disk-based WAV chunking to an in-memory NumPy pipeline reduces FFmpeg overhead and disk I/O significantly, especially for the pre-transcription phase (preprocessing and chunking). Benchmarks show a ~1.63x speedup for this phase on 600s audio.
**Action:** Use FFmpeg's `pipe:1` with `s16le` format and `np.frombuffer` to ingest audio directly into memory. Perform chunking via NumPy array slicing for O(1) time complexity.
