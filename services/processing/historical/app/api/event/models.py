from datetime import datetime, timedelta

from sqlalchemy import ForeignKeyConstraint, DateTime, Interval
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.api.session.models import Session
from app.api.driver.models import Driver
from app.api.event_role.models import EventRoleResponse
from app.api.location.models import Location, LocationResponse
from app.api.pit.models import Pit, PitResponse
from app.api.race_control.models import RaceControl, RaceControlResponse
from app.db.core import Base
from app.models import ResourceModel, ResponseModel

class Event(Base):
    __tablename__ = "event"
    __table_args__ = (
        ForeignKeyConstraint(
            columns=("meeting_id", "session_name"),
            refcolumns=("session.meeting_id, session.name"),
            name="fk_event_meeting_id_and_session_name"
        )
    )
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    date: Mapped[DateTime]
    elapsed_time: Mapped[Interval]
    lap_number: Mapped[int | None]
    category: Mapped[str]
    cause: Mapped[str]

    # Many-to-one rel with session as parent
    meeting_id: Mapped[int]
    session_name: Mapped[str]
    session: Mapped[Session] = relationship(back_populates="events")

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
    meeting_id: int | None = None
    session_name: str | None = None
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
    session_name: str
    data: EventDataResponse