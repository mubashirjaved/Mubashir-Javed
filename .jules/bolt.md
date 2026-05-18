## 2026-05-18 - In-memory pipeline optimization
**Learning:** Audio transcription is significantly bottlenecked by redundant FFmpeg calls and disk I/O when chunking files. By piping raw PCM data from FFmpeg directly into NumPy arrays and using array slicing for chunking, we can achieve over 2x speedup in the preprocessing phase.
**Action:** Always prefer in-memory piping and NumPy manipulation for audio/video processing tasks to eliminate I/O overhead. Ensure NumPy arrays are writable when passing to PyTorch-based libraries like Whisper.
