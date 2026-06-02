# Bolt's Performance Journal - Whisper Audio Transcriber GUI

## 2025-05-15 - Journal Initialization
**Learning:** Initializing the performance journal for the Whisper Audio Transcriber GUI project.
**Action:** Will use this to track critical performance insights and avoid regressions.

## 2025-05-15 - In-Memory Pipeline & Writable Buffers
**Learning:** `np.frombuffer` returns a read-only view of the underlying memory. PyTorch/Whisper requires writable tensors, so calling `.copy()` on the resulting array is necessary to avoid `UserWarning` or potential errors.
**Action:** Always use `.copy()` when converting FFmpeg stdout pipes to NumPy arrays for Whisper.

## 2025-05-15 - Timestamp Offset Logic
**Learning:** Discovered a latent bug where chunk offsets for segments were hardcoded to 180 seconds, causing incorrect timestamps if the user changed the "Chunk seconds" setting.
**Action:** Dynamically calculate `chunk_offset` using the actual `chunk_seconds` parameter.
