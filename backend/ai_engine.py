import os
import time
import random
from dotenv import load_dotenv
from google import genai
import requests
from openai import OpenAI

load_dotenv()

# API Keys
GEMINI_KEYS = [v for k, v in sorted(os.environ.items()) if k.startswith("GEMINI_KEY_") and v.strip()]
NVIDIA_API_KEY = os.environ.get("NVIDIA_API_KEY", "")

if not GEMINI_KEYS and not NVIDIA_API_KEY:
    raise RuntimeError("No GEMINI_KEY_* or NVIDIA_API_KEY found in .env")

# ─────────────────────────────────────────────────────────
# Generic fallback animation
# ─────────────────────────────────────────────────────────
FALLBACK_SCRIPT = '''from manim import *

class MainScene(Scene):
    def construct(self):
        self.camera.background_color = BLACK
        title = Text("EduMotion AI", font_size=56, color=TEAL_A)
        sub   = Text("Your ideas, animated.", font_size=28, color=WHITE)
        sub.next_to(title, DOWN, buff=0.5)
        self.play(FadeIn(title, shift=UP*0.3), run_time=0.8)
        self.play(FadeIn(sub), run_time=0.6)
        self.wait(2.5)
        self.play(FadeOut(title), FadeOut(sub), run_time=0.5)

        done = Text("Try again in a moment!", font_size=36, color=YELLOW)
        hint = Text("AI servers are busy right now.", font_size=24, color=LIGHT_GRAY)
        hint.next_to(done, DOWN, buff=0.4)
        self.play(FadeIn(done), FadeIn(hint), run_time=0.7)
        self.wait(3.0)
'''

FALLBACK_VOICE_TEXT = "EduMotion AI turns your ideas into educational animated videos. The AI servers are currently busy. Please try again in a moment."

