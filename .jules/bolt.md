## 2025-05-14 - [In-memory audio processing pipeline]
**Learning:** Disk I/O and redundant FFmpeg calls for chunking are significant bottlenecks in the preprocessing phase of Whisper transcription.
**Action:** Implement an in-memory pipeline using FFmpeg pipes and NumPy slicing to eliminate intermediate files and reduce processing time.
