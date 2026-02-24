import unittest
from unittest.mock import MagicMock, patch
import numpy as np
import whisper
from whisper_transcriber_gui import AudioPreprocessor, WhisperEngine, HardwareProfile

class TestOptimization(unittest.TestCase):
    def test_chunk_audio_slicing(self):
        # 16000 samples per second. 5 seconds total.
        audio = np.zeros(16000 * 5, dtype=np.float32)
        chunk_seconds = 2
        # Expected chunks: [0:32000], [32000:64000], [64000:80000]
        chunks = AudioPreprocessor.chunk_audio(audio, chunk_seconds)
        self.assertEqual(len(chunks), 3)
        self.assertEqual(len(chunks[0]), 16000 * 2)
        self.assertEqual(len(chunks[1]), 16000 * 2)
        self.assertEqual(len(chunks[2]), 16000 * 1)

    @patch("whisper.load_model")
    def test_transcribe_chunks_offset(self, mock_load_model):
        mock_model = MagicMock()
        mock_load_model.return_value = mock_model

        # Mock transcribe result for a single chunk
        mock_model.transcribe.return_value = {
            "text": "Hello",
            "segments": [{"start": 0.5, "end": 1.5, "text": "Hello", "avg_logprob": -0.1}]
        }

        profile = HardwareProfile(device="cpu", fp16=False, torch_threads=1, amd_gpu_detected=False, notes=[])
        engine = WhisperEngine(profile, "tiny")

        chunks = [np.zeros(16000 * 2, dtype=np.float32), np.zeros(16000 * 2, dtype=np.float32)]
        chunk_seconds = 2

        stop_event = MagicMock()
        stop_event.is_set.return_value = False
        progress_cb = MagicMock()

        result = engine.transcribe_chunks(
            chunks=chunks,
            chunk_seconds=chunk_seconds,
            language="en",
            timestamps=True,
            word_timestamps=False,
            stop_event=stop_event,
            progress_cb=progress_cb
        )

        # Two chunks, so segments should be merged with offsets
        self.assertEqual(len(result["segments"]), 2)
        # First chunk segment start should be 0.5
        self.assertEqual(result["segments"][0]["start"], 0.5)
        # Second chunk segment start should be 0.5 + 2.0 = 2.5
        self.assertEqual(result["segments"][1]["start"], 2.5)

if __name__ == "__main__":
    unittest.main()
