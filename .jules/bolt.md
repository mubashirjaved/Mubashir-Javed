## 2026-05-08 - In-memory Audio Pipeline
**Learning:** Moving from file-based chunking and preprocessing to an in-memory NumPy-based pipeline significantly reduces disk I/O overhead and redundant FFmpeg calls. Whisper's `detect_language` and `transcribe` methods can directly accept NumPy arrays, allowing for a much cleaner and faster processing flow.
**Action:** Always check if core processing libraries (like Whisper or PyTorch) can accept in-memory buffers or NumPy arrays before resorting to temporary files on disk.
