from pydantic import BaseModel


class ResultResponse(BaseModel):
    result: int | float
