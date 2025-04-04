from pydantic import BaseModel


class BaseResponse(BaseModel):
    code: int = 200
    msg: str = "Success"
