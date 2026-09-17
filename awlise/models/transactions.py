import pydantic


class Transaction(pydantic.BaseModel):
    """
    A single debit/credit entry on the account.
    """
    date: str | None = None
    description: str | None = None
    debit: float | None = None
    credit: float | None = None
