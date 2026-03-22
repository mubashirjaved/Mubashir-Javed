## 2025-06-25 - [In-memory Pipeline Optimization]
**Learning:** Moving from a file-based audio processing pipeline to an in-memory NumPy-based one significantly reduces transcription latency by eliminating redundant Disk I/O and process overhead. For a 60s audio file, this optimization resulted in a ~34% speed improvement.
**Action:** Always prefer piping raw PCM data from FFmpeg directly into NumPy arrays for audio processing tasks to avoid temporary file overhead.

## 2025-06-25 - [Subprocess PIPE Exclusivity]
**Learning:** In `subprocess.run`, using `stdout=subprocess.PIPE` is incompatible with `capture_output=True` (which sets both stdout and stderr to PIPE) if you are also explicitly setting `stderr=subprocess.DEVNULL`.
**Action:** Use `stdout=subprocess.PIPE` and `stderr=subprocess.DEVNULL` explicitly instead of `capture_output=True` to avoid `ValueError` when selective redirection is needed.
