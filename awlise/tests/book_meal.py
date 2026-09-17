import asyncio
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


async def book_meal_test(identifier: str):
    client = await AliseClient.from_credentials(site_id, username, password)
    return await client.book_meal(identifier)


async def cancel_meal_test(identifier: str):
    client = await AliseClient.from_credentials(site_id, username, password)
    return await client.cancel_meal(identifier)


if __name__ == "__main__":
    print(asyncio.run(book_meal_test(BOOKING_IDENTIFIER)))
