from datetime import datetime, UTC

from bson import ObjectId
from pydantic import BaseModel, ConfigDict, Field


class RedisPoint(BaseModel):
    latitude: float = Field(None, ge=-85, le=85)
    longitude: float = Field(None, ge=-180, le=180)


class RedisLocation(BaseModel):
    point: RedisPoint
    timestamp: datetime = Field(default_factory=lambda: datetime.now(UTC))
    resource_id: int = None

    model_config = ConfigDict(arbitrary_types_allowed=True, json_encoders={ObjectId: str, datetime: str})
