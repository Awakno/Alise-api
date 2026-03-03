from urllib.parse import urlencode

from awlise.core.request import Request
from awlise.models.session import Session


async def bookMeal(
    session: Session,
    identifier: str,
    quantity: int = 1,
    cancel: bool = False,
) -> bool:
    """
    Books or cancels a meal reservation.

    :param session: The user session.
    :param identifier: The reservation date identifier.
    :param quantity: The quantity to reserve (booking only).
    :param cancel: True to cancel, False to book.
    :return: True on success, False otherwise.
    """
    identifier = identifier.strip()
    if not identifier:
        raise ValueError("Identifier cannot be empty.")
    if quantity < 1:
        raise ValueError("Quantity must be greater than 0.")

    endpoint = "aliReservationCancel.php" if cancel else "aliReservationDetail.php"

    request_get = Request(f"{endpoint}?date={identifier}")
    request_get.set_session(session.get("id"))
    response_get = await request_get.send(session)
    if response_get["status"] != 200:
        return False

    form_data = {
        "ref": "cancel" if cancel else "",
        "btnOK.x": "53",
        "btnOK.y": "17",
        "valide_form": "1",
    }

    if not cancel:
        form_data["CONS_QUANTITE"] = str(quantity)
        form_data["restaurant"] = "1"

    request_post = Request(endpoint)
    request_post.set_session(session.get("id"))
    request_post.set_form_data(urlencode(form_data))
    response_post = await request_post.send(session)

    return 200 <= response_post["status"] < 400
