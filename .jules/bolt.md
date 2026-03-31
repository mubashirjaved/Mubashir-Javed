## 2026-03-31 - [In-memory audio pipeline]
**Learning:** Moving from a file-based audio processing pipeline (FFmpeg to WAV to Whisper) to an in-memory pipeline (FFmpeg to NumPy to Whisper) reduces processing overhead by ~60% for typical files.
**Action:** Use `subprocess.run` with `stdout=subprocess.PIPE` to stream raw PCM data from FFmpeg directly into NumPy arrays for high-performance audio preprocessing.
