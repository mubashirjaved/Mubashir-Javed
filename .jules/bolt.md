## 2026-03-29 - In-memory Audio Pipeline Optimization
**Learning:** Moving from a file-based pipeline to an in-memory NumPy pipeline for Whisper significantly reduces pre-transcription overhead (benchmarked ~35-60% improvement for 60s audio). Key savings come from avoiding redundant FFmpeg process spawns and disk I/O for chunking and language detection.
**Action:** Always prefer piping raw PCM data from FFmpeg to memory when the full audio can fit in RAM (10 hours at 16kHz mono float32 is only ~2.3GB).

**Learning:** `subprocess.run` cannot use `capture_output=True` if `stderr` is also redirected to `subprocess.DEVNULL` (or any other pipe).
**Action:** Use `stdout=subprocess.PIPE` explicitly when manual `stderr` redirection is required.

**Learning:** Whisper's `detect_language` and `transcribe` can accept raw NumPy arrays (float32, normalized to [-1, 1]), which is more efficient than passing file paths that force internal `load_audio` calls (re-spawning FFmpeg).
**Action:** Pre-load audio once and pass the NumPy array to Whisper methods to eliminate redundant loading.
