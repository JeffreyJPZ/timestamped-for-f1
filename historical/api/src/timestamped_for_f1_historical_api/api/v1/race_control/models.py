from typing import TYPE_CHECKING
from datetime import datetime

from sqlalchemy import ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from timestamped_for_f1_historical_api.core.db import Base, get_base_metadata
from timestamped_for_f1_historical_api.core.models import ResponseModel
# Prevent circular imports for SQLAlchemy models since we are using type annotation
if TYPE_CHECKING:
    from timestamped_for_f1_historical_api.api.v1.event.models import Event


class RaceControl(Base):
    __tablename__ = "race_control"
    metadata = get_base_metadata()

    id: Mapped[int] = mapped_column(unique=True) # For internal use only
    date: Mapped[datetime] = mapped_column(DateTime())
    message: Mapped[str]
    
    # One-to-one weak rel with event as owner
    event_id: Mapped[int] = mapped_column(ForeignKey(column="event.id"), primary_key=True)
    event: Mapped["Event"] = relationship(back_populates="race_control", cascade="all, delete-orphan", single_parent=True)
    
    def __repr__(self) -> str:
        return f"RaceControl(id={self.id!r}, date={self.date!r}, message={self.message!r}, event_id={self.event_id!r}"


class RaceControlResponse(ResponseModel):
    date: datetime
    message: str