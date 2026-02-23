# Bolt's Journal - Whisper Transcriber GUI

## 2025-06-25 - Initial Performance Audit
**Learning:** Identified a significant I/O and process overhead bottleneck. The current implementation re-reads and re-encodes the audio file for every chunk using multiple `ffmpeg` calls and temporary disk storage. For a 1-hour file with 3-minute chunks, this results in over 60 redundant file reads and 30 redundant `ffmpeg` process spawns.
**Action:** Implement in-memory audio slicing using numpy arrays. Load the preprocessed audio once and pass slices to Whisper's `transcribe` method. This will eliminate redundant I/O and subprocess overhead.

## 2025-06-25 - Model Caching and Array-based Detection
**Learning:** Whisper model loading is a heavy operation (several seconds on CPU). Re-loading it for every transcription is a major efficiency loss. Also, Whisper methods like `detect_language` can accept numpy arrays directly, avoiding additional file reads if the audio is already in memory.
**Action:** Implemented a module-level `_MODEL_CACHE` and updated `detect_language` to accept numpy arrays. Combined with in-memory slicing, this reduces total audio reads from ~60 to just 2 (initial preprocessing + loading into memory).
