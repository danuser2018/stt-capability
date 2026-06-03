FROM python:3.12-slim

WORKDIR /app

# Install system dependencies required by faster-whisper and audio processing
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY ./app /app/app

# Set default environment variables
ENV PORT=8000
ENV WHISPER_MODEL=base
ENV WHISPER_DEVICE=cpu
ENV LOG_LEVEL=INFO

EXPOSE $PORT

CMD uvicorn app.main:app --host 0.0.0.0 --port $PORT
