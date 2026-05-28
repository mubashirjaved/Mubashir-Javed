import math
import os
import queue
import re
import shutil
import subprocess
import threading
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Dict, List, Optional, Tuple

import tkinter as tk
from tkinter import filedialog, messagebox, ttk

import numpy as np
import torch
import whisper

try:
    from deep_translator import GoogleTranslator
except Exception:
    GoogleTranslator = None


SUPPORTED_MODELS = ["tiny", "base", "small", "medium", "large"]
OUTPUT_LANGUAGES = [
    "original",
    "english",
    "urdu",
    "hindi",
    "arabic",
    "french",
    "german",
    "spanish",
    "turkish",
    "chinese",
]
FILLER_WORDS = [
    "uh", "um", "hmm", "erm", "ah", "like", "you know", "i mean",
]


@dataclass
class HardwareProfile:
    device: str
    fp16: bool
    torch_threads: int
    amd_gpu_detected: bool
    notes: List[str]


class HardwareOptimizer:
    @staticmethod
    def detect_amd_gpu() -> Tuple[bool, List[str]]:
        notes = []
        amd_found = False

        if torch.cuda.is_available():
            for idx in range(torch.cuda.device_count()):
                name = torch.cuda.get_device_name(idx)
                notes.append(f"CUDA device {idx}: {name}")
                if "amd" in name.lower() or "radeon" in name.lower():
                    amd_found = True
        else:
            notes.append("torch.cuda not available.")

        if getattr(torch.version, "hip", None):
            amd_found = True
            notes.append(f"ROCm/HIP runtime detected: {torch.version.hip}")

        if shutil.which("rocminfo"):
            try:
                out = subprocess.check_output(["rocminfo"], text=True, stderr=subprocess.STDOUT, timeout=4)
                if "gfx" in out.lower() or "amd" in out.lower():
                    amd_found = True
                    notes.append("rocminfo indicates AMD GPU support.")
            except Exception as exc:
                notes.append(f"rocminfo probe failed: {exc}")

        if shutil.which("clinfo"):
            try:
                out = subprocess.check_output(["clinfo"], text=True, stderr=subprocess.STDOUT, timeout=4)
                if "amd" in out.lower() or "radeon" in out.lower():
                    amd_found = True
                    notes.append("OpenCL reports AMD/Radeon device.")
            except Exception as exc:
                notes.append(f"clinfo probe failed: {exc}")

        return amd_found, notes

    @staticmethod
    def recommend_model(cpu_threads: int, amd_gpu: bool) -> str:
        if amd_gpu and torch.cuda.is_available():
            return "small"
        if cpu_threads <= 4:
            return "tiny"
        if cpu_threads <= 8:
            return "base"
        return "small"

    @staticmethod
    def build_profile(thread_limit: Optional[int] = None) -> HardwareProfile:
        cpu_count = os.cpu_count() or 4
        threads = min(thread_limit or cpu_count, cpu_count)
        torch.set_num_threads(threads)

        amd_gpu, notes = HardwareOptimizer.detect_amd_gpu()

        use_cuda = torch.cuda.is_available()
        fp16 = use_cuda
        device = "cuda" if use_cuda else "cpu"

        if not use_cuda:
            notes.append("Running in CPU mode with fp16=False for stability.")
        elif amd_gpu and not getattr(torch.version, "hip", None):
            notes.append("AMD GPU found but native Whisper CUDA path may be unavailable; using hybrid/CPU-safe path.")

        return HardwareProfile(
            device=device,
            fp16=fp16,
            torch_threads=threads,
            amd_gpu_detected=amd_gpu,
            notes=notes,
        )


