## 2026-04-23 - In-memory NumPy pipeline for Whisper
**Learning:** The in-memory processing pipeline significantly reduces overhead by eliminating redundant FFmpeg calls and disk I/O, providing a measurable speedup in the preprocessing and chunking phase. Slicing a NumPy array is near-instant compared to FFmpeg-based disk chunking.
**Action:** Favor streaming raw PCM data from FFmpeg to NumPy for Whisper-based transcribers to eliminate temporary file management and redundant decoding.
