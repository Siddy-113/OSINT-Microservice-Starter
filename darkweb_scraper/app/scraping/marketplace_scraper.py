from typing import List, Dict, Any
from app.scraping.base_scraper import BaseScraper
from app.utils.parser import to_soup
from app.utils.logger import log

class MarketplaceScraper(BaseScraper):
    source_type = "marketplace"

    def scrape_listings_for_keywords(self, url: str, keywords: list[str]) -> List[Dict[str, Any]]:
        html = self.fetch(url)
        if not html:
            return []
        soup = to_soup(html)
        results = []
        for li in soup.select(".listing"):  # site-specific selector
            title_el = li.select_one(".title")
            desc_el = li.select_one(".description")
            vendor_el = li.select_one(".vendor")

            title = title_el.get_text(" ", strip=True) if title_el else ""
            desc = desc_el.get_text(" ", strip=True) if desc_el else ""
            vendor = vendor_el.get_text(" ", strip=True) if vendor_el else None
            body = f"{title} {desc}".lower()

            for kw in keywords:
                if kw.lower() in body:
                    results.append(self.normalize_result(
                        source_url=url,
                        match_type="keyword_match",
                        content_snippet=(f"{title}\n{desc}")[:800],
                        author_username=vendor,
                        post_url=url,
                        matched_keyword=kw
                    ))
                    break
        log.info("marketplace_scrape_done", extra={"hits": len(results)})
        return results

