from bs4 import BeautifulSoup
from typing import Optional

def to_soup(html: str) -> BeautifulSoup:
    return BeautifulSoup(html, "html.parser")

def text_or_none(node) -> Optional[str]:
    if not node:
        return None
    txt = node.get_text(strip=True)
    return txt if txt else None

def select_text(soup: BeautifulSoup, selector: str) -> Optional[str]:
    el = soup.select_one(selector)
    return text_or_none(el)

