from datetime import datetime
from typing import Generic, TypeVar, Optional, List

from pydantic import BaseModel, ConfigDict


class BaseSchema(BaseModel):
    """Базовая схема для всех Pydantic моделей в проекте"""
    model_config = ConfigDict(
        from_attributes=True,      # важно для .model_validate + ORM
        populate_by_name=True,
        str_strip_whitespace=True,
    )


class SuccessResponse(BaseSchema):
    success: bool = True
    message: Optional[str] = None


T = TypeVar("T")


class PaginatedResponse(BaseSchema, Generic[T]):
    """Стандартный пагинированный ответ"""
    items: List[T]
    total: int
    skip: int = 0
    limit: int = 20