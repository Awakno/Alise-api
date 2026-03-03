from awlise.models.session import Session
from awlise.core.request import Request
from awlise.parser.home import _html_home_parser


class HomeError(Exception):
    """Custom exception for errors in the home function."""
    pass


async def home(session: Session) -> str:
    request = Request("aliIndexClient.php")
    request.set_session(session.get("id"))

    try:
        response = await request.send(session)
    except Exception as e:
        raise HomeError(f"Failed to send request: {e}")

    # parse the response
    try:
        data = _html_home_parser(response["bytes"].decode("utf-8"))
    except Exception as e:
        raise HomeError(f"Error parsing home page: {e}")

    return data
