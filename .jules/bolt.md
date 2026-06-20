## 2025-05-15 - In-memory Audio Processing Pipeline
**Learning:** Switching from disk-based WAV chunks to an in-memory NumPy pipeline significantly reduces pre-transcription overhead (over 2x speedup for 10-minute files) and fixes hardcoded chunk offset bugs.
**Action:** Use FFmpeg pipes to read audio directly into NumPy arrays and perform slicing in memory for Whisper-based applications to avoid disk I/O and redundant process spawning. Always clean up binary artifacts and __pycache__ before submission.
