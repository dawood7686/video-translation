from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    videos = relationship("Video", back_populates="owner")


class Video(Base):
    __tablename__ = "videos"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    original_filename = Column(String)
    target_language = Column(String)

    # Storage keys in MinIO
    original_video_key = Column(String)
    translated_video_key = Column(String, nullable=True)
    subtitles_key = Column(String, nullable=True)

    status = Column(String, default="pending") # pending, processing, completed, failed
    error_message = Column(String, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # ⚡ Bolt Optimization: Add index to owner_id to prevent full table scans
    # when the frontend dashboard polls the /videos/ endpoint for status updates
    owner_id = Column(Integer, ForeignKey("users.id"), index=True)
    owner = relationship("User", back_populates="videos")
