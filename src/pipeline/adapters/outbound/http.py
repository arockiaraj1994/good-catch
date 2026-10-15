"""Checks that source links load."""

import urllib.error
import urllib.request

# Some news sites refuse requests without a browser-like agent.
_HEADERS = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) goodcatch-link-check/1.0"}


class HttpProbe:
    def __init__(self, timeout: float = 20.0) -> None:
        self._timeout = timeout

    def _request(self, url: str, method: str) -> int | None:
        request = urllib.request.Request(url, method=method, headers=_HEADERS)
        try:
            with urllib.request.urlopen(request, timeout=self._timeout) as response:
                return int(response.status)
        except urllib.error.HTTPError as e:
            return int(e.code)
        except (urllib.error.URLError, TimeoutError, ValueError):
            return None

    def status(self, url: str) -> int | None:
        code = self._request(url, "HEAD")
        # Many sites reject HEAD; ask again the normal way before calling it broken.
        if code is None or code >= 400:
            code = self._request(url, "GET")
        return code
