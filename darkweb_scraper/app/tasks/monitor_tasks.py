from app.worker import celery
from app.utils.logger import log
from app.scraping.forum_scraper import ForumScraper
from app.scraping.marketplace_scraper import MarketplaceScraper
from app.scraping.paste_scraper import PasteScraper

TARGETS = {
    "forum": [
        # "http://<redacted>.onion/subforum/..."
    ],
    "marketplace": [
        # "http://<redacted>.onion/listings"
    ],
    "paste_site": [
        # "http://<redacted>.onion/paste/..."
    ],
}

@celery.task(bind=True)
def monitor_keywords(self, keywords: list[str]):
    """
    One-shot execution for demo. In production, run on a schedule/beat.
    """
    log.info("task_monitor_keywords", extra={"task_id": self.request.id, "keywords_count": len(keywords)})
    results = []

    forum = ForumScraper()
    market = MarketplaceScraper()
    paste = PasteScraper()

    for url in TARGETS.get("forum", []):
        results.extend(forum.scrape_for_keywords(url, keywords))
    for url in TARGETS.get("marketplace", []):
        results.extend(market.scrape_listings_for_keywords(url, keywords))
    for url in TARGETS.get("paste_site", []):
        results.extend(paste.scrape_paste_for_keywords(url, keywords))

    return {
        "status": "complete",
        "keywords": keywords,
        "hits": results
    }

