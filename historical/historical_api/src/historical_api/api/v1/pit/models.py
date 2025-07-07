from datetime import datetime
from decimal import Decimal

from sqlalchemy import ForeignKey, PrimaryKeyConstraint, UniqueConstraint, DateTime, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship

from historical_api.api.v1.event.models import Event
from historical_api.core.db import Base
from historical_api.core.models import ResponseModel


class Pit(Base):
    __tablename__ = "pit"

    id: Mapped[int] = mapped_column(unique=True) # For internal use only
    date: Mapped[DateTime]
    duration: Mapped[Numeric] = mapped_column(Numeric(precision=6, scale=1)) # Max pit duration should be in the hours
    
    # One-to-one weak rel with event as owner
    event_id: Mapped[int] = mapped_column(ForeignKey(column="event.id"), primary_key=True)
    event: Mapped[Event] = relationship(back_populates="pit", cascade="all, delete-orphan", single_parent=True)
    
    def __repr__(self) -> str:
        return f"Pit(id={self.id!r}, date={self.date!r}, duration={self.duration!r}, event_id={self.event_id!r}"


class PitResponse(ResponseModel):
    date: datetime
    duration: Decimal