from typing import Union
import pydantic


class Operation(pydantic.BaseModel):
    date: str = None
    description: str = None
    debit: Union[float, None] = None
    credit: Union[float, None] = None
