from worker import celery
from app.logger import log
from app.scraping.forum_scraper import ForumScraper
from app.scraping.marketplace_scraper import MarketplaceScraper
from app.scraping.paste_scraper import PasteScraper

TARGETS = {
    "forum": [],
    "marketplace": [],
    "paste_site": []
}

@celery.task(bind=True)
def monitor_keywords(self, keywords: list):
    log.info("monitor_keywords_start", extra={"task_id": self.request.id, "keywords_count": len(keywords)})
    results = []
    forum = ForumScraper()
    market = MarketplaceScraper()
    paste = PasteScraper()

    for url in TARGETS.get("forum", []):
        try:
            results.extend(forum.scrape_for_keywords(url, keywords))
        except Exception as e:
            log.warning("monitor_forum_err", extra={"url": url, "err": str(e)})

    for url in TARGETS.get("marketplace", []):
        try:
            results.extend(market.scrape_listings_for_keywords(url, keywords))
        except Exception as e:
            log.warning("monitor_market_err", extra={"url": url, "err": str(e)})

    for url in TARGETS.get("paste_site", []):
        try:
            results.extend(paste.scrape_paste_for_keywords(url, keywords))
        except Exception as e:
            log.warning("monitor_paste_err", extra={"url": url, "err": str(e)})

    log.info("monitor_complete", extra={"task_id": self.request.id, "hits": len(results)})
    return {"status": "complete", "keywords": keywords, "hits": results}
