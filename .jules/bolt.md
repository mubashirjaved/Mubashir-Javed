# Bolt's Performance Journal

## 2026-05-05 - In-memory Audio Pipeline
**Learning:** Transitioning from a file-based audio processing pipeline to an in-memory NumPy-based one yields significant performance gains. For a 10-minute audio file, the initial processing and chunking phase saw a ~2.65x speedup by eliminating redundant disk I/O and FFmpeg subprocess overhead. Even for shorter 60s files, a ~1.74x speedup was observed.
**Action:** Always favor piping FFmpeg output to memory for transcription tasks to avoid the bottleneck of temporary file creation and management.
