## 2025-06-25 - In-memory Audio Processing for Whisper
**Learning:** Piping FFmpeg output directly to NumPy arrays eliminates the need for temporary WAV files and redundant disk I/O. For short chunks, the overhead of re-opening and re-parsing WAV files with FFmpeg in `whisper.load_audio` (which calls FFmpeg internally) becomes significant relative to the transcription time.
**Action:** Prefer `ffmpeg -f s16le` piped to `np.frombuffer` for audio preprocessing when working with Whisper to keep the entire pipeline in memory.