class AudioPreprocessor:
    @staticmethod
    def preprocess_to_memory(input_path: str, smart_silence: bool) -> np.ndarray:
        """Preprocesses audio using FFmpeg and returns a NumPy array (float32, 16kHz mono)."""
        silence_filter = ["-af", "silenceremove=stop_periods=-1:stop_duration=0.6:stop_threshold=-45dB"] if smart_silence else []
        cmd = [
            "ffmpeg", "-y", "-hwaccel", "auto", "-i", input_path,
            "-f", "f32le", "-ac", "1", "-ar", "16000",
            *silence_filter,
            "pipe:1",
        ]
        process = subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return np.frombuffer(process.stdout, dtype=np.float32).copy()

    @staticmethod
    def chunk_audio_in_memory(audio: np.ndarray, chunk_seconds: int, sample_rate: int = 16000) -> List[np.ndarray]:
        """Slices a NumPy audio array into chunks of specified duration."""
        chunk_size = chunk_seconds * sample_rate
        if len(audio) <= chunk_size:
            return [audio]

        chunks = []
        for i in range(0, len(audio), chunk_size):
            chunks.append(audio[i : i + chunk_size])
        return chunks



class TextPostProcessor:
    @staticmethod
    def cleanup_text(text: str) -> str:
        pattern = r"\b(" + "|".join(re.escape(w) for w in FILLER_WORDS) + r")\b"
        text = re.sub(pattern, "", text, flags=re.IGNORECASE)
        text = re.sub(r"\b(\w+)(\s+\1\b)+", r"\1", text, flags=re.IGNORECASE)
        text = re.sub(r"\s+", " ", text).strip()
        return text


class WhisperEngine:
    def __init__(self, profile: HardwareProfile, model_name: str):
        self.profile = profile
        self.model_name = model_name
        self.model = whisper.load_model(model_name, device=profile.device)

    def detect_language(self, audio: np.ndarray) -> Tuple[str, float]:
        """Detects the language of the provided NumPy audio array."""
        audio = whisper.pad_or_trim(audio)
        mel = whisper.log_mel_spectrogram(audio).to(self.model.device)
        _, probs = self.model.detect_language(mel)
        lang, confidence = max(probs.items(), key=lambda item: item[1])
        return lang, confidence

    def transcribe_chunks(
        self,
        chunks: List[np.ndarray],
        chunk_seconds: int,
        language: Optional[str],
        timestamps: bool,
        word_timestamps: bool,
        stop_event: threading.Event,
        progress_cb: Callable[[float, str], None],
    ) -> Dict:
        """Transcribes audio chunks from memory and merges results."""
        all_segments = []
        full_text = []

        for idx, chunk in enumerate(chunks):
            if stop_event.is_set():
                raise RuntimeError("Transcription stopped by user.")

            progress_cb(idx / len(chunks), f"Transcribing chunk {idx + 1}/{len(chunks)}")
            result = self.model.transcribe(
                chunk,
                language=language,
                fp16=self.profile.fp16,
                task="transcribe",
                word_timestamps=word_timestamps,
                verbose=False,
                condition_on_previous_text=False,
            )
            chunk_offset = idx * chunk_seconds
            for seg in result.get("segments", []):
                seg = dict(seg)
                seg["start"] = seg.get("start", 0.0) + chunk_offset
                seg["end"] = seg.get("end", 0.0) + chunk_offset
                seg["confidence"] = round(math.exp(seg.get("avg_logprob", -4.0)), 3)
                all_segments.append(seg)
            full_text.append(result.get("text", ""))

        merged_text = " ".join(full_text).strip()
        if not timestamps:
            return {"text": merged_text, "segments": []}
        return {"text": merged_text, "segments": all_segments}


