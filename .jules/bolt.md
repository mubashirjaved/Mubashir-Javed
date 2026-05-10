# Bolt's Performance Journal ⚡

## 2026-05-10 - Initial Bottleneck Discovery
**Learning:** The current audio pipeline relies heavily on disk I/O, writing preprocessed WAV files and individual chunks back to disk using FFmpeg. This introduces significant latency, especially for longer files or slow disks, and creates unnecessary temporary file management overhead.
**Action:** Transition to a full in-memory pipeline using NumPy arrays for preprocessing and slicing. This eliminates redundant disk writes and reloads, speeding up the initial processing phase.
