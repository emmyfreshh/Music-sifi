import re

# Centralized mapping of canonical emotion intents to possible synonyms/phrases.
INTENT_SYNONYMS = {
    "happy": [
        "happy", "joyful", "elated", "cheerful", "excited", "blissful", "very happy", "feeling good"
    ],
    "sad": [
        "sad", "unhappy", "down", "melancholy", "depressed", "blue", "gloomy", "tearful"
    ],
    "neutral": [
        "neutral", "fine", "okay", "so so", "average"
    ],
    "disgust": [
        "disgust", "disgusted", "grossed out", "repulsed"
    ],
    "angry": [
        "angry", "mad", "furious", "irate", "annoyed", "pissed off"
    ],
    "surprised": [
        "surprised", "astonished", "amazed", "shocked", "startled", "surprise"
    ],
    "fear": [
        "fear", "fearful", "scared", "afraid", "anxious", "nervous", "terrified"
    ],
    "calm": [
        "calm", "relax", "relaxing", "relaxed", "chill", "soothing", "peaceful", "super calm"
    ],
}

# Build reverse mapping for fast lookup (synonym -> canonical emotion)
REVERSE_SYNONYM_MAP = {}
for intent, synonyms in INTENT_SYNONYMS.items():
    for s in synonyms:
        REVERSE_SYNONYM_MAP[s] = intent

def normalize(text: str) -> str:
    """Lowercases and strips non-alphanumeric characters from text."""
    text = (text or "").lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

def detect_emotion_command(transcript: str) -> str | None:
    """
    Returns the canonical emotion intent (e.g., "happy", "sad")
    if a supported emotion keyword/phrase is found alongside "play" in the transcript.
    """
    t = normalize(transcript)
    if not t or "play" not in t:
        return None

    # Prioritize longer phrases over shorter ones (e.g., "very happy" before "happy")
    synonyms_sorted = sorted(REVERSE_SYNONYM_MAP, key=len, reverse=True)
    for synonym in synonyms_sorted:
        # Use word boundaries for precise matching (supports multi-word phrases)
        if re.search(rf"\b{re.escape(synonym)}\b", t):
            return REVERSE_SYNONYM_MAP[synonym]

    return None