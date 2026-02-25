## 2025-05-15 - In-memory Audio Chunking
**Learning:** In projects using Whisper and FFmpeg for audio processing, repeated subprocess calls for chunking and disk I/O for temporary files create significant overhead. Piping FFmpeg output directly to a `numpy` array and using array slicing for chunks is much faster and cleaner.
**Action:** Always prefer in-memory piping and slicing for audio processing pipelines if the hardware has sufficient RAM (approx. 230MB per hour of audio for 16kHz mono float32).
