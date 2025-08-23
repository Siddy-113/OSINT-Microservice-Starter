import os

# Redis / Celery settings
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

# Celery config
CELERY_BROKER_URL = REDIS_URL
CELERY_RESULT_BACKEND = REDIS_URL
