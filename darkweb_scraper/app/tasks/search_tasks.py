from app.worker import celery
import time

@celery.task(bind=True)
def run_search(self, identifier_type: str, identifier_value: str):
    # Simulate a heavy scraping task
    time.sleep(5)
    return {
        "status": "complete",
        "identifier_type": identifier_type,
        "identifier_value": identifier_value,
        "results": [
            {
                "source_url": "http://exampleonion.onion/post/123",
                "source_type": "forum",
                "capture_timestamp": "2025-08-23T12:00:00Z",
                "match_type": "targeted_search_hit",
                "matched_keyword": identifier_value,
                "content_snippet": "Leaked data mentioning this identifier...",
                "author_username": "darkuser123",
                "post_url": "http://exampleonion.onion/post/123"
            }
        ]
    }
