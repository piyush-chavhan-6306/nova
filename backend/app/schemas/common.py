from typing import Generic, List, Optional, TypeVar
from pydantic import BaseModel, ConfigDict

T = TypeVar("T")


class BaseResponseModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class PaginatedResponse(BaseResponseModel, Generic[T]):
    items: List[T]
    total: int
    page: int = 1
    page_size: int = 50
