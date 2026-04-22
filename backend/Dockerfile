# استخدم نسخة بايثون خفيفة
FROM python:3.10-slim

# منع بايثون من كتابة ملفات التخزين المؤقت
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# تعيين مجلد العمل
WORKDIR /app

# تثبيت متطلبات النظام الأساسية لـ Manim و FFmpeg
RUN apt-get update && apt-get install -y \
    build-essential \
    pkg-config \
    ffmpeg \
    libcairo2-dev \
    libpango1.0-dev \
    texlive \
    texlive-latex-extra \
    texlive-fonts-extra \
    texlive-latex-recommended \
    && rm -rf /var/lib/apt/lists/*

# نسخ متطلبات بايثون وتثبيتها
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# إنشاء المجلدات المطلوبة للسكربتات والفيديوهات
RUN mkdir -p /app/scenes /app/media/videos

# نسخ باقي ملفات الباك-إند
COPY . .

# السماح للاتصال عبر بورت 8000
EXPOSE 8000

# تشغيل خادم Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
