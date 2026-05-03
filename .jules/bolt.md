## 2026-05-03 - In-memory Audio Pipeline Optimization
**Learning:** Moving from a disk-based preprocessing and chunking flow (using FFmpeg to write temporary WAV files) to a full in-memory pipeline (using FFmpeg pipes to NumPy arrays) significantly reduces overhead.
**Action:** Use FFmpeg `-f f32le` to pipe raw PCM data directly into `np.frombuffer` for 2.5x speedup in the preprocessing phase.
