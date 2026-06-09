## 2025-05-15 - In-memory Audio Processing Pipeline
**Learning:** Moving from disk-based preprocessing and chunking to an in-memory pipeline using FFmpeg pipes and NumPy slicing significantly reduces latency. Preprocessing and chunking for a 10-minute audio file was reduced from ~2.1s to ~0.18s (~11.5x speedup), and chunking itself became virtually instantaneous.
**Action:** Use FFmpeg pipes to stdout with `f32le` format for direct NumPy loading to avoid intermediate WAV files. Perform audio segmentation using NumPy array slicing for O(1) chunking overhead.
