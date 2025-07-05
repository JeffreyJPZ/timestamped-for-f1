from datetime import datetime

from sqlalchemy import ForeignKey, PrimaryKeyConstraint, UniqueConstraint, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.api.event.models import Event
from app.db.core import Base
from app.models import ResponseModel


class RaceControl(Base):
    __tablename__ = "race_control"

    id: Mapped[int] = mapped_column(unique=True) # For internal use only
    date: Mapped[DateTime]
    message: Mapped[str]
    
    # One-to-one weak rel with event as owner
    event_id: Mapped[int] = mapped_column(ForeignKey(column="event.id"), primary_key=True)
    event: Mapped[Event] = relationship(back_populates="race_control", cascade="all, delete-orphan", single_parent=True)
    
    def __repr__(self) -> str:
        return f"RaceControl(id={self.id!r}, date={self.date!r}, message={self.message!r}, event_id={self.event_id!r}"


class RaceControlResponse(ResponseModel):
    date: datetime
    message: str