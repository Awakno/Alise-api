import pydantic


class Booking(pydantic.BaseModel):
    """
    A booking object.
    """
    status: str
    cancelable: bool = False
    link: str = None
    date: str = None
    identifier: str = None