def format_srt(segments: List[Dict]) -> str:
    def ts(sec: float) -> str:
        ms = int((sec - int(sec)) * 1000)
        h = int(sec // 3600)
        m = int((sec % 3600) // 60)
        s = int(sec % 60)
        return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"

    lines = []
    for i, seg in enumerate(segments, 1):
        lines.append(str(i))
        lines.append(f"{ts(seg['start'])} --> {ts(seg['end'])}")
        lines.append(seg.get("text", "").strip())
        lines.append("")
    return "\n".join(lines)


class TranscriberGUI:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Whisper Audio Transcriber (Optimized)")
        self.root.geometry("1050x760")

        self.selected_file = tk.StringVar()
        self.model_var = tk.StringVar(value="base")
        self.detected_lang_var = tk.StringVar(value="Not detected")
        self.input_lang_override_var = tk.StringVar(value="auto")
        self.output_lang_var = tk.StringVar(value="original")
        self.thread_var = tk.IntVar(value=max(2, (os.cpu_count() or 4) - 1))
        self.chunk_var = tk.IntVar(value=180)
        self.timestamps_var = tk.BooleanVar(value=True)
        self.word_timestamps_var = tk.BooleanVar(value=False)
        self.silence_var = tk.BooleanVar(value=True)
        self.cleanup_var = tk.BooleanVar(value=True)
        self.translate_var = tk.BooleanVar(value=False)

        self.log_queue: queue.Queue = queue.Queue()
        self.stop_event = threading.Event()
        self.worker_thread: Optional[threading.Thread] = None
        self.last_result: Optional[Dict] = None

        self._build_ui()
        self._set_recommended_model()
        self.root.after(120, self._pump_logs)

    def _build_ui(self) -> None:
        pad = {"padx": 8, "pady": 6}
        top = ttk.Frame(self.root)
        top.pack(fill="x")

        ttk.Label(top, text="Input file").grid(row=0, column=0, sticky="w", **pad)
        ttk.Entry(top, textvariable=self.selected_file, width=90).grid(row=0, column=1, columnspan=6, sticky="we", **pad)
        ttk.Button(top, text="Browse", command=self.browse_file).grid(row=0, column=7, **pad)

        ttk.Label(top, text="Model").grid(row=1, column=0, sticky="w", **pad)
        ttk.Combobox(top, textvariable=self.model_var, values=SUPPORTED_MODELS, width=10, state="readonly").grid(row=1, column=1, sticky="w", **pad)

        ttk.Label(top, text="Detected language").grid(row=1, column=2, sticky="w", **pad)
        ttk.Label(top, textvariable=self.detected_lang_var).grid(row=1, column=3, sticky="w", **pad)

        ttk.Label(top, text="Input language").grid(row=1, column=4, sticky="w", **pad)
        ttk.Combobox(top, textvariable=self.input_lang_override_var, values=["auto", "en", "ur", "hi", "ar", "fr", "de", "es", "tr", "zh"], width=12, state="readonly").grid(row=1, column=5, sticky="w", **pad)

        ttk.Label(top, text="Output language").grid(row=1, column=6, sticky="w", **pad)
        ttk.Combobox(top, textvariable=self.output_lang_var, values=OUTPUT_LANGUAGES, width=12, state="readonly").grid(row=1, column=7, sticky="w", **pad)

        opts = ttk.LabelFrame(self.root, text="Performance & Features")
        opts.pack(fill="x", padx=8, pady=8)

        ttk.Label(opts, text="CPU threads").grid(row=0, column=0, **pad)
        ttk.Spinbox(opts, from_=1, to=max(1, os.cpu_count() or 8), textvariable=self.thread_var, width=8).grid(row=0, column=1, **pad)

        ttk.Label(opts, text="Chunk seconds").grid(row=0, column=2, **pad)
        ttk.Spinbox(opts, from_=30, to=600, increment=30, textvariable=self.chunk_var, width=8).grid(row=0, column=3, **pad)

        ttk.Checkbutton(opts, text="Timestamps", variable=self.timestamps_var).grid(row=0, column=4, sticky="w", **pad)
        ttk.Checkbutton(opts, text="Word timestamps", variable=self.word_timestamps_var).grid(row=0, column=5, sticky="w", **pad)
        ttk.Checkbutton(opts, text="Smart silence removal", variable=self.silence_var).grid(row=0, column=6, sticky="w", **pad)
        ttk.Checkbutton(opts, text="Text cleanup", variable=self.cleanup_var).grid(row=1, column=4, sticky="w", **pad)
        ttk.Checkbutton(opts, text="Auto-translate output", variable=self.translate_var).grid(row=1, column=5, sticky="w", **pad)

        actions = ttk.Frame(self.root)
        actions.pack(fill="x", padx=8, pady=6)
        ttk.Button(actions, text="Start", command=self.start_transcription).pack(side="left", padx=6)
        ttk.Button(actions, text="Stop", command=self.stop_transcription).pack(side="left", padx=6)
        ttk.Button(actions, text="Copy", command=self.copy_output).pack(side="left", padx=6)
        ttk.Button(actions, text="Save TXT", command=lambda: self.save_output("txt")).pack(side="left", padx=6)
        ttk.Button(actions, text="Save SRT", command=lambda: self.save_output("srt")).pack(side="left", padx=6)

        self.progress = ttk.Progressbar(self.root, orient="horizontal", mode="determinate")
        self.progress.pack(fill="x", padx=8, pady=6)

        self.log_panel = tk.Text(self.root, height=12)
        self.log_panel.pack(fill="both", expand=False, padx=8, pady=4)

        self.output_box = tk.Text(self.root, height=18)
        self.output_box.pack(fill="both", expand=True, padx=8, pady=8)

    def _set_recommended_model(self) -> None:
        profile = HardwareOptimizer.build_profile(self.thread_var.get())
        rec = HardwareOptimizer.recommend_model(profile.torch_threads, profile.amd_gpu_detected)
        self.model_var.set(rec)
        self._log("Recommended model for this hardware: " + rec)
        for note in profile.notes:
            self._log(note)

    def _log(self, msg: str) -> None:
        self.log_queue.put(("log", msg))

    def _set_progress(self, value: float, msg: str) -> None:
        self.log_queue.put(("progress", (value, msg)))

    def _pump_logs(self) -> None:
        try:
            while True:
                event, payload = self.log_queue.get_nowait()
                if event == "log":
                    self.log_panel.insert("end", payload + "\n")
                    self.log_panel.see("end")
                elif event == "progress":
                    value, msg = payload
                    self.progress["value"] = int(value * 100)
                    self.root.title(f"Whisper Audio Transcriber (Optimized) - {msg}")
                elif event == "done":
                    self.progress["value"] = 100
                    self.output_box.delete("1.0", "end")
                    self.output_box.insert("1.0", payload)
                    self.root.title("Whisper Audio Transcriber (Optimized) - Completed")
                elif event == "error":
                    messagebox.showerror("Transcription Error", payload)
                    self.root.title("Whisper Audio Transcriber (Optimized) - Error")
        except queue.Empty:
            pass
        self.root.after(120, self._pump_logs)

    def browse_file(self) -> None:
        path = filedialog.askopenfilename(filetypes=[("Media", "*.wav *.mp3 *.m4a *.mp4 *.mkv *.flac *.aac *.ogg"), ("All", "*.*")])
        if path:
            self.selected_file.set(path)

    def start_transcription(self) -> None:
        if self.worker_thread and self.worker_thread.is_alive():
            messagebox.showwarning("Busy", "Transcription is already running.")
            return

        input_file = self.selected_file.get().strip()
        if not input_file or not Path(input_file).exists():
            messagebox.showerror("Missing file", "Please select a valid input file.")
            return

        self.stop_event.clear()
        self.progress["value"] = 0
        self.worker_thread = threading.Thread(target=self._run_transcription, daemon=True)
        self.worker_thread.start()

    def stop_transcription(self) -> None:
        self.stop_event.set()
        self._log("Stop requested. Finishing current chunk then aborting...")

    def _run_transcription(self) -> None:
        input_file = self.selected_file.get().strip()
        timestamps = self.timestamps_var.get()
        word_ts = self.word_timestamps_var.get()
        thread_limit = self.thread_var.get()
        chunk_seconds = self.chunk_var.get()

        try:
            profile = HardwareOptimizer.build_profile(thread_limit)
            self._log(f"Device={profile.device}, fp16={profile.fp16}, threads={profile.torch_threads}")
            for note in profile.notes:
                self._log(note)

            engine = WhisperEngine(profile, self.model_var.get())

            self._set_progress(0.05, "Preprocessing audio")
            # Optimized: In-memory preprocessing eliminates temporary WAV files
            audio_data = AudioPreprocessor.preprocess_to_memory(input_file, self.silence_var.get())

            self._set_progress(0.12, "Detecting language")
            detected_lang, lang_prob = engine.detect_language(audio_data)
            self.detected_lang_var.set(f"{detected_lang} ({lang_prob:.2f})")
            self._log(f"Detected language={detected_lang} confidence={lang_prob:.2f}")

            language = None if self.input_lang_override_var.get() == "auto" else self.input_lang_override_var.get()
            if language is None:
                language = detected_lang

            self._set_progress(0.2, "Chunking")
            # Optimized: NumPy slicing is significantly faster than FFmpeg segmenting
            chunks = AudioPreprocessor.chunk_audio_in_memory(audio_data, chunk_seconds)
            self._log(f"Prepared {len(chunks)} chunk(s)")

            result = engine.transcribe_chunks(
                chunks=chunks,
                chunk_seconds=chunk_seconds,
                language=language,
                timestamps=timestamps,
                word_timestamps=word_ts,
                stop_event=self.stop_event,
                progress_cb=lambda p, msg: self._set_progress(0.2 + 0.75 * p, msg),
            )

            text = result.get("text", "")
            if self.cleanup_var.get():
                text = TextPostProcessor.cleanup_text(text)

            out_lang = self.output_lang_var.get()
            if self.translate_var.get() and out_lang != "original":
                text = self._translate_text(text, detected_lang, out_lang)

            result["text"] = text
            self.last_result = result
            self._set_progress(1.0, "Done")
            self.log_queue.put(("done", text))
        except Exception as exc:
            self.log_queue.put(("error", str(exc)))

    def _translate_text(self, text: str, source_lang: str, target_lang: str) -> str:
        if target_lang == "english":
            target = "en"
        elif target_lang == "urdu":
            target = "ur"
        elif target_lang == "hindi":
            target = "hi"
        elif target_lang == "arabic":
            target = "ar"
        elif target_lang == "french":
            target = "fr"
        elif target_lang == "german":
            target = "de"
        elif target_lang == "spanish":
            target = "es"
        elif target_lang == "turkish":
            target = "tr"
        elif target_lang == "chinese":
            target = "zh-CN"
        else:
            return text

        if GoogleTranslator is None:
            self._log("deep-translator not installed; skipping translation.")
            return text

        src = "auto" if source_lang == "" else source_lang
        self._log(f"Translating output {src} -> {target}")
        try:
            return GoogleTranslator(source=src, target=target).translate(text)
        except Exception as exc:
            self._log(f"Translation failed: {exc}")
            return text

    def copy_output(self) -> None:
        text = self.output_box.get("1.0", "end").strip()
        if text:
            self.root.clipboard_clear()
            self.root.clipboard_append(text)
            self._log("Output copied to clipboard.")

    def save_output(self, fmt: str) -> None:
        if not self.last_result:
            messagebox.showwarning("No output", "No transcription result available yet.")
            return

        if fmt == "txt":
            path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text", "*.txt")])
            if not path:
                return
            Path(path).write_text(self.last_result.get("text", ""), encoding="utf-8")
            self._log(f"Saved TXT: {path}")
        else:
            segments = self.last_result.get("segments", [])
            if not segments:
                messagebox.showwarning("No timestamps", "Enable timestamps to export SRT.")
                return
            path = filedialog.asksaveasfilename(defaultextension=".srt", filetypes=[("SubRip", "*.srt")])
            if not path:
                return
            Path(path).write_text(format_srt(segments), encoding="utf-8")
            self._log(f"Saved SRT: {path}")


def main() -> None:
    root = tk.Tk()
    app = TranscriberGUI(root)
    del app
    root.mainloop()


if __name__ == "__main__":
    main()
