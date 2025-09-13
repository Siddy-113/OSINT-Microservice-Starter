import os

# Load from environment (safe defaults for local dev)
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

# Celery
CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL", REDIS_URL)
CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND", REDIS_URL)

# Tor (SOCKS5 proxy + control)
TOR_SOCKS_HOST = os.getenv("TOR_SOCKS_HOST", "tor")              # "127.0.0.1" if running locally without docker
TOR_SOCKS_PORT = int(os.getenv("TOR_SOCKS_PORT", "9050"))
TOR_CONTROL_HOST = os.getenv("TOR_CONTROL_HOST", "tor")
TOR_CONTROL_PORT = int(os.getenv("TOR_CONTROL_PORT", "9051"))
TOR_CONTROL_PASSWORD = os.getenv("TOR_CONTROL_PASSWORD", "changeme")  # set via docker-compose

# OPSEC / scraping behavior
MIN_REQUEST_DELAY_SEC = float(os.getenv("MIN_REQUEST_DELAY_SEC", "2.0"))
MAX_REQUEST_DELAY_SEC = float(os.getenv("MAX_REQUEST_DELAY_SEC", "6.0"))
MAX_RETRIES = int(os.getenv("MAX_RETRIES", "3"))
REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", "30"))

# Service metadata
SERVICE_NAME = "darkweb-scraper"
ENVIRONMENT = os.getenv("ENVIRONMENT", "dev")

