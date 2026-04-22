<div align="center">

<img src="https://img.shields.io/badge/EduMotion-AI-6366f1?style=for-the-badge&logo=google&logoColor=white" />
<img src="https://img.shields.io/badge/Gemini-2.0_Flash-4285F4?style=for-the-badge&logo=google&logoColor=white" />
<img src="https://img.shields.io/badge/Manim-Animation-00C4FF?style=for-the-badge" />
<img src="https://img.shields.io/badge/FastAPI-Backend-009688?style=for-the-badge&logo=fastapi&logoColor=white" />
<img src="https://img.shields.io/badge/React-Frontend-61DAFB?style=for-the-badge&logo=react&logoColor=black" />

---

# 🎬 EduMotion AI
### *Turn Any Idea Into an Educational Video — In Seconds*


 · [**📖 Documentation**](#architecture)

</div>


---

## 🧠 What Is EduMotion AI?

**EduMotion AI** is an end-to-end platform that converts any educational concept into a **fully animated, narrated video** — automatically. 

Teachers, students, and content creators simply type a topic (e.g., *"Explain Bubble Sort step by step"*), choose their settings, and within **60–90 seconds** receive a polished animated video with synchronized AI voiceover — in **Arabic or English**.

---

## ✨ Key Features

| Feature | Description |
|---|---|
| 🤖 **Unified AI Pipeline** | Single Gemini API call generates Manim animation code + full narration script simultaneously |
| 🎨 **Manim Animation Engine** | Mathematically precise animations: graphs, sorting, geometry, physics |
| 🎙️ **Neural Voiceover** | Microsoft Edge TTS — 4 voice options (Arabic ♀/♂, English ♀/♂) |
| ⚡ **3-Key × 4-Model Rotation** | 12 API combinations — always finds an available Gemini endpoint |
| 🌍 **Bilingual** | Full Arabic (RTL) + English support with dynamic font switching |
| 📐 **Aspect Ratio Control** | 16:9 (YouTube) / 9:16 (TikTok/Reels) |
| 🛡️ **Resilient Error Handling** | Pre-run Manim validator, duration cap (requested + 20s grace), fallback animation |
| 🎨 **4 Visual Styles** | Minimalist, Neon, Colorful, Chalkboard |

---

## 🎓 Problem We Solve

Creating educational animations currently requires:
- 🕐 **Hours** of manual work in After Effects, Blender, or Manim
- 💰 **Expensive** freelancers or specialized studios
- 🧑‍💻 **Deep technical skills** most educators don't have

**EduMotion AI eliminates all three barriers** — a teacher can generate a 30-second animated lesson on *Newton's Second Law* in under 2 minutes, for free.

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    USER BROWSER                          │
│         React + Vite Frontend (bilingual UI)             │
└──────────────────────┬──────────────────────────────────┘
                       │ POST /generate
                       ▼
┌─────────────────────────────────────────────────────────┐
│                  FastAPI Backend                          │
│                                                          │
│  ┌──────────────┐   ┌──────────────┐   ┌─────────────┐  │
│  │  AI Engine   │   │ Video Engine │   │  Edge-TTS   │  │
│  │              │   │              │   │  CLI Voice  │  │
│  │ 3 API Keys × │──▶│ Manim Python │──▶│ ar/en ♀/♂  │  │
│  │ 4 Gemini     │   │ Renderer     │   │             │  │
│  │ Models       │   │ + Validator  │   │             │  │
│  └──────────────┘   └──────────────┘   └─────────────┘  │
│                              │                           │
│                       ffmpeg mixes                       │
│                       video + audio                      │
└──────────────────────┬──────────────────────────────────┘
                       │ .mp4 URL
                       ▼
                  🎬 Final Video
```

---

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- Node.js 18+
- [FFmpeg](https://ffmpeg.org/download.html) in PATH
- Google Gemini API Key ([get one free](https://aistudio.google.com))

### 1. Clone the repo
```bash
git clone https://github.com/YOUR_USERNAME/EduMotion-AI.git
cd EduMotion-AI
```

### 2. Backend setup
```bash
cd backend
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # Linux/Mac

pip install -r requirements.txt
```

### 3. Add your API key
Copy the provided `.env.example` file to create a `.env` file inside the `backend` folder and add your keys (it supports auto-rotation!):
```bash
cp .env.example .env
```
```env
# backend/.env
GEMINI_KEY_1=your_first_google_gemini_api_key
GEMINI_KEY_2=your_second_api_key_optional
ALLOWED_ORIGINS=http://localhost:5173
CACHE_TTL_SECONDS=3600
```

### 4. Start the backend
```bash
uvicorn main:app --port 8000 --reload
```
> **Note:** Generated video files are saved in `backend/media/videos/`, while the Python script for each video is stored neatly in `backend/scenes/`. The backend also includes a smart **in-memory SHA-256 caching system** to avoid regenerating identical requests!

### 5. Frontend setup
```bash
cd frontend
npm install
npm run dev
```

### 6. Open the app
Visit **http://localhost:5173** 🎉

---

## 🛠️ Tech Stack

### Backend
| Technology | Role |
|---|---|
| **Python 3.13** | Core runtime |
| **FastAPI** | REST API server |
| **Google Gemini 2.0 Flash** | AI code + narration generation |
| **Manim Community** | Mathematical animation rendering |
| **Edge-TTS** | Neural voice synthesis (Microsoft) |
| **FFmpeg** | Audio/video mixing & trimming |

### Frontend
| Technology | Role |
|---|---|
| **React 18 + Vite** | UI framework |
| **Framer Motion** | Animations & transitions |
| **Lucide Icons** | Icon set |
| **CSS Variables** | Theme system (dark/light mode) |

---

## 🛡️ Resilient AI Engine & Key Rotation

During development, we faced constant `503 Service Unavailable` errors and quota limits from Google's Gemini free tier. To fix this and make the project production-ready, we designed a custom **AI Engine (`ai_engine.py`)**:

1. **Multi-Key Rotation**: You can provide up to 5 API keys in the `.env` file.
2. **Model Fallback**: The engine holds an array of models (`gemini-2.0-flash`, `gemini-2.5-flash`, `gemini-flash-latest`, `gemini-2.0-flash-lite`).
3. **Smart Retry & Backoff**: If an API key hits a quota limit or the model returns a 503, the engine automatically catches the exception, applies exponential backoff (with jitter to stagger retries), and immediately rotates to the next available API key or model.
4. **Zero-Downtime Generation**: This ensures that as long as one key/model combination has quota, the user *never* sees a failed generation.

---

## 🎯 How It Works — Step by Step

```
1. User types topic: "Traveling Salesman Problem with Tabu Search"
   + selects: Duration=30s, Style=Neon, Voice=Arabic Female

2. Backend sends unified prompt to Gemini:
   → Generates Manim Python code (7 animated scenes)  
   → Generates synchronized narration script (Arabic)
   (Single API call — no double round-trip)

3. Pre-validation catches any bad code before running Manim

4. Manim renders the .mp4 animation @ 480p15

5. Duration cap: if video > 50s (30+20), ffmpeg trims it silently

6. Edge-TTS CLI generates neural Arabic voiceover from narration

7. FFmpeg mixes video + audio, loops audio if needed

8. Frontend receives .mp4 URL and plays it inline
```

---

## 🌍 Supported Voices

| Language | Gender | Voice Model |
|---|---|---|
| 🇸🇦 Arabic | ♀ Female | `ar-SA-ZariyahNeural` |
| 🇸🇦 Arabic | ♂ Male | `ar-SA-HamedNeural` |
| 🇺🇸 English | ♀ Female | `en-US-JennyNeural` |
| 🇺🇸 English | ♂ Male | `en-US-GuyNeural` |

---

## 🔮 Roadmap

- [ ] Cloud deployment (Render + Vercel)
- [ ] User authentication & video history
- [ ] 1080p render option
- [ ] ElevenLabs premium voice integration
- [ ] PDF/slide-to-video conversion
- [ ] Custom color themes per video

---

## 👥 Team

Built with ❤️ by Mohammed Salah.

| Role | Contribution |
|---|---|
| 🧠 AI & Backend | Gemini pipeline, Manim engine, API resilience |
| 🎨 Frontend | React UI, animations, bilingual support |
| 🔊 Audio | Edge-TTS integration, FFmpeg mixing |

---

## 📄 License

MIT License — feel free to build on this!

---

<div align="center">

**⭐ If EduMotion helped you, give it a star!**

*Powered by Google Gemini · April 2026*

</div>
