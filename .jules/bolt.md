## 2025-05-15 - Initial Assessment
**Learning:** The current transcription pipeline relies heavily on intermediate WAV files and multiple FFmpeg calls for preprocessing and chunking. This introduces significant I/O overhead and redundant decoding.
**Action:** Plan to implement an in-memory audio processing pipeline using FFmpeg pipes and NumPy to eliminate temporary files and streamline the data flow to Whisper.
## 2025-05-15 - In-Memory Audio Pipeline
**Learning:** Transitioning from a disk-based workflow with temporary WAV files to a full in-memory pipeline using FFmpeg pipes and NumPy arrays provides measurable performance gains and reduces I/O pressure.
**Action:** Use FFmpeg's `-f s16le` format to pipe raw PCM data directly to Python's `subprocess.run` stdout for the most efficient data ingestion into NumPy/PyTorch.
