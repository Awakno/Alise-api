import aiohttp
from urllib.parse import urlencode
from ..models.session import Session
from ..core.request import Request


class FetcherError(Exception):
    pass


async def default_fetcher(req: Request):
    headers = {
        key: value for key, value in req.headers.items()
    }  # Fix iteration over headers

    # Add a User-Agent header
    headers["User-Agent"] = (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
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
                return {"status": status, "headers": response_headers, "bytes": bytes_data}
    except aiohttp.ClientError as e:
        raise FetcherError(f"HTTP request failed: {e}")


def get_cookies_from_response(response):
    # Extract cookies from response headers
    cookies = {}

    for header, value in response["headers"]:
        if header == "set-cookie":
            cookie_parts = value.split(";")[0].split("=")
            if len(cookie_parts) == 2:  # Fixed condition
                cookies[cookie_parts[0]] = cookie_parts[1]
    return cookies


async def login_credentials(
    site_id: str, username: str, password: str, fetcher=None
) -> Session:
    if fetcher is None:
        fetcher = default_fetcher

    request = Request(f"aliAuthentification.php?site={site_id}")
    form_data = urlencode(
        {"txtLogin": username, "txtMdp": password, "chkKeepSession": "1"}
    )
    request.set_form_data(form_data)

    try:
        response = await fetcher(request)
    except FetcherError as e:
        raise ValueError(f"Login request failed: {e}")

    cookies = get_cookies_from_response(response)
    session_id = cookies.get("PHPSESSID")
    if not session_id:
        raise ValueError("No session ID found in response cookies")
    return Session(id=session_id, site_id=site_id, fetcher=fetcher)


async def login_token(site_id: str, token: str, fetcher=None) -> Session:
    if fetcher is None:
        fetcher = default_fetcher

    request = Request(f"aliAuthentification.php?site={site_id}&token={token}")
    try:
        response = await fetcher(request)
    except FetcherError as e:
        raise ValueError(f"Token login request failed: {e}")

    cookies = get_cookies_from_response(response)
    session_id = cookies.get("PHPSESSID")

    if not session_id:
        raise ValueError("No session ID found in response cookies")

    return Session(id=session_id, site_id=site_id, fetcher=fetcher)
