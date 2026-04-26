## 2026-04-26 - In-memory NumPy pipeline for Whisper
**Learning:** Using `np.frombuffer` to read FFmpeg piped PCM data results in a non-writable view. This triggers PyTorch `UserWarning` in Whisper's `load_audio` path. Explicitly calling `.copy()` on the array ensures compatibility and avoids warnings without significant overhead.
**Action:** Always ensure NumPy arrays loaded from buffers are made writable via `.copy()` before passing them to PyTorch-based libraries like Whisper.
