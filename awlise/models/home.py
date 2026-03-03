import pydantic


class ChildProps(pydantic.BaseModel):
    """
    A child object.
    """
    name: str = None
    first_name: str = None
    last_name: str = None


class Home(pydantic.BaseModel):
    """
    A home object.
    """
    responsable: str = None
    responsable_first_name: str = None
    responsable_last_name: str = None
    adress: str = None
    balance: tuple[float, str] = None
    childs: ChildProps = None
