FROM python:3.10-slim

# إعداد البيئة الأساسية
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# تثبيت متطلبات النظام الأساسية لـ FFmpeg و Manim
RUN apt-get update && apt-get install -y \
    ffmpeg \
    libcairo2-dev \
    libpango1.0-dev \
    texlive \
    texlive-latex-extra \
    texlive-fonts-extra \
    texlive-latex-recommended \
    && rm -rf /var/lib/apt/lists/*

# إضافة مستخدم بصلاحيات محدودة (مطلب أساسي من Hugging Face)
RUN useradd -m -u 1000 user
USER user
ENV HOME=/home/user \
    PATH=/home/user/.local/bin:$PATH

# ضبط مجلد العمل الرئيسي
WORKDIR $HOME/app

# نسخ ملفات المتطلبات وتثبيت الحزم
COPY --chown=user requirements.txt .
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# إنشاء المجلدات المطلوبة قبل بدء التشغيل
RUN mkdir -p $HOME/app/scenes $HOME/app/media/videos

# نسخ باقي مجلد الباك-إند
COPY --chown=user . .

# كشف بورت 7860 الذي تعتمده Hugging Face
EXPOSE 7860

# تشغيل خادم Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]
