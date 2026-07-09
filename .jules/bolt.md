## 2025-05-23 - [In-memory Audio Pipeline Optimization]
**Learning:** Disk I/O and redundant FFmpeg process spawning for audio chunking is a major bottleneck in transcription pipelines. Moving from disk-based temporary WAV files to a single FFmpeg pipe into a NumPy array, followed by O(1) array slicing for chunking, yielded a ~2.3x to 3.5x speedup in the pre-transcription phase.
**Action:** Always prefer in-memory NumPy pipelines for audio processing when using Whisper, as its Python API natively supports NumPy arrays and eliminates the need for intermediate storage.
