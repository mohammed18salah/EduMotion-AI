import os
import re
import subprocess
import glob
from gtts import gTTS

# Map invalid/unknown colors → nearest valid Manim color
INVALID_COLORS = {
    "CYAN":    "TEAL",
    "PURPLE":  "BLUE_D",
    "VIOLET":  "BLUE_D",
    "INDIGO":  "BLUE_E",
    "BROWN":   "MAROON",
    "MAGENTA": "PINK",
    "LIME":    "GREEN_A",
    "NAVY":    "BLUE_E",
    "CRIMSON": "RED_D",
    "SILVER":  "LIGHT_GRAY",
    "AQUA":    "TEAL_A",
}

def sanitize_script(code: str) -> str:
    """Replace any invalid Manim color names with safe equivalents."""
    for bad, good in INVALID_COLORS.items():
        # Replace whole-word matches only
        code = re.sub(rf'\b{bad}\b', good, code)
    return code

def generate_video(script_content: str, request, filename: str = "output_scene.py") -> str:
    # 1. Handle Configuration
    if request.style == "neon":
        bg_color = "#000000"
    elif request.style == "colorful":
        bg_color = "#1E1E2E"
    elif request.style == "chalkboard":
        bg_color = "#2F4F4F"
    else:  # minimalist
        bg_color = "#111111" # Using dark gray for minimalist so colors still pop instead of white

    if request.aspect_ratio == "9:16":
        w, h = 480, 854
        fw, fh = 8.0, 14.22
    else:
        w, h = 854, 480
        fh, fw = 8.0, 14.22

    config_injection = f"""
config.pixel_width = {w}
config.pixel_height = {h}
config.frame_width = {fw}
config.frame_height = {fh}
config.background_color = "{bg_color}"
"""

    script_content = sanitize_script(script_content)

    # Insert config automatically after imports
    if "from manim import *" in script_content:
        script_content = script_content.replace(
            "from manim import *", 
            f"from manim import *\n{config_injection}"
        )
    else:
        script_content = f"from manim import *\n{config_injection}\n{script_content}"

    backend_dir = os.path.dirname(os.path.abspath(__file__))
    script_path = os.path.join(backend_dir, filename)
    with open(script_path, "w", encoding="utf-8") as f:
        f.write(script_content)

    # 2. Run Manim
    media_dir = os.path.join(backend_dir, "media")
    command = ["python", "-m", "manim", "-ql", script_path, "MainScene", "--format=mp4", "--disable_caching", "--media_dir", "./media"]
    
    venv_python = os.path.join(backend_dir, "venv", "Scripts", "python.exe")
    if os.path.exists(venv_python):
        command[0] = venv_python

    result = subprocess.run(command, capture_output=True, text=True, cwd=backend_dir)
    if result.returncode != 0:
        raise Exception(f"Failed to generate video. Logs: {result.stderr}")

    # Find the Manim output file
    base_name = filename.replace(".py", "")
    expected_path = os.path.join(media_dir, "videos", base_name, "480p15", "MainScene.mp4")
    
    if not os.path.exists(expected_path):
        files = glob.glob(os.path.join(media_dir, "**", "*.mp4"), recursive=True)
        if files:
            files.sort(key=os.path.getmtime, reverse=True)
            expected_path = files[0]
        else:
            raise Exception("Video generated successfully but .mp4 file missing in media directory.")

    # 3. Add Voiceover if enabled
    if request.voice_enabled:
        import uuid
        audio_path = os.path.join(backend_dir, f"audio_{uuid.uuid4().hex[:8]}.mp3")
        try:
            tts = gTTS(text=request.topic, lang=request.language)
            tts.save(audio_path)
            
            final_path = expected_path.replace(".mp4", "_audio.mp4")
            # Mix audio and video, cut at the shortest of the two
            # We use ffmpeg built-in if available (manim requires ffmpeg)
            ffmpeg_cmd = ["ffmpeg", "-y", "-i", expected_path, "-i", audio_path, "-c:v", "copy", "-c:a", "aac", "-shortest", final_path]
            ff_res = subprocess.run(ffmpeg_cmd, capture_output=True, text=True, cwd=backend_dir)
            
            if ff_res.returncode == 0 and os.path.exists(final_path):
                expected_path = final_path
        except Exception as e:
            print(f"TTS Failed: {e}")
        finally:
            if os.path.exists(audio_path):
                os.remove(audio_path)
                
    return expected_path
