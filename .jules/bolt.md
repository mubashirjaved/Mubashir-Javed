## 2026-05-25 - In-memory Audio Processing Pipeline
**Learning:** Transitioning from disk-based temporary WAV chunks to an in-memory `numpy` pipeline significantly reduces I/O overhead and FFmpeg startup latency. In-memory slicing with `numpy` is virtually instantaneous (0.00s) compared to FFmpeg-based file segmenting (~0.23s for 1 min).
**Action:** Prioritize in-memory data pipelines over temporary files whenever the dataset (e.g., audio samples) fits within reasonable RAM limits (approx 230MB/hour for 16kHz float32).

## 2026-05-25 - Whisper Engine Direct Array Input
**Learning:** Whisper's `transcribe` and `detect_language` methods can accept raw `numpy` arrays directly. This avoids redundant disk I/O and `whisper.load_audio` calls, which internally use FFmpeg pipes anyway.
**Action:** Pass `numpy` arrays directly to Whisper methods to streamline the processing pipeline.
