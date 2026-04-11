## 2026-04-11 - In-memory audio processing pipeline
**Learning:** Moving from file-based preprocessing and chunking to a full in-memory pipeline using NumPy and FFmpeg pipes significantly reduces overhead and eliminates redundant disk I/O. For a 60-second audio file, the preprocessing and chunking phase was accelerated by ~3x (0.24s down to 0.08s).
**Action:** Prioritize in-memory data flow for multi-stage media processing pipelines to bypass disk latency.
