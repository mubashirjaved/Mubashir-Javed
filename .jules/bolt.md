## 2025-05-15 - [In-memory Pipeline Optimization]
**Learning:** Moving from a file-based pipeline to an in-memory NumPy pipeline with FFmpeg pipes reduced processing time by ~68%. Redundant FFmpeg subprocesses and disk I/O are significant bottlenecks in audio processing.
**Action:** Always prefer streaming data through pipes to memory for intermediate processing steps if the data size fits within reasonable memory limits (~230MB per hour of audio).

## 2025-05-15 - [Repository Hygiene]
**Learning:** Automated tools and quick tests can leave behind binary artifacts like `__pycache__` and `.pyc` files.
**Action:** Explicitly clean up any temporary scripts, test files, and binary artifacts before submission.
