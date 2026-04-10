## 2026-04-10 - In-Memory Pipeline for Audio Processing
**Learning:** Moving from a disk-based FFmpeg pipeline to an in-memory NumPy pipeline significantly reduces transcription overhead. In this project, eliminating redundant FFmpeg subprocesses for chunking and avoiding intermediate `.wav` writes provided a ~68% speedup in the preprocessing/chunking phase.
**Action:** Prioritize FFmpeg pipes (`pipe:1`) and NumPy slicing for audio manipulation instead of temporary files and repeated subprocess calls.
