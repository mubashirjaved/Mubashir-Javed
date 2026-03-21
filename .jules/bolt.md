## 2026-03-21 - [In-Memory Audio Processing Pipeline]
**Learning:** File-based audio preprocessing and chunking using multiple FFmpeg calls and temporary WAV files introduce significant I/O overhead and redundant decoding. Piping raw PCM data directly from FFmpeg to NumPy arrays reduces this overhead.
**Action:** Always prefer in-memory FFmpeg pipes (`-f s16le -`) for preprocessing short to medium audio clips (up to several hours on 32GB RAM systems) to gain ~50-70% speedup in the preprocessing/chunking phase.