# ─────────────────────────────────────────────────────────
# System Prompt
# ─────────────────────────────────────────────────────────
UNIFIED_PROMPT = """\
# IDENTITY
You are an expert educational video director AND a Manim Python engineer.
You think like a teacher first, then like an animator.
Your job is to produce a CLEAN, BUG-FREE animated video that genuinely teaches.

Your output has TWO parts separated by: ===VOICE===
PART 1 — Manim Python code
PART 2 — Voiceover narration

═══ INPUT ═══
TOPIC:        {topic}
LANGUAGE:     {language}
DURATION:     {duration} seconds
STYLE:        {style}
ASPECT RATIO: {aspect_ratio}

═══ STEP 1 — EDUCATIONAL ANALYSIS ═══
Before writing any code, decide internally:
1. The single most important concept to teach
2. The best order to present 4-8 steps
3. A real-world analogy that makes it click

═══ STEP 2 — SCENE PLANNING ═══
SCENE PLAN:
[N] SCENE_NAME — purpose — duration (sec)
TOTAL: {duration} sec

Rules:
- 4 to 8 scenes
- First scene hooks in ≤ 5 sec
- Last scene: clear summary

═══ STEP 3 — MANIM CODE ═══

TIMING:
- Total self.wait() must sum to ≥ {total_wait:.1f} sec
- run_time: 0.5–0.8 sec per play() call

STRUCTURE (REQUIRED):
- from manim import *  ← first line, always
- Exactly ONE class: MainScene(Scene)
- self.camera.background_color = BLACK  ← first line in construct()
- Clear screen: self.play(FadeOut(Group(*self.mobjects)))

VISUAL SYSTEM:
- Primary: TEAL_A | Accent: PINK | Success: GREEN
- Warning: YELLOW_A | Problem: RED_B | Text: WHITE | BG: BLACK

VALID OBJECTS ONLY:
Text, Circle, Square, Rectangle, Arrow, Line, NumberLine,
Dot, VGroup, Polygon, Brace, DoubleArrow, Triangle

FORBIDDEN — WILL CRASH THE RENDERER:
✗ MathTex, Tex, SVGMobject, ImageMobject — NEVER use these!
✗ Colors: CYAN PURPLE VIOLET INDIGO BROWN MAGENTA
✗ NEVER pass x_values/y_values to add_coordinates()
✗ NEVER omit () on method calls (.get_center() not .get_center)
✗ NEVER use get_part_by_tex, get_part_by_text, get_substring_to_isolate
✗ NEVER pass tip_angle or tip_length to Arrow()
✗ NEVER reuse a variable name that was already FadeOut'd — create fresh objects

ANIMATION QUALITY RULES (fix common AI mistakes):
1. OBJECT REUSE: After FadeOut(obj), NEVER animate or reference obj again.
   Always create a NEW object for each scene. Example:
     BAD:  self.play(FadeOut(box)); self.play(box.animate.move_to(UP))  ← crashes!
     GOOD: self.play(FadeOut(box)); box2 = Square(); self.play(Create(box2))

2. SWAP ANIMATIONS: To swap two elements A and B:
   Store positions BEFORE moving:
     pos_a = a.get_center()
     pos_b = b.get_center()
     self.play(a.animate.move_to(pos_b), b.animate.move_to(pos_a))
   NEVER use .arrange() after individual moves — it ignores real positions.

3. TEXT ON SCREEN: Never overlap text. Use .next_to(), .to_edge(), or .shift().
   Each text element must be in a DIFFERENT position.

4. SCENE CLEARING: Before every new scene call:
     self.play(FadeOut(Group(*self.mobjects)))
   This clears ALL objects. Do this before drawing new scene content.

MATH NOTATION:
Use plain Text() only. Example: Text("E = m × c²")

FONTS & ARABIC (CRITICAL):
If language is Arabic ('ar'), add font="Arial" to EVERY Text() call!
Example: Text("مرحبا", font="Arial", font_size=36)

5. CONTENT ACCURACY: The topic explanation MUST be 100% factually correct.
   - Show steps IN ORDER. Never skip steps or show a later result before an earlier step.
   - Each scene must logically follow the previous one.
   - If explaining an algorithm or process, animate it step-by-step accurately.

═══ STEP 4 — VOICEOVER ═══
After ===VOICE=== write narration:
- TOTAL length: match {duration} seconds of speech (≈ {words_per_sec:.0f} words)
- One flowing paragraph per scene — no scene labels or numbers
- Smooth, natural, conversational tone in {language}
- ONLY spoken words — NO asterisks, hashes, bullets, dashes, or any symbols!
- Do NOT repeat the same sentence. Each sentence must add new information.
- The narration must stay synchronized with what is shown on screen.

═══ FINAL CHECK (before outputting) ═══
Before writing your final answer, verify:
✓ Does `class MainScene(Scene):` exist exactly once?
✓ Is every Text() using font="Arial" if language is Arabic?
✓ Are all FadeOut'd objects never referenced again?
✓ Is every scene cleared with FadeOut(Group(*self.mobjects)) before the next?
✓ Does the narration match the video content exactly?
✓ Is there any repeated sentence in the narration?
If any check fails, fix it before outputting.

═══ OUTPUT FORMAT ═══
SCENE PLAN:
[scene plan]

---

[Manim Python code starting with: from manim import *]

===VOICE===
[narration]
"""

# ─────────────────────────────────────────────────────────
# Callers
# ─────────────────────────────────────────────────────────

def _call_gemini(prompt: str) -> str:
    if not GEMINI_KEYS: return None
    key = random.choice(GEMINI_KEYS)
    client = genai.Client(api_key=key)
    # Using 2.5-flash as the primary fast and smart model
    model = "gemini-2.5-flash"
    try:
        res = client.models.generate_content(model=model, contents=prompt)
        print(f"[ai_engine] ✓ Gemini ({model}) completed successfully.")
        return res.text.strip()
    except Exception as e:
        print(f"[ai_engine] ✗ Gemini failed: {e}")
        return None

def _call_nvidia_gpt(prompt: str) -> str:
    if not NVIDIA_API_KEY: return None
    try:
        client = OpenAI(base_url="https://integrate.api.nvidia.com/v1", api_key=NVIDIA_API_KEY)
        completion = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[{"role":"user","content":prompt}],
            temperature=0.8,
            top_p=1,
            max_tokens=4096,
            stream=False
        )
        print(f"[ai_engine] ✓ Nvidia GPT completed successfully.")
        return completion.choices[0].message.content.strip()
    except Exception as e:
        print(f"[ai_engine] ✗ Nvidia GPT failed: {e}")
        return None

