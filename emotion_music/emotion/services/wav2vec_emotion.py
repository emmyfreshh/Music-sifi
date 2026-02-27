import logging

logger = logging.getLogger(__name__)

# Keep your model id since you confirmed it has the full label set you need
WAV2VEC_MODEL_ID = "ehcalabres/wav2vec2-lg-xlsr-en-speech-emotion-recognition"

_PIPE = None
_ID2LABEL = None

# Map model labels -> your 8 target emotions:
# happy, sad, neutral, disgust, angry, surprised, fear, calm
LABEL_MAP = {
    "angry": "angry",
    "happy": "happy",
    "sad": "sad",
    "neutral": "neutral",
    "disgust": "disgust",
    "surprised": "surprised",
    "fearful": "fear",
    "calm":"calm",

   
}

def _norm_label(lbl: str) -> str:
    return (lbl or "").strip().lower().replace("_", " ")

def get_pipeline():
    global _PIPE, _ID2LABEL
    if _PIPE is not None:
        return _PIPE

    from transformers import pipeline, AutoModelForAudioClassification, AutoFeatureExtractor

    logger.info("Loading wav2vec2 emotion model: %s", WAV2VEC_MODEL_ID)
    model = AutoModelForAudioClassification.from_pretrained(WAV2VEC_MODEL_ID)
    fe = AutoFeatureExtractor.from_pretrained(WAV2VEC_MODEL_ID)

    _ID2LABEL = (
        {int(k): v for k, v in model.config.id2label.items()}
        if hasattr(model.config, "id2label")
        else None
    )

    _PIPE = pipeline(
        "audio-classification",
        model=model,
        feature_extractor=fe,
        top_k=5,
    )
    return _PIPE

def model_labels():
    get_pipeline()
    if not _ID2LABEL:
        return []
    return sorted(set(_norm_label(v) for v in _ID2LABEL.values()))

def predict_emotion_from_wav(wav_path: str) -> tuple[str, float, str]:
    """
    Returns: (mapped_emotion, confidence, raw_label)
    """
    pipe = get_pipeline()

    import soundfile as sf

    audio, sr = sf.read(wav_path)  # audio: (n,) or (n, channels)
    if hasattr(audio, "ndim") and audio.ndim > 1:
        audio = audio.mean(axis=1)  # mono

    outputs = pipe({"array": audio, "sampling_rate": sr})  # <-- no ffmpeg
    best = max(outputs, key=lambda x: x["score"])

    raw_label = _norm_label(best["label"])
    score = float(best["score"])

    mapped = LABEL_MAP.get(raw_label, "neutral")
    return mapped, score, raw_label