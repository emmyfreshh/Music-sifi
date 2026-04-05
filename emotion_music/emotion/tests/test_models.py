from django.test import TestCase
from emotion_music.emotion.models import Emotion  # Replace with your actual model

class EmotionModelTest(TestCase):
    def test_create_emotion(self):
        emotion = Emotion.objects.create(name="happy")
        self.assertEqual(str(emotion), "happy")