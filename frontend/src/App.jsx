import { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Video, Wand2, Download, RotateCw, PlayCircle, Globe, Layout, Palette, Clock, CheckCircle2, AlertCircle, Moon, Sun, Info, Home, Sparkles } from 'lucide-react';
import './index.css';

// ─── Cookie helpers (persist user settings) ───────────────────────────────
const setCookie = (name, value, days = 365) => {
  const expires = new Date(Date.now() + days * 864e5).toUTCString();
  document.cookie = `${name}=${encodeURIComponent(JSON.stringify(value))}; expires=${expires}; path=/; SameSite=Strict`;
};
const getCookie = (name) => {
  const match = document.cookie.match(new RegExp('(?:^|; )' + name + '=([^;]*)'));
  try { return match ? JSON.parse(decodeURIComponent(match[1])) : null; } catch { return null; }
};
const loadPref  = (key, fallback) => { const v = getCookie(`em_${key}`); return v !== null ? v : fallback; };
const savePref  = (key, value)    => setCookie(`em_${key}`, value);

const EXAMPLES = {
  ar: [
    "كيف تعمل الشبكات العصبية؟",
    "دورة حياة النجوم والثقوب السوداء",
    "خوارزمية البحث الثنائي (Binary Search)",
    "كيف يحدث الكسوف والخسوف؟",
  ],
  en: [
    "How Neural Networks learn",
    "Life cycle of a star to a black hole",
    "Binary Search algorithm step-by-step",
    "Solar and Lunar eclipses explained",
  ]
};

const API_BASE = import.meta.env.VITE_API_BASE_URL || "https://165.227.147.165.nip.io";

const SAMPLE_VIDEO = `${API_BASE}/video/media/videos/scene_4933795092450800427/480p15/MainScene.mp4`;

const DICT = {
  ar: {
    subtitle: "حوّل أي فكرة إلى فيديو تعليمي في ثوانٍ",
    placeholder: "صف فكرة الفيديو التعليمي...",
    generate: "اصنع الفيديو",
    generating: "جاري الإنشاء...",
    duration: "المدة (ثواني)",
    style: "النمط البصري",
    aspectRatio: "أبعاد الفيديو",
    voiceover: "التعليق الصوتي",
    tryAlso: "جرب مثلاً:",
    success: "اكتمل إنشاء الفيديو بنجاح",
    download: "تحميل",
    newVideo: "فيديو جديد",
    sampleVideoLabel: "فيديو مميز من إنشاء النظام",
    footer: "© 2026 EduMotion. مدعوم بالذكاء الاصطناعي.",
    styles: { minimalist: "بسيط وأنيق", neon: "نيون ساطع", colorful: "ملون وجذاب", chalkboard: "سبورة كلاسيكية" },
    aspects: { "16:9": "عرض (يوتيوب)", "9:16": "طولي (تيك توك/ريلز)" },
    navHome: "الرئيسية",
    navAbout: "حول المنصة",
    aboutTitle: "عن EduMotion AI",
    aboutDesc: "منصة متطورة ومدعومة بالذكاء الاصطناعي تهدف لتبسيط عملية إنشاء المحتوى التعليمي للأساتذة والمحاضرين وصناع المحتوى.",
    aboutTech: "التقنيات المستخدمة:",
    aboutTech1: "يعتمد النظام على محرك Manim لإنشاء رسوميات رياضياتية دقيقة وعالية الجودة.",
    aboutTech2: "يتم استخدام قدرات Gemini 2.0 Flash من جوجل في كتابة الشيفرات بشكل آلي وسريع جداً.",
    aboutTech3: "تم بناء واجهة الاستخدام على منصة React & TailwindCSS لتجربة سلسة وحديثة.",
    aboutDevText: "طور هذا المشروع محب للتقنية والذكاء الاصطناعي وهدفه إثراء المحتوى التعليمي العربي وتسهيل إنتاجه.",
  },
  en: {
    subtitle: "Turn any idea into an educational video in seconds",
    placeholder: "Describe the educational video idea...",
    generate: "Generate Video",
    generating: "Generating...",
    duration: "Duration (sec)",
    style: "Visual Style",
    aspectRatio: "Aspect Ratio",
    voiceover: "Voiceover",
    tryAlso: "Try this:",
    success: "Video generated successfully",
    download: "Download",
    newVideo: "New Video",
    sampleVideoLabel: "Sample Generated Video",
    footer: "© 2026 EduMotion. Powered by AI.",
    styles: { minimalist: "Minimal & Clean", neon: "Bright Neon", colorful: "Vibrant & Colorful", chalkboard: "Classic Chalkboard" },
    aspects: { "16:9": "Horizontal (YouTube)", "9:16": "Vertical (TikTok/Reels)" },
    navHome: "Home",
    navAbout: "About",
    aboutTitle: "About EduMotion AI",
    aboutDesc: "A cutting-edge AI-powered platform aimed at simplifying the creation of educational content for teachers, lecturers, and creators.",
    aboutTech: "Core Technologies:",
    aboutTech1: "Relies on the Manim engine to generate mathematically precise, high-quality animations.",
    aboutTech2: "Utilizes Google's Gemini 2.0 Flash capabilities to rapidly and automatically write underlying code.",
    aboutTech3: "The UI is built on React & TailwindCSS for a seamless, modern experience.",
    aboutDevText: "This project was developed by an AI & tech enthusiast with the goal of enriching Arabic educational content and expediting its production.",
  }
};

