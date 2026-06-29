## 2025-01-24 - [In-memory Audio Pipeline with FFmpeg Pipes]
**Learning:** Transitioning from disk-based intermediate WAV chunks to an in-memory NumPy pipeline significantly reduces pre-transcription latency. Using FFmpeg pipes (`-f s16le -`) allows for streaming raw PCM data directly into NumPy arrays, enabling O(1) chunking via array slicing instead of spawning multiple FFmpeg processes for disk I/O.
**Action:** Prefer in-memory piping and NumPy slicing for audio processing tasks involving multiple chunks to eliminate redundant disk I/O and process overhead.

## 2025-01-24 - [Avoid Committing Bytecode]
**Learning:** Compiled Python bytecode (`__pycache__`) can be accidentally included in patches if not explicitly cleared, violating repository hygiene.
**Action:** Always run `find . -name "__pycache__" -type d -exec rm -rf {} +` before finalizing a submission.
