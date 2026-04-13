## 2026-04-13 - In-memory NumPy Pipeline for Whisper

**Learning:** Moving from a disk-based (WAV files) to an in-memory (NumPy) pipeline eliminates significant I/O overhead and redundant FFmpeg calls. For a 10-minute audio file with 30-second chunks, switching to in-memory slicing reduced the initial processing and chunking phase from ~0.90s to ~0.75s, but more importantly, it eliminated the creation of 21 temporary WAV files and over 20 separate FFmpeg calls.

**Action:** Prioritize NumPy-based audio manipulation over intermediate file creation. Use FFmpeg's `s16le` pipe format to load raw data directly into NumPy arrays for efficient slicing and direct consumption by Whisper's `transcribe` function.
