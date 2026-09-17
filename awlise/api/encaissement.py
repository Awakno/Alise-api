from urllib.parse import urlencode

import aiohttp

from awlise.core.request import Request
from awlise.models.session import Session
from awlise.parser.encaissement import _html_encaissement_parser

async def get_booking_price(session: Session):
    request = Request("aliEncaissement.php")
    request.set_session(session.get("id"))

    response = await request.send(session)
    # parse the response
    try:
        data = _html_encaissement_parser(response["bytes"].decode("utf-8"))
    except Exception:
        raise Exception("Error parsing booking page")
    if not data:
        return []


    return data['booking_price']