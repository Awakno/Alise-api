# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

`awlise` is an async Python API wrapper for the Alise school meal booking platform (webparent.paiementdp.com). It scrapes HTML responses from the platform using `aiohttp` + `BeautifulSoup4`, and models data with `pydantic`.

## Commands

Install dependencies:
```bash
pip install -r requirements.txt
```

Install the package in editable mode:
```bash
pip install -e .
```

Run a test script (tests are standalone scripts, not pytest):
```bash
python awlise/tests/login.py
python awlise/tests/bookings.py
python awlise/tests/book_meal.py
python awlise/tests/transactions.py
python awlise/tests/payments.py
```

Tests require a `.env` file with:
```
ALISE_USERNAME=...
ALISE_PASSWORD=...
ALISE_SITE_ID=...
```

Lint:
```bash
flake8 awlise/
```

Build for PyPI:
```bash
python -m build
```

## Architecture

### Public API: `AliseClient`

The main entry point is `awlise.AliseClient`, a thin wrapper around a `Session` that exposes the API as methods:

```python
client = await AliseClient.from_credentials(site_id, username, password)
account = await client.get_account()
bookings = await client.list_bookings()
```

`AliseClient` does not contain any logic itself — every method delegates to the corresponding free function in `awlise/api/*.py` (e.g. `client.list_bookings()` calls `awlise.api.bookings.list_bookings(session)`). Those free functions are also exported directly from `awlise` for callers who prefer to manage the `Session` themselves (custom fetchers, composition, testing).

### Request flow

Every API call builds a `Request` object (`awlise/core/request.py`), which stores the URL, method, headers, cookies, and form data. The `Session` TypedDict (`awlise/models/session.py`) holds the `session_id` (from the `PHPSESSID` cookie), the `site_id`, and the **fetcher** callable.

`Request.send(session)` calls `session["fetcher"](request)` and returns a dict: `{"status", "headers", "bytes", "text"}`. The default fetcher (`awlise/core/fetcher.py:default_fetcher`) uses `aiohttp`. Custom fetchers can be injected (via `AliseClient.from_credentials(..., fetcher=...)` or the free login functions) for testing or alternate HTTP backends.

### Layer structure

| Layer | Path | Role |
|-------|------|------|
| Client | `awlise/client.py` | `AliseClient` — ergonomic method-based wrapper over the API layer |
| API | `awlise/api/*.py` | Async entry points — build requests, call parsers, return models |
| Parsers | `awlise/parser/*.py` | Pure HTML parsing via BeautifulSoup4 |
| Models | `awlise/models/*.py` | Pydantic BaseModel or TypedDict for data shapes |
| Core | `awlise/core/*.py` | `request.py` (HTTP request abstraction), `fetcher.py` (default aiohttp fetcher + cookie extraction) |
| Exceptions | `awlise/exceptions.py` | Centralized exception hierarchy, rooted at `AwliseError` |

Each API module maps 1:1 to a domain, not a PHP page name: `api/auth.py`, `api/account.py`, `api/bookings.py`, `api/transactions.py`, `api/payments.py` — mirrored by `parser/*.py` and `models/*.py` of the same name.

### Auth

`login_with_credentials` / `login_with_token` (`awlise/api/auth.py`) POST to `aliAuthentification.php`, extract `PHPSESSID` from `Set-Cookie` via `core/fetcher.py:extract_session_cookies`, and return a `Session`. All subsequent requests attach this cookie. `AliseClient.from_credentials` / `AliseClient.from_token` are the classmethod equivalents that return a ready-to-use client.

### book_meal / cancel_meal heuristic

Success detection in `book_meal` / `cancel_meal` (`awlise/api/bookings.py`, shared helper `_submit_reservation_action`) is based on response body length: a successful booking/cancellation returns a short HTML meta-redirect (<100 chars); a failure returns a full error page. This is intentional — the platform does not return machine-readable status codes for booking results.

### get_meal_price

`awlise/api/payments.py:get_meal_price` hits `aliEncaissement.php` and returns the price of a single canteen meal as `(float, currency_symbol)`. It is **not** the account balance — that's part of `get_account()`'s `balance` field.
