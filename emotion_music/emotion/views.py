import os
import tempfile

from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login

from .models import Track
from .services.intent import detect_emotion_command
from .services.wav2vec_emotion import predict_emotion_from_wav, model_labels
from .forms import SignUpForm

def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("/")
    else:
        form = SignUpForm()

    return render(request, "registration/signup.html", {"form": form})

@login_required
def index(request):
    return render(request, "emotion/index.html")

@login_required
def api_model_labels(request):
    return JsonResponse({"labels": model_labels()})

@login_required
@csrf_exempt
def api_analyze(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST required"}, status=405)

    transcript = request.POST.get("transcript", "")
    emotion_from_cmd = detect_emotion_command(transcript)

    audiofile = request.FILES.get("audio")
    if not audiofile:
        return JsonResponse({"error": "audio file missing"}, status=400)

    suffix = os.path.splitext(audiofile.name)[1] or ".wav"
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        for chunk in audiofile.chunks():
            tmp.write(chunk)
        wav_path = tmp.name

    try:
        if emotion_from_cmd:
            emotion = emotion_from_cmd
            confidence = 1.0
            mode = "keyword"
            raw_label = "keyword"
        else:
            emotion, confidence, raw_label = predict_emotion_from_wav(wav_path)
            mode = "ml"

        qs = Track.objects.filter(active=True, emotion=emotion).order_by("id")[:30]
        tracks = [
            {
                "id": t.id,
                "title": t.title,
                "artist": t.artist,
                "emotion": t.emotion,
                "url": f"/media/{t.file.name}",
            }
            for t in qs
        ]

        return JsonResponse(
            {
                "transcript": transcript,
                "mode": mode,
                "emotion": emotion,
                "confidence": round(float(confidence), 4),
                "raw_label": raw_label,
                "track_count": len(tracks),
                "tracks": tracks,
            }
        )
    finally:
        try:
            os.remove(wav_path)
        except Exception:
            pass