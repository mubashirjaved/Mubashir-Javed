# Whisper Audio Transcriber GUI (Hardware-Optimized)

Production-ready Tkinter GUI transcriber using OpenAI Whisper, optimized for Ryzen 3 3300U + Vega 6-class systems with fast CPU fallback and optional translation.

## Features

- Fast pipeline with preprocessing (`16kHz` mono), chunking, and CPU-thread tuning.
- Hardware probe for AMD GPU / ROCm / OpenCL and stable fallback to CPU (`fp16=False`).
- Dynamic model selection (`tiny`, `base`, `small`, `medium`, `large`) with auto recommendation.
- Automatic language detection + manual input-language override.
- Output language picker + optional auto-translation.
- Mixed-language speech handling (Urdu + English works through Whisper language detection/transcription flow).
- Optional timestamps + word timestamps.
- Smart silence removal (FFmpeg `silenceremove`).
- Basic text cleanup (filler words + repetition reduction).
- Segment-level confidence approximation using `exp(avg_logprob)`.
- GUI controls for start/stop, progress bar, logs, copy, TXT save, and SRT save.

## Requirements

- Python 3.10+
- `ffmpeg` + `ffprobe` available in PATH
- Whisper models already local (as you stated)

Install Python dependencies:

```bash
pip install -r requirements.txt
```

## Run

```bash
python whisper_transcriber_gui.py
```

## How language/output works

1. Tool auto-detects spoken language from preprocessed audio.
2. You can keep **Input language = auto** or force a language manually.
3. Choose output language:
   - `original`: keep transcript language
   - any listed target language: enable **Auto-translate output** to translate
4. If translator package/API fails, tool logs the issue and returns original transcript.

## Performance guidance for your Ryzen 3 3300U + 32GB RAM + Vega 6

- Start with `tiny` or `base` for fastest turnaround.
- `small` is usable for better quality if latency is acceptable.
- Use chunk size `120-180s` to balance speed and memory.
- Keep CPU threads around `3-4` for responsive desktop usage, `6-8` for max throughput.
- Keep smart silence removal enabled for speech-heavy files with long pauses.
- Enable word timestamps only when needed (it adds overhead).
- Translation is network/service dependent; disable for fastest offline path.

## Notes on AMD Vega 6 acceleration

Whisper official Python package is primarily optimized for CUDA paths. This tool:
- Detects AMD-related runtime hints (HIP/ROCm/OpenCL tools)
- Uses GPU where supported by local PyTorch runtime
- Falls back safely to optimized CPU execution when full acceleration is not available

This ensures stable production behavior on your hardware.
