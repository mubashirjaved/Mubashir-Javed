import unittest
from unittest.mock import MagicMock, patch
import numpy as np
import threading
from whisper_transcriber_gui import WhisperEngine, HardwareProfile, AudioPreprocessor

class TestInMemoryOptimization(unittest.TestCase):
    def setUp(self):
        self.profile = HardwareProfile(
            device="cpu",
            fp16=False,
            torch_threads=4,
            amd_gpu_detected=False,
            notes=[]
        )
        # Mock whisper.load_model to avoid loading the actual model
        with patch('whisper.load_model') as mock_load:
            self.engine = WhisperEngine(self.profile, "tiny")
            self.engine.model = MagicMock()

    def test_transcribe_chunks_slicing(self):
        # Create dummy audio: 10 seconds at 16000Hz
        audio = np.zeros(16000 * 10, dtype=np.float32)
        chunk_seconds = 4

        # We expect 3 chunks: [0:4s], [4:8s], [8:10s]
        expected_chunks = 3

        # Mock transcribe to return a dummy result
        self.engine.model.transcribe.side_effect = lambda audio_chunk, **kwargs: {
            "text": "sample text",
            "segments": [{"start": 0.0, "end": 1.0, "text": "sample text", "avg_logprob": -0.1}]
        }

        stop_event = threading.Event()
        progress_cb = MagicMock()

        result = self.engine.transcribe_chunks(
            audio=audio,
            chunk_seconds=chunk_seconds,
            language="en",
            timestamps=True,
            word_timestamps=False,
            stop_event=stop_event,
            progress_cb=progress_cb
        )

        self.assertEqual(len(result["segments"]), expected_chunks)
        self.assertEqual(self.engine.model.transcribe.call_count, expected_chunks)

        # Verify chunk offsets
        # Chunk 0: offset 0, start 0.0 -> 0.0, end 1.0 -> 1.0
        # Chunk 1: offset 4, start 0.0 -> 4.0, end 1.0 -> 5.0
        # Chunk 2: offset 8, start 0.0 -> 8.0, end 1.0 -> 9.0
        self.assertEqual(result["segments"][0]["start"], 0.0)
        self.assertEqual(result["segments"][1]["start"], 4.0)
        self.assertEqual(result["segments"][2]["start"], 8.0)

        self.assertEqual(result["segments"][0]["end"], 1.0)
        self.assertEqual(result["segments"][1]["end"], 5.0)
        self.assertEqual(result["segments"][2]["end"], 9.0)

    def test_detect_language_input(self):
        audio = np.zeros(16000 * 30, dtype=np.float32)

        with patch('whisper.pad_or_trim', return_value=audio) as mock_pad, \
             patch('whisper.log_mel_spectrogram') as mock_mel:

            mock_mel.return_value.to.return_value = MagicMock()
            self.engine.model.detect_language.return_value = (None, {"en": 0.9, "fr": 0.1})

            lang, confidence = self.engine.detect_language(audio)

            self.assertEqual(lang, "en")
            self.assertAlmostEqual(confidence, 0.9)
            mock_pad.assert_called_once()

if __name__ == "__main__":
    unittest.main()
