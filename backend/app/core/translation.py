import whisper
from transformers import pipeline

# Lazy loading of models so they don't block the API thread

whisper_model = None

def get_whisper_model():
    global whisper_model
    if whisper_model is None:
        whisper_model = whisper.load_model("base")
    return whisper_model

def transcribe_audio(audio_path: str):
    """
    Transcribe audio using Whisper.
    Returns the transcription result which contains text and segments with timestamps.
    """
    model = get_whisper_model()
    result = model.transcribe(audio_path)
    return result

# Simple dictionary fallback or we can use transformers pipeline

# Load translation model pipeline (e.g. NLLB or MarianMT)
# Using a small MarianMT model for speed as an example, but we could use NLLB
translation_pipes = {}

def get_translator(source_lang, target_lang):
    # Mapping Whisper lang code to MarianMT if possible, or fallback
    # For a real robust system, nllb-200-distilled-600M is great but heavier.
    # We will just use pipeline for demonstration if the language pair exists.
    model_name = f"Helsinki-NLP/opus-mt-{source_lang}-{target_lang}"
    try:
        if model_name not in translation_pipes:
            translation_pipes[model_name] = pipeline("translation", model=model_name)
        return translation_pipes[model_name]
    except Exception as e:
        print(f"Could not load translator {model_name}: {e}")
        return None

def translate_text(text: str, source_lang: str, target_lang: str) -> str:
    """
    Translate text using huggingface transformers.
    """
    if source_lang == target_lang:
        return text

    translator = get_translator(source_lang, target_lang)
    if translator:
        try:
            res = translator(text)
            return res[0]['translation_text']
        except Exception:
            return text

    # As a fallback, if we cannot translate, just return the text
    return text
