# Alise HTTP API Reference

Alise (webparent.paiementdp.com) does not publish an official API. This document is a reverse-engineered reference derived from the `awlise` wrapper library.

**Base URL:** `https://webparent.paiementdp.com/`

All responses are HTML pages. There is no JSON or XML API. Data must be extracted by parsing the HTML.

---

## Authentication

Alise uses server-side PHP sessions. Every authenticated request must include a `PHPSESSID` cookie obtained from a login call.

### Login with credentials

```
POST aliAuthentification.php?site={site_id}
```

**Query parameters**

| Parameter | Type   | Required | Description                              |
|-----------|--------|----------|------------------------------------------|
| `site`    | string | Yes      | Establishment identifier (e.g. `12345`) |

**Request body** — `application/x-www-form-urlencoded`

| Field            | Type   | Description                          |
|------------------|--------|--------------------------------------|
| `txtLogin`       | string | Username                             |
| `txtMdp`         | string | Password                             |
| `chkKeepSession` | string | Always `"1"` to keep the session alive |

**Response**

- HTTP 302 redirect on success.
- `Set-Cookie: PHPSESSID=<token>; path=/` is present in the response headers on success.
- No `PHPSESSID` cookie means authentication failed (wrong credentials or unknown site ID).

**Session extraction**

Parse the `Set-Cookie` response header. Split on `;`, then on `=`. The cookie name is `PHPSESSID`.

---

### Login with token

```
GET aliAuthentification.php?site={site_id}&token={token}
```

**Query parameters**

| Parameter | Type   | Required | Description              |
|-----------|--------|----------|--------------------------|
| `site`    | string | Yes      | Establishment identifier |
| `token`   | string | Yes      | Pre-issued auth token    |

**Response** — same as credentials login: check `Set-Cookie` for `PHPSESSID`.

---

### Session usage

All subsequent requests must include:

```
Cookie: PHPSESSID=<session_id>
```

A `User-Agent` header that looks like a browser is also required. The platform rejects or misbehaves with missing or bot-like user agents:

```
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36
```

---

## Endpoints

### Home page

```
GET aliIndexClient.php
```

Returns the user's dashboard. Contains account holder info, balance, and currently selected child.

**Parsed fields from HTML**

| Field                    | HTML selector                          | Notes                                              |
|--------------------------|----------------------------------------|----------------------------------------------------|
| `responsable`            | `<p class="responsable">`              | Full name of the account holder                    |
| `responsable_first_name` | —                                      | First token of `responsable` split on first space  |
| `responsable_last_name`  | —                                      | Remainder after first space                        |
| `adress`                 | `<p class="adresse">`                  | Address string                                     |
| `balance`                | `<label class="soldeplus"> <b>…</b>`  | Tuple of `(float, currency_symbol)`, e.g. `(12.5, "€")` |
| `childs.name`            | `<select class="eleve"> <option selected>` | Full name, text in parentheses stripped        |
| `childs.first_name`      | —                                      | First token of child name                          |
| `childs.last_name`       | —                                      | Remainder                                          |

**Data model**

```python
class Account(pydantic.BaseModel):
    responsable: str | None
    responsable_first_name: str | None
    responsable_last_name: str | None
    address: str | None
    balance: tuple[float, str] | None   # (amount, currency_symbol)
    child: Child | None

class Child(pydantic.BaseModel):
    name: str | None
    first_name: str | None
    last_name: str | None
```

---

### Bookings calendar

```
GET aliReservation.php
```

Returns a monthly HTML calendar. Each day is a `<td id="{date}">` cell. The cell's `bgcolor` and child anchor tags indicate the booking status.

**Parsed fields from HTML**

Each calendar cell maps to a booking entry. The parser scans every `<td id="…">`:

| Cell state | Condition | `status` |
|---|---|---|
| Reserved (cancellable) | Contains `<a href>` with `aliReservationCancel.php` in URL | `"reserved"` |
| Available | Contains `<a href>` pointing elsewhere | `"available"` |
| Non-reservable | `bgcolor` contains `E8E8E8` or `FDFFFF`, no link | `"non-reservable"` |

**Booking identifier**

The URL fragment `date=…` from the cell's anchor href. This is a URL-encoded opaque string (e.g. `F%2FrWMpaHllxaxwTQSSGlWqWOzTElAh5C0G12VWvKmlg%3D`). It is required by the book/cancel endpoints.

**Data model**

```python
class Booking(pydantic.BaseModel):
    status: str                 # "reserved" | "available" | "non-reservable"
    cancelable: bool            # True only for "reserved"
    link: str | None            # Full href from the anchor
    date: str | None            # Cell id, typically YYYY-MM-DD
    identifier: str | None      # Value of the `date=` query param from the link
```

---

### Book a meal

Two-step process: GET the detail page first, then POST the confirmation form.

#### Step 1 — Fetch the booking form

```
GET aliReservationDetail.php?date={identifier}
```

**Query parameters**

