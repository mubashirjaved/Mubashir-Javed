## 2025-06-25 - [In-memory Pipeline Optimization]
**Learning:** Moving from disk-based chunking to in-memory NumPy slicing significantly reduces FFmpeg overhead and disk I/O latency. For a 60s file, the preprocessing time dropped from ~0.4s to ~0.09s (~75% reduction). In-memory processing also simplifies temporary file management.
**Action:** Prioritize FFmpeg pipes and NumPy for audio processing tasks to avoid intermediate files and redundant subprocess calls.

## 2025-06-25 - [Subprocess Pipe Deadlock]
**Learning:** capturing both `stdout` and `stderr` with `subprocess.run(capture_output=True)` or `stdout=PIPE, stderr=PIPE` can cause a deadlock if the output exceeds the OS pipe buffer size (typically 64KB) and the parent process is not actively reading from the other pipe.
**Action:** Redirect `stderr` to `DEVNULL` or use `subprocess.communicate()` when capturing large `stdout` streams from FFmpeg.
