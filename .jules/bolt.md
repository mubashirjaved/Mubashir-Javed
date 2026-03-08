## 2025-06-25 - [In-Memory Audio Pipeline Optimization]
**Learning:** Decoding audio directly to memory via FFmpeg pipes and using NumPy for chunking eliminates disk I/O bottlenecks and redundant decoding processes. For 60-second files, this reduced overhead from multiple FFmpeg calls (preprocess + chunks) to a single call, resulting in a ~22% speedup on CPU. Class-level model caching in `WhisperEngine` is critical to avoid multi-second reloading times across different transcription runs in the same session.
**Action:** Prioritize in-memory NumPy processing for audio tasks. Use FFmpeg with `-f s16le -` to pipe raw data directly into `np.frombuffer`. Implement model caching at the class level for heavy ML models.

## 2025-06-25 - [FFmpeg in Restricted Environments]
**Learning:** In sandboxed or restricted environments where `apt-get` is unavailable, `static-ffmpeg` provides a reliable way to ensure FFmpeg binaries are present.
**Action:** Use `pip install static-ffmpeg` and `from static_ffmpeg import add_paths; add_paths()` as a standard fallback for audio/video processing tasks.
