## 2025-06-25 - [In-memory Audio Pipeline]
**Learning:** Transitioning from file-based chunking (multiple FFmpeg calls writing to disk) to a single in-memory FFmpeg pipe with NumPy slicing provides a measurable performance boost by eliminating redundant I/O and process overhead. Additionally, `np.frombuffer` returns a read-only view, which can cause issues with `torch` unless `.copy()` is called to create a writable array.
**Action:** Use `subprocess.run(..., capture_output=True)` with `np.frombuffer(...).copy()` for efficient, writable in-memory audio processing.

## 2025-06-25 - [Whisper Timestamp Logic]
**Learning:** Hardcoded offsets in chunked transcription pipelines (e.g., `idx * 180`) create incorrect timestamps when users customize chunk sizes.
**Action:** Always derive segment offsets dynamically from the actual `chunk_seconds` parameter.
