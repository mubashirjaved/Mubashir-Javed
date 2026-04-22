## 2026-04-22 - [In-memory audio pipeline optimization]
**Learning:** Transitioning from disk-based audio preprocessing to an in-memory pipeline using FFmpeg pipes and NumPy array slicing provides a significant performance boost (up to 5x speedup for the preprocessing phase) by eliminating redundant disk I/O and repetitive FFmpeg invocations.
**Action:** Prioritize in-memory processing for media pipelines when data fits comfortably within modern memory limits (e.g., 10 hours of audio @ 16kHz float32 is ~2.3GB).
