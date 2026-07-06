## 2025-01-24 - [In-memory NumPy Audio Pipeline]
**Learning:** Transitioning from disk-based WAV chunking to an in-memory NumPy pipeline using FFmpeg pipes (`f32le`) significantly reduces I/O overhead and process spawn latency. Slicing a large NumPy array is O(1) or O(k) compared to O(N) re-encoding with FFmpeg for each chunk.
**Action:** Use `subprocess.run` with `stdout=subprocess.PIPE` to capture raw PCM data and `np.frombuffer(result.stdout, np.float32).copy()` to create a writable Whisper-compatible array.

## 2025-01-24 - [Whisper Segment Offset Logic]
**Learning:** When chunking audio for Whisper, both the segment-level `start`/`end` timestamps and the individual `word` timestamps (if `word_timestamps=True`) must be manually offset by the chunk's start time in seconds.
**Action:** Always iterate through `result['segments']` and their internal `words` list to apply `chunk_offset` before merging results.
