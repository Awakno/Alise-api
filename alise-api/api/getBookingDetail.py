import re
from awlise.api.getBooking import getBookings
from awlise.models.session import Session
from awlise.models.bookings import Booking


class BookingDetailError(Exception):
    """Custom exception for booking detail errors."""
    pass


async def getBookingDetailByDateISO8601(session: Session, date: str) -> Booking | None:
    """
    Retrieves the booking details for a specific date in ISO 8601 format.

    :param session: The user session.
    :param date: The date in ISO 8601 format (YYYY-MM-DD).
    :return: A Booking object or None if no booking is found.
    :raises ValueError: If the date format is invalid.
    """
    if not re.match(r"^\d{4}-\d{2}-\d{2}$", date):
        raise ValueError("Invalid date format. Expected ISO 8601 format (YYYY-MM-DD).")

    try:
        bookings = await getBookings(session)
    except Exception as e:
        raise BookingDetailError(f"Error retrieving bookings: {e}")

    for booking in bookings:
        if booking.date == date:
            return booking

    return None


async def getBookingDetail(session: Session, identifier: str) -> Booking | None:
    """
    Retrieves the booking details for a specific identifier.

    :param session: The user session.
    :param identifier: The booking identifier.
    :return: A Booking object or None if no booking is found.
    :raises ValueError: If the identifier is empty.
    """
    identifier = identifier.strip()
    if not identifier:
        raise ValueError("Identifier cannot be empty.")

    try:
        bookings = await getBookings(session)
    except Exception as e:
        raise BookingDetailError(f"Error retrieving bookings: {e}")

    return next((booking for booking in bookings if booking.identifier and booking.identifier.strip() == identifier), None)
