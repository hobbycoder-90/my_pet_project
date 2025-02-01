from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import JSON, ForeignKey

from app.database import Base
from app.hotels.models import Hotels


class Rooms(Base):
    __tablename__ = "rooms"

    id          : Mapped[int] = mapped_column(primary_key=True, nullable=False)
    hotel_id    : Mapped[int] = mapped_column(ForeignKey("hotels.id", ondelete="CASCADE"), nullable=False)
    name        : Mapped[str] = mapped_column(nullable=False)
    description : Mapped[str] = mapped_column(nullable=False)
    price       : Mapped[int] = mapped_column(nullable=False)
    services    : Mapped[list[str]] = mapped_column(JSON, nullable=False)
    quantity    : Mapped[int] = mapped_column(nullable=False)
    image_id    : Mapped[int]