def _call_nvidia_qwen(prompt: str) -> str:
    if not NVIDIA_API_KEY: return None
    try:
        invoke_url = "https://integrate.api.nvidia.com/v1/chat/completions"
        headers = {"Authorization": f"Bearer {NVIDIA_API_KEY}", "Accept": "application/json"}
        payload = {
            "model": "qwen/qwen3.5-122b-a10b",
            "messages": [{"role":"user","content":prompt}],
            "max_tokens": 4096,
            "temperature": 0.60,
            "top_p": 0.95,
            "stream": False,
        }
        res = requests.post(invoke_url, headers=headers, json=payload, timeout=60)
        res.raise_for_status()
        print(f"[ai_engine] ✓ Nvidia Qwen completed successfully.")
        return res.json()["choices"][0]["message"]["content"].strip()
    except Exception as e:
        print(f"[ai_engine] ✗ Nvidia Qwen failed: {e}")
        return None

# ─────────────────────────────────────────────────────────
# Error Correction Logic
# ─────────────────────────────────────────────────────────

def _check_for_errors(raw_response: str) -> list:
    """Fast local check for common Manim/prompt constraints."""
    import re
    errors = []
    if "===VOICE===" not in raw_response:
        errors.append("Missing '===VOICE===' separator.")
    if "from manim import *" not in raw_response:
        errors.append("Missing 'from manim import *'.")
    if "class MainScene" not in raw_response:
        errors.append("Missing 'class MainScene(Scene):'.")
    for bad_obj in ["MathTex", "Tex(", "SVGMobject", "ImageMobject"]:
        if bad_obj in raw_response:
            errors.append(f"Contains forbidden object: {bad_obj}")
    if "VGroup(*self.mobjects)" in raw_response:
        errors.append("CRITICAL: Used VGroup(*self.mobjects) which causes TypeError. MUST use Group(*self.mobjects) instead.")
    if "add_coordinates(" in raw_response and ("x_values" in raw_response or "y_values" in raw_response):
        errors.append("CRITICAL: TypeError in add_coordinates(). NEVER pass x_values or y_values to add_coordinates(). Use add_coordinates() with no arguments.")
    if re.search(r'\.get_(center|left|right|top|bottom|width|height|corner)(?![\(\w])', raw_response):
        errors.append("CRITICAL: Missing parentheses on method call (e.g. used .get_center instead of .get_center()). This causes a TypeError.")
    for bad_method in ["get_substring_to_isolate", "get_part_by_tex", "get_part_by_text"]:
        if bad_method in raw_response:
            errors.append(f"CRITICAL: Used {bad_method} which crashes on Text objects. NEVER use these methods.")
    if "tip_angle=" in raw_response or "tip_length=" in raw_response:
        errors.append("CRITICAL: Passed 'tip_angle' or 'tip_length' to Arrow(). These are unexpected keyword arguments and will crash. Remove them.")
    if re.search(r'Square\([^)]*\bside=', raw_response):
        errors.append("CRITICAL: Square() does not take 'side' as an argument. Use 'side_length' instead.")
    return errors

def fix_runtime_error(bad_code: str, traceback_str: str) -> str:
    """Uses Nvidia GPT to fix a runtime Manim crash."""
    fix_prompt = f"""
You are an expert Python Manim engineer. 
The following Manim script crashed during rendering.

THE CRASH TRACEBACK:
{{traceback_str}}

YOUR TASK:
Fix the script to resolve the runtime error above.
Preserve the educational content, but rewrite the Manim code to be 100% bug-free.

CRITICAL RULES:
1. NEVER use `MathTex`, `Tex`, `SVGMobject`, or `ImageMobject`. Use plain `Text()` strings only!
2. If there is Arabic text, you MUST add `font="Arial"` to the `Text()` call.
3. NEVER pass `x_values` or `y_values` to `add_coordinates()`.
4. Output ONLY the new, COMPLETE Manim Python code. Do not use snippets or placeholders.
5. You MUST include `class MainScene(Scene):` and the full `construct` method.
Start with: from manim import *

ORIGINAL BROKEN SCRIPT:
{{bad_code}}
"""
    print(f"[ai_engine] Sending broken script to Nvidia GPT to fix runtime error...")
    fixed = _call_nvidia_gpt(fix_prompt)
    if not fixed:
        print(f"[ai_engine] Nvidia GPT failed to fix runtime error. Trying Nvidia Qwen...")
        fixed = _call_nvidia_qwen(fix_prompt)
    
    if fixed:
        code = fixed.strip()
        if "from manim import *" in code:
            code = "from manim import *" + code.split("from manim import *", 1)[1]
            if "```" in code:
                code = code.split("```")[0].strip()
        else:
            if "```python" in code:
                code = code.split("```python")[-1].split("```")[0].strip()
            elif "```" in code:
                code = code.split("```")[-1].split("```")[0].strip()
        return code
    return None

