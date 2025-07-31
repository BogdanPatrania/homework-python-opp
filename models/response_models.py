from typing import Union
from pydantic import BaseModel

class ResultResponse(BaseModel):
    result: Union[float, int, str]
