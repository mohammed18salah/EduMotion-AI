import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

from ai_engine import generate_manim_script
from video_engine import generate_video

app = FastAPI(title="EduMotion AI")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class GenerateRequest(BaseModel):
    topic: str
    language: str = "ar"
    duration: int = 8
    style: str = "minimalist"
    voice_enabled: bool = False
    aspect_ratio: str = "16:9"
    
class VideoResponse(BaseModel):
    video_url: str

@app.post("/generate", response_model=VideoResponse)
async def create_video(request: GenerateRequest):
    try:
        script_code = generate_manim_script(request)
        filename = f"scene_{hash(request.topic)}.py"
        video_path = generate_video(script_code, request, filename=filename)
        
        # We will serve the video correctly. Return URL path
        # Using the relative path from the fastapi app
        relative_path = os.path.relpath(video_path, start=os.path.dirname(os.path.abspath(__file__)))
        # Make path web-compatible
        web_path = relative_path.replace(os.path.sep, "/")
        
        return VideoResponse(video_url=f"/video/{web_path}")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/video/{filepath:path}")
async def serve_video(filepath: str):
    file_full_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), os.path.normpath(filepath))
    if not os.path.exists(file_full_path):
         raise HTTPException(status_code=404, detail="Video not found")
    return FileResponse(file_full_path, media_type="video/mp4")

@app.get("/")
async def root():
    return {"status": "success", "message": "EduMotion AI Backend API is running."}
