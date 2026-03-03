from typing import Callable, TypedDict


class Session(TypedDict, total=False):
    """
    Represents a session with its associated properties.
    """

    id: str  # Content of PHPSESSID cookie.
    site_id: str  # Identifier of the site for your establishment.
    fetcher: Callable  # Fetcher function or callable.
