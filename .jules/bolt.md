## 2026-05-26 - In-Memory Audio Pipeline Optimization
**Learning:** Significant performance gains can be achieved by streaming raw PCM data from FFmpeg directly into NumPy arrays, bypassing expensive disk I/O and redundant process spawns for chunking. Specifically, for a 10-minute audio file, the preprocessing and chunking phase saw an ~11.5x speedup.
**Action:** Always prefer in-memory pipelines for audio/video processing in Python when the data size permits (e.g., ~230MB per hour for float32 mono).

## 2026-05-26 - Whisper NumPy Native Support
**Learning:** Whisper's `detect_language` and `transcribe` methods can accept NumPy arrays directly, which allows for extremely efficient slicing and eliminates the need for temporary WAV files.
**Action:** When working with Whisper, skip disk-based segmenting and use NumPy slices.
