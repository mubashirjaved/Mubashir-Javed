## 2025-06-25 - [In-memory pipeline and Model caching]
**Learning:** The in-memory processing pipeline significantly reduces transcription overhead by eliminating redundant FFmpeg calls and disk I/O, providing a consistent ~20% speedup for standard audio lengths. Model caching at the class level eliminates multi-second loading times on repeated tasks.
**Action:** Always prioritize in-memory NumPy/FFmpeg pipes for audio processing to avoid I/O bottlenecks. Use class-level caches for heavy model objects in GUI apps.
