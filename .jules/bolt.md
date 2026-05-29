## 2026-05-29 - In-Memory Audio Pipeline Optimization
**Learning:** Moving from a file-based audio preprocessing and chunking pipeline to an in-memory NumPy-based pipeline eliminates redundant disk I/O and FFmpeg process overhead. This resulted in a ~1.4x speedup for the preprocessing and chunking phase of 10-minute audio files on the target architecture.
**Action:** Prefer piping FFmpeg output to stdout and loading into NumPy for audio processing tasks to avoid temporary file management and improve performance.