export default function App() {
  const [lang, setLang] = useState(() => loadPref('lang', 'en'));
  const [darkMode, setDarkMode] = useState(() => loadPref('dark', false));
  const [currentPage, setCurrentPage] = useState('home');
  
  const [topic, setTopic] = useState('');
  const [loading, setLoading] = useState(false);
  const [videoUrl, setVideoUrl] = useState('');
  const [error, setError] = useState(null);
  
  // Configuration Options — restored from cookies
  const [duration, setDuration]       = useState(() => loadPref('duration', 15));
  const [style, setStyle]             = useState(() => loadPref('style', 'minimalist'));
  const [aspectRatio, setAspectRatio] = useState(() => loadPref('aspect', '16:9'));
  const [voiceEnabled, setVoiceEnabled] = useState(() => loadPref('voice', false));
  const [voiceGender, setVoiceGender] = useState(() => loadPref('gender', 'female'));

  // Persist settings to cookies whenever they change
  useEffect(() => savePref('lang',     lang),        [lang]);
  useEffect(() => savePref('dark',     darkMode),    [darkMode]);
  useEffect(() => savePref('duration', duration),    [duration]);
  useEffect(() => savePref('style',    style),       [style]);
  useEffect(() => savePref('aspect',   aspectRatio), [aspectRatio]);
  useEffect(() => savePref('voice',    voiceEnabled),[voiceEnabled]);
  useEffect(() => savePref('gender',   voiceGender), [voiceGender]);

  const t = DICT[lang];
  const isRtl = lang === 'ar';

  useEffect(() => {
    document.documentElement.dir = isRtl ? 'rtl' : 'ltr';
    // Cairo is elegant for Arabic, Inter for English
    document.documentElement.style.fontFamily = isRtl ? "'Cairo', sans-serif" : "'Inter', sans-serif";
  }, [isRtl]);

  useEffect(() => {
    if (darkMode) {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }
  }, [darkMode]);

  const handleGenerate = async (e) => {
    if (e) e.preventDefault();
    if (!topic.trim() || loading) return;
    
    setLoading(true);
    setError(null);
    setVideoUrl('');

    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 480000); // 8 min timeout

    try {
      const res = await fetch(`${API_BASE}/generate`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        signal: controller.signal,
        body: JSON.stringify({ 
          topic, 
          language: lang,
          duration,
          style,
          aspect_ratio: aspectRatio,
          voice_enabled: voiceEnabled,
          voice_gender: voiceGender,
        }),
      });
      clearTimeout(timeoutId);
      if (!res.ok) {
        const err = await res.json().catch(() => ({ detail: `Server error ${res.status}` }));
        throw new Error(err.detail || `Server error ${res.status}`);
      }
      const data = await res.json();
      setVideoUrl(`${API_BASE}${data.video_url}`);
    } catch (err) {
      clearTimeout(timeoutId);
      if (err.name === 'AbortError') {
        setError('Request timed out after 8 minutes. The server may be busy — please try again.');
      } else if (err.message === 'Failed to fetch' || err.message === 'NetworkError when attempting to fetch resource.') {
        setError('Cannot connect to the backend. Make sure the server is running on port 8000.');
      } else {
        // Show the actual server error message
        setError(err.message);
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className={`min-h-screen relative overflow-hidden transition-colors duration-500`}>
      
      {/* Background Decorative Blobs */}
      <div className="absolute top-0 left-0 w-full h-full overflow-hidden -z-10 bg-slate-50 dark:bg-slate-900 transition-colors duration-500">
        <div className="absolute top-[-10%] left-[-10%] w-96 h-96 rounded-full bg-blue-200/40 dark:bg-blue-900/40 mix-blend-multiply dark:mix-blend-screen filter blur-3xl opacity-70 animate-blob"></div>
        <div className="absolute top-[20%] right-[-10%] w-96 h-96 rounded-full bg-purple-200/40 dark:bg-purple-900/40 mix-blend-multiply dark:mix-blend-screen filter blur-3xl opacity-70 animate-blob animation-delay-2000"></div>
        <div className="absolute bottom-[-10%] left-[20%] w-96 h-96 rounded-full bg-pink-200/40 dark:bg-pink-900/40 mix-blend-multiply dark:mix-blend-screen filter blur-3xl opacity-70 animate-blob animation-delay-4000"></div>
      </div>

      {/* Header */}
      <header className="fixed top-0 w-full backdrop-blur-xl bg-white/70 dark:bg-slate-900/70 border-b border-white/20 dark:border-slate-800/50 z-50 shadow-sm transition-colors duration-500">
        <div className="max-w-6xl mx-auto px-6 h-16 flex items-center justify-between">
          <div className="flex items-center gap-6">
            <div className="flex items-center gap-2 cursor-pointer" onClick={() => setCurrentPage('home')}>
              <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-blue-600 to-indigo-600 shadow-lg shadow-indigo-500/30 flex items-center justify-center text-white">
                <PlayCircle className="w-6 h-6" />
              </div>
              {/* Brand Name always in English despite language toggle */}
              <span className="text-xl font-bold tracking-tight text-slate-800 dark:text-white font-[Inter]" dir="ltr">
                Edu<span className="text-indigo-600 dark:text-indigo-400">Motion</span>
              </span>
            </div>

            <nav className="hidden md:flex items-center gap-2">
              <button onClick={() => setCurrentPage('home')} className={`px-4 py-2 rounded-full text-sm font-semibold transition-colors ${currentPage === 'home' ? 'bg-indigo-50 dark:bg-indigo-900/30 text-indigo-600 dark:text-indigo-400' : 'text-slate-600 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-800'}`}>
                {t.navHome}
              </button>
              <button onClick={() => setCurrentPage('about')} className={`px-4 py-2 rounded-full text-sm font-semibold transition-colors ${currentPage === 'about' ? 'bg-indigo-50 dark:bg-indigo-900/30 text-indigo-600 dark:text-indigo-400' : 'text-slate-600 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-800'}`}>
                {t.navAbout}
              </button>
            </nav>
          </div>

          <div className="flex items-center gap-2">
            <button 
              onClick={() => setDarkMode(!darkMode)}
              className="p-2 rounded-full hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors text-slate-600 dark:text-slate-300"
            >
              {darkMode ? <Sun className="w-5 h-5" /> : <Moon className="w-5 h-5" />}
            </button>
            <button 
              onClick={() => setLang(lang === 'ar' ? 'en' : 'ar')}
              className="flex items-center gap-2 px-4 py-2 rounded-full hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors text-sm font-semibold text-slate-600 dark:text-slate-300"
            >
              <Globe className="w-4 h-4" />
              {lang === 'ar' ? 'English' : 'عربي'}
            </button>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className={`relative z-10 pt-32 pb-20 px-6 mx-auto ${currentPage === 'about' ? 'max-w-4xl flex flex-col items-center' : 'max-w-7xl grid grid-cols-1 lg:grid-cols-2 gap-12 lg:gap-16 items-start lg:pt-40'}`}>
        
        {currentPage === 'about' ? (
          <motion.div 
            initial={{ opacity: 0, scale: 0.95 }} animate={{ opacity: 1, scale: 1 }}
            className="w-full bg-white/80 dark:bg-slate-800/80 backdrop-blur-xl border border-slate-200 dark:border-slate-700/50 p-8 md:p-12 rounded-3xl shadow-xl"
          >
            <div className="flex items-center gap-3 mb-6 text-indigo-600 dark:text-indigo-400">
              <Info className="w-8 h-8" />
              <h2 className="text-3xl font-bold dark:text-white">{t.aboutTitle}</h2>
            </div>
            <p className="text-lg text-slate-600 dark:text-slate-300 leading-relaxed mb-8">
              {t.aboutDesc}
            </p>
            
            <h3 className="text-xl font-bold text-slate-800 dark:text-white mb-4">{t.aboutTech}</h3>
            <ul className="space-y-4 mb-10 text-slate-600 dark:text-slate-300">
              <li className="flex items-start gap-3">
                <CheckCircle2 className="w-6 h-6 text-emerald-500 flex-shrink-0" />
                <span>{t.aboutTech1}</span>
              </li>
              <li className="flex items-start gap-3">
                <CheckCircle2 className="w-6 h-6 text-emerald-500 flex-shrink-0" />
                <span>{t.aboutTech2}</span>
              </li>
              <li className="flex items-start gap-3">
                <CheckCircle2 className="w-6 h-6 text-emerald-500 flex-shrink-0" />
                <span>{t.aboutTech3}</span>
              </li>
            </ul>

            <div className="bg-indigo-50 dark:bg-indigo-900/20 rounded-2xl p-6 border border-indigo-100 dark:border-indigo-800/50">
              <p className="text-indigo-900 dark:text-indigo-200 font-semibold leading-relaxed">
                {t.aboutDevText}
              </p>
            </div>
          </motion.div>
        ) : (
          <>
            <motion.div 
              initial={{ opacity: 0, x: isRtl ? 20 : -20 }}
              animate={{ opacity: 1, x: 0 }}
              className={`w-full ${isRtl ? 'text-right' : 'text-left'}`}
            >
              <h1 className="text-4xl md:text-6xl font-extrabold text-slate-900 dark:text-white tracking-tight leading-tight mb-4">
                {isRtl ? 'اصنع' : 'Create'} <span className="text-transparent bg-clip-text bg-gradient-to-r from-blue-600 to-indigo-600 dark:from-blue-400 dark:to-indigo-400">
                  {isRtl ? 'المحتوى التعليمي' : 'Educational Content'}
                </span> <br />
                {isRtl ? 'بسرعة الخيال' : 'at the speed of thought'}
              </h1>
              <p className="text-lg text-slate-500 dark:text-slate-400 mb-10 max-w-xl">
                {t.subtitle}
              </p>

              <form onSubmit={handleGenerate} className="w-full relative z-10 flex flex-col gap-4">
                <div className="relative group bg-white dark:bg-slate-800 rounded-3xl p-2 shadow-[0_8px_30px_rgb(0,0,0,0.04)] dark:shadow-none border border-slate-200/60 dark:border-slate-700/50 backdrop-blur-xl transition-all focus-within:shadow-[0_8px_30px_rgba(99,102,241,0.15)] focus-within:border-indigo-300 dark:focus-within:border-indigo-500">
                  <textarea
                    className="w-full bg-transparent border-none outline-none resize-none p-5 text-lg text-slate-800 dark:text-white placeholder-slate-400 min-h-[120px]"
                    placeholder={t.placeholder}
                    value={topic}
                    onChange={(e) => setTopic(e.target.value)}
                    disabled={loading}
                  />
                  
                  <div className="flex items-center justify-between px-4 pb-2 border-t border-slate-100 dark:border-slate-700 pt-3">
                    <div></div>
                    <button
                      type="submit"
                      disabled={loading || !topic.trim()}
                      className="flex items-center gap-2 bg-slate-900 dark:bg-indigo-600 hover:bg-indigo-600 dark:hover:bg-indigo-500 text-white px-6 py-2.5 rounded-full font-semibold transition-all shadow-md disabled:opacity-50 disabled:hover:bg-slate-900 dark:disabled:hover:bg-indigo-600"
                    >
                      {loading ? (
                        <motion.div animate={{ rotate: 360 }} transition={{ repeat: Infinity, ease: "linear", duration: 1 }}>
                          <RotateCw className="w-5 h-5" />
                        </motion.div>
                      ) : (
                        <Wand2 className="w-5 h-5" />
                      )}
                      {loading ? t.generating : t.generate}
                    </button>
                  </div>
                </div>

                <div className="grid grid-cols-2 md:grid-cols-4 gap-3 mt-2">
                  <div className="bg-white/60 dark:bg-slate-800/60 backdrop-blur-md rounded-2xl p-4 border border-slate-200 dark:border-slate-700">
                    <div className="flex items-center gap-2 text-slate-700 dark:text-slate-300 mb-3 text-sm font-semibold">
                      <Clock className="w-4 h-4 text-indigo-500" /> {t.duration}
                    </div>
                    <input 
                      type="range" 
                      min="5" max="30" step="5"
                      value={duration}
                      onChange={(e) => setDuration(e.target.value)}
                      className="w-full accent-indigo-600 dark:accent-indigo-400"
                    />
                    <div className="text-center text-xs font-bold text-slate-500 dark:text-slate-400 mt-1">{duration}s</div>
                  </div>

                  <div className="bg-white/60 dark:bg-slate-800/60 backdrop-blur-md rounded-2xl p-4 border border-slate-200 dark:border-slate-700">
                    <div className="flex items-center gap-2 text-slate-700 dark:text-slate-300 mb-3 text-sm font-semibold">
                      <Palette className="w-4 h-4 text-pink-500" /> {t.style}
                    </div>
                    <select 
                      value={style} onChange={(e) => setStyle(e.target.value)}
                      className="w-full bg-slate-50 dark:bg-slate-900 border border-slate-200 dark:border-slate-700 rounded-lg p-1.5 text-xs font-medium text-slate-700 dark:text-slate-300 outline-none"
                    >
                      <option value="minimalist">{t.styles.minimalist}</option>
                      <option value="neon">{t.styles.neon}</option>
                      <option value="colorful">{t.styles.colorful}</option>
                      <option value="chalkboard">{t.styles.chalkboard}</option>
                    </select>
                  </div>

                  <div className="bg-white/60 dark:bg-slate-800/60 backdrop-blur-md rounded-2xl p-4 border border-slate-200 dark:border-slate-700">
                    <div className="flex items-center gap-2 text-slate-700 dark:text-slate-300 mb-3 text-sm font-semibold">
                      <Layout className="w-4 h-4 text-blue-500" /> {t.aspectRatio}
                    </div>
                    <select 
                      value={aspectRatio} onChange={(e) => setAspectRatio(e.target.value)}
                      className="w-full bg-slate-50 dark:bg-slate-900 border border-slate-200 dark:border-slate-700 rounded-lg p-1.5 text-xs font-medium text-slate-700 dark:text-slate-300 outline-none"
                    >
                      <option value="16:9">{t.aspects["16:9"]}</option>
                      <option value="9:16">{t.aspects["9:16"]}</option>
                    </select>
                  </div>

                  <div className="bg-white/60 dark:bg-slate-800/60 backdrop-blur-md rounded-2xl p-4 border border-slate-200 dark:border-slate-700 flex flex-col justify-between">
                    <div className="flex items-center justify-between text-slate-700 dark:text-slate-300 text-sm font-semibold">
                      <span className="flex items-center gap-2"><Video className="w-4 h-4 text-emerald-500" /> {t.voiceover}</span>
                    </div>
                    {/* ON / OFF toggle */}
                    <button 
                      type="button"
                      onClick={() => setVoiceEnabled(!voiceEnabled)}
                      className={`mt-2 py-1.5 rounded-lg text-xs font-bold transition-colors border ${voiceEnabled ? 'bg-emerald-50 dark:bg-emerald-900/30 text-emerald-600 dark:text-emerald-400 border-emerald-200 dark:border-emerald-800' : 'bg-slate-50 dark:bg-slate-900 text-slate-400 border-slate-200 dark:border-slate-700'}`}
                    >
                      {voiceEnabled ? '🎙️ ON' : 'OFF'}
                    </button>
                    {/* Gender selector — shown only when voice is ON */}
                    {voiceEnabled && (
                      <div className="flex gap-1 mt-2">
                        <button
                          type="button"
                          onClick={() => setVoiceGender('female')}
                          className={`flex-1 py-1 rounded-md text-xs font-bold border transition-colors ${voiceGender === 'female' ? 'bg-pink-50 dark:bg-pink-900/30 text-pink-600 border-pink-300' : 'bg-slate-50 dark:bg-slate-900 text-slate-400 border-slate-200 dark:border-slate-700'}`}
                        >♀ {lang === 'ar' ? 'أنثى' : 'Female'}</button>
                        <button
                          type="button"
                          onClick={() => setVoiceGender('male')}
                          className={`flex-1 py-1 rounded-md text-xs font-bold border transition-colors ${voiceGender === 'male' ? 'bg-blue-50 dark:bg-blue-900/30 text-blue-600 border-blue-300' : 'bg-slate-50 dark:bg-slate-900 text-slate-400 border-slate-200 dark:border-slate-700'}`}
                        >♂ {lang === 'ar' ? 'ذكر' : 'Male'}</button>
                      </div>
                    )}
                  </div>
                </div>
              </form>

              <div className="mt-8 flex flex-col sm:flex-row sm:items-center gap-3">
                <span className="text-sm font-semibold text-slate-500 flex items-center gap-1.5">
                  <Sparkles className="w-4 h-4 text-amber-500" />
                  {t.tryAlso}
                </span>
                <div className="flex flex-wrap gap-2">
                  {EXAMPLES[lang].map((ex, i) => (
                    <button 
                      key={i} 
                      onClick={() => { setTopic(ex); setVideoUrl(''); setError(null); }}
                      className="group px-3 py-1.5 rounded-lg bg-white dark:bg-slate-800/80 border border-slate-200 dark:border-slate-700 text-xs font-medium text-slate-600 dark:text-slate-300 hover:border-indigo-400 hover:bg-indigo-50/50 dark:hover:bg-indigo-500/10 dark:hover:border-indigo-500 hover:text-indigo-700 dark:hover:text-indigo-300 transition-all shadow-sm"
                    >
                      <span className="opacity-70 group-hover:opacity-100 transition-opacity me-1.5">›</span>
                      {ex}
                    </button>
                  ))}
                </div>
              </div>

              {/* GENERATION INLINE RESULT */}
              <AnimatePresence>
                {(loading || error || videoUrl) && (
                  <motion.div 
                    initial={{ opacity: 0, y: 15 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0, y: 15 }}
                    className="mt-8 relative w-full bg-white dark:bg-slate-800 rounded-2xl shadow-xl overflow-hidden border border-slate-200 dark:border-slate-700 flex flex-col"
                  >
                      <div className="px-5 py-3 border-b border-slate-100 dark:border-slate-700/50 flex items-center justify-between bg-slate-50/50 dark:bg-slate-900/50">
                        <div className="flex items-center gap-3">
                          {error ? (
                              <AlertCircle className="w-5 h-5 text-red-500" />
                          ) : loading ? (
                              <RotateCw className="w-5 h-5 text-indigo-500 min-w-5 animate-spin" />
                          ) : (
                              <CheckCircle2 className="w-5 h-5 text-emerald-500" />
                          )}
                          <h2 className="text-sm font-bold text-slate-800 dark:text-white">
                            {error ? "Error" : loading ? t.generating : t.success}
                          </h2>
                        </div>
                        {!loading && (
                          <button onClick={() => { setError(null); setVideoUrl(''); }} className="text-slate-400 hover:text-slate-600 dark:hover:text-slate-200">
                            <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" /></svg>
                          </button>
                        )}
                      </div>

                      <div className="p-4 overflow-y-auto max-h-[60vh]">
                          {error ? (
                              <div className="bg-red-50 dark:bg-red-900/20 text-red-600 dark:text-red-400 p-4 rounded-xl text-xs font-medium break-words" dir="ltr">
                                {error}
                              </div>
                          ) : loading ? (
                              <div className="flex flex-col items-center justify-center py-6">
                                <div className="flex gap-2 mb-4">
                                  <motion.div animate={{ scale: [1, 1.5, 1] }} transition={{ repeat: Infinity, duration: 1, delay: 0 }} className="w-2.5 h-2.5 rounded-full bg-indigo-500" />
                                  <motion.div animate={{ scale: [1, 1.5, 1] }} transition={{ repeat: Infinity, duration: 1, delay: 0.2 }} className="w-2.5 h-2.5 rounded-full bg-purple-500" />
                                  <motion.div animate={{ scale: [1, 1.5, 1] }} transition={{ repeat: Infinity, duration: 1, delay: 0.4 }} className="w-2.5 h-2.5 rounded-full bg-pink-500" />
                                </div>
                                <p className="text-slate-500 dark:text-slate-400 text-xs py-2 text-center">
                                  {lang === 'ar' ? 'يتم الإنشاء بسرعة... يرجى الانتظار.' : 'Generating video rapidly... Please wait.'}
                                </p>
                                <div className="w-full max-w-[200px] h-1.5 bg-slate-100 dark:bg-slate-700 rounded-full mt-2 overflow-hidden">
                                  <motion.div 
                                    initial={{ width: "0%" }} animate={{ width: ["20%", "80%", "100%"] }} transition={{ duration: 7, ease: "linear" }}
                                    className="h-full bg-gradient-to-r from-indigo-500 via-purple-500 to-pink-500"
                                  />
                                </div>
                              </div>
                          ) : (
                              <div>
                                <div className="bg-slate-100 dark:bg-black rounded-lg overflow-hidden aspect-[16/9] flex items-center justify-center border border-slate-200 dark:border-slate-800">
                                  <video src={videoUrl} controls autoPlay className="w-full h-full object-contain" />
                                </div>
                                <div className="mt-4 flex justify-end">
                                  <a 
                                    href={videoUrl} download
                                    className="flex items-center justify-center gap-2 bg-indigo-600 dark:bg-indigo-500 text-white px-4 py-2.5 rounded-lg font-semibold text-xs hover:bg-indigo-700 dark:hover:bg-indigo-400 transition-colors shadow-sm"
                                  >
                                    <Download className="w-4 h-4" /> {t.download}
                                  </a>
                                </div>
                              </div>
                          )}
                      </div>
                  </motion.div>
                )}
              </AnimatePresence>

            </motion.div>

            {/* Isometric Video Presentation Container */}
            <div className="relative w-full aspect-square md:aspect-auto md:h-full flex items-start justify-center [perspective:1400px] mt-10 lg:mt-0 xl:-ml-10">
              
              <motion.div 
                initial={{ opacity: 0, rotateX: 0, rotateY: isRtl ? 25 : -25, rotateZ: 0, scale: 0.9, y: 30 }}
                animate={{ opacity: 1, rotateX: 0, rotateY: isRtl ? 15 : -15, rotateZ: 0, scale: 1, y: -40 }}
                transition={{ duration: 1.2, ease: "easeOut" }}
                style={{ transformStyle: 'preserve-3d' }}
                className="relative w-full max-w-lg flex flex-col items-center justify-center 2xl:scale-110 origin-top"
              >
                  {/* Decorative background shape mimicking a modern glass block */}
                  <div 
                    className="absolute -top-12 -right-12 md:-top-20 md:-right-20 w-64 h-64 md:w-80 md:h-80 bg-gradient-to-br from-amber-400 to-pink-500 rounded-[4rem] shadow-2xl opacity-60 z-0 blur-2xl"
                    style={{ transform: "translateZ(-120px)" }}
                  ></div>
                  <div 
                    className="absolute top-10 -left-10 w-40 h-40 bg-gradient-to-tr from-indigo-500 to-purple-500 rounded-full shadow-2xl opacity-50 z-0 blur-3xl"
                    style={{ transform: "translateZ(-80px)" }}
                  ></div>
                  
                  {/* Outer Glass Plate for layered effect */}
                  <div 
                    className="absolute inset-0 bg-white/20 dark:bg-slate-800/20 backdrop-blur-3xl rounded-[2.5rem] border border-white/40 dark:border-slate-600/40 shadow-[0_0_80px_rgba(0,0,0,0.1)] dark:shadow-[0_0_80px_rgba(0,0,0,0.4)]"
                    style={{ transform: "translateZ(-20px) scale(1.05)" }}
                  ></div>

                  {/* Main Isometric Card */}
                  <div 
                    className="relative z-10 w-full bg-white/95 dark:bg-slate-900/90 rounded-3xl shadow-[10px_30px_60px_rgba(0,0,0,0.2)] dark:shadow-[10px_30px_60px_rgba(0,0,0,0.7)] border border-white dark:border-slate-700/80 backdrop-blur-2xl flex flex-col overflow-hidden"
                    style={{ transform: "translateZ(40px)" }}
                  >
                    {/* Glowing highlight line at the top */}
                    <div className="absolute top-0 left-0 right-0 h-1 bg-gradient-to-r from-indigo-500 via-purple-500 to-pink-500 opacity-80"></div>
                    
                    <div className="px-6 py-5 border-b border-slate-100 dark:border-slate-800 flex items-center justify-between bg-slate-50/50 dark:bg-slate-900/30">
                      <div className="flex items-center gap-3">
                        <div className="w-8 h-8 rounded-full bg-indigo-100 dark:bg-indigo-500/20 flex items-center justify-center">
                          <Video className="w-4 h-4 text-indigo-600 dark:text-indigo-400" />
                        </div>
                        <h2 className="text-sm font-bold text-slate-800 dark:text-white tracking-wide">
                          {t.sampleVideoLabel}
                        </h2>
                      </div>
                      
                      {/* Decorative dots to simulate OS window controls */}
                      <div className="flex gap-1.5" dir="ltr">
                        <div className="w-2.5 h-2.5 rounded-full bg-slate-300 dark:bg-slate-600"></div>
                        <div className="w-2.5 h-2.5 rounded-full bg-slate-300 dark:bg-slate-600"></div>
                        <div className="w-2.5 h-2.5 rounded-full bg-slate-300 dark:bg-slate-600"></div>
                      </div>
                    </div>

                    <div className="p-6 relative">
                      <div className="absolute inset-0 bg-grid-slate-100/[0.05] dark:bg-grid-slate-800/[0.05] bg-[size:16px_16px] z-0"></div>
                      <div className="relative z-10 bg-black rounded-2xl overflow-hidden shadow-2xl aspect-[16/9] ring-2 ring-slate-900/10 dark:ring-white/10 group cursor-default">
                        <div className="absolute inset-0 bg-gradient-to-t from-slate-900/40 to-transparent z-10 pointer-events-none opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>
                        <video src={SAMPLE_VIDEO} autoPlay loop muted playsInline className="w-full h-full object-cover pointer-events-none select-none rounded-2xl" />
                      </div>
                    </div>
                  </div>
              </motion.div>
            </div>
          </>
        )}
      </main>

      {/* Generation Status / Result Modal */}


      {/* Footer */}
      <footer className="absolute bottom-6 w-full text-center text-xs font-semibold text-slate-400 dark:text-slate-500">
        {t.footer}
      </footer>
    </div>
  );
}
