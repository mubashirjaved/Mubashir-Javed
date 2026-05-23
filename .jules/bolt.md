## 2026-05-23 - In-memory pipeline optimization
**Learning:** Moving from a disk-based preprocessing/chunking pipeline to an in-memory NumPy slicing pipeline eliminates redundant FFmpeg calls and disk I/O, resulting in significant speedups (e.g., reducing 1-minute audio prep/chunk from ~0.22s to ~0.12s). It also simplifies the architecture by removing the need for temporary directories and files.
**Action:** Prioritize FFmpeg pipes (`-f f32le`) and NumPy for audio manipulation instead of intermediate WAV files.

## 2026-05-23 - Whisper detect_language memory input
**Learning:** Whisper's `detect_language` and `transcribe` methods can accept NumPy arrays directly, which perfectly complements the in-memory FFmpeg pipe approach.
**Action:** Pass NumPy arrays directly to Whisper engine methods to avoid unnecessary disk reads.
