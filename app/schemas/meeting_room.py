from typing import Optional

from pydantic import BaseModel, Field


class MeetingRoomCreate(BaseModel):
    name: str = Field(None, min_length=1, max_length=100)
    description: Optional[str]
