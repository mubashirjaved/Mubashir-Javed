## 2026-04-04 - [In-Memory Audio Pipeline Performance]
**Learning:** Piping raw PCM (s16le) data from FFmpeg directly into a NumPy array eliminates significant disk I/O overhead and temporary WAV file creation. Benchmarking showed a ~70% reduction in total pipeline time (7.09s to 2.22s) for a 60-second audio file. Additionally, in-memory slicing for chunking is essentially instantaneous compared to FFmpeg-based file segmenting.
**Action:** Always prefer streaming from subprocess pipes into memory for small-to-medium datasets (< 1GB) instead of intermediate files.
