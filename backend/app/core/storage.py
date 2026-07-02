from minio import Minio
from .config import settings
from datetime import timedelta

# Initialize MinIO client
minio_client = Minio(
    settings.MINIO_ENDPOINT,
    access_key=settings.MINIO_ACCESS_KEY,
    secret_key=settings.MINIO_SECRET_KEY,
    secure=False # Set to True if using HTTPS
)

BUCKET_NAME = "videos"

def ensure_bucket_exists():
    try:
        found = minio_client.bucket_exists(BUCKET_NAME)
        if not found:
            minio_client.make_bucket(BUCKET_NAME)
    except Exception as e:
        print(f"Error checking/creating bucket: {e}")

def upload_file(object_name: str, file_path: str):
    ensure_bucket_exists()
    minio_client.fput_object(BUCKET_NAME, object_name, file_path)

def upload_file_stream(object_name: str, file_stream, length: int, content_type: str):
    ensure_bucket_exists()
    minio_client.put_object(
        BUCKET_NAME,
        object_name,
        file_stream,
        length,
        content_type=content_type
    )

def get_presigned_url(object_name: str, expires_minutes: int = 60) -> str:
    try:
        return minio_client.presigned_get_object(
            BUCKET_NAME,
            object_name,
            expires=timedelta(minutes=expires_minutes)
        )
    except Exception:
        return None
