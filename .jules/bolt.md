## 2025-05-15 - In-memory Audio Pipeline with FFmpeg Pipes
**Learning:** Piping FFmpeg stdout (`f32le`) directly into a NumPy array using `np.frombuffer` is significantly faster than disk-based preprocessing and chunking (~1.6x-2.0x total pre-transcription speedup). However, `np.frombuffer` returns a read-only view of the buffer.
**Action:** Always use `.copy()` on the resulting NumPy array to ensure the buffer is writable, as Whisper and PyTorch often require mutable arrays for processing.

## 2025-05-15 - FFmpeg Hardware Acceleration in Pipes
**Learning:** Including `-hwaccel auto` in FFmpeg commands when piping to memory helps leverage hardware decoding, but the bottleneck in the preprocessing phase is often the pipe overhead and NumPy conversion rather than just decoding.
**Action:** Keep `-hwaccel auto` for stability and potential gain on supported systems, even when streaming to pipes.
