from datetime import datetime, timedelta

from sqlalchemy import Table, Column, ForeignKey, ForeignKeyConstraint, PrimaryKeyConstraint, DateTime, Integer, Interval
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.api.meeting.models import Meeting
from app.api.driver.models import Driver
from app.api.event.models import Event
from app.api.team.models import Team
from app.db.core import Base
from app.models import QueryModel, ResourceModel, ResponseModel


session_team_assoc = Table(
    Column("meeting_id", Integer),
    Column("session_name", Integer),
    Column("team_id", Integer, ForeignKey("team.id")),
    PrimaryKeyConstraint(
        ("meeting_id", "session_name", "team_id"),
        name="pk_session_team_meeting_id_and_session_name_and_team_id"
    ),
    ForeignKeyConstraint(
        columns=("meeting_id", "session_name"),
        refcolumns=("session.meeting_id", "session.name"),
        name="fk_session_team_meeting_id_and_session_name"
    ),
    name="session_team",
    metadata=Base.metadata
)


session_driver_assoc = Table(
    Column("meeting_id", Integer),
    Column("session_name", Integer),
    Column("driver_id", Integer, ForeignKey("driver.id")),
    PrimaryKeyConstraint(
        ("meeting_id", "session_name", "driver_id"),
        name="pk_session_driver_meeting_id_and_session_name_and_driver_id"
    ),
    ForeignKeyConstraint(
        columns=("meeting_id", "session_name"),
        refcolumns=("session.meeting_id", "session.name"),
        name="fk_session_driver_meeting_id_and_session_name"
    ),
    name="session_driver",
    metadata=Base.metadata
)


class Session(Base):
    __tablename__ = "session"

    id: Mapped[int] = mapped_column(unique=True) # For internal use only
    name: Mapped[str] = mapped_column(primary_key=True)
    type: Mapped[str]
    start_date: Mapped[DateTime]
    end_date: Mapped[DateTime]
    utc_offset: Mapped[Interval]

    # Weak rel with meeting as parent
    meeting_id: Mapped[int] = mapped_column(ForeignKey(column="meeting.id"), primary_key=True)
    meeting: Mapped[Meeting] = relationship(back_populates="sessions")

    events: Mapped[list[Event]] = relationship(
        back_populates="session", cascade="all, delete-orphan"
    )

    teams: Mapped[list[Team]] = relationship(
        secondary=session_team_assoc, back_populates="sessions", cascade="all, delete-orphan"
    )

    drivers: Mapped[list[Driver]] = relationship(
        secondary=session_driver_assoc, back_populates="sessions", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"Session(id={self.id!r}, name={self.name!r}, type={self.type!r}, start_date={self.start_date}, end_date={self.end_date}, utc_offset={self.utc_offset!r}, meeting_id={self.meeting_id!r}"
    

class SessionResource(ResourceModel):
    """
    Base Pydantic model for session actions.
    """

    meeting_id: int | None = None
    meeting_name: str | None = None
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
    circuit_id: int
    meeting_id: int
    meeting_name: str
    year: int
    session_name: str
    session_type: str
    start_date: datetime
    end_date: datetime
    utc_offset: timedelta