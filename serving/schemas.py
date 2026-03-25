from typing import Literal
from pydantic import BaseModel, Field


class InputData(BaseModel):
    price: float = Field(..., gt=0)
    surface: float = Field(..., gt=0)
    description_length: int = Field(..., ge=0)
    photo_count: int = Field(..., ge=0)
    location_precision: Literal["street", "district", "city"]
    rooms: int = Field(..., ge=0)


class OutputData(BaseModel):
    quality_score: float
    tier: Literal["HIGH", "MEDIUM", "LOW"]
    issues: list[str]
