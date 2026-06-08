## 2025-05-14 - [Initial Optimization: In-Memory Audio Pipeline]
**Learning:** The baseline audio pipeline uses disk I/O for both preprocessing (FFmpeg to WAV) and chunking (FFmpeg to multiple WAVs). For a 600s audio file, this takes ~1.23s just for the preprocessing and chunking phase. By using FFmpeg pipes to load raw PCM data directly into a NumPy array and then slicing that array in memory, we can significantly reduce latency and eliminate disk wear.
**Action:** Implement `AudioPreprocessor.preprocess_to_memory` and refactor `WhisperEngine.transcribe_chunks` to use NumPy slicing.
