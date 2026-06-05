## 2025-06-25 - [In-memory Audio Processing Pipeline]
**Learning:** Transitioning from disk-based temporary files to in-memory FFmpeg pipes significantly reduces preprocessing and chunking time, especially for short files (up to 3x speedup). Using `np.frombuffer(...).copy()` is essential because Whisper/PyTorch requires writable tensors, and `frombuffer` returns a read-only view.
**Action:** Prefer in-memory pipelines for audio/video processing tasks to eliminate disk I/O bottlenecks. Always ensure NumPy arrays are writable before passing them to ML frameworks.
