# OSINT Dark Web Scraper Microservice

This microservice provides dark web scraping, monitoring, and keyword search as part of the larger OSINT Platform.
It is built with FastAPI + Celery + Redis + Tor for asynchronous scraping and API integration.

# Setup
# Local Development
clone repo
```
git clone https://github.com/your-org/osint-scraper.git
cd osint-scraper
```
create venv
```
python3 -m venv venv
source venv/bin/activate
```

install deps
```
pip install -r requirements.txt
```

Start FastAPI app:
```
uvicorn app.main:app --reload
```

Start Celery worker:
```
celery -A worker.app worker --loglevel=info
```

# Docker + Compose (Recommended)
```
docker-compose up --build
```

This runs:

=>FastAPI at http://localhost:8000
=>Redis (broker + result backend)
=>Tor service (SOCKS5 proxy at tor:9050)

Celery worker can be scaled with:
```
docker-compose up --scale worker=3
```

# API Endpoints

# Search
```
POST /search
{
  "keywords": ["bitcoin", "leak", "credentials"]
}
```

#Response:
```
{ "status": "submitted" }
```

# Monitor
```
POST /monitor
{
  "query": "ransomware"
}
```

# Results
```
GET /results
```

Returns mock results (replace with DB lookup later).

#Celery Tasks

=>search_tasks.run_search(keywords) → Perform dark web keyword search
=>monitor_tasks.monitor(query) → Periodically scrape sources and alert

# Tor Integration

All requests go through Tor SOCKS5 proxy with retry + backoff + opsec delays.
You can trigger new Tor identity with:
```
from app.utils.tor_client import TorSession
TorSession.new_identity()
```
# Alerts

Alerts module (app/utils/alerts.py) is a stub. Extend it to:
=>Send email
=>Push to Slack/Discord
=>Trigger webhook


# Development Notes

=>Never log scraped PII/content → logger only stores operational metadata.
=>Use config.py to override defaults via environment variables.
=>Designed as a plug-and-play microservice inside bigger OSINT system.
