## 2025-05-15 - [In-memory audio pipeline]
**Learning:** Transitioning from disk-based WAV chunking to an in-memory NumPy pipeline significantly reduces pre-transcription overhead. Measuring a 600s audio file showed a reduction from ~0.96s to ~0.76s for preprocessing and chunking (eliminating all disk I/O for chunks).
**Action:** Always prefer FFmpeg pipes to memory for intermediate audio processing in Whisper workflows to avoid subprocess and disk overhead.
