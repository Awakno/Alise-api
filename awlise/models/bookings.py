import pydantic


class Booking(pydantic.BaseModel):
    """
    A single day's booking status on the calendar.
    """
    status: str
    cancelable: bool = False
    link: str | None = None
    date: str | None = None
    identifier: str | None = None
