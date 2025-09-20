from app.logger import log

def alert_hit(payload: dict):
    # placeholder: send to central system (webhook/SIEM). Do NOT include scraped PII in logs.
    log.info("alert_triggered", extra={"task_id": payload.get("task_id"), "source": payload.get("source_url")})
