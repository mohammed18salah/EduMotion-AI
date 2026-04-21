from google import genai

# User's Gemini API key (from AI Studio)
API_KEY = "AIzaSyCG8nxa9PTqkiO3R_2fb7ZaDo3gFksSrWA"

client = genai.Client(api_key=API_KEY)

import time

def generate_manim_script(request) -> str:
    lang_instruction = "output ALL text in Arabic (RTL support via standard Arabic text)." if request.language == 'ar' else "output ALL text in English."
    
    prompt = f"""
You are an expert Python developer who creates educational videos using the Manim library.
The user's idea for the video is: {request.topic}

If the user's idea describes an animation or concept, create it.
CRITICAL MISTAKE PREVENTION: If the user's idea looks like a meta-instruction, a complaint, or a conversation (e.g., "don't show the video here", "how does this work?"), IGNORE their text and instead generate a generic visually beautiful example video (e.g., about Physics, Math Geometry, or data structures). You MUST NEVER output the user's prompt as code.

Configuration:
- Language: {request.language} ({lang_instruction})
- Video Duration: Max {request.duration} seconds
- Visual Style: {request.style}
- Aspect Ratio: {request.aspect_ratio}

Write a Manim animation script to explain this idea visually.

STRICT RULES — follow every single rule:
1. Start with: from manim import *
2. There MUST be exactly ONE class named MainScene that inherits from Scene
3. SPEED CRITICAL: Keep animations extremely fast! The entire scene should run mathematically quickly. Use run_time=0.5 or 1 maximum for creations. DO NOT exceed {request.duration} seconds in total.
4. Output ONLY raw Python code — absolutely NO markdown, NO ```, NO explanations
5. FORBIDDEN objects (DO NOT USE EVER): MathTex, Tex, SVGMobject, ImageMobject
   - LaTeX is NOT installed. Using MathTex or Tex will CRASH the program.
6. ALLOWED objects ONLY: Text, Circle, Square, Rectangle, Arrow, Line,
   NumberLine, Dot, VGroup, Polygon, Brace, DoubleArrow
7. VALID COLORS ONLY — use ONLY these color names (others will crash):
   BLUE, RED, GREEN, YELLOW, WHITE, BLACK, ORANGE, PINK, TEAL, GOLD,
   BLUE_A, BLUE_B, BLUE_C, BLUE_D, BLUE_E,
   RED_A, RED_B, RED_C, RED_D, RED_E,
   GREEN_A, GREEN_B, GREEN_C, GREEN_D, GREEN_E,
   YELLOW_A, YELLOW_B, YELLOW_C, YELLOW_D, YELLOW_E,
   TEAL_A, TEAL_B, TEAL_C, TEAL_D, TEAL_E,
   LIGHT_GRAY, DARK_GRAY, GRAY, MAROON
   DO NOT USE: CYAN, PURPLE, VIOLET, INDIGO, BROWN, MAGENTA (they are NOT defined)
8. Write math formulas as plain Text strings — example: Text("F = m * a")
9. Do NOT import anything besides: from manim import *
10. Ensure there are ZERO syntax errors

Begin your response directly with: from manim import *
"""

    models_to_try = [
        "gemini-2.0-flash",
        "gemini-flash-latest",
        "gemini-2.0-flash-lite",
        "gemini-2.5-flash", 
        "gemini-pro-latest",
        "gemini-3.1-pro-preview",
        "gemini-3.1-flash-lite-preview",
        "gemini-3-flash-preview"
    ]
    
    last_error = None
    for model_name in models_to_try * 2: # Try each model twice
        try:
            response = client.models.generate_content(
                model=model_name,
                contents=prompt
            )
            code = response.text.strip()
            
            # Strip markdown code fences if model added them
            if "```python" in code:
                code = code.split("```python")[1].split("```")[0].strip()
            elif "```" in code:
                code = code.split("```")[1].split("```")[0].strip()
                
            return code
        except Exception as e:
            err_str = str(e)
            print(f"Model {model_name} failed: {err_str}")
            last_error = e
            
            # If it's a 503 high demand error, wait a few seconds before trying the next model
            if "503" in err_str or "UNAVAILABLE" in err_str or "high demand" in err_str:
                time.sleep(3)
            continue
            
    # If the loop finishes without returning, all models failed
    raise Exception(f"All models failed due to high demand or quota limits. Last error: {last_error}")
