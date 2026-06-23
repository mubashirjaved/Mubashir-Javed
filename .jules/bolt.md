## 2025-06-25 - [In-memory Audio Pipeline Optimization]
**Learning:** Transitioning from disk-based audio chunking (using multiple FFmpeg processes) to an in-memory NumPy pipeline significantly reduces pre-transcription latency. Spawning FFmpeg processes and performing disk I/O for each 30-180s chunk is a major bottleneck compared to NumPy slicing.
**Action:** Use FFmpeg pipes to read raw PCM into NumPy arrays and perform slicing in memory for chunk-based model processing. Ensure audio is normalized to float32 [-1, 1] for Whisper compatibility.
