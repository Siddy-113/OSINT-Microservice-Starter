from typing import List, Dict
from app.scraping.base_scraper import BaseScraper
from app.logger import log

class PasteScraper(BaseScraper):
    source_type = "paste_site"

    def scrape_paste_for_keywords(self, url: str, keywords: List[str]) -> List[Dict]:
        html = self.fetch(url)
        if not html:
            return []
        text = html.lower()
        hits = []
        for kw in keywords:
            if kw.lower() in text:
                hits.append(self.normalize_result(
                    source_url=url,
                    match_type="keyword_match",
                    content_snippet=html[:800],
                    author_username="anonymous",
                    post_url=url,
                    matched_keyword=kw
                ))
        log.info("paste_scrape_done", extra={"hits": len(hits)})
        return hits
