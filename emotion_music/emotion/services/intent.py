import re

TARGET_EMOTIONS = ["happy", "sad", "neutral", "disgust", "angry", "surprised", "fear", "calm"]

def normalize(text: str) -> str:
    text = (text or "").lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

def detect_emotion_command(transcript: str) -> str | None:
    t = normalize(transcript)
    if not t:
        return None
    if "play" not in t:
        return None

    for e in TARGET_EMOTIONS:
        if re.search(rf"\b{re.escape(e)}\b", t):
            return e

    # small synonym support
    synonyms = {
        "fearful": "fear",
        "surprise": "surprised",
        "relax": "calm",
        "relaxing": "calm",
        "chill": "calm",
    }
    for k, v in synonyms.items():
        if re.search(rf"\b{re.escape(k)}\b", t):
            return v

    return None