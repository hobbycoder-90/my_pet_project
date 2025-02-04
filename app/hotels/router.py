from fastapi import APIRouter, Depends, Query
from fastapi_cache.decorator import cache

from sqlalchemy import update

from app.database import async_session_maker

from app.exceptions import HotelAlreadyExistsExeption, HotelNotFoundExeption
from app.auth.dependencies import get_current_user
from app.users.schema import UserResponseSchema
from app.hotels.schema import HotelCreateSchema, HotelResponseSchema, HotelUpdateImageSchema, HotelUpdateServicesSchema, HotelUpdateRoomQuantitySchema, HotelUpdate
from app.hotels.dao import HotelDAO
from app.hotels.models import Hotels
from datetime import date, datetime, timedelta



router = APIRouter(
    prefix="/hotels",
    tags=["Hotels"]
)


@router.get("/all", response_model=list[HotelResponseSchema], status_code=200)
async def get_all_hotels():
    return await HotelDAO.find_all()

@router.get("/{hotel_id}", response_model=HotelCreateSchema, status_code=200)
async def get_hotel_by_id(hotel_id: int):
    result = await HotelDAO.find_one_or_none(id = hotel_id)
    if not result:
        raise HotelNotFoundExeption
    return result


#@router.get("/{location}")
#@cache(expire=30)
#async def get_hotels_by_location_and_time(
#    location: str,
#    date_from: date = Query(..., description=f"Например, {datetime.now().date()}"),
#    date_to: date = Query(..., description=f"Например, {(datetime.now() + timedelta(days=14)).date()}"),
#) -> List[SHotelInfo]:
#    if date_from > date_to:
#        raise DateFromCannotBeAfterDateTo
#    if (date_to - date_from).days > 31:
#        raise CannotBookHotelForLongPeriod 
#    hotels = await HotelDAO.find_all(location, date_from, date_to)
#    return hotels


@router.post("/add", response_model=HotelCreateSchema, status_code=201)
async def add_hotel(hotel_data: HotelCreateSchema):
    existing_hotel = await HotelDAO.find_one_or_none(name=hotel_data.name)
    if existing_hotel:
        raise HotelAlreadyExistsExeption
    new_hotel= await HotelDAO.add(name=hotel_data.name,
                                location=hotel_data.location,
                                services=hotel_data.services,
                                rooms_quantity=hotel_data.rooms_quantity,
                                image_id=hotel_data.image_id)
    return new_hotel


@router.patch("/{hotel_id}/update_image", response_model=HotelResponseSchema, status_code=200)
async def update_hotel_image(hotel_id:int, hotel_data: HotelUpdateImageSchema):
    async with async_session_maker() as session:
        hotel_exis = await HotelDAO.find_one_or_none(hotel_id)
        if not hotel_exis:
            raise HotelNotFoundExeption
        query = update(Hotels).where(Hotels.id == hotel_id).values(
            image_id = hotel_data.image_id
        ).returning(Hotels.__table__.columns)
        upd_hotel = await session.execute(query)
        await session.commit()
        return upd_hotel.mappings().one()


@router.patch("/{hotel_id}/update_services", response_model=HotelResponseSchema, status_code=200)
async def update_hotel_services(hotel_id:int, hotel_data: HotelUpdateServicesSchema):
    async with async_session_maker() as session:
        hotel_exis = await HotelDAO.find_one_or_none(hotel_id)
        if not hotel_exis:
            raise HotelNotFoundExeption
        query = update(Hotels).where(Hotels.id == hotel_id).values(
            services = hotel_data.services
        ).returning(Hotels.__table__.columns)
        upd_hotel = await session.execute(query)
        await session.commit()
        return upd_hotel.mappings().one()


@router.patch("/{hotel_id}/update_rooms_quantity", response_model=HotelResponseSchema, status_code=200)
async def update_hotel_rooms_quantity(hotel_id:int, hotel_data: HotelUpdateRoomQuantitySchema):
    async with async_session_maker() as session:
        hotel_exis = await HotelDAO.find_one_or_none(id=hotel_id)
        if not hotel_exis:
            raise HotelNotFoundExeption
        query = update(Hotels).where(Hotels.id == hotel_id).values(
            rooms_quantity = hotel_data.rooms_quantity
        ).returning(Hotels.__table__.columns)
        upd_hotel = await session.execute(query)
        await session.commit()
        return upd_hotel.mappings().one()


@router.put("/{hotel_id}/update_room_quantity_and_services_and_image", response_model=HotelResponseSchema, status_code=200)
async def update_hotel_room_quantity_and_services_and_image(hotel_id : int, hotel_data: HotelUpdate):
    async with async_session_maker() as session:
        hotel_exis = await HotelDAO.find_one_or_none(hotel_id)
        if not hotel_exis:
            raise HotelNotFoundExeption
        query = update(Hotels).where(Hotels.id == hotel_id).values(
            rooms_quantity = hotel_data.rooms_quantity,
            services = hotel_data.services,
            image_id = hotel_data.image_id,
        ).returning(Hotels.__table__.columns)
        upd_hotel = await session.execute(query)
        await session.commit()
        return upd_hotel.mappings().one()



@router.delete("/{hotel_id}/delete", response_model=HotelResponseSchema, status_code=202)
async def delete_hotel_by_id(hotel_id: int):
    hotel = await HotelDAO.find_one_or_none(hotel_id)
    if not hotel:
        raise HotelNotFoundExeption
    return await HotelDAO.delete(hotel_id)