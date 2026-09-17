from typing import Callable, TypedDict


class Session(TypedDict, total=False):
    """
    Represents an authenticated session with its associated properties.
    """

    session_id: str  # Content of the PHPSESSID cookie.
    site_id: str  # Identifier of the site for your establishment.
    fetcher: Callable  # Fetcher function or callable.
