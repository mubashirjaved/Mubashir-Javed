## 2026-04-25 - In-Memory Audio Pipeline Optimization

**Learning:** The previous file-based audio processing pipeline had significant overhead due to redundant disk I/O and multiple FFmpeg process spawns. By switching to an in-memory pipeline using FFmpeg pipes and NumPy arrays, the preprocessing and chunking phase was sped up by approximately 2x for a 10-minute audio file.

**Action:** Always consider using pipes for inter-process communication with tools like FFmpeg to avoid disk latency and temporary file management overhead. Use NumPy for efficient in-memory audio manipulation like slicing and chunking.
