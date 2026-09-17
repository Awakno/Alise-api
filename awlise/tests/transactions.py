import asyncio
import os

from dotenv import load_dotenv

from awlise import AliseClient

load_dotenv()
site_id = os.getenv("ALISE_SITE_ID")
username = os.getenv("ALISE_USERNAME")
password = os.getenv("ALISE_PASSWORD")

if not username or not password or not site_id:
    raise ValueError(
        "Environment variables ALISE_USERNAME, ALISE_PASSWORD, or ALISE_SITE_ID are not set properly."
    )


def test_transactions():
    try:
        client = asyncio.run(AliseClient.from_credentials(site_id, username, password))
        return asyncio.run(client.list_transactions())
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


if __name__ == "__main__":
    print(test_transactions())
