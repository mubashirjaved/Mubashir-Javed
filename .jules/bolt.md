## 2025-05-15 - Redundant FFmpeg decodes in Whisper pipelines
**Learning:** Standard Whisper pipelines often call `whisper.load_audio` (which spawns FFmpeg) for every chunk if using file-based chunking. This introduces significant overhead from subprocess spawning and repeated decoding.
**Action:** Load audio into a NumPy array ONCE using `whisper.load_audio` and use array slicing for chunking and language detection to eliminate redundant I/O and decodes.
