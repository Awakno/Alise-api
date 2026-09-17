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


def test_get_meal_price():
    client = asyncio.run(AliseClient.from_credentials(site_id, username, password))
    return asyncio.run(client.get_meal_price())


if __name__ == "__main__":
    print(test_get_meal_price())
