# Bolt's Performance Journal - Whisper Transcriber GUI

## 2026-05-21 - Initial Environment Setup
**Learning:** The environment requires `static-ffmpeg` for audio processing as system `ffmpeg` is missing.
**Action:** Always initialize `static-ffmpeg` with `from static_ffmpeg import add_paths; add_paths()` in benchmarks and verify its presence before assuming `ffmpeg` works.
