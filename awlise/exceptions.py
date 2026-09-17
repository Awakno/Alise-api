class AwliseError(Exception):
    """Base class for all awlise errors."""


class RequestError(AwliseError):
    """Raised when sending an HTTP request fails."""


class FetcherError(AwliseError):
    """Raised when the underlying fetcher fails to perform an HTTP request."""


class AuthenticationError(AwliseError):
    """Raised when logging in fails."""


class AccountError(AwliseError):
    """Raised when retrieving account information fails."""


class BookingError(AwliseError):
    """Raised when a bookings operation fails."""


class TransactionError(AwliseError):
    """Raised when retrieving transactions fails."""


class PaymentError(AwliseError):
    """Raised when retrieving payment information fails."""
