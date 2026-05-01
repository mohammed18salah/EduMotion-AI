import os
import hashlib
import time
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel, field_validator
from dotenv import load_dotenv

# ─── Fix for Windows asyncio ConnectionResetError ───────────────────────────
import sys
if sys.platform == "win32":
    import asyncio
    from functools import wraps
    from asyncio.proactor_events import _ProactorBasePipeTransport
    
    def silence_connection_reset(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            try:
                return func(self, *args, **kwargs)
            except RuntimeError as e:
                if str(e) != 'Event loop is closed':
                    raise
            except ConnectionResetError:
                pass
        return wrapper

    if hasattr(_ProactorBasePipeTransport, '_call_connection_lost'):
        _ProactorBasePipeTransport._call_connection_lost = silence_connection_reset(_ProactorBasePipeTransport._call_connection_lost)
    _ProactorBasePipeTransport.__del__ = silence_connection_reset(_ProactorBasePipeTransport.__del__)

load_dotenv()

from ai_engine import generate_manim_script
from video_engine import generate_video

# ─── App ──────────────────────────────────────────────────────────────────
app = FastAPI(
    title="EduMotion AI",
    docs_url=None,   # Disable Swagger in production (security)
    redoc_url=None,
)

# ─── CORS — allow all for hackathon ───────────────────────────────────────
ALLOWED_ORIGINS = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=False,          # No credentials needed
    allow_methods=["GET", "POST"],    # Only what we use
    allow_headers=["Content-Type"],
)

# ─── Security headers middleware ──────────────────────────────────────────
@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    # Cache-Control for API responses (not videos)
    if not request.url.path.startswith("/video"):
        response.headers["Cache-Control"] = "no-store"
    return response

# ─── In-Memory Video Cache ────────────────────────────────────────────────
# Key: SHA-256 hash of (topic + settings), Value: {url, expires_at}
_video_cache: dict[str, dict] = {}
CACHE_TTL = int(os.getenv("CACHE_TTL_SECONDS", "3600"))  # default 1 hour

def _cache_key(request) -> str:
    """Deterministic hash of all request parameters."""
    raw = f"{request.topic}|{request.language}|{request.duration}|{request.style}|{request.aspect_ratio}|{request.voice_enabled}|{request.voice_gender}"
    return hashlib.sha256(raw.encode()).hexdigest()[:16]

def _cache_get(key: str) -> str | None:
    entry = _video_cache.get(key)
    if entry and time.time() < entry["expires_at"]:
        return entry["url"]
    if entry:
        del _video_cache[key]   # expired
    return None

def _cache_set(key: str, url: str):
    _video_cache[key] = {"url": url, "expires_at": time.time() + CACHE_TTL}

def _cache_evict_expired():
    """Remove all expired entries."""
    now = time.time()
    expired = [k for k, v in _video_cache.items() if now >= v["expires_at"]]
    for k in expired:
        del _video_cache[k]

# ─── Request Model — with validation ──────────────────────────────────────
VALID_STYLES  = {"minimalist", "neon", "colorful", "chalkboard"}
VALID_ASPECTS = {"16:9", "9:16"}
VALID_GENDERS = {"female", "male"}
VALID_LANGS   = {"ar", "en"}

