## 2026-04-03 - In-memory Audio Pipeline Optimization
**Learning:** Transitioning from a disk-based preprocessing and chunking pipeline (multiple FFmpeg calls writing WAV files) to an in-memory NumPy pipeline (single FFmpeg pipe to PCM) yields a measurable 20-30% speedup for short audio files (60s). This is achieved by eliminating disk I/O and process spawning overhead. Furthermore, in-memory chunking via array slicing is instantaneous compared to FFmpeg's seek-and-extract operations.
**Action:** Prioritize in-memory data flows for processing tasks where the data size (e.g., PCM audio at 16kHz) is manageable within typical RAM limits (e.g., ~230MB per hour of audio).

## 2026-04-03 - Chronicling Accuracy in Chunked Transcription
**Learning:** When transcribing in chunks, global chronological accuracy depends on correctly adding the `chunk_offset` to both segment-level and word-level (if enabled) timestamps. A previously hardcoded 180s offset in the codebase was a significant bottleneck/bug for flexible chunk sizes.
**Action:** Always derive offsets dynamically from the current chunking parameters to ensure metadata remains synchronized across the full output.
