from datetime import datetime

from pydantic import BaseModel, field_validator, model_validator


class ReservationBase(BaseModel):
    from_reserve: datetime
    to_reserve: datetime


class ReservationUpdate(ReservationBase):

    @field_validator('from_reserve')
    def check_from_reserve_later_than_now(cls, value):
        if value <= datetime.now():
            raise ValueError('reservation start must be in future')
        return value

    @model_validator(mode='after')
    def check_from_reserve_before_to_reserve(self):
        if self.from_reserve >= self.to_reserve:
            raise ValueError('reservation end must be after start')
        return self


class ReservationCreate(ReservationUpdate):
    room_id: int


class ReservationDB(ReservationBase):
    id: int
    room_id: int

    class Config:
        orm_mode = True
