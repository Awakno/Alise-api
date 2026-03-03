from typing import TypedDict


class Authentification(TypedDict, total=False):
    siteID: str
    token: str
