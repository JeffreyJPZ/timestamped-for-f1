from typing import TYPE_CHECKING
from datetime import datetime
from decimal import Decimal

from sqlalchemy import ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from timestamped_for_f1_historical_api.core.db import Base
from timestamped_for_f1_historical_api.core.models import ResponseModel
# Prevent circular imports for SQLAlchemy models since we are using type annotation
if TYPE_CHECKING:
    from timestamped_for_f1_historical_api.api.v1.event.models import Event
    

class Location(Base):
    __tablename__ = "location"

    id: Mapped[int] = mapped_column(primary_key=True)
    date: Mapped[datetime] = mapped_column(DateTime())
    x: Mapped[int]
    y: Mapped[int]
    z: Mapped[int]
    
    # One-to-one weak rel with event as owner
    event_id: Mapped[int] = mapped_column(ForeignKey("event.id"), unique=True)
    event: Mapped["Event"] = relationship(back_populates="location", single_parent=True)
    
    def __repr__(self) -> str:
        return f"Location(id={self.id!r}, date={self.date!r}, x={self.x!r}, y={self.y!r}, z={self.z!r}, event_id={self.event_id!r}"


class LocationResponse(ResponseModel):
    date: datetime
    x: Decimal
    y: Decimal