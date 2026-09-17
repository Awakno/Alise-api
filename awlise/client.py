from .api.account import get_account
from .api.auth import login_with_credentials, login_with_token
from .api.bookings import book_meal, cancel_meal, get_booking, get_booking_by_date, list_bookings
from .api.payments import get_meal_price
from .api.transactions import list_transactions
from .models.account import Account
from .models.bookings import Booking
from .models.session import Session
from .models.transactions import Transaction


class AliseClient:
    """
    A logged-in Alise session, exposing the API as methods instead of
    free functions taking a Session. Thin wrapper: all the actual work
    happens in awlise.api.*.
    """

    def __init__(self, session: Session):
        self._session = session

    @classmethod
    async def from_credentials(
        cls, site_id: str, username: str, password: str, fetcher=None
    ) -> "AliseClient":
        session = await login_with_credentials(site_id, username, password, fetcher)
        return cls(session)

    @classmethod
    async def from_token(cls, site_id: str, token: str, fetcher=None) -> "AliseClient":
        session = await login_with_token(site_id, token, fetcher)
        return cls(session)

    @property
    def session(self) -> Session:
        return self._session

    async def get_account(self) -> Account:
        return await get_account(self._session)

    async def list_bookings(self) -> list[Booking]:
        return await list_bookings(self._session)

    async def get_booking(self, identifier: str) -> Booking | None:
        return await get_booking(self._session, identifier)

    async def get_booking_by_date(self, date: str) -> Booking | None:
        return await get_booking_by_date(self._session, date)

    async def book_meal(self, identifier: str, quantity: int = 1) -> bool:
        return await book_meal(self._session, identifier, quantity)

    async def cancel_meal(self, identifier: str) -> bool:
        return await cancel_meal(self._session, identifier)

    async def list_transactions(self) -> list[Transaction]:
        return await list_transactions(self._session)

    async def get_meal_price(self) -> tuple[float, str]:
        return await get_meal_price(self._session)
