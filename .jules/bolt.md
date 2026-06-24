## 2025-05-14 - Baseline Performance Measurement
**Learning:** Baseline preprocessing and chunking for a 600s audio file takes ~2.29s (1.17s preprocessing + 1.12s chunking) using disk-based WAV files.
**Action:** Transition to in-memory NumPy pipeline to eliminate disk I/O and redundant FFmpeg calls.
## 2025-05-14 - In-memory pipeline optimization
**Learning:** Transitioning to an in-memory pipeline using NumPy slicing reduced chunking time from ~1.16s to <0.001s for a 600s audio file. Total pre-transcription time (preprocessing + chunking) was reduced by ~1.75x.
**Action:** Use FFmpeg pipes to read audio directly into NumPy arrays for processing when low latency and minimal disk I/O are desired.
