from datetime import datetime
from decimal import Decimal

from sqlalchemy import ForeignKey, PrimaryKeyConstraint, UniqueConstraint, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from historical_api.api.v1.event.models import Event
from historical_api.core.db import Base
from historical_api.core.models import ResponseModel


class Location(Base):
    __tablename__ = "location"
    
    id: Mapped[int] = mapped_column(unique=True) # For internal use only
    date: Mapped[DateTime]
    x: Mapped[int]
    y: Mapped[int]
    z: Mapped[int]
    
    # One-to-one weak rel with event as owner
    event_id: Mapped[int] = mapped_column(ForeignKey(column="event.id"), primary_key=True)
    event: Mapped[Event] = relationship(back_populates="location", cascade="all, delete-orphan", single_parent=True)
    
    def __repr__(self) -> str:
        return f"Location(id={self.id!r}, date={self.date!r}, x={self.x!r}, y={self.y!r}, z={self.z!r}, event_id={self.event_id!r}"


class LocationResponse(ResponseModel):
    date: datetime
    x: Decimal
    y: Decimal