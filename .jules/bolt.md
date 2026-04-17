# Bolt's Journal - Critical Learnings Only

## 2026-04-17 - In-memory Audio Pipeline vs Disk-based Chunking
**Learning:** Spawning FFmpeg processes for each chunk and writing/reading temporary WAV files introduces significant latency. For a 60s file, ~75% of preprocessing time was just I/O overhead. Whisper can ingest NumPy arrays directly, allowing for O(1) chunking via NumPy slicing.
**Action:** Always prioritize piping raw PCM from FFmpeg to memory for audio tasks rather than using intermediate files if the data fits in RAM (e.g., ~230MB per hour of 16kHz audio).
