## 2026-04-28 - In-memory NumPy Pipeline Optimization
**Learning:** Moving from disk-based chunking to in-memory NumPy slicing significantly reduces latency (1.5x overall speedup) and eliminates redundant FFmpeg calls. Language detection specifically benefits (2.4x faster) by avoiding file re-loading.
**Action:** Always prefer piping FFmpeg output directly to NumPy for intermediate processing stages to eliminate disk I/O overhead.

**Learning:** `np.frombuffer` produces a read-only view. PyTorch/Whisper requires writable tensors.
**Action:** Use `.copy()` on arrays derived from `np.frombuffer` to ensure they are writable and avoid downstream errors or warnings.

**Learning:** Whisper segments typically include their own leading spaces.
**Action:** Use `"".join()` instead of `" ".join()` when merging transcribed chunks to avoid double-spacing regressions.
