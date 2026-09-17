from ..core.request import Request
from ..exceptions import PaymentError
from ..models.session import Session
from ..parser.payments import _html_payments_parser


async def get_meal_price(session: Session) -> tuple[float, str]:
    """
    Retrieves the price of a single canteen meal, as shown on the payment page.
    """
    request = Request("aliEncaissement.php")
    request.set_session(session.get("session_id"))

    response = await request.send(session)
    try:
        data = _html_payments_parser(response["bytes"].decode("utf-8"))
    except Exception as e:
        raise PaymentError(f"Error parsing payment page: {e}")

    return data["meal_price"]
