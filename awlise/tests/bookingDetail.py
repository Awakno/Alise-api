import asyncio
import datetime
import os
import sys

from dotenv import load_dotenv

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../awlise"))
)

from awlise.api.bookMeal import bookMeal
from awlise.api.getBookingDetail import getBookingDetail, getBookingDetailByDateISO8601
from awlise.api.login import login_credentials

load_dotenv()
site_id = os.getenv("ALISE_SITE_ID")
username = os.getenv("ALISE_USERNAME")
password = os.getenv("ALISE_PASSWORD")

BOOKING_MEAL = "F%2FrWMpaHllxaxwTQSSGlWqWOzTElAh5C0G12VWvKmlg%3D"


def test_bookings_by_iso():
    session = asyncio.run(login_credentials(site_id, username, password))
    bookings = asyncio.run(
        getBookingDetailByDateISO8601(
            session, datetime.datetime.now().isoformat().split("T")[0]
        )
    )
    return bookings


def test_bookings():
    session = asyncio.run(login_credentials(site_id, username, password))
    bookings = asyncio.run(getBookingDetail(session, BOOKING_MEAL))
    return bookings


def test_bookmeal():
    session = asyncio.run(login_credentials(site_id, username, password))
    bookings = asyncio.run(bookMeal(session, BOOKING_MEAL))
    return bookings


if __name__ == "__main__":
    print(test_bookings_by_iso())
    print(test_bookings())
    print(test_bookmeal())
