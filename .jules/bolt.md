## 2026-05-22 - In-Memory Audio Pipeline Optimization
**Learning:** Moving the entire audio processing pipeline (preprocessing and chunking) to memory using FFmpeg pipes and NumPy arrays provides a significant speedup (up to 4x for large files) by eliminating disk I/O and redundant FFmpeg calls.
**Action:** Use `np.frombuffer(...).copy()` when piping raw PCM data from FFmpeg to ensure the resulting NumPy array is writable, as Whisper/PyTorch requires writable tensors. Always clean up unused imports like `json`, `tempfile`, and `time` after refactoring to maintain high Pylint scores.
