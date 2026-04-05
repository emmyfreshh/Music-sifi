import unittest
import os

# Import your prediction function or class from the actual module
from emotion_music.ravdess_wav2vec2_finetuned import predict_emotion

class TestRavdessModel(unittest.TestCase):
    def setUp(self):
        # Setup: point to a few sample audio clips (ensure these exist in your test folder or generate at runtime)
        self.happy_audio = "emotion_music/emotion/test_data/happy.wav"
        self.sad_audio = "emotion_music/emotion/test_data/sad.wav"
        self.calm_audio = "emotion_music/emotion/test_data/calm.wav"

    def test_happy_detection(self):
        if os.path.exists(self.happy_audio):
            result = predict_emotion(self.happy_audio)
            self.assertEqual(result, 'happy')
        else:
            self.skipTest("happy.wav not found")

    def test_sad_detection(self):
        if os.path.exists(self.sad_audio):
            result = predict_emotion(self.sad_audio)
            self.assertEqual(result, 'sad')
        else:
            self.skipTest("sad.wav not found")

    def test_calm_detection(self):
        if os.path.exists(self.calm_audio):
            result = predict_emotion(self.calm_audio)
            self.assertEqual(result, 'calm')
        else:
            self.skipTest("calm.wav not found")

if __name__ == '__main__':
    unittest.main()