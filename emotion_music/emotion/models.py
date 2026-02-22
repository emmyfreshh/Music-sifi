from django.db import models

class Track(models.Model):
    EMOTIONS = [
        ("happy", "happy"),
        ("sad", "sad"),
        ("neutral", "neutral"),
        ("disgust", "disgust"),
        ("angry", "angry"),
        ("surprised", "surprised"),
        ("fearful", "fearful"),
        ("calm", "calm"),

    ]

    title = models.CharField(max_length=200)
    artist = models.CharField(max_length=200, blank=True)
    file = models.FileField(upload_to="tracks/")
    emotion = models.CharField(max_length=20, choices=EMOTIONS)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.title} ({self.emotion})"
