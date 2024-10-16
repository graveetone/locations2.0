from datetime import datetime, UTC

from bson import ObjectId
from pydantic import BaseModel, ConfigDict, Field


class Point(BaseModel):
    latitude: float
    longitude: float


class Location(BaseModel):
    point: Point
    timestamp: datetime = Field(default_factory=lambda: datetime.now(UTC))
    resource_id: int = None

    model_config = ConfigDict(arbitrary_types_allowed=True, json_encoders={ObjectId: str, datetime: str})
