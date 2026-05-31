## 2025-05-22 - [In-memory audio processing]
**Learning:** Moving audio chunking from FFmpeg-based disk I/O to in-memory NumPy slicing provides a ~11.5x speedup for the preprocessing/chunking phase on 600s files. It also eliminates the need for managing temporary directories and fixes a latent bug where segment timestamps were hardcoded to 180s offsets regardless of the user-defined chunk size.
**Action:** Prefer piping raw PCM data from FFmpeg to memory for high-performance audio pipelines, and always use dynamic offsets based on actual chunk parameters.
