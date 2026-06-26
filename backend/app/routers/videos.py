from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from sqlalchemy.orm import Session
from typing import List
import uuid
import os

from .. import models, schemas, database
from .auth import get_current_user
from ..core.storage import upload_file_stream, get_presigned_url
from ..worker import process_video_translation

router = APIRouter()

SUPPORTED_LANGUAGES = {
    "es": "Spanish",
    "fr": "French",
    "de": "German",
    "it": "Italian",
    "pt": "Portuguese",
    "hi": "Hindi",
    "zh": "Chinese",
    "ja": "Japanese",
    "ko": "Korean"
}

@router.get("/languages")
def get_languages():
    return SUPPORTED_LANGUAGES

@router.post("/upload", response_model=schemas.VideoResponse)
def upload_video(
    target_language: str = Form(...),
    file: UploadFile = File(...),
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(database.get_db)
):
    if target_language not in SUPPORTED_LANGUAGES:
        raise HTTPException(status_code=400, detail="Unsupported target language")

    file.file.seek(0, 2)
    file_size = file.file.tell()
    file.file.seek(0)

    # 50MB limit
    if file_size > 50 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="File too large")

    # Sanitize the filename to prevent path traversal
    safe_filename = os.path.basename(file.filename)

    # Generate a unique key for MinIO
    file_extension = safe_filename.split(".")[-1]
    # Ensure extension only contains alphanumeric characters
    file_extension = "".join([c for c in file_extension if c.isalnum()])
    if not file_extension:
        file_extension = "mp4"

    unique_id = str(uuid.uuid4())
    original_video_key = f"{current_user.id}/{unique_id}/original.{file_extension}"

    # Save metadata to DB
    video = models.Video(
        title=safe_filename,
        original_filename=safe_filename,
        target_language=target_language,
        original_video_key=original_video_key,
        owner_id=current_user.id,
        status="pending"
    )
    db.add(video)
    db.commit()
    db.refresh(video)

    # Upload to MinIO
    upload_file_stream(
        original_video_key,
        file.file,
        file_size,
        content_type=file.content_type
    )

    # Update status to processing and trigger Celery task
    video.status = "processing"
    db.commit()

    process_video_translation.delay(video.id)

    return _attach_urls_to_video(video)

@router.get("/", response_model=List[schemas.VideoResponse])
def list_videos(current_user: models.User = Depends(get_current_user), db: Session = Depends(database.get_db)):
    videos = db.query(models.Video).filter(models.Video.owner_id == current_user.id).order_by(models.Video.created_at.desc()).all()
    return [_attach_urls_to_video(v) for v in videos]

@router.get("/{video_id}", response_model=schemas.VideoResponse)
def get_video(video_id: int, current_user: models.User = Depends(get_current_user), db: Session = Depends(database.get_db)):
    video = db.query(models.Video).filter(models.Video.id == video_id, models.Video.owner_id == current_user.id).first()
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")
    return _attach_urls_to_video(video)

from ..core.config import settings

def _attach_urls_to_video(video: models.Video) -> dict:
    video_dict = video.__dict__.copy()
    if video.translated_video_key:
        internal_url = get_presigned_url(video.translated_video_key)
        if internal_url:
             # Replace the internal minio hostname with the public one so it works on host machine
             video_dict["translated_video_url"] = internal_url.replace(
                f"http://{settings.MINIO_ENDPOINT}", settings.MINIO_PUBLIC_ENDPOINT
             )
    if video.subtitles_key:
        internal_url = get_presigned_url(video.subtitles_key)
        if internal_url:
            video_dict["subtitles_url"] = internal_url.replace(
                f"http://{settings.MINIO_ENDPOINT}", settings.MINIO_PUBLIC_ENDPOINT
            )
    return video_dict
