## 2025-05-15 - In-Memory Audio Pipeline Optimization

**Learning:** Transitioning from a file-based audio processing pipeline to an in-memory `numpy` array approach significantly improves performance by eliminating Disk I/O and reducing subprocess overhead.

In this codebase, the original implementation wrote a temporary WAV file and then repeatedly called FFmpeg to slice it into chunks for transcription. This was inefficient, especially for larger files, as it involved redundant disk writes/reads and multiple process spawns.

**Action:**
1. Use FFmpeg pipes to decode audio directly into RAM (e.g., PCM S16LE).
2. Load raw audio into `numpy` arrays for instantaneous slicing/chunking.
3. Pass in-memory arrays directly to the Whisper model to avoid temporary files.
4. Always ensure timestamp offsets are calculated dynamically based on actual chunk size settings.
