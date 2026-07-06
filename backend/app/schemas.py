from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

# User Schemas
class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True

# Token Schemas
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

# Video Schemas
class VideoResponse(BaseModel):
    id: int
    title: str
    original_filename: str
    target_language: str
    status: str
    error_message: Optional[str]
    created_at: datetime

    # We might not want to expose the raw keys, but URLs instead,
    # which we will generate in the endpoint.
    translated_video_url: Optional[str] = None
    subtitles_url: Optional[str] = None

    class Config:
        from_attributes = True
