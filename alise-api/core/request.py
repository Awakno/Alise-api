from typing import Any
from urllib.parse import urljoin


class RequestError(Exception):
    """Custom exception for request errors."""

    pass


class Request:
    def __init__(self, path: str, method: str = "GET"):
        self.base_url = "https://webparent.paiementdp.com/"
        self.url = urljoin(self.base_url, path)
        self.headers: dict[str, str] = {}
        self.cookies: dict[str, str] = {}
        self.method = method
        self.data: str | None = None

    def set_form_data(self, data: str):
        self.method = "POST"
        self.data = data
        self.headers["Content-Type"] = "application/x-www-form-urlencoded"

    def set_headers(self, headers: dict[str, str]):
        self.headers = headers

    def set_session(self, session_id: str):
        self.cookies["PHPSESSID"] = session_id

    async def send(self, fetcher: dict[str, Any]):
        """
        Sends the request using the provided fetcher function.

        :param fetcher: A callable that performs the HTTP request.
        :return: The response from the fetcher.
        """
        # Ensure cookies are included in the headers
        if self.cookies:
            cookie_header = "; ".join(
                f"{key}={value}" for key, value in self.cookies.items()
            )
            self.headers["Cookie"] = cookie_header

        try:
            return await fetcher["fetcher"](self)
        except Exception as e:
            raise RequestError(f"Failed to send request: {e}")
