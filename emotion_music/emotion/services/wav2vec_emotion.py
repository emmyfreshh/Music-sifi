import logging

logger = logging.getLogger(__name__)

# NEW: use local fine-tuned model stored in emotion_music/models/...
from pathlib import Path
BASE_DIR = Path(__file__).resolve()   # -> emotion_music/
LOCAL_MODEL_DIR = BASE_DIR / "ravdess_wav2vec2_finetuned"   # Adjust if your model is in a different subdirectory
WAV2VEC_MODEL_ID = str(LOCAL_MODEL_DIR)

_PIPE = None
_ID2LABEL = None

# With a fine-tuned model, labels should already match your target set.
TARGET = {"angry", "calm", "disgust", "fear", "happy", "neutral", "sad", "surprised"}

def _norm_label(lbl: str) -> str:
    return (lbl or "").strip().lower().replace("_", " ")

def get_pipeline():
    global _PIPE, _ID2LABEL
    if _PIPE is not None:
        return _PIPE

    from transformers import pipeline, AutoModelForAudioClassification, AutoFeatureExtractor

    logger.info("Loading fine-tuned wav2vec2 emotion model from: %s", WAV2VEC_MODEL_ID)
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
    Returns: (predicted_emotion, confidence, raw_label)
    """
    pipe = get_pipeline()

    import soundfile as sf

    audio, sr = sf.read(wav_path)
    if hasattr(audio, "ndim") and audio.ndim > 1:
        audio = audio.mean(axis=1)

    outputs = pipe({"array": audio, "sampling_rate": sr})
    best = max(outputs, key=lambda x: x["score"])

    raw_label = _norm_label(best["label"])
    score = float(best["score"])

    pred = raw_label if raw_label in TARGET else "neutral"
    return pred, score, raw_label