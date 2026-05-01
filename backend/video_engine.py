import os
import re
import subprocess
import glob
import uuid

# ─── Edge-TTS voice map ───────────────────────────────────────────────────
# Format: (language_code, gender) → edge-tts voice name
VOICE_MAP = {
    # Arabic
    ("ar", "female"): "ar-AE-FatimaNeural",    # UAE Arabic – female (More natural)
    ("ar", "male"):   "ar-AE-HamdanNeural",    # UAE Arabic – male
    # English
    ("en", "female"): "en-US-JennyNeural",      # US English – female
    ("en", "male"):   "en-US-GuyNeural",        # US English – male
}
DEFAULT_VOICE = "en-US-JennyNeural"

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
        code = re.sub(rf'\b{bad}\b', good, code)
    return code


# Forbidden objects that cause Manim to crash
FORBIDDEN_OBJECTS = ["MathTex", "Tex(", "SVGMobject", "ImageMobject"]

def validate_script(code: str) -> None:
    """
    Quick pre-run check. Raises ValueError with a clear message if the
    AI-generated script has known crash-inducing patterns.
    """
    # Must have MainScene
    if "class MainScene" not in code:
        raise ValueError("Generated code is missing 'class MainScene(Scene)'. Regenerate.")

    # Must start with manim import
    if "from manim import" not in code:
        raise ValueError("Generated code is missing 'from manim import *'. Regenerate.")

    # Check forbidden objects
    for obj in FORBIDDEN_OBJECTS:
        if obj in code:
            raise ValueError(
                f"AI used forbidden Manim object '{obj}' which crashes the renderer. "
                "Regenerate with a different topic or style."
            )

    # Basic Python syntax check
    try:
        compile(code, "<manim_script>", "exec")
    except SyntaxError as e:
        raise ValueError(f"AI generated Python syntax error at line {e.lineno}: {e.msg}. Regenerate.")


