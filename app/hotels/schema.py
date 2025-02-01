from pydantic import BaseModel
from typing import Optional


class HotelCreateSchema(BaseModel):
    name: str
    location: str
    services: list
    rooms_quantity: int
    image_id: Optional[int] = None



class HotelResponseSchema(HotelCreateSchema):
    id: int

    class Config:
        from_attributes = True


class HotelUpdateImageSchema(BaseModel):
    image_id: int


class HotelUpdateServicesSchema(BaseModel):
    services: Optional[list | None]


class HotelUpdateRoomQuantitySchema(BaseModel):
    rooms_quantity: int


class HotelUpdate(HotelUpdateImageSchema, HotelUpdateRoomQuantitySchema, HotelUpdateServicesSchema):
    pass