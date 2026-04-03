## 2026-04-03 - In-memory NumPy audio pipeline for Whisper
**Learning:** Transitioning from disk-based `.wav` chunking to in-memory NumPy slicing reduces preprocessing overhead by ~57% for 60s files and makes chunking virtually instantaneous. Passing the array directly to `whisper.pad_or_trim` and `whisper.transcribe` eliminates redundant FFmpeg calls and disk I/O.
**Action:** Prioritize in-memory piping for media processing pipelines when working with models (like Whisper) that can accept raw buffers or NumPy arrays directly.