def _fix_errors_with_nvidia(bad_response: str, errors: list) -> str:
    """Uses Nvidia GPT to fix errors made by Gemini."""
    fix_prompt = f"""
You are an expert Python Manim engineer. 
Another AI generated the following Manim script and voiceover, but it contains CRITICAL ERRORS that will crash the system.

THE ERRORS FOUND:
{chr(10).join(errors)}

YOUR TASK:
Fix the script so it resolves all the errors above.
Preserve the educational content and voiceover exactly as intended, but rewrite the Manim code to be 100% bug-free.
Remember: NEVER use MathTex or Tex. Use plain Text() instead.

ORIGINAL BROKEN OUTPUT:
{bad_response}

Return the COMPLETE corrected output in the exact same format (SCENE PLAN, Manim Code, then ===VOICE===).
"""
    print(f"[ai_engine] Sending broken script to Nvidia GPT for error correction...")
    fixed = _call_nvidia_gpt(fix_prompt)
    if not fixed:
        print(f"[ai_engine] Nvidia GPT failed to fix. Trying Nvidia Qwen...")
        fixed = _call_nvidia_qwen(fix_prompt)
    
    return fixed if fixed else bad_response


# ─────────────────────────────────────────────────────────
# Main Pipeline
# ─────────────────────────────────────────────────────────

def get_best_model_response(prompt: str) -> str:
    """
    Primary: Gemini
    Fallback 1: Nvidia GPT
    Fallback 2: Nvidia Qwen
    """
    print("[ai_engine] Requesting primary model: Gemini...")
    res = _call_gemini(prompt)
    
    if res:
        return res
        
    print("[ai_engine] Primary model failed! Falling back to Nvidia GPT...")
    res = _call_nvidia_gpt(prompt)
    
    if res:
        return res
        
    print("[ai_engine] Fallback 1 failed! Falling back to Nvidia Qwen...")
    res = _call_nvidia_qwen(prompt)
    
    if res:
        return res
        
    raise Exception("503_ALL_MODELS: Gemini and Nvidia fallbacks all failed.")

def generate_manim_script(request):
    """
    Returns a tuple: (manim_code: str, voice_text: str)
    """
    duration = int(request.duration)
    total_wait = duration * 0.60
    words_per_sec = duration * 2.2  # average Arabic/English TTS pace

    prompt = UNIFIED_PROMPT.format(
        topic=request.topic,
        language=request.language,
        duration=duration,
        style=request.style,
        aspect_ratio=request.aspect_ratio,
        total_wait=total_wait,
        words_per_sec=words_per_sec,
    )

    try:
        # Step 1: Generate using Primary (Gemini) with Fallbacks
        raw = get_best_model_response(prompt)

        # Step 2: Error Monitoring & Auto-Correction
        errors = _check_for_errors(raw)
        if errors:
            print(f"[ai_engine] Found {len(errors)} errors in generated script! Triggering Correction Agent...")
            corrected_raw = _fix_errors_with_nvidia(raw, errors)
            if corrected_raw:
                raw = corrected_raw

        # Step 3: Parsing Output
        if "===VOICE===" in raw:
            code_part, voice_part = raw.split("===VOICE===", 1)
        else:
            code_part  = raw
            voice_part = f"This video explains {request.topic}."

        # Robust code extraction: start at "from manim import *"
        code = code_part.strip()
        if "from manim import *" in code:
            code = "from manim import *" + code.split("from manim import *", 1)[1]
            # Remove any trailing markdown fences
            if "```" in code:
                code = code.split("```")[0].strip()
        else:
            # Fallback if the LLM forgot the import
            if "```python" in code:
                code = code.split("```python")[-1].split("```")[0].strip()
            elif "```" in code:
                code = code.split("```")[-1].split("```")[0].strip()

        voice_text = voice_part.strip()
        print(f"[ai_engine] Code: {len(code)} chars | Voice: {len(voice_text)} chars")
        return code, voice_text

    except Exception as e:
        print(f"[ai_engine] All models failed or unavailable: {e} — using fallback animation.")
        return FALLBACK_SCRIPT.strip(), FALLBACK_VOICE_TEXT
