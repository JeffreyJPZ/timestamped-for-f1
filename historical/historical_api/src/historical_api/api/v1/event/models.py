from datetime import datetime, timedelta

from sqlalchemy import ForeignKey, DateTime, Interval
from sqlalchemy.orm import Mapped, mapped_column, relationship

from historical_api.api.v1.session.models import Session
from historical_api.api.v1.driver.models import Driver
from historical_api.api.v1.event_role.models import EventRoleResponse
from historical_api.api.v1.location.models import Location, LocationResponse
from historical_api.api.v1.pit.models import Pit, PitResponse
from historical_api.api.v1.race_control.models import RaceControl, RaceControlResponse
from historical_api.core.db import Base
from historical_api.core.models import ResourceModel, ResponseModel

class Event(Base):
    __tablename__ = "event"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    date: Mapped[DateTime]
    elapsed_time: Mapped[Interval]
    lap_number: Mapped[int | None]
    category: Mapped[str]
    cause: Mapped[str]

    # Many-to-one rel with session as parent
    session_id: Mapped[int] = mapped_column(ForeignKey(column="session.id"))
    session: Mapped[Session] = relationship(back_populates="events", cascade="all, delete-orphan")

    # One-to-one rel with location
    location: Mapped[Location | None] = relationship(back_populates="event", cascade="all, delete-orphan")

    # One-to-one rel with pit
    pit: Mapped[Pit | None] = relationship(back_populates="event", cascade="all, delete-orphan")

    # One-to-one rel with race control
    race_control: Mapped[RaceControl | None] = relationship(back_populates="event", cascade="all, delete-orphan")

    # Many-to-many rel with driver
    drivers: Mapped[list[Driver] | None] = relationship(back_populates="event", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"Event(id={self.id!r}, date={self.date!r}, elapsed_time={self.elapsed_time!r}), lap_number={self.lap_number!r}, category={self.category!r}, cause={self.cause!r}, meeting_id={self.meeting_id!r}, session_name={self.session_name!r}"


class EventResource(ResourceModel):
    """
    Base Pydantic model for event actions.
    """

    event_id: int | None = None
    session_id: str | None = None
    date: datetime | None = None
    elapsed_time: timedelta | None = None
    lap_number: int | None = None
    category: str | None = None
    cause: str | None = None


class EventGet(EventResource):
    """
    Pydantic model for retrieving events.
    """

    pass


class EventDataResponse(ResponseModel):
    date: datetime
    elapsed_time: timedelta
    lap_number: int | None
    category: str
    cause: str
    roles: list[EventRoleResponse] | None
    details: LocationResponse | PitResponse | RaceControlResponse


class EventResponse(ResponseModel):
    event_id: int
    circuit_id: int
    meeting_id: int
    session_id: int
    data: EventDataResponse