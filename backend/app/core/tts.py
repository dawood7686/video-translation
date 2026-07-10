import edge_tts
import asyncio

# Map standard language codes to edge-tts voice names
# This is a small subset, edge_tts has many more
VOICE_MAPPING = {
    "es": "es-ES-AlvaroNeural",
    "fr": "fr-FR-HenriNeural",
    "de": "de-DE-KillianNeural",
    "it": "it-IT-DiegoNeural",
    "pt": "pt-BR-AntonioNeural",
    "hi": "hi-IN-MadhurNeural",
    "zh": "zh-CN-YunxiNeural",
    "ja": "ja-JP-KeitaNeural",
    "ko": "ko-KR-InJoonNeural",
    "en": "en-US-ChristopherNeural"
}

async def _generate_audio(text: str, voice: str, output_path: str):
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(output_path)

def generate_tts(text: str, target_lang: str, output_path: str):
    """
    Generate Text-to-Speech using edge-tts.
    """
    voice = VOICE_MAPPING.get(target_lang, "en-US-ChristopherNeural") # fallback to english
    asyncio.run(_generate_audio(text, voice, output_path))
