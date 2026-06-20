import os
import tempfile
from celery import Celery
from pydub import AudioSegment

from .database import SessionLocal
from .models import Video
from .core.storage import minio_client, BUCKET_NAME, upload_file
from .core.video import extract_audio, create_srt_file, merge_audio_video
from .core.translation import transcribe_audio, translate_text
from .core.tts import generate_tts

REDIS_URL = os.environ.get("REDIS_URL", "redis://localhost:6379/0")

celery_app = Celery(
    "worker",
    broker=REDIS_URL,
    backend=REDIS_URL
)

celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
)

@celery_app.task(bind=True)
def process_video_translation(self, video_id: int):
    db = SessionLocal()
    video = db.query(Video).filter(Video.id == video_id).first()
    if not video:
        db.close()
        return

    try:
        with tempfile.TemporaryDirectory() as temp_dir:
            # 1. Download original video
            original_video_path = os.path.join(temp_dir, "original_video.mp4")
            minio_client.fget_object(BUCKET_NAME, video.original_video_key, original_video_path)

            # 2. Extract Audio
            original_audio_path = os.path.join(temp_dir, "original_audio.wav")
            extract_audio(original_video_path, original_audio_path)

            # 3. Transcribe Audio
            transcription = transcribe_audio(original_audio_path)
            segments = transcription.get("segments", [])
            source_lang = transcription.get("language", "en")
            target_lang = video.target_language

            # 4. Translate Text and Generate TTS for each segment
            translated_audio_path = os.path.join(temp_dir, "translated_audio.wav")
            combined_audio = AudioSegment.silent(duration=0) # start with empty audio

            for segment in segments:
                text = segment["text"]
                # Translate
                translated_text = translate_text(text, source_lang, target_lang)
                segment["translated_text"] = translated_text

                # Generate TTS
                segment_audio_path = os.path.join(temp_dir, f"segment_{segment['id']}.wav")
                generate_tts(translated_text, target_lang, segment_audio_path)

                # Load the TTS audio
                if os.path.exists(segment_audio_path):
                    seg_audio = AudioSegment.from_file(segment_audio_path)

                    # Calculate padding needed to align with original video timing
                    start_ms = int(segment["start"] * 1000)
                    current_dur_ms = len(combined_audio)

                    if start_ms > current_dur_ms:
                        padding = AudioSegment.silent(duration=(start_ms - current_dur_ms))
                        combined_audio += padding

                    combined_audio += seg_audio

            # Export combined translated audio
            combined_audio.export(translated_audio_path, format="wav")

            # 5. Create SRT subtitles file
            srt_path = os.path.join(temp_dir, "subtitles.srt")
            create_srt_file(segments, srt_path)

            # 6. Merge translated audio with original video
            final_video_path = os.path.join(temp_dir, "final_video.mp4")
            merge_audio_video(original_video_path, translated_audio_path, final_video_path)

            # 7. Upload results to MinIO
            translated_video_key = f"{video.owner_id}/{video_id}/translated.mp4"
            subtitles_key = f"{video.owner_id}/{video_id}/subtitles.srt"

            upload_file(translated_video_key, final_video_path)
            upload_file(subtitles_key, srt_path)

            # 8. Update database
            video.translated_video_key = translated_video_key
            video.subtitles_key = subtitles_key
            video.status = "completed"
            db.commit()

    except Exception as e:
        video.status = "failed"
        video.error_message = str(e)
        db.commit()
        print(f"Error processing video {video_id}: {e}")
    finally:
        db.close()
