import asyncio
import os
from dotenv import load_dotenv

from awlise.api.login import login_credentials
from awlise.api.operation import getOperation

load_dotenv()

username = os.getenv("ALISE_USERNAME")
password = os.getenv("ALISE_PASSWORD")
site_id = os.getenv("ALISE_SITE_ID")

if not username or not password or not site_id:
    raise ValueError(
        "Environment variables ALISE_USERNAME, ALISE_PASSWORD, or ALISE_SITE_ID are not set properly."
    )


def test_operation():
    try:
        session = asyncio.run(login_credentials(site_id, username, password))
        operations = asyncio.run(getOperation(session))
        return operations
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


if __name__ == "__main__":
    print(test_operation())
