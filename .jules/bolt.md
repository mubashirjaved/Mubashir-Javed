## 2025-05-24 - [In-memory Audio Pipeline]
**Learning:** Decoding audio directly to memory using FFmpeg pipes and `numpy.frombuffer` avoids significant disk I/O overhead and redundant subprocess calls. `np.frombuffer(...).copy()` is essential because the buffer is read-only, and Whisper/Torch requires a writable array.
**Action:** Always prefer in-memory piping for audio preprocessing tasks when system RAM permits.
