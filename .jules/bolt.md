## 2026-03-27 - In-memory audio pipeline
**Learning:** Transitioning from a disk-based FFmpeg pipeline (WAV files) to an in-memory NumPy pipeline (raw PCM pipe) reduces preprocessing and chunking overhead by ~50%. In-memory slicing of NumPy arrays makes chunking virtually instantaneous compared to multiple FFmpeg calls.
**Action:** Always prefer piping raw data from subprocesses into memory for intermediate processing steps if the data fits in RAM (e.g., 10h of 16kHz audio ≈ 2.3GB).
