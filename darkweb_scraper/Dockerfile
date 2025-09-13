FROM python:3.11-slim

# System hardening basics
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Minimal OS deps (no browsers)
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc curl ca-certificates \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /srv/app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Create non-root user
RUN useradd -m appuser
USER appuser

COPY app ./app
COPY worker.py ./worker.py

# Default command is uvicorn; worker will override in docker-compose
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

