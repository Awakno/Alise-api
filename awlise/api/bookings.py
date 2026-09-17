import re
from urllib.parse import urlencode

from ..core.request import Request
from ..exceptions import BookingError
from ..models.bookings import Booking
from ..models.session import Session
from ..parser.bookings import _html_bookings_parser


async def list_bookings(session: Session) -> list[Booking]:
    """
    Retrieves every booking on the calendar.
    """
    request = Request("aliReservation.php")
    request.set_session(session.get("session_id"))

    response = await request.send(session)
    try:
        data = _html_bookings_parser(response["bytes"].decode("utf-8"))
    except Exception as e:
        raise BookingError(f"Error parsing bookings page: {e}")

    return [Booking(**entry) for entry in data]


async def get_booking(session: Session, identifier: str) -> Booking | None:
    """
    Retrieves the booking matching the given identifier.

    :raises ValueError: If the identifier is empty.
    """
    identifier = identifier.strip()
    if not identifier:
        raise ValueError("Identifier cannot be empty.")

    bookings = await list_bookings(session)
    return next(
        (b for b in bookings if b.identifier and b.identifier.strip() == identifier),
        None,
    )


async def get_booking_by_date(session: Session, date: str) -> Booking | None:
    """
    Retrieves the booking for a specific date.

    :param date: The date in ISO 8601 format (YYYY-MM-DD).
    :raises ValueError: If the date format is invalid.
    """
    if not re.match(r"^\d{4}-\d{2}-\d{2}$", date):
        raise ValueError("Invalid date format. Expected ISO 8601 format (YYYY-MM-DD).")

    bookings = await list_bookings(session)
    return next((b for b in bookings if b.date == date), None)


async def _submit_reservation_action(
    session: Session, identifier: str, cancel: bool, quantity: int = 1
) -> bool:
    endpoint = "aliReservationCancel.php" if cancel else "aliReservationDetail.php"

    request_get = Request(f"{endpoint}?date={identifier}")
    request_get.set_session(session.get("session_id"))
    response_get = await request_get.send(session)
    if response_get["status"] != 200:
        return False

    form_data = {
        "ref": "cancel" if cancel else "",
        "btnOK.x": "53",
        "btnOK.y": "17",
        "valide_form": "1",
    }
    if not cancel:
        form_data["CONS_QUANTITE"] = str(quantity)
        form_data["restaurant"] = "1"

    request_post = Request(endpoint)
    request_post.set_session(session.get("session_id"))
    request_post.set_form_data(urlencode(form_data))
    response_post = await request_post.send(session)

    # The page for a successful booking/cancellation is just a meta-refresh
    # redirect, while a failed one is a full HTML error page — the platform
    # does not return a machine-readable status code for the result.
    if len(response_post["text"]) > 100:
        return False
    return 200 <= response_post["status"] < 400


async def book_meal(session: Session, identifier: str, quantity: int = 1) -> bool:
    """
    Books a meal reservation.

    :param identifier: The reservation date identifier.
    :param quantity: The quantity to reserve.
    :return: True on success, False otherwise.
    """
    identifier = identifier.strip()
    if not identifier:
        raise ValueError("Identifier cannot be empty.")
    if quantity < 1:
        raise ValueError("Quantity must be greater than 0.")

    return await _submit_reservation_action(session, identifier, cancel=False, quantity=quantity)


async def cancel_meal(session: Session, identifier: str) -> bool:
    """
    Cancels an existing meal reservation.

    :param identifier: The reservation date identifier.
    :return: True on success, False otherwise.
    """
    identifier = identifier.strip()
    if not identifier:
        raise ValueError("Identifier cannot be empty.")

    return await _submit_reservation_action(session, identifier, cancel=True)
