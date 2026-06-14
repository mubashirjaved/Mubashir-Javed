## 2025-05-22 - [In-memory Audio Pipeline]
**Learning:** Moving from disk-based temporary chunks to an in-memory NumPy pipeline reduces pre-transcription overhead by ~70% and fixes a bug where timestamps were miscalculated if the chunk size was not 180 seconds.
**Action:** Always prefer piping FFmpeg output to memory via `pipe:1` for intermediate processing steps to avoid expensive disk I/O. Ensure NumPy arrays are copied using `.copy()` to make them writable for Whisper/Torch.