class GenerateRequest(BaseModel):
    topic: str
    language: str = "en"
    duration: int = 15
    style: str = "minimalist"
    voice_enabled: bool = False
    voice_gender: str = "female"
    aspect_ratio: str = "16:9"

    @field_validator("topic")
    @classmethod
    def topic_not_empty(cls, v):
        v = v.strip()
        if not v:
            raise ValueError("topic cannot be empty")
        if len(v) > 500:
            raise ValueError("topic too long (max 500 chars)")
        return v

    @field_validator("duration")
    @classmethod
    def duration_in_range(cls, v):
        if not (5 <= v <= 120):
            raise ValueError("duration must be between 5 and 120 seconds")
        return v

    @field_validator("style")
    @classmethod
    def style_valid(cls, v):
        if v not in VALID_STYLES:
            raise ValueError(f"style must be one of {VALID_STYLES}")
        return v

    @field_validator("aspect_ratio")
    @classmethod
    def aspect_valid(cls, v):
        if v not in VALID_ASPECTS:
            raise ValueError(f"aspect_ratio must be one of {VALID_ASPECTS}")
        return v

    @field_validator("voice_gender")
    @classmethod
    def gender_valid(cls, v):
        if v not in VALID_GENDERS:
            return "female"
        return v

    @field_validator("language")
    @classmethod
    def lang_valid(cls, v):
        if v not in VALID_LANGS:
            return "en"
        return v

class VideoResponse(BaseModel):
    video_url: str
    cached: bool = False

# ─── Routes ────────────────────────────────────────────────────────────────
@app.post("/generate", response_model=VideoResponse)
async def create_video(request: GenerateRequest):
    # 1. Check cache first
    cache_key = _cache_key(request)
    cached_url = _cache_get(cache_key)
    if cached_url:
        print(f"[cache] HIT for key {cache_key}")
        return VideoResponse(video_url=cached_url, cached=True)

    _cache_evict_expired()   # housekeeping

    try:
        # 2. Generate
        script_code, voice_text = generate_manim_script(request)
        
        # Ensure scenes dir exists
        scenes_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "scenes")
        os.makedirs(scenes_dir, exist_ok=True)
        
        filename = f"scenes/scene_{cache_key}.py"
        try:
            video_path = generate_video(
                script_code, request,
                filename=filename,
                voice_text=voice_text
            )
        except Exception as e:
            err_msg = str(e)
            if "Failed to generate video" in err_msg or "AI generated Python syntax error" in err_msg or "forbidden Manim object" in err_msg or "Regenerate." in err_msg:
                print(f"[main] Script error caught: {err_msg[:50]}... Triggering Runtime Correction Agent!")
                from ai_engine import fix_runtime_error
                fixed_code = fix_runtime_error(script_code, err_msg)
                if fixed_code:
                    print("[main] Retrying video generation with fixed code...")
                    video_path = generate_video(
                        fixed_code, request,
                        filename=filename,
                        voice_text=voice_text
                    )
                else:
                    raise
            else:
                raise

        relative_path = os.path.relpath(
            video_path,
            start=os.path.dirname(os.path.abspath(__file__))
        )
        web_path = relative_path.replace(os.path.sep, "/")
        video_url = f"/video/{web_path}"

        # 3. Cache the result
        _cache_set(cache_key, video_url)
        print(f"[cache] SET key={cache_key} ttl={CACHE_TTL}s")

        return VideoResponse(video_url=video_url, cached=False)

    except ValueError as e:
        # Validation / script errors — client bug
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/video/{filepath:path}")
async def serve_video(filepath: str, request: Request):
    # Security: prevent path traversal (e.g. ../../etc/passwd)
    backend_dir = os.path.dirname(os.path.abspath(__file__))
    safe_path = os.path.normpath(os.path.join(backend_dir, filepath))
    if not safe_path.startswith(backend_dir):
        raise HTTPException(status_code=403, detail="Access denied")
    if not os.path.exists(safe_path):
        raise HTTPException(status_code=404, detail="Video not found")

    return FileResponse(
        safe_path,
        media_type="video/mp4",
        headers={
            "Cache-Control": "public, max-age=3600",   # browsers cache the video 1hr
            "Accept-Ranges": "bytes",                   # enables video seeking
        }
    )


@app.get("/health")
async def health():
    return {
        "status": "ok",
        "cache_entries": len(_video_cache),
        "cache_ttl_seconds": CACHE_TTL,
    }


@app.get("/")
async def root():
    return {"status": "success", "message": "EduMotion AI Backend API is running."}
