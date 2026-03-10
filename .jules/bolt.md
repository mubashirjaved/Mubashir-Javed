## 2025-06-25 - [In-Memory Audio Pipeline Optimization]
**Learning:** The previous implementation used temporary `.wav` files for both preprocessing and chunking, leading to significant disk I/O overhead. By piping raw PCM data (`s16le`) from FFmpeg directly into NumPy arrays and using NumPy slicing for chunking, we eliminate disk latency and multiple redundant FFmpeg calls. This provides a measurable speedup, especially for longer audio files.
**Action:** Always prefer in-memory piping and NumPy array manipulation over temporary file creation for audio/video processing tasks to maximize throughput and minimize resource cleanup logic.

## 2025-06-25 - [Whisper Model Caching]
**Learning:** Loading Whisper models (even `base` or `small`) is a heavy operation that can take several seconds. Repeatedly initializing the engine for different transcription tasks in the same session wastes significant time. Class-level caching of models keyed by `(model_name, device)` ensures models are only loaded once.
**Action:** Implement singleton or class-level caching for heavy machine learning models to ensure near-instantaneous starts on subsequent inference requests.
