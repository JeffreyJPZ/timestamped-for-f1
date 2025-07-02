from datetime import datetime
from decimal import Decimal

from sqlalchemy import ForeignKey, PrimaryKeyConstraint, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.api.event.models import Event
from app.db.core import Base
from app.models import QueryModel, ResponseModel


class Location(Base):
    __tablename__ = "location"
    __table_args__ = (
        PrimaryKeyConstraint(
            ("event_id", "date"),
            name="pk_location_event_id_and_date"
        )
    )
    
    date: Mapped[DateTime]
    x: Mapped[int]
    y: Mapped[int]
    z: Mapped[int]
    
    # One-to-one weak rel with event as owner
    event_id: Mapped[int] = mapped_column(ForeignKey(column="event.id"))
    event: Mapped[Event] = relationship(back_populates="location", cascade="all, delete-orphan", single_parent=True)
    
    def __repr__(self) -> str:
        return f"Location(date={self.date!r}, x={self.x!r}, y={self.y!r}, z={self.z!r}, event_id={self.event_id!r}"


class LocationColumns(QueryModel):
    date: datetime | None = None
    x: Decimal | None = None
    y: Decimal | None = None


class LocationResponse(ResponseModel):
    date: datetime
    x: Decimal
    y: Decimal