## 2025-05-22 - [In-memory audio pipeline]
**Learning:** Moving from disk-based temporary file chunking to in-memory NumPy array slicing provides a significant speedup (O(1) slicing vs O(N) disk I/O) and fixes timestamp synchronization issues by allowing dynamic chunk offsets.
**Action:** Use FFmpeg pipes with `-f f32le` and `np.frombuffer` to bridge FFmpeg and NumPy for high-performance audio processing.
