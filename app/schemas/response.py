from typing import Generic, TypeVar
from pydantic import BaseModel

DataT = TypeVar("DataT")

class StandardResponse(BaseModel, Generic[DataT]):
    success: bool
    message: str
    data: DataT
