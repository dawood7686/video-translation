from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine, Base
from .routers import auth, videos

# Create DB tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Video Translator API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"], # Next.js frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(videos.router, prefix="/api/videos", tags=["videos"])

@app.get("/")
def read_root():
    return {"message": "Welcome to Video Translator API"}
