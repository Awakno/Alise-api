from urllib.parse import urljoin

from ..exceptions import RequestError


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

    async def send(self, session: dict):
        """
        Sends the request using the fetcher stored on the given session.

        :param session: A Session dict, holding the `fetcher` callable to use.
        :return: The response from the fetcher.
        """
        if self.cookies:
            cookie_header = "; ".join(
                f"{key}={value}" for key, value in self.cookies.items()
            )
            self.headers["Cookie"] = cookie_header

        try:
            return await session["fetcher"](self)
        except Exception as e:
            raise RequestError(f"Failed to send request: {e}")
