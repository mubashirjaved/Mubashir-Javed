## 2026-04-19 - In-memory audio processing pipeline
**Learning:** Piping raw PCM data from FFmpeg directly into NumPy arrays (`s16le` -> `float32`) eliminates significant disk I/O overhead and temporary file management. For 60s audio, this resulted in a ~2.4x speedup in the preprocessing phase. Additionally, NumPy slicing is instantaneous compared to FFmpeg-based chunking.
**Action:** Always prefer in-memory pipes and NumPy slicing for audio/video preprocessing in Python when the data fits in RAM (~230MB per hour for 16kHz mono float32).
