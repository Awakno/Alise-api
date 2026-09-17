import aiohttp

from ..exceptions import FetcherError
from .request import Request


async def default_fetcher(req: Request) -> dict:
    """
    Default aiohttp-based fetcher. Sends the given request and returns
    a dict with the raw response: status, headers, bytes and decoded text.
    """
    headers = dict(req.headers)
    headers["User-Agent"] = (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    )

    try:
        async with aiohttp.ClientSession() as session:
            async with session.request(
                method=req.method,
                url=req.url,
                data=req.data,
                headers=headers,
                allow_redirects=False,
            ) as response:
                status = response.status
                bytes_data = await response.read()
                response_headers = [
                    (key.lower(), value) for key, value in response.headers.items()
                ]
                return {
                    "status": status,
                    "headers": response_headers,
                    "bytes": bytes_data,
                    "text": bytes_data.decode("utf-8", errors="ignore"),
                }
    except aiohttp.ClientError as e:
        raise FetcherError(f"HTTP request failed: {e}")


def extract_session_cookies(response: dict) -> dict[str, str]:
    """Extracts cookies from a fetcher response's headers."""
    cookies = {}
    for header, value in response["headers"]:
        if header == "set-cookie":
            cookie_parts = value.split(";")[0].split("=")
            if len(cookie_parts) == 2:
                cookies[cookie_parts[0]] = cookie_parts[1]
    return cookies
