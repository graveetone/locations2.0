from datetime import datetime, UTC

from bson import ObjectId
from pydantic import BaseModel, ConfigDict, Field


class Point(BaseModel):
    latitude: float = Field(None, ge=-90, le=90)
    longitude: float = Field(None, ge=-180, le=180)


class Resource(BaseModel):
    mongo_id: ObjectId = Field(alias="_id", default=None)
    identifier: int

    model_config = ConfigDict(arbitrary_types_allowed=True, json_encoders={ObjectId: str})


class Location(BaseModel):
    point: Point
    timestamp: datetime = Field(default_factory=lambda: datetime.now(UTC))
    resource_id: ObjectId = None

    model_config = ConfigDict(arbitrary_types_allowed=True, json_encoders={ObjectId: str, datetime: str})
