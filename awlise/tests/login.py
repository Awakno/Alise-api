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


def test_login():
    client = asyncio.run(AliseClient.from_credentials(site_id, username, password))
    return client.session


def test_account():
    client = asyncio.run(AliseClient.from_credentials(site_id, username, password))
    return asyncio.run(client.get_account())


if __name__ == "__main__":
    print(test_login())
    print(test_account())
