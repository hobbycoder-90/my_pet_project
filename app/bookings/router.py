from fastapi import APIRouter, Depends
from app.database import async_session_maker
from app.exceptions import BookingNotFoundExeption

from app.auth.dependencies import get_current_user

from app.users.schema import UserResponseSchema

from app.users.models import Users
from app.bookings.dao import BookingDAO
from app.bookings.schema import BookingResponseSchema, BookingCreateSchema
from app.exceptions import RoomCannotBeBooked, BookingNotMyExeption


router = APIRouter(
    prefix="/bookings",
    tags=["Bookings"]
)


@router.get("/all", response_model= list[BookingResponseSchema], status_code=200)
async def get_all_bookings(current_user: UserResponseSchema = Depends(get_current_user)):
    return await BookingDAO.find_all()


@router.get("/my_bookins", response_model= list[BookingResponseSchema], status_code=200)
async def get_my_bookings(current_user: UserResponseSchema = Depends(get_current_user)):
    result = await BookingDAO.find_all(user_id=current_user.id)
    if not result:
       raise BookingNotFoundExeption
    return result


@router.get("/{booking_id}")
async def get_bookings_by_id(booking_id:int):
   result = await BookingDAO.find_one_or_none(id=booking_id)
   if not result:
       raise BookingNotFoundExeption
   return result


@router.post("/add", response_model=BookingResponseSchema, status_code=201)
async def add_booking(booking_data: BookingCreateSchema, user: Users = Depends(get_current_user)):
    booking = await BookingDAO.add(user.id, booking_data.hotel_id, booking_data.room_id,
                                   booking_data.date_from, booking_data.date_to)
    if not booking:
       raise RoomCannotBeBooked
    
    return booking


@router.delete("/{booking_id}/delete", response_model=BookingResponseSchema, status_code=202)
async def delete_my_booking_by_id(booking_id:int, user: Users = Depends(get_current_user)):
    booking = await BookingDAO.find_one_or_none(id=booking_id)
    if not booking:
        raise BookingNotFoundExeption
    elif booking.user_id != user.id:
        raise BookingNotMyExeption
    return await BookingDAO.delete(booking_id)