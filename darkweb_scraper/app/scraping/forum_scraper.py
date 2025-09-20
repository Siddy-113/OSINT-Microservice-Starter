from typing import List, Dict
from app.scraping.base_scraper import BaseScraper
from app.logger import log

class ForumScraper(BaseScraper):
    source_type = "forum"

    # site-specific login and navigation can be added here
    def scrape_for_keywords(self, url: str, keywords: List[str]) -> List[Dict]:
        html = self.fetch(url)
        if not html:
            return []
        posts = self.parse_generic_posts(html, base_url=url)
        hits = []
        for p in posts:
            text = (p.get("content_snippet") or "").lower()
            matched = next((k for k in keywords if k.lower() in text), None)
            if matched:
                p["matched_keyword"] = matched
                hits.append(p)
        log.info("forum_scrape_done", extra={"hits": len(hits)})
        return hits

    def scrape_target_identifier(self, url: str, identifier_value: str) -> List[Dict]:
        html = self.fetch(url)
        if not html:
            return []
        posts = self.parse_generic_posts(html, base_url=url)
        hits = []
        iv = identifier_value.lower()
        for p in posts:
            if iv in (p.get("content_snippet") or "").lower():
                p["match_type"] = "targeted_search_hit"
                p["matched_keyword"] = identifier_value
                hits.append(p)
        log.info("forum_target_search_done", extra={"hits": len(hits)})
        return hits
