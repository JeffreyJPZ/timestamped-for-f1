from typing import Optional, TYPE_CHECKING
from datetime import datetime, timedelta

from sqlalchemy import Table, Column, ForeignKey, PrimaryKeyConstraint, UniqueConstraint, DateTime, Integer, Interval
from sqlalchemy.orm import Mapped, mapped_column, relationship

from timestamped_for_f1_historical_api.core.db import Base
from timestamped_for_f1_historical_api.core.models import ResourceModel, ResponseModel
# Prevent circular imports for SQLAlchemy models since we are using type annotation
if TYPE_CHECKING:
    from timestamped_for_f1_historical_api.api.v1.circuit.models import Circuit
    from timestamped_for_f1_historical_api.api.v1.driver.models import Driver
    from timestamped_for_f1_historical_api.api.v1.session.models import Session
    from timestamped_for_f1_historical_api.api.v1.team.models import Team


meeting_team_assoc = Table(
    "meeting_team",
    Base.metadata,
    Column("meeting_id", Integer, ForeignKey("meeting.id")),
    Column("team_id", Integer, ForeignKey("team.id")),
    PrimaryKeyConstraint("meeting_id", "team_id")
)


meeting_driver_assoc = Table(
    "meeting_driver",
    Base.metadata,
    Column("meeting_id", Integer, ForeignKey("meeting.id")),
    Column("driver_id", Integer, ForeignKey("driver.id")),
    PrimaryKeyConstraint("meeting_id", "driver_id"),
)


class Meeting(Base):
    __tablename__ = "meeting"
    __table_args__ = (
        UniqueConstraint("year", "name"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    year: Mapped[int]
    name: Mapped[str]
    official_name: Mapped[str]
    start_date: Mapped[datetime] = mapped_column(DateTime())
    utc_offset: Mapped[str] = mapped_column(Interval())

    # Many-to-one rel with circuit as parent
    circuit_id: Mapped[Optional[int]] = mapped_column(ForeignKey("circuit.id"))
    circuit: Mapped[Optional["Circuit"]] = relationship(back_populates="meetings")

    sessions: Mapped[list["Session"]] = relationship(
        back_populates="meeting", cascade="all, delete-orphan"
    )

    teams: Mapped[list["Team"]] = relationship(
        secondary=meeting_team_assoc, back_populates="meetings", cascade="all, delete-orphan"
    )

    drivers: Mapped[list["Driver"]] = relationship(
        secondary=meeting_driver_assoc, back_populates="meetings", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"Meeting(id={self.id!r}, year={self.year!r}, name={self.name!r}, official_name={self.official_name!r}, start_date={self.start_date}, utc_offset={self.utc_offset!r}, circuit_id={self.circuit_id!r})"
    

class MeetingResource(ResourceModel):
    """
    Base Pydantic model for meeting actions.
    """

    meeting_id: int | None = None
    year: int | None = None
    meeting_name: str | None = None
    meeting_official_name: str | None = None
    start_date: datetime | None = None
    utc_offset: timedelta | None = None


class MeetingGet(MeetingResource):
    """
    Pydantic model for retrieving meetings.
    """

    pass


class MeetingResponse(ResponseModel):
    meeting_id: int
    session_ids: list[int]
    circuit_id: int
    year: int
    meeting_name: str
    meeting_official_name: str
    start_date: datetime
    utc_offset: timedelta