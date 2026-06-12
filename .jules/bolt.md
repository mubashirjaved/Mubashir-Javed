## 2025-01-24 - [In-Memory Audio Pipeline]
**Learning:** Moving from disk-based WAV chunking to an in-memory NumPy pipeline using FFmpeg pipes significantly reduces preprocessing time (measured ~2x speedup for 10-minute audio). Whisper can process NumPy arrays directly, eliminating the need for temporary files.
**Action:** Always prefer in-memory streaming/piping for audio processing in Whisper-based apps to avoid disk I/O bottlenecks.

## 2025-01-24 - [Artifact Hygiene]
**Learning:** Committing `__pycache__` or other binary artifacts is a major violation of repository standards and leads to PR rejection.
**Action:** Always ensure `rm -rf __pycache__` is run and verified before final submission.
