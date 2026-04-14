## 2026-04-14 - In-memory Audio Pipeline with FFmpeg and NumPy
**Learning:** Moving from a file-based chunking strategy to an in-memory NumPy slicing pipeline eliminates significant I/O overhead. Specifically, FFmpeg pipes combined with `np.frombuffer` provide a ~10x speedup for the initial audio loading and chunking phase compared to repeated `ffmpeg` calls and disk reads.
**Action:** Always prefer in-memory NumPy array slicing over temporary WAV file chunking for Whisper-based projects to reduce latency and eliminate file system clutter.
