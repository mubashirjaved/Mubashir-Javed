## 2025-05-15 - In-memory Audio Processing Speedup

**Learning:** Migrating from disk-based WAV chunking to an in-memory NumPy pipeline significantly reduces I/O overhead and redundant process calls. Using FFmpeg pipes to decode audio directly into a NumPy array and then slicing that array for transcription is ~3x faster for a 10-minute audio file.

**Action:** Prefer in-memory processing pipelines (using NumPy and FFmpeg pipes) over intermediate file-based workflows for audio/data processing tasks where RAM allows.
