from awlise.core.request import Request
from awlise.models.session import Session
from awlise.parser.bookings import _html_booking_parser
from awlise.models.bookings import Booking


async def getBookings(session: Session) -> list[Booking]:
    """
    Retrieves the bookings of the user.
    """
    request = Request("aliReservation.php")
    request.set_session(session.get("id"))

    response = await request.send(session)
    # parse the response
    try:
        data = _html_booking_parser(response["bytes"].decode("utf-8"))
    except Exception:
        raise Exception("Error parsing booking page")
    if not data:
        return []

    data_return = []
    for key in data:
        data_return.append(Booking(**key))

    return data_return
