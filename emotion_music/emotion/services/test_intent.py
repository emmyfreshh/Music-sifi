import unittest

from emotion.services.intent import detect_emotion_command


class TestIntentDetection(unittest.TestCase):
    def test_happy_intents(self):
        self.assertEqual(detect_emotion_command("Play happy music"), "happy")
        self.assertEqual(detect_emotion_command("play very happy song"), "happy")
        self.assertEqual(detect_emotion_command("play feeling good"), "happy")

    def test_sad_intents(self):
        self.assertEqual(detect_emotion_command("play melancholy song"), "sad")
        self.assertEqual(detect_emotion_command("play blue music"), "sad")
        self.assertEqual(detect_emotion_command("play I am sad"), "sad")

    def test_calm_variants(self):
        self.assertEqual(detect_emotion_command("play something very calm"), "calm")
        self.assertEqual(detect_emotion_command("play relax playlist"), "calm")
        self.assertEqual(detect_emotion_command("play soothing music"), "calm")

    def test_requires_play_keyword(self):
        self.assertIsNone(detect_emotion_command("I am sad"))
        self.assertIsNone(detect_emotion_command("just relax"))

    def test_unsupported_intent(self):
        self.assertIsNone(detect_emotion_command("play something wild"))


if __name__ == "__main__":
    unittest.main()