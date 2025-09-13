import random
import time
from typing import Optional, Dict, Any
import requests
from requests.adapters import HTTPAdapter, Retry
from stem import Signal
from stem.control import Controller
from app.config import (
    TOR_SOCKS_HOST, TOR_SOCKS_PORT, TOR_CONTROL_HOST, TOR_CONTROL_PORT,
    TOR_CONTROL_PASSWORD, REQUEST_TIMEOUT, MAX_RETRIES, MIN_REQUEST_DELAY_SEC,
    MAX_REQUEST_DELAY_SEC
)
from app.utils.logger import log

class TorSession:
    """
    Requests session pinned to Tor SOCKS5 proxy with retry/backoff and optional NEWNYM rotation.
    """
    def __init__(self):
        self.session = requests.Session()

        retries = Retry(
            total=MAX_RETRIES,
            backoff_factor=1.5,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["HEAD", "GET", "OPTIONS", "POST"]
        )
        adapter = HTTPAdapter(max_retries=retries)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)

        proxy = f"socks5h://{TOR_SOCKS_HOST}:{TOR_SOCKS_PORT}"
        self.session.proxies.update({
            "http": proxy,
            "https": proxy
        })
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                          "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        })

    def _opsec_delay(self):
        delay = random.uniform(MIN_REQUEST_DELAY_SEC, MAX_REQUEST_DELAY_SEC)
        time.sleep(delay)

    def get(self, url: str, **kwargs) -> requests.Response:
        self._opsec_delay()
        kwargs.setdefault("timeout", REQUEST_TIMEOUT)
        log.info("tor_http_get", extra={"url_host_only": url.split("/")[2] if "://" in url else url})
        return self.session.get(url, **kwargs)

    def post(self, url: str, data: Optional[Dict[str, Any]] = None,
             json: Optional[Dict[str, Any]] = None, **kwargs) -> requests.Response:
        self._opsec_delay()
        kwargs.setdefault("timeout", REQUEST_TIMEOUT)
        log.info("tor_http_post", extra={"url_host_only": url.split("/")[2] if "://" in url else url})
        return self.session.post(url, data=data, json=json, **kwargs)

    @staticmethod
    def new_identity() -> bool:
        """
        Ask Tor for a new circuit. Returns True if successful.
        """
        try:
            with Controller.from_port(address=TOR_CONTROL_HOST, port=TOR_CONTROL_PORT) as controller:
                controller.authenticate(password=TOR_CONTROL_PASSWORD)
                controller.signal(Signal.NEWNYM)
                log.info("tor_newnym_requested", extra={})
                return True
        except Exception as e:
            log.warning("tor_newnym_failed", extra={"err": str(e)})
            return False

