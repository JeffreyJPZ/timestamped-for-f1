from typing import TYPE_CHECKING
from datetime import datetime
from decimal import Decimal

from sqlalchemy import ForeignKey, DateTime, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship

from timestamped_for_f1_historical_api.core.db import Base
from timestamped_for_f1_historical_api.core.models import ResponseModel
# Prevent circular imports for SQLAlchemy models since we are using type annotation
if TYPE_CHECKING:
    from timestamped_for_f1_historical_api.api.v1.event.models import Event


class Pit(Base):
    __tablename__ = "pit"

    id: Mapped[int] = mapped_column(primary_key=True)
    date: Mapped[datetime] = mapped_column(DateTime())
    duration: Mapped[Decimal] = mapped_column(Numeric(precision=6, scale=1)) # Max pit duration should be in the hours
    
    # One-to-one weak rel with event as owner
    event_id: Mapped[int] = mapped_column(ForeignKey("event.id"), unique=True)
    event: Mapped["Event"] = relationship(back_populates="pit", single_parent=True)
    
    def __repr__(self) -> str:
        return f"Pit(id={self.id!r}, date={self.date!r}, duration={self.duration!r}, event_id={self.event_id!r}"


class PitResponse(ResponseModel):
    date: datetime
    duration: Decimal