from datetime import datetime, date
from typing import Optional, List

from src.api.v1.schemas.common import BaseSchema
from pydantic import BaseModel, Field, field_validator, model_validator


class BatchBase(BaseSchema):
    is_closed: bool
    closed_at: datetime
    task_description: str = Field(..., min_length=1, max_length=2000)
    shift: str = Field(..., min_length=1, max_length=50)
    team: str = Field(..., min_length=1, max_length=150)
    batch_number: int = Field(...,gt=0)
    batch_date: date
    nomenclature: str = Field(..., min_length=1, max_length=200)
    ekn_code: str = Field(..., min_length=1, max_length=100)
    model_config = {
        "from_attributes": True,  # Для ORM моделей
        "json_schema_extra": {
            "examples": [
                {
                    "id": 66583,
                    "work_center_id": 21,
                    "closed_at": "2024-01-01T12:00:00",
                    "products": [{"id": 662515583, "unique_code": "123e4567-e89b-12d3-a456", "aggregated_at": None},
                                 {"id": 662842142, "unique_code": "61422313e4567-e8349b-12d423-a4ff15a6",
                                  "aggregated_at": "2024-01-01T10:00:00"}],
                    "created_at": "2024-01-01T12:00:00",
                    "updated_at": "2024-01-01T12:00:00"
                }
            ]
        }
    }


class BatchCreate(BatchBase):
    work_center_id : int = Field(..., gt =0)
    shift_start: datetime
    shift_end: datetime

    @model_validator(mode='after')
    def validate_shift_times(self) -> 'BatchBase':
        """Валидация времени смены"""
        if self.shift_end <= self.shift_start:
            raise ValueError("Время окончания смены должно быть строго позже времени начала")

        if self.shift_start.date() != self.shift_end.date():
            raise ValueError("Смена должна начинаться и заканчиваться в один календарный день")

        return self

class BatchUpdate(BatchBase):
    task_description: Optional[str] = Field(None, min_length=10, max_length=1000)
    shift: Optional[str] = Field(None, min_length=1, max_length=50)
    team: Optional[str] = Field(None, min_length=3, max_length=100)
    nomenclature: Optional[str] = Field(None, min_length=3, max_length=200)
    ekn_code: Optional[str] = Field(None, min_length=3, max_length=100)
    is_closed: Optional[bool] = None

class ProductResponse(BaseSchema):
    id: int
    unique_code: str
    aggregated_at: Optional[datetime] = None

class BatchResponse(BatchBase):
    id: int
    work_center_id : str
    closed_at: Optional[datetime] = None
    products: List[ProductResponse] = Field(default_factory=list)

    created_at: datetime
    updated_at: datetime

class BatchListResponse(BaseSchema):
    items: List[BatchResponse]
    total: int
    skip: int = 0
    limit: int = 20
