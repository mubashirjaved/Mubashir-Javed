## 2026-04-29 - In-memory Audio Pipeline
**Learning:** The in-memory processing pipeline significantly reduces overhead by eliminating redundant FFmpeg calls and disk I/O, providing a measurable speedup (~1.6x in the initial processing phase for short audio). NumPy slicing makes chunking instantaneous.
**Action:** Use `np.frombuffer(...).copy()` when piping from FFmpeg to ensure the array is writable for PyTorch/Whisper.
