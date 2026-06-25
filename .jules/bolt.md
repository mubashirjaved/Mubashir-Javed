## 2025-05-14 - In-memory Audio Processing Pipeline
**Learning:** The current implementation relies on intermediate disk files for preprocessing and chunking, which introduces significant I/O overhead and redundant FFmpeg subprocess calls.
**Action:** Implement an in-memory pipeline using FFmpeg pipes and NumPy for preprocessing and chunking. Pass NumPy arrays directly to Whisper to eliminate disk I/O.
