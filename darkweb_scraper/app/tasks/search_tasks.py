from app.worker import celery
from app.utils.logger import log
from app.scraping.forum_scraper import ForumScraper
from app.scraping.marketplace_scraper import MarketplaceScraper
from app.scraping.paste_scraper import PasteScraper

# In production, target URLs are managed separately (sensitive list).
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
def run_search(self, identifier_type: str, identifier_value: str):
    """
    Targeted search across configured sources for a specific identifier.
    Returns normalized JSON array under 'results'.
    """
    log.info("task_run_search_accepted", extra={"task_id": self.request.id, "id_type": identifier_type})
    results = []

    # For now, scan all sources lightly. Subtler strategies can be added later.
    forum = ForumScraper()
    market = MarketplaceScraper()
    paste = PasteScraper()

    for url in TARGETS.get("forum", []):
        results.extend(forum.scrape_target_identifier(url, identifier_value))
    for url in TARGETS.get("marketplace", []):
        # marketplaces may also mention identifiers in listing text/descriptions
        results.extend(market.scrape_listings_for_keywords(url, [identifier_value]))
        # normalize match_type for targeted
        for r in results:
            r["match_type"] = "targeted_search_hit"
            r["matched_keyword"] = identifier_value
    for url in TARGETS.get("paste_site", []):
        results.extend(paste.scrape_paste_for_keywords(url, [identifier_value]))
        for r in results:
            r["match_type"] = "targeted_search_hit"
            r["matched_keyword"] = identifier_value

    return {
        "status": "complete",
        "identifier_type": identifier_type,
        "identifier_value": identifier_value,
        "results": results
    }

