import asyncio
import datetime
import os
import sys

from dotenv import load_dotenv

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../awlise"))
)

from awlise import AliseClient

load_dotenv()
site_id = os.getenv("ALISE_SITE_ID")
username = os.getenv("ALISE_USERNAME")
password = os.getenv("ALISE_PASSWORD")

BOOKING_IDENTIFIER = "F%2FrWMpaHllxaxwTQSSGlWqWOzTElAh5C0G12VWvKmlg%3D"


async def _client() -> AliseClient:
    return await AliseClient.from_credentials(site_id, username, password)


def test_list_bookings():
    client = asyncio.run(_client())
    return asyncio.run(client.list_bookings())


def test_get_booking_by_date():
    client = asyncio.run(_client())
    today = datetime.datetime.now().isoformat().split("T")[0]
    return asyncio.run(client.get_booking_by_date(today))


def test_get_booking():
    client = asyncio.run(_client())
    return asyncio.run(client.get_booking(BOOKING_IDENTIFIER))


if __name__ == "__main__":
    print(test_list_bookings())
    print(test_get_booking_by_date())
    print(test_get_booking())
