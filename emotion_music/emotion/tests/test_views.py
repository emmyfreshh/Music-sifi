from django.test import TestCase
from django.urls import reverse

class EmotionViewsTest(TestCase):
    def test_home_view_status(self):
        response = self.client.get(reverse('home'))  # Replace 'home' with your view's name
        self.assertEqual(response.status_code, 200)