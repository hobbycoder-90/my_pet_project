from typing import TYPE_CHECKING
from sqlalchemy import JSON, Integer
from sqlalchemy.orm import relationship, mapped_column, Mapped

from app.database import Base


if TYPE_CHECKING:
    # Убирает предупреждения отсутствия импорта и неприятные подчеркивания в 
    # PyCharm и VSCode
    from app.rooms.models import Rooms


class Hotels(Base):
    __tablename__ = "hotels"

    id             : Mapped[int] = mapped_column(Integer, primary_key=True)
    name           : Mapped[str] = mapped_column(nullable=False)
    location       : Mapped[str] = mapped_column(nullable=False)
    services       : Mapped[list[str]] = mapped_column(JSON)
    rooms_quantity : Mapped[int] = mapped_column(nullable=False)
    image_id       : Mapped[int]

