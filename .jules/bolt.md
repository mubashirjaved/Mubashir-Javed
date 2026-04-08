# Bolt's Performance Journal ⚡

## 2026-04-08 - Disk I/O and Redundant FFmpeg Bottleneck
**Learning:** The current pipeline performs multiple disk writes and reads (preprocessing to WAV, then chunking to multiple WAVs, then Whisper loading those WAVs). Additionally, calling FFmpeg for each chunk separately is extremely inefficient for long audio files due to process invocation overhead.
**Action:** Transition to a full in-memory pipeline using NumPy. Preprocess once into a NumPy array using FFmpeg's pipe, then use NumPy slicing for instantaneous zero-copy chunking.

## 2026-04-08 - In-memory pipeline optimization results
**Learning:** Transitioning from a file-based pipeline to an in-memory NumPy pipeline significantly reduces overhead.
**Impact:**
- Chunking is now instantaneous (0.0000s for 20 chunks vs 1.0468s previously).
- Redundant disk I/O eliminated.
- Overall preprocessing + chunking phase is ~1.52s (total) for 10m audio, which is primarily the single-pass FFmpeg run.
- Dynamic chunk size support added to transcription offsets.
