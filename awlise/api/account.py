from ..exceptions import AccountError
from ..models.account import Account
from ..models.session import Session
from ..core.request import Request
from ..parser.account import _html_account_parser


async def get_account(session: Session) -> Account:
    """
    Retrieves the account holder's information from the dashboard.
    """
    request = Request("aliIndexClient.php")
    request.set_session(session.get("session_id"))

    try:
        response = await request.send(session)
    except Exception as e:
        raise AccountError(f"Failed to send request: {e}")

    try:
        return _html_account_parser(response["bytes"].decode("utf-8"))
    except Exception as e:
        raise AccountError(f"Error parsing account page: {e}")
