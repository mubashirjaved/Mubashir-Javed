## 2026-04-21 - In-memory FFmpeg piping vs file-based chunking
**Learning:** Transitioning from a multi-process, file-based chunking strategy (spawning FFmpeg for every 120s-180s chunk) to a single-process in-memory decoding pipeline (using FFmpeg pipes and NumPy) reduced preprocessing and chunking overhead by ~50% for 60s files. In-memory slicing in NumPy is essentially instantaneous, unlike FFmpeg-based file extraction.
**Action:** Always evaluate if third-party binaries (FFmpeg, Magick, etc.) can pipe raw data to stdout for consumption in memory to avoid disk I/O and redundant process initialization overhead.

## 2026-04-21 - Pylint and PEP 8 whitespace sensitivity
**Learning:** In this project, maintaining a 10/10 Pylint score requires strict adherence to PEP 8 whitespace rules (e.g., exactly 2 blank lines between classes). Aggressive removal of whitespace for "conciseness" can drop scores and flag readability issues in code reviews.
**Action:** Use a script or formatter to ensure PEP 8 spacing is maintained after refactoring to keep linting clean and avoid "stylistic churn" feedback.
