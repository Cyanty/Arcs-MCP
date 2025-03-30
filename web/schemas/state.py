from pydantic import BaseModel


class ToggleState(BaseModel):
    type: str
    new_state: bool

