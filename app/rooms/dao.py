from sqlalchemy import update

from app.rooms.models import Rooms
from app.dao.basedao import BaseDAO

from app.database import async_session_maker
from app.hotels.dao import HotelDAO
from app.hotels.models import Hotels
from app.exceptions import HotelNotFoundExeption




class RoomDAO(BaseDAO):
    model = Rooms
    

    @classmethod
    async def update_hotel_rooms_quantity(cls, hotel_id:int, rooms_quantity: int):
        async with async_session_maker() as session:
            hotel_exis = await HotelDAO.find_by_id(hotel_id)
            if not hotel_exis:
                raise HotelNotFoundExeption
            
            old_quantity = hotel_exis.rooms_quantity 

            query = update(Hotels).where(Hotels.id == hotel_id).values(
                rooms_quantity = rooms_quantity + old_quantity
            ).returning(Hotels.__table__.columns)
            await session.execute(query)
            await session.commit()
            