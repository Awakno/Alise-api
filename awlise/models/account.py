import pydantic


class Child(pydantic.BaseModel):
    """
    The child currently selected on the account.
    """
    name: str | None = None
    first_name: str | None = None
    last_name: str | None = None


class Account(pydantic.BaseModel):
    """
    The account holder's information, as shown on the dashboard.
    """
    responsable: str | None = None
    responsable_first_name: str | None = None
    responsable_last_name: str | None = None
    address: str | None = None
    balance: tuple[float, str] | None = None
    child: Child | None = None
