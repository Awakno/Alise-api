from urllib.parse import urlencode

from ..core.fetcher import default_fetcher, extract_session_cookies
from ..core.request import Request
from ..exceptions import AuthenticationError, FetcherError
from ..models.session import Session


async def login_with_credentials(
    site_id: str, username: str, password: str, fetcher=None
) -> Session:
    """
    Logs in with a username and password.
    """
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
        raise AuthenticationError(f"Login request failed: {e}")

    cookies = extract_session_cookies(response)
    session_id = cookies.get("PHPSESSID")
    if not session_id:
        raise AuthenticationError("No session ID found in response cookies")
    return Session(session_id=session_id, site_id=site_id, fetcher=fetcher)


async def login_with_token(site_id: str, token: str, fetcher=None) -> Session:
    """
    Logs in with a pre-issued auth token.
    """
    if fetcher is None:
        fetcher = default_fetcher

    request = Request(f"aliAuthentification.php?site={site_id}&token={token}")
    try:
        response = await fetcher(request)
    except FetcherError as e:
        raise AuthenticationError(f"Token login request failed: {e}")

    cookies = extract_session_cookies(response)
    session_id = cookies.get("PHPSESSID")
    if not session_id:
        raise AuthenticationError("No session ID found in response cookies")

    return Session(session_id=session_id, site_id=site_id, fetcher=fetcher)
