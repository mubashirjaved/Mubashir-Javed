## 2026-05-19 - In-Memory Audio Pipeline
**Learning:** The in-memory processing pipeline provides a measurable speedup of approximately 5x in the preprocessing and chunking phase for 60-second audio files by eliminating redundant FFmpeg calls and disk I/O.
**Action:** Use `subprocess.PIPE` to stream raw PCM data from FFmpeg directly into `numpy` arrays instead of using temporary WAV files.

**Learning:** When using `np.frombuffer` to read FFmpeg piped PCM data, the resulting array is a read-only view.
**Action:** Explicitly call `.copy()` on the array to ensure compatibility with PyTorch/Whisper which requires writable tensors.

**Learning:** Whisper's `detect_language` and `transcribe` methods can accept pre-loaded NumPy arrays directly, which avoids redundant disk reads when an in-memory pipeline is already implemented.
**Action:** Pass NumPy arrays directly to Whisper engine methods to maintain the efficiency of the in-memory pipeline.
