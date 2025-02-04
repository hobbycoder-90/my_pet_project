from fastapi import APIRouter
from sqlalchemy import update

from app.exceptions import HotelNotFoundExeption, RoomAlreadyExistsExeption, RoomNotFoundExeption
from app.rooms.models import Rooms
from app.rooms.schema import RoomResponseSchema, RoomCreateSchema, RoomUpdate, RoomUpdateDescription, RoomUpdateImageSchema, RoomUpdatePrice, RoomUpdateQuantitySchema, RoomUpdateServicesSchema
from app.rooms.dao import RoomDAO
from app.database import async_session_maker
from app.hotels.dao import HotelDAO





router = APIRouter(
    prefix="/rooms",
    tags=["Rooms"]
)


@router.get("/all", response_model=list[RoomResponseSchema], status_code=200)
async def get_all_rooms():
    return await RoomDAO.find_all()


@router.get("/{room_id}", response_model=RoomCreateSchema, status_code=200)
async def get_room_by_id(room_id: int):
    result = await RoomDAO.find_one_or_none(id=room_id)
    if not result:
        raise RoomNotFoundExeption 
    return result


@router.post("/add", response_model=RoomResponseSchema, status_code=201)
async def add_room(room_data: RoomCreateSchema):
    existing_room = await RoomDAO.find_one_or_none(name=room_data.name)
    if existing_room:
        raise RoomAlreadyExistsExeption
    existing_hotel = await HotelDAO.find_one_or_none(id = room_data.hotel_id)
    if not existing_hotel:
        raise HotelNotFoundExeption
    new_room = await RoomDAO.add(
            hotel_id = room_data.hotel_id,
            name = room_data.name,
            description = room_data.description,
            price = room_data.price,
            services = room_data.services,
            quantity = room_data.quantity,
            image_id = room_data.image_id)
    await RoomDAO.update_hotel_rooms_quantity(room_data.hotel_id, room_data.quantity)
    return new_room


@router.patch("/{room_id}/update_image", response_model=RoomResponseSchema, status_code=200)
async def update_room_services(room_id:int, room_data: RoomUpdateImageSchema):
    async with async_session_maker() as session:
        room_exis = await RoomDAO.find_one_or_none(id = room_id)
        if not room_exis:
            raise RoomNotFoundExeption
        query = update(Rooms).where(Rooms.id == room_id).values(
            image_id = room_data.image_id
        ).returning(Rooms.__table__.columns)
        upd_room = await session.execute(query)
        await session.commit()
        return upd_room.mappings().one()
    

@router.patch("/{room_id}/update_price", response_model=RoomResponseSchema, status_code=200)
async def update_room_price(room_id:int, room_data: RoomUpdatePrice):
    async with async_session_maker() as session:
        room_exis = await RoomDAO.find_one_or_none(id = room_id)
        if not room_exis:
            raise RoomNotFoundExeption
        query = update(Rooms).where(Rooms.id == room_id).values(
            price = room_data.price
        ).returning(Rooms.__table__.columns)
        upd_room = await session.execute(query)
        await session.commit()
        return upd_room.mappings().one()
    

@router.patch("/{room_id}/update_description", response_model=RoomResponseSchema, status_code=200)
async def update_room_description(room_id:int, room_data: RoomUpdateDescription):
    async with async_session_maker() as session:
        room_exis = await RoomDAO.find_one_or_none(id = room_id)
        if not room_exis:
            raise RoomNotFoundExeption
        query = update(Rooms).where(Rooms.id == room_id).values(
            description = room_data.description
        ).returning(Rooms.__table__.columns)
        upd_room = await session.execute(query)
        await session.commit()
        return upd_room.mappings().one()
    

@router.patch("/{room_id}/update_services", response_model=RoomResponseSchema, status_code=200)
async def update_room_services(room_id:int, room_data: RoomUpdateServicesSchema):
    async with async_session_maker() as session:
        room_exis = await RoomDAO.find_one_or_none(id = room_id)
        if not room_exis:
            raise RoomNotFoundExeption
        query = update(Rooms).where(Rooms.id == room_id).values(
            services = room_data.services
        ).returning(Rooms.__table__.columns)
        upd_room = await session.execute(query)
        await session.commit()
        return upd_room.mappings().one()
    

@router.patch("/{room_id}/update_quantity", response_model=RoomResponseSchema, status_code=200)
async def update_room_quantity(room_id:int, room_data: RoomUpdateQuantitySchema):
    async with async_session_maker() as session:
        room_exis = await RoomDAO.find_one_or_none(id = room_id)
        if not room_exis:
            raise RoomNotFoundExeption
        query = update(Rooms).where(Rooms.id == room_id).values(
            quantity = room_data.quantity
        ).returning(Rooms.__table__.columns)

        upd_room = await session.execute(query)
        await RoomDAO.update_hotel_rooms_quantity(room_exis.hotel_id, room_data.quantity - room_exis.quantity)
        await session.commit()
        return upd_room.mappings().one()


@router.put("/{room_id}/update", response_model=RoomResponseSchema, status_code=200)
async def update_room(room_id:int, room_data: RoomUpdate):
    async with async_session_maker() as session:
        room_exis = await RoomDAO.find_one_or_none(id = room_id)
        if not room_exis:
            raise RoomNotFoundExeption
        query = update(Rooms).where(Rooms.id == room_id).values(
            description = room_data.description,
            price = room_data.price,
            services = room_data.services,
            quantity = room_data.quantity,
            image_id = room_data.image_id
        ).returning(Rooms.__table__.columns)

        upd_room = await session.execute(query)
        await RoomDAO.update_hotel_rooms_quantity(room_exis.hotel_id, room_data.quantity - room_exis.quantity)
        await session.commit()
        return upd_room.mappings().one()


@router.delete("/{room_id}/delete", response_model=RoomResponseSchema, status_code=202)
async def delete_hotel_by_id(room_id: int):
    return await RoomDAO.delete(room_id)