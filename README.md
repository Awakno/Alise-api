# awlise

An async Python API wrapper for the [Alise](https://alise.net/) school meal booking platform (`webparent.paiementdp.com`).

_This library **is not** affiliated with Alise in any way._

Alise does not publish an official API — it only serves HTML pages. `awlise` logs in, sends the right requests, and scrapes the responses (`aiohttp` + `BeautifulSoup4`) into typed `pydantic` models, so you don't have to.

## Installation

```bash
pip install awlise
```

## Quick start

```python
import asyncio
from awlise import AliseClient


async def main():
    client = await AliseClient.from_credentials(
        site_id="12345", username="user", password="password"
    )

    account = await client.get_account()
    print(account.responsable, account.balance)

    bookings = await client.list_bookings()
    for booking in bookings:
        print(booking.date, booking.status)

    available = next(b for b in bookings if b.status == "available")
    await client.book_meal(available.identifier)


asyncio.run(main())
```

You can also log in with a pre-issued token instead of credentials:

```python
client = await AliseClient.from_token(site_id="12345", token="...")
```

## API overview

Every method on `AliseClient` maps to one domain of the platform:

| Method | Description |
|---|---|
| `AliseClient.from_credentials(site_id, username, password)` | Log in and return a ready-to-use client |
| `AliseClient.from_token(site_id, token)` | Log in with a pre-issued token |
| `client.get_account()` | Account holder info, balance, currently selected child |
| `client.list_bookings()` | Every day on the booking calendar and its status |
| `client.get_booking(identifier)` | A single booking by its identifier |
| `client.get_booking_by_date(date)` | A single booking by ISO 8601 date (`YYYY-MM-DD`) |
| `client.book_meal(identifier, quantity=1)` | Book a meal for a given day |
| `client.cancel_meal(identifier)` | Cancel an existing booking |
| `client.list_transactions()` | Debit/credit history of the account |
| `client.get_meal_price()` | Price of a single canteen meal (not the account balance) |

`client.session` gives you the underlying `Session` (`session_id`, `site_id`, `fetcher`) if you need to persist or inspect it.

### Functional API

Every client method is a thin wrapper around a free function that takes a `Session` explicitly — useful if you want to manage sessions yourself (e.g. store one per user) instead of holding an `AliseClient` instance:

```python
from awlise import login_with_credentials, get_account, list_bookings, book_meal

session = await login_with_credentials(site_id, username, password)
account = await get_account(session)
bookings = await list_bookings(session)
```

These are the same functions `AliseClient` calls internally — nothing is duplicated between the two styles.

### Custom fetcher

Every login function accepts a `fetcher` callable if you want to swap out the default `aiohttp`-based transport (for testing, proxies, retries, etc.):

```python
async def my_fetcher(request):
    ...  # perform the HTTP call yourself, return {"status", "headers", "bytes", "text"}

client = await AliseClient.from_credentials(site_id, username, password, fetcher=my_fetcher)
```

### Errors

All exceptions inherit from `awlise.AwliseError`: `AuthenticationError`, `AccountError`, `BookingError`, `TransactionError`, `PaymentError`, plus the lower-level `RequestError` and `FetcherError`.

```python
from awlise import AliseClient, AuthenticationError

try:
    client = await AliseClient.from_credentials(site_id, username, password)
except AuthenticationError:
    print("Wrong credentials or unknown site ID")
```

## Documentation

See [`docs/alise-api.md`](docs/alise-api.md) for a reverse-engineered reference of the raw HTTP endpoints this library wraps — useful if you need to debug a parsing issue or extend the library.

## Development

```bash
pip install -e .
flake8 awlise/
```

Tests are standalone scripts (not pytest) that hit the real platform, and require a `.env` file with `ALISE_USERNAME`, `ALISE_PASSWORD`, and `ALISE_SITE_ID`:

```bash
python awlise/tests/login.py
python awlise/tests/bookings.py
python awlise/tests/book_meal.py
python awlise/tests/transactions.py
python awlise/tests/payments.py
```

## License

GPL-3.0-or-later.
