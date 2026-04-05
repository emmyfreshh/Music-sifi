from django.test import TestCase
from emotion_music.emotion.forms import EmotionForm  # Replace with your actual form

class EmotionFormTest(TestCase):
    def test_valid_data(self):
        form = EmotionForm(data={'name': 'sad'})
        self.assertTrue(form.is_valid())