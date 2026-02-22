from django.contrib import admin
from .models import Track

@admin.register(Track)
class TrackAdmin(admin.ModelAdmin):
    list_display = ("title", "artist", "emotion", "active")
    list_filter = ("emotion", "active")
    search_fields = ("title", "artist")
