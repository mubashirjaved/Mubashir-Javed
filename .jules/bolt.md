## 2025-05-15 - [In-memory NumPy Audio Pipeline]
**Learning:** Transitioning from disk-based WAV chunking to an in-memory NumPy pipeline significantly reduces pre-transcription latency by eliminating redundant FFmpeg process spawns and disk I/O. NumPy array slicing provides an O(1) chunking mechanism that is thousands of times faster than FFmpeg-based file splitting.
**Action:** Always prefer piping raw PCM data from FFmpeg to a NumPy array via stdout when using Whisper, as it avoids intermediate file artifacts and allows for efficient in-memory manipulation.
