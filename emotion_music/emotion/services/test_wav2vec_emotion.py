import unittest
import os

from emotion.services.wav2vec_emotion import predict_emotion_from_wav

class TestWav2VecRavdessModel(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Map target labels to corresponding test audio files.
        cls.test_audio_files = {
            "happy": "emotion_music/emotion/test_data/happy.wav",
            "sad": "emotion_music/emotion/test_data/sad.wav",
            "calm": "emotion_music/emotion/test_data/calm.wav",
            "angry": "emotion_music/emotion/test_data/angry.wav",
            "fear": "emotion_music/emotion/test_data/fear.wav",
            "neutral": "emotion_music/emotion/test_data/neutral.wav",
            "surprised": "emotion_music/emotion/test_data/surprised.wav",
            "disgust": "emotion_music/emotion/test_data/disgust.wav",
        }

    def _test_audio_prediction(self, emotion):
        path = self.test_audio_files[emotion]
        if os.path.exists(path):
            pred, score, raw_label = predict_emotion_from_wav(path)
            self.assertEqual(pred, emotion, f"For {emotion}.wav, got prediction: {pred}, model raw label: {raw_label}, confidence: {score:.2f}")
        else:
            self.skipTest(f"{emotion}.wav test file is missing")

    def test_happy(self):
        self._test_audio_prediction("happy")

    def test_sad(self):
        self._test_audio_prediction("sad")

    def test_calm(self):
        self._test_audio_prediction("calm")

    def test_angry(self):
        self._test_audio_prediction("angry")

    def test_fear(self):
        self._test_audio_prediction("fear")

    def test_neutral(self):
        self._test_audio_prediction("neutral")

    def test_surprised(self):
        self._test_audio_prediction("surprised")

    def test_disgust(self):
        self._test_audio_prediction("disgust")

    def test_invalid_file(self):
        """Ensure that a missing file raises an error."""
        with self.assertRaises(Exception):
            predict_emotion_from_wav("emotion_music/emotion/test_data/does_not_exist.wav")

if __name__ == "__main__":
    unittest.main()