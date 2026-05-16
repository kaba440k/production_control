from datetime import datetime
from typing import Optional

from pydantic import Field

from src.api.v1.schemas.common import BaseSchema


class ProductBase(BaseSchema):
    is_aggregated : bool = Field(default=False)
    unique_code : str = Field(..., min_length=1, max_length=100)

class ProductCreate(ProductBase):
    batch_id : int = Field(...,gt=0)
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "unique_code": "CODE003",
                    "batch_id": 1,
                }
            ]
        }
    }

class ProductResponse(ProductBase):
    batch_id : int = Field(...,gt=0)
    created_at: Optional[datetime]
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "unique_code": "CODE003",
                    "batch_id": 1,
                    "is_aggregated" : True,
                    "created_at" : "2024-01-02T12:00:00",

                }
            ]
        }
    }