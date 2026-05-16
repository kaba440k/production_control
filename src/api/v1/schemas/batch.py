from datetime import datetime, date
from typing import Optional, List

from src.api.v1.schemas.common import BaseSchema
from pydantic import Field, model_validator


class BatchBase(BaseSchema):
    is_closed: bool = Field(default=False)
    task_description: str = Field(..., min_length=1, max_length=2000)
    shift: str = Field(..., min_length=1, max_length=50)
    team: str = Field(..., min_length=1, max_length=100)
    batch_number: int = Field(..., gt=0)
    batch_date: date
    nomenclature: str = Field(..., min_length=1, max_length=200)
    ekn_code: str = Field(..., min_length=1, max_length=100)


class BatchCreate(BatchBase):
    work_center_name: str = Field(..., min_length=1, max_length=200)
    work_center_identifier: str = Field(
        ...,
        min_length=1,
        max_length=50,
    )
    shift_start: datetime
    shift_end: datetime

    @model_validator(mode='after')
    def validate_shift_times(self) -> 'BatchCreate':
        """Валидация времени смены"""
        if self.shift_end <= self.shift_start:
            raise ValueError("Время окончания смены должно быть строго позже времени начала")

        if self.shift_start.date() != self.shift_end.date():
            raise ValueError("Смена должна начинаться и заканчиваться в один календарный день")

        return self

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "is_closed": False,
                    "task_description": "Изготовить 1000 болтов М10",
                    "work_center_name": "Цех №1",
                    "work_center_identifier": "RC-001",
                    "shift": "1 смена",
                    "team": "Бригада Иванова",
                    "batch_number": 22222,
                    "batch_date": "2026-05-14",
                    "nomenclature": "Болт М10х50",
                    "ekn_code": "EKN-12345",
                    "shift_start": "2026-05-14T08:00:00",
                    "shift_end": "2026-05-14T20:00:00",
                }
            ]
        }
    }


class BatchUpdate(BaseSchema):
    is_closed: Optional[bool] = None
    task_description: Optional[str] = Field(None, min_length=1, max_length=2000)
    shift: Optional[str] = Field(None, min_length=1, max_length=50)
    team: Optional[str] = Field(None, min_length=1, max_length=100)
    nomenclature: Optional[str] = Field(None, min_length=1, max_length=200)
    ekn_code: Optional[str] = Field(None, min_length=1, max_length=100)
    model_config = {
        "from_attributes": True,  # Для ORM моделей
        "json_schema_extra": {
            "examples": [
                {
                    "is_closed": True,
                    "task_description": "Новое описание задачи",
                    "shift": "2 смена",
                    "team": "Бригада Петрова",
                    "nomenclature": "Гайка М12х50",
                    "ekn_code": "EKN-67890",
                }
            ]

        }
    }


class ProductResponse(BaseSchema):
    id: int
    unique_code: str
    is_aggregated: bool
    aggregated_at: Optional[datetime] = None


class BatchResponse(BatchBase):
    id: int
    work_center_id: int
    closed_at: Optional[datetime] = None
    products: List[ProductResponse] = Field(default_factory=list)

    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True,  # Для ORM моделей
        "json_schema_extra": {
            "examples": [
                {
                    "id": "123e4567-e89b-12d3-a456-426614174000",
                    "work_center_id": 31231,
                    "closed_at": None,
                    "products": {
                        "id": 12314122,
                        "unique_code": "AGSWDha1231ADJFSD-0sad12en",
                        "is_aggregated": True,
                        "aggregated_at": "2024-01-01T15:00:00"
                    },
                    "created_at": "2024-01-01T12:00:00",
                    "updated_at": "2024-01-02T12:00:00",
                }
            ]

        }
    }


class BatchListResponse(BaseSchema):
    items: List[BatchResponse]
    total: int
    skip: int = 0
    limit: int = 20


class ProductAggregateRequest(BaseSchema):
    unique_codes : List[str]
    model_config = {
        "from_attributes": True,  # Для ORM моделей
        "json_schema_extra": {
            "examples": [
                {
                    "unique_codes": ["CODE001", "CODE002"]
                }
            ]

        }
    }


class ProductAggregateError(BaseSchema):
    unique_code : str
    reason : str


class ProductAggregateResponse(BaseSchema):
    success: bool
    total: int
    aggregated : int
    failed : int
    errors : List[ProductAggregateError]
