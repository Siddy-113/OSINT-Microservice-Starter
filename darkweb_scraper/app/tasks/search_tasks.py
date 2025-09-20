from worker import celery
from app.logger import log
from app.scraping.forum_scraper import ForumScraper
from app.scraping.marketplace_scraper import MarketplaceScraper
from app.scraping.paste_scraper import PasteScraper
from app.config import DEFAULT_KEYWORDS
import time

# TARGETS is intentionally empty; configure your .onion targets via secure config/store
TARGETS = {
    "forum": [],         # e.g. ["http://exampleonion.onion/forum/"]
    "marketplace": [],   # e.g. ["http://exampleonion.onion/market/"]
    "paste_site": []     # e.g. ["http://exampleonion.onion/paste/"]
}

@celery.task(bind=True)
def run_search(self, identifier_type: str, identifier_value: str):
    log.info("run_search_started", extra={"task_id": self.request.id, "type": identifier_type})
    results = []

    # create scrapers
    forum = ForumScraper()
    market = MarketplaceScraper()
    paste = PasteScraper()

    # scan forums
    for url in TARGETS.get("forum", []):
        try:
            hits = forum.scrape_target_identifier(url, identifier_value)
            results.extend(hits)
        except Exception as e:
            log.warning("forum_scan_error", extra={"url": url, "err": str(e)})

    # scan marketplaces
    for url in TARGETS.get("marketplace", []):
        try:
            hits = market.scrape_listings_for_keywords(url, [identifier_value])
            # mark as targeted hit
            for h in hits:
                h["match_type"] = "targeted_search_hit"
                h["matched_keyword"] = identifier_value
            results.extend(hits)
        except Exception as e:
            log.warning("market_scan_error", extra={"url": url, "err": str(e)})

    # scan paste sites
    for url in TARGETS.get("paste_site", []):
        try:
            hits = paste.scrape_paste_for_keywords(url, [identifier_value])
            for h in hits:
                h["match_type"] = "targeted_search_hit"
                h["matched_keyword"] = identifier_value
            results.extend(hits)
        except Exception as e:
            log.warning("paste_scan_error", extra={"url": url, "err": str(e)})

    log.info("run_search_complete", extra={"task_id": self.request.id, "hits": len(results)})
    return {"status": "complete", "identifier_type": identifier_type, "identifier_value": identifier_value, "results": results}
