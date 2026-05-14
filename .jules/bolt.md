## 2026-05-14 - Full In-Memory Audio Pipeline
**Learning:** Eliminating disk I/O for intermediate audio artifacts (preprocessing and chunking) significantly reduces latency and complexity. Whisper's `transcribe` and `detect_language` methods can handle NumPy arrays directly, making FFmpeg pipes the most efficient way to ingest audio.
**Action:** Always prefer piping raw PCM data from FFmpeg to NumPy when intermediate processing is required, avoiding temporary WAV files and redundant disk reads.
