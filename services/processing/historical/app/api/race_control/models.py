from datetime import datetime

from sqlalchemy import ForeignKey, PrimaryKeyConstraint, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.api.event.models import Event
from app.db.core import Base
from app.models import QueryModel, ResponseModel


class RaceControl(Base):
    __tablename__ = "race_control"
    __table_args__ = (
        PrimaryKeyConstraint(
            ("event_id", "date"),
            name="pk_race_control_event_id_and_date"
        )
    )

    date: Mapped[DateTime]
    message: Mapped[str]
    
    # One-to-one weak rel with event as owner
    event_id: Mapped[int] = mapped_column(ForeignKey(column="event.id"))
    event: Mapped[Event] = relationship(back_populates="race_control", cascade="all, delete-orphan", single_parent=True)
    
    def __repr__(self) -> str:
        return f"RaceControl(date={self.date!r}, message={self.message!r}, event_id={self.event_id!r}"


class RaceControlColumns(QueryModel):
    date: datetime | None = None
    message: str | None = None


class RaceControlResponse(ResponseModel):
    date: datetime
    message: str