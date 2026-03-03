from awlise.core.request import Request
from awlise.models.operation import Operation
from awlise.models.session import Session
from typing import List

from awlise.parser.operation import _html_operation_parser


async def getOperation(session: Session) -> List[Operation]:
    """
    Retrieves the operations of the current session.

    :param session: The user session.
    :return: A list of Operation objects.
    """
    request = Request("aliOperationsFin.php")
    request.set_session(session.get("id"))
    response = await request.send(session)
    try:
        return _html_operation_parser(response['bytes'])
    except Exception as e:
        raise ValueError(f"Failed to parse operations: {e}")
