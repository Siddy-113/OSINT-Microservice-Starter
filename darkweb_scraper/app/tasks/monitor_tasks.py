from app.worker import celery
import time

@celery.task(bind=True)
def monitor_keywords(self, keywords: list[str]):
    # Simulate monitoring
    time.sleep(3)
    return {
        "status": "complete",
        "keywords": keywords,
        "hits": [
            {
                "source_url": "http://pasteonion.onion/paste/abc",
                "source_type": "paste_site",
                "capture_timestamp": "2025-08-23T12:30:00Z",
                "match_type": "keyword_match",
                "matched_keyword": keywords[0],
                "content_snippet": "This paste contains Aadhaar numbers...",
                "author_username": "anonymous",
                "post_url": "http://pasteonion.onion/paste/abc"
            }
        ]
    }
