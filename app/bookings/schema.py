from pydantic import BaseModel
from typing import Optional
from datetime import date


class BookingCreateSchema(BaseModel):    
    room_id: int
    user_id: int
    hotel_id: int
    date_from: date
    date_to: date




class BookingResponseSchema(BookingCreateSchema):
    id: int
    total_cost: int
    totel_days: int
    price: int

    class Config:
        from_attributes = True


class BookingUpdateDate(BaseModel):
    date_from: date
    date_to: date




