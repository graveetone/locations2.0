from datetime import datetime, UTC

from bson import ObjectId
from pydantic import BaseModel, ConfigDict, Field


class Point(BaseModel):
    latitude: float = Field(None, ge=-90, le=90)
    longitude: float = Field(None, ge=-180, le=180)


class Location(BaseModel):
    point: Point
    timestamp: float = Field(default_factory=lambda: datetime.now(UTC).timestamp())

    model_config = ConfigDict(arbitrary_types_allowed=True, json_encoders={ObjectId: str, datetime: str})
