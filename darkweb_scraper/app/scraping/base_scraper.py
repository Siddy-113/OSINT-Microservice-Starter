from typing import Dict, Any, List, Optional
from datetime import datetime, timezone
from app.utils.tor_client import TorSession
from app.utils.logger import log
from app.utils.parser import to_soup

class BaseScraper:
    """
    Common Tor-routed HTTP + parsing helpers.
    """
    source_type: str = "forum"  # override in subclasses: "forum" | "marketplace" | "paste_site"

    def __init__(self):
        self.tor = TorSession()

    @staticmethod
    def now_utc_iso() -> str:
        return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

    def fetch(self, url: str) -> Optional[str]:
        try:
            resp = self.tor.get(url)
            if resp.status_code == 200 and resp.text:
                return resp.text
            log.info("fetch_non200_or_empty", extra={"status": resp.status_code})
        except Exception as e:
            log.warning("fetch_error", extra={"err": str(e)})
        return None

    def normalize_result(
        self,
        source_url: str,
        match_type: str,
        content_snippet: str,
        author_username: Optional[str],
        post_url: Optional[str],
        matched_keyword: Optional[str] = None,
    ) -> Dict[str, Any]:
        return {
            "source_url": source_url,
            "source_type": self.source_type,
            "capture_timestamp": self.now_utc_iso(),
            "match_type": match_type,
            "matched_keyword": matched_keyword,
            "content_snippet": content_snippet,
            "author_username": author_username,
            "post_url": post_url,
        }

    # Example parse routine—subclasses should override appropriately.
    def parse_generic_posts(self, html: str, base_url: str) -> List[Dict[str, Any]]:
        soup = to_soup(html)
        results = []
        for post in soup.select(".post"):   # site-specific selector to be overridden
            title = post.select_one(".title")
            user = post.select_one(".user")
            link = post.select_one("a")
            content = post.select_one(".content")

            snippet = (content.get_text(" ", strip=True) if content else "")[:800]
            author = user.get_text(strip=True) if user else None
            post_url = base_url if not link else link.get("href", base_url)

            results.append(
                self.normalize_result(
                    source_url=base_url,
                    match_type="keyword_match",
                    content_snippet=snippet,
                    author_username=author,
                    post_url=post_url,
                    matched_keyword=None,
                )
            )
        return results

