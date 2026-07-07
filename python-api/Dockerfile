FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /app
RUN apt-get update && apt-get install -y \
    # Для компиляции некоторых Python пакетов
    gcc \
    # Для работы с изображениями в matplotlib
    libpng-dev \
    # Для работы со шрифтами
    libfreetype6-dev \
    # Для работы с PDF (reportlab)
    libjpeg-dev \
    # Чистим кэш для уменьшения размера образа
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt
COPY ./app ./app
RUN mkdir -p uploads results

EXPOSE=8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]