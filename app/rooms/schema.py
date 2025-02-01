from pydantic import BaseModel
from typing import Optional


class RoomCreateSchema(BaseModel):
    hotel_id: int
    name: str
    description: str
    price: float
    services: list
    quantity: int
    image_id: int

class RoomResponseSchema(RoomCreateSchema):
    id: int

    class Config:
        from_attributes = True


class RoomUpdateImageSchema(BaseModel):
    image_id: int


class RoomUpdatePrice(BaseModel):
    price: int


class RoomUpdateDescription(BaseModel):
    description: str
 
 
class RoomUpdateServicesSchema(BaseModel):
    services: list


class RoomUpdateQuantitySchema(BaseModel):
    quantity: int


class RoomUpdate(BaseModel):
    description: str
    price: float
    services: list
    quantity: int
    image_id: int