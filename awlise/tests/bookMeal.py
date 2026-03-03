import asyncio
import os
import sys

from dotenv import load_dotenv

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../awlise"))
)

from awlise.api.bookMeal import bookMeal
from awlise.api.login import login_credentials

load_dotenv()

site_id = os.getenv("ALISE_SITE_ID")
username = os.getenv("ALISE_USERNAME")
password = os.getenv("ALISE_PASSWORD")

BOOKING_MEAL = "F%2FrWMpaHllxaxwTQSSGlWqWOzTElAh5C0G12VWvKmlg%3D"


async def book_meal_test(meal_id: str):
    session = await login_credentials(site_id, username, password)
    bookings = await bookMeal(session, meal_id)
    return bookings


if __name__ == "__main__":
    print(asyncio.run(book_meal_test(BOOKING_MEAL)))
