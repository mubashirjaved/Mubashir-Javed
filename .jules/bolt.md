## 2025-05-22 - In-Memory Audio Processing & Model Caching
**Learning:** Redundant FFmpeg calls and disk I/O for temporary WAV files create significant overhead in Whisper pipelines. Moving to a single FFmpeg pipe into a NumPy array reduced processing time by ~65% for short files. Implementing class-level model caching eliminates multi-second delays on repeated transcriptions.
**Action:** Always prefer streaming pipes (stdout/stdin) and in-memory arrays for media processing unless file size exceeds available RAM. Implement model caching for any heavy AI model used in interactive applications.
