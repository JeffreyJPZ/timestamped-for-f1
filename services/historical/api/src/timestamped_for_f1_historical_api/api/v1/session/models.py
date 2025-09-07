from typing import Optional, TYPE_CHECKING
from datetime import datetime, timedelta

from sqlalchemy import Table, Column, ForeignKey, UniqueConstraint, PrimaryKeyConstraint, DateTime, Integer, Interval
from sqlalchemy.orm import Mapped, mapped_column, relationship

from timestamped_for_f1_historical_api.core.db import Base
from timestamped_for_f1_historical_api.core.models import ResourceModel, ResponseModel
# Prevent circular imports for SQLAlchemy models since we are using type annotation
if TYPE_CHECKING:
    from timestamped_for_f1_historical_api.api.v1.meeting.models import Meeting
    from timestamped_for_f1_historical_api.api.v1.driver.models import Driver
    from timestamped_for_f1_historical_api.api.v1.event.models import Event
    from timestamped_for_f1_historical_api.api.v1.team.models import Team


session_team_assoc = Table(
    "session_team",
    Base.metadata,
    Column("session_id", Integer, ForeignKey("session.id")),
    Column("team_id", Integer, ForeignKey("team.id")),
    PrimaryKeyConstraint("session_id", "team_id")
)


session_driver_assoc = Table(
    "session_driver",
    Base.metadata,
    Column("session_id", Integer, ForeignKey("session.id")),
    Column("driver_id", Integer, ForeignKey("driver.id")),
    PrimaryKeyConstraint("session_id", "driver_id")
)


class Session(Base):
    __tablename__ = "session"
    __table_args__ = (
        UniqueConstraint("meeting_id", "name"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    type: Mapped[str]
    start_date: Mapped[datetime] = mapped_column(DateTime())
    end_date: Mapped[datetime] = mapped_column(DateTime())
    utc_offset: Mapped[timedelta] = mapped_column(Interval())

    # Many-to-one rel with meeting as parent
    meeting_id: Mapped[Optional[int]] = mapped_column(ForeignKey("meeting.id"))
    meeting: Mapped[Optional["Meeting"]] = relationship(back_populates="sessions")

    events: Mapped[list["Event"]] = relationship(
        back_populates="session", cascade="save-update, merge"
    )

    teams: Mapped[list["Team"]] = relationship(
        secondary=session_team_assoc, back_populates="sessions", cascade="save-update, merge"
    )

    drivers: Mapped[list["Driver"]] = relationship(
        secondary=session_driver_assoc, back_populates="sessions", cascade="save-update, merge"
    )

    def __repr__(self) -> str:
        return f"Session(id={self.id!r}, name={self.name!r}, type={self.type!r}, start_date={self.start_date}, end_date={self.end_date}, utc_offset={self.utc_offset!r}, meeting_id={self.meeting_id!r}"
    

class SessionResource(ResourceModel):
    """
    Base Pydantic model for session actions.
    """

    session_id: int | None = None
    meeting_id: int | None = None
    year: int | None = None
    session_name: str | None = None
    session_type: str | None = None
    start_date: datetime | None = None
    end_date: datetime | None = None
    utc_offset: timedelta | None = None


class SessionGet(SessionResource):
    """
    Pydantic model for retrieving sessions.
    """

    pass


class SessionResponse(ResponseModel):
    session_id: int
    circuit_id: int
    meeting_id: int
    year: int
    session_name: str
    session_type: str
    start_date: datetime
    end_date: datetime
    utc_offset: timedelta