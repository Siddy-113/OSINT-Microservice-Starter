import os

# Redis / Celery
REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379/0")
CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL", REDIS_URL)
CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND", REDIS_URL)

# Tor (use service name "tor" in docker-compose)
TOR_SOCKS_HOST = os.getenv("TOR_SOCKS_HOST", "tor")
TOR_SOCKS_PORT = int(os.getenv("TOR_SOCKS_PORT", "9050"))
TOR_CONTROL_HOST = os.getenv("TOR_CONTROL_HOST", "tor")
TOR_CONTROL_PORT = int(os.getenv("TOR_CONTROL_PORT", "9051"))
TOR_CONTROL_PASSWORD = os.getenv("TOR_CONTROL_PASSWORD", "changeme")

# Request behavior and OPSEC
MIN_REQUEST_DELAY_SEC = float(os.getenv("MIN_REQUEST_DELAY_SEC", "2.0"))
MAX_REQUEST_DELAY_SEC = float(os.getenv("MAX_REQUEST_DELAY_SEC", "6.0"))
MAX_RETRIES = int(os.getenv("MAX_RETRIES", "3"))
REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", "30"))

# Scraper safety
MAX_PAGES_PER_JOB = int(os.getenv("MAX_PAGES_PER_JOB", "50"))
DEFAULT_KEYWORDS = os.getenv("DEFAULT_KEYWORDS", "market,breach,leak").split(",")

# Service metadata
SERVICE_NAME = os.getenv("SERVICE_NAME", "darkweb-scraper")
ENVIRONMENT = os.getenv("ENVIRONMENT", "dev")
