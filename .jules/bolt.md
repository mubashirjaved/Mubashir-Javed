## 2026-05-13 - In-memory FFmpeg pipeline optimization
**Learning:** Transitioning from a disk-based FFmpeg workflow (writing/reading temporary WAV files) to an in-memory NumPy pipeline using FFmpeg pipes eliminates significant subprocess overhead and disk I/O latency. Benchmarking showed a ~3.4x to 6x speedup in the preprocessing and chunking phase.
**Action:** Use `subprocess.run` with `stdout=subprocess.PIPE` and `-f f32le` for FFmpeg to load audio directly into NumPy arrays for high-performance audio processing tasks.
