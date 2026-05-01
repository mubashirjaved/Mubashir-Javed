## 2026-05-01 - In-memory audio processing pipeline
**Learning:** Moving from disk-based temporary WAV files to in-memory NumPy arrays for Whisper preprocessing and chunking significantly reduces I/O overhead. Specifically, chunking becomes instantaneous (0.0000s) as it's just array slicing instead of separate FFmpeg calls.
**Action:** Always prefer in-memory pipes for intermediate audio processing steps when the memory footprint (approx. 2.3GB per 10 hours of audio at 16kHz float32) is acceptable for the target hardware.
