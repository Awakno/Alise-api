import asyncio
import os
import sys

from dotenv import load_dotenv

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../awlise"))
)

from awlise.api.getBooking import getBookings
from awlise.api.login import login_credentials

load_dotenv()
site_id = os.getenv("ALISE_SITE_ID")
username = os.getenv("ALISE_USERNAME")
password = os.getenv("ALISE_PASSWORD")


def test_bookings():
    session = asyncio.run(login_credentials(site_id, username, password))
    bookings = asyncio.run(getBookings(session))
    return bookings


if __name__ == "__main__":
    print(test_bookings())
