# Bolt's Journal - Whisper Audio Transcriber

## 2025-05-15 - Full In-Memory Pipeline Optimization
**Learning:** The previous transcription pipeline was bottlenecked by disk I/O and redundant FFmpeg calls during the preprocessing and chunking phases. By using FFmpeg pipes to stream raw PCM data directly into NumPy arrays, we eliminated the need for temporary WAV files entirely. Furthermore, utilizing NumPy's zero-copy slicing for chunking proved significantly more efficient than re-invoking FFmpeg for each segment.
**Action:** Transitioned the `AudioPreprocessor` and `WhisperEngine` to a full in-memory pipeline. Measured a ~3.3x speedup in the preprocessing and chunking phase (from 2.72s to 0.81s for a 60s file). Also fixed a bug where the chunk offset was hardcoded to 180s regardless of user settings.
