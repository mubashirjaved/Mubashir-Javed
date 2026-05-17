# Bolt's Performance Journal ⚡

## 2026-05-17 - Audio Pipeline Optimization
**Learning:** The previous audio pipeline used redundant FFmpeg calls and disk I/O to preprocess and chunk audio files. Preprocessing to a temporary WAV and then chunking it into multiple WAV files adds significant latency, especially on slower storage.
**Action:** Transitioned to a full in-memory pipeline. By piping raw PCM data from FFmpeg directly into a NumPy array, we eliminate all temporary audio files. In-memory slicing for chunks is virtually instantaneous compared to FFmpeg-based segmenting.
**Measurement:** 10-minute audio file preprocessing and chunking time reduced from ~2.1s to ~0.5s (~4x speedup in this phase). Total speedup will be more significant on slower disks. Also fixed a bug where the chunk offset was hardcoded to 180s.
