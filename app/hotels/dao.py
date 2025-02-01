from app.hotels.models import Hotels
from app.dao.basedao import BaseDAO


class HotelDAO(BaseDAO):
    model = Hotels
    