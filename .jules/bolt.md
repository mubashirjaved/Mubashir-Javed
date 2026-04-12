## 2026-04-12 - In-Memory Audio Pipeline
**Learning:** Moving from disk-based audio chunking (individual FFmpeg calls per chunk) to an in-memory NumPy pipeline reduces preprocessing overhead by ~70%. Using FFmpeg pipes for raw PCM data is significantly more efficient than writing intermediate WAV files.
**Action:** Always prefer piping raw data from FFmpeg to memory for small to medium-sized audio assets in Whisper-based projects to eliminate I/O bottlenecks.
