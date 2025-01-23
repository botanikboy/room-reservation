from datetime import datetime, timedelta

from pydantic import BaseModel, field_validator, model_validator, Field

FROM_TIME = (datetime.now() + timedelta(minutes=10)
             ).isoformat(sep=' ', timespec='minutes')
TO_TIME = (datetime.now() + timedelta(hours=1)
           ).isoformat(sep=' ', timespec='minutes')


class ReservationBase(BaseModel):
    from_reserve: datetime = Field(..., example=FROM_TIME)
    to_reserve: datetime = Field(..., example=TO_TIME)


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

    class Config:
        extra = 'forbid'


class ReservationCreate(ReservationUpdate):
    room_id: int


class ReservationDB(ReservationBase):
    id: int
    room_id: int

    class Config:
        orm_mode = True

    @staticmethod
    def _format_datetime(value: datetime) -> datetime:
        if isinstance(value, datetime):
            return value.isoformat(sep=' ', timespec='minutes')
        return value

    @field_validator('from_reserve', 'to_reserve')
    def format_datetime(cls, value):
        return cls._format_datetime(value)