| Parameter | Type   | Description                             |
|-----------|--------|-----------------------------------------|
| `date`    | string | URL-encoded booking identifier from the calendar |

A HTTP 200 response is required to proceed. Any other status means the slot is not available.

#### Step 2 — Submit the booking

```
POST aliReservationDetail.php
```

**Request body** — `application/x-www-form-urlencoded`

| Field            | Value                       | Notes                           |
|------------------|-----------------------------|----------------------------------|
| `ref`            | `""` (empty string)         |                                  |
| `btnOK.x`        | `53`                        | Simulates a click on the OK button |
| `btnOK.y`        | `17`                        | Simulates a click on the OK button |
| `valide_form`    | `1`                         |                                  |
| `CONS_QUANTITE`  | `"1"` (or higher)           | Number of meals to book          |
| `restaurant`     | `1`                         |                                  |

**Success detection**

The platform does not return a structured success/failure signal. Detection is based on response body length:

- **Success** → response body < 100 characters (a bare `<meta http-equiv="refresh">` redirect).
- **Failure** → response body ≥ 100 characters (a full HTML error page).

HTTP status is between 200–399 in both cases; it alone is not sufficient.

---

### Cancel a booking

Two-step process mirroring the book flow, but against the cancel endpoint.

#### Step 1 — Fetch the cancel form

```
GET aliReservationCancel.php?date={identifier}
```

Same query parameter as booking. HTTP 200 required to proceed.

#### Step 2 — Submit the cancellation

```
POST aliReservationCancel.php
```

**Request body** — `application/x-www-form-urlencoded`

| Field         | Value    |
|---------------|----------|
| `ref`         | `cancel` |
| `btnOK.x`     | `53`     |
| `btnOK.y`     | `17`     |
| `valide_form` | `1`      |

`CONS_QUANTITE` and `restaurant` are **not** sent for cancellations.

**Success detection** — same body-length heuristic as booking (< 100 chars = success).

---

### Financial operations

```
GET aliOperationsFin.php
```

Returns a list of debit/credit entries for the account.

**Parsed fields from HTML**

The parser scans `<tr class="detail">` rows:

| Field         | HTML selector                              | Notes                                 |
|---------------|--------------------------------------------|---------------------------------------|
| `date`        | `<td class="detail_date">`                 | Date string as displayed              |
| `description` | `<td class="detail_data">`                 | Operation label                       |
| `debit`       | `<td class="detail_debit_montant">`        | Float, comma-separated decimal. `None` if empty |
| `credit`      | `<td class="detail_credit_montant">`       | Float, comma-separated decimal. `None` if empty |

**Data model**

```python
class Transaction(pydantic.BaseModel):
    date: str | None
    description: str | None
    debit: float | None
    credit: float | None
```

---

### Meal price

```
GET aliEncaissement.php
```

Returns the billing page. Used to read the price of a single canteen meal (not the account balance — that comes from the home page's `balance` field).

**Parsed fields from HTML**

| Field        | HTML selector                       | Notes                                              |
|--------------|--------------------------------------|-----------------------------------------------------|
| `meal_price` | `<label class="label-credit-lib">`  | Parsed out of a `"... (12,50 € ...)"`-style string, comma decimal converted to a float; tuple of `(float, currency_symbol)` |

If the label is missing or empty, defaults to `(0.0, "€")`.

---

## Request structure summary

| Endpoint                    | Method | Auth cookie | Body type                         |
|-----------------------------|--------|-------------|-----------------------------------|
| `aliAuthentification.php`   | POST   | No          | `application/x-www-form-urlencoded` |
| `aliAuthentification.php`   | GET    | No          | —                                 |
| `aliIndexClient.php`        | GET    | Yes         | —                                 |
| `aliReservation.php`        | GET    | Yes         | —                                 |
| `aliReservationDetail.php`  | GET    | Yes         | —                                 |
| `aliReservationDetail.php`  | POST   | Yes         | `application/x-www-form-urlencoded` |
| `aliReservationCancel.php`  | GET    | Yes         | —                                 |
| `aliReservationCancel.php`  | POST   | Yes         | `application/x-www-form-urlencoded` |
| `aliOperationsFin.php`      | GET    | Yes         | —                                 |
| `aliEncaissement.php`       | GET    | Yes         | —                                 |

---

## Notes

- **Redirects must be disabled.** The login response is a 302 redirect that carries the `Set-Cookie` header. Following the redirect loses the cookie. Set `allow_redirects=False`.
- **Identifiers are URL-encoded opaque tokens.** The `date=` parameter values look like base64 but should be treated as opaque — pass them verbatim (still URL-encoded) in query strings.
- **Session is single-child.** The platform session is tied to one child at a time (the one selected in the `<select class="eleve">` dropdown on the home page). Switching child would require a separate interaction not yet mapped.
- **No versioning.** All endpoints use plain `.php` filenames with no version prefix. The platform has no published API contract and may change at any time.
