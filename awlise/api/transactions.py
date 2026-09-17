from ..core.request import Request
from ..exceptions import TransactionError
from ..models.session import Session
from ..models.transactions import Transaction
from ..parser.transactions import _html_transactions_parser


async def list_transactions(session: Session) -> list[Transaction]:
    """
    Retrieves the financial transactions (debits/credits) of the current session.
    """
    request = Request("aliOperationsFin.php")
    request.set_session(session.get("session_id"))
    response = await request.send(session)
    try:
        return _html_transactions_parser(response["bytes"].decode("utf-8"))
    except Exception as e:
        raise TransactionError(f"Failed to parse transactions: {e}")
