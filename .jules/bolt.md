## 2025-05-15 - [In-memory Audio Pipeline Refactor]
**Learning:** Transitioning from disk-based audio chunking (spawning FFmpeg processes per chunk) to an in-memory NumPy pipeline significantly reduces overhead. Chunking becomes a near-instant O(1) array slicing operation.
**Action:** Use FFmpeg to pipe raw PCM data (`f32le`) directly to memory and leverage NumPy for all subsequent signal manipulation and chunking to avoid disk I/O and process-spawning bottlenecks.