def _generate_tts(text: str, voice: str, output_path: str) -> bool:
    """
    Generate TTS audio via edge-tts CLI (subprocess).
    Avoids asyncio event loop conflicts with uvicorn.
    """
    try:
        venv_dir = os.path.dirname(os.path.abspath(__file__))
        edge_exe = os.path.join(venv_dir, "venv", "Scripts", "edge-tts.exe")
        if not os.path.exists(edge_exe):
            edge_exe = "edge-tts"  # fallback to PATH

        cmd = [
            edge_exe,
            "--voice", voice,
            "--text", text,
            "--write-media", output_path,
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        if result.returncode == 0 and os.path.exists(output_path):
            size = os.path.getsize(output_path)
            print(f"[video_engine] TTS OK — {voice} — {size//1024}KB")
            return size > 1000  # must be a real audio file
        else:
            print(f"[video_engine] edge-tts CLI failed: {result.stderr[:200]}")
            return False
    except Exception as e:
        print(f"[video_engine] TTS error: {e}")
        return False


def generate_video(
    script_content: str,
    request,
    filename: str = "output_scene.py",
    voice_text: str = ""
) -> str:
    # ── 1. Style → background color ──
    bg_map = {
        "neon":       "#000000",
        "colorful":   "#1E1E2E",
        "chalkboard": "#2F4F4F",
    }
    bg_color = bg_map.get(request.style, "#111111")

    # ── 2. Aspect ratio → dimensions ──
    if request.aspect_ratio == "9:16":
        w, h, fw, fh = 480, 854, 8.0, 14.22
    else:
        w, h, fw, fh = 854, 480, 14.22, 8.0

    config_injection = f"""
config.pixel_width = {w}
config.pixel_height = {h}
config.frame_width = {fw}
config.frame_height = {fh}
config.background_color = "{bg_color}"
"""

    script_content = sanitize_script(script_content)
    validate_script(script_content)   # ← raises ValueError early if code is broken

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

    # ── 3. Run Manim ──
    media_dir = os.path.join(backend_dir, "media")
    venv_python = os.path.join(backend_dir, "venv", "Scripts", "python.exe")
    python_exe = venv_python if os.path.exists(venv_python) else "python"

    command = [
        python_exe, "-m", "manim", "-ql",
        script_path, "MainScene",
        "--format=mp4", "--disable_caching",
        "--media_dir", "./media"
    ]

    result = subprocess.run(command, capture_output=True, text=True, cwd=backend_dir)
    if result.returncode != 0:
        raise Exception(f"Failed to generate video. Logs: {result.stderr}")

    # ── 4. Find output .mp4 ──
    base_name = filename.replace(".py", "")
    expected_path = os.path.join(media_dir, "videos", base_name, "480p15", "MainScene.mp4")
    if not os.path.exists(expected_path):
        files = glob.glob(os.path.join(media_dir, "**", "*.mp4"), recursive=True)
        if files:
            files.sort(key=os.path.getmtime, reverse=True)
            expected_path = files[0]
        else:
            raise Exception("Video file not found after Manim render.")

    # ── 4b. Duration cap: trim to requested_duration + 20s grace period ──
    max_allowed_sec = int(request.duration) + 20
    try:
        # Get actual video duration via ffprobe
        probe = subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration",
             "-of", "default=noprint_wrappers=1:nokey=1", expected_path],
            capture_output=True, text=True, timeout=10
        )
        actual_dur = float(probe.stdout.strip()) if probe.stdout.strip() else 0
        if actual_dur > max_allowed_sec:
            trimmed = expected_path.replace(".mp4", "_trimmed.mp4")
            trim_cmd = [
                "ffmpeg", "-y", "-i", expected_path,
                "-t", str(max_allowed_sec),
                "-c", "copy",
                trimmed
            ]
            tr = subprocess.run(trim_cmd, capture_output=True, text=True, cwd=backend_dir)
            if tr.returncode == 0 and os.path.exists(trimmed):
                expected_path = trimmed
                print(f"[video_engine] Trimmed {actual_dur:.1f}s → {max_allowed_sec}s (cap)")
            else:
                print(f"[video_engine] Trim failed, keeping original: {tr.stderr[:100]}")
        else:
            print(f"[video_engine] Duration {actual_dur:.1f}s ≤ cap {max_allowed_sec}s — no trim needed")
    except Exception as e:
        print(f"[video_engine] Duration check skipped: {e}")

    # ── 5. Generate voiceover with edge-tts ──
    if request.voice_enabled:
        lang_code   = "ar" if request.language == "ar" else "en"
        voice_gender = getattr(request, "voice_gender", "female")
        voice_name  = VOICE_MAP.get((lang_code, voice_gender), DEFAULT_VOICE)

        tts_text = voice_text.strip() if voice_text.strip() else request.topic
        # Remove markdown characters like asterisks and hashes so TTS doesn't read them
        tts_text = re.sub(r'[*#_]', '', tts_text)
        
        audio_path = os.path.join(backend_dir, f"tts_{uuid.uuid4().hex[:8]}.mp3")
        final_path = expected_path.replace(".mp4", "_voiced.mp4")

        print(f"[video_engine] TTS: voice={voice_name}, text={tts_text[:60]}...")
        tts_ok = _generate_tts(tts_text, voice_name, audio_path)

        if tts_ok and os.path.exists(audio_path):
            # Get actual video duration to trim audio to it (prevents video looping)
            probe = subprocess.run(
                ["ffprobe", "-v", "error", "-show_entries", "format=duration",
                 "-of", "default=noprint_wrappers=1:nokey=1", expected_path],
                capture_output=True, text=True, timeout=10
            )
            video_dur = probe.stdout.strip()

            ffmpeg_cmd = [
                "ffmpeg", "-y",
                "-i", expected_path,   # video — plays ONCE, no loop
                "-i", audio_path,
                "-c:v", "copy",
                "-c:a", "aac",
                "-b:a", "128k",
                "-map", "0:v:0",
                "-map", "1:a:0",
            ]
            # Trim audio to video length so video never has to loop
            if video_dur:
                ffmpeg_cmd += ["-t", video_dur]
            ffmpeg_cmd += ["-shortest", final_path]
            ff = subprocess.run(ffmpeg_cmd, capture_output=True, text=True, cwd=backend_dir)
            if ff.returncode == 0 and os.path.exists(final_path):
                expected_path = final_path
                print(f"[video_engine] ✓ Voice mixed: {voice_name}")
            else:
                print(f"[video_engine] ffmpeg mix failed: {ff.stderr[:200]}")
        else:
            print("[video_engine] TTS generation failed — serving video without audio")

        if os.path.exists(audio_path):
            os.remove(audio_path)

    return expected_path
