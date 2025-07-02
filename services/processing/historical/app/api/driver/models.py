from sqlalchemy import ForeignKey, UniqueConstraint, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.api.country.models import Country
from app.api.meeting.models import Meeting, meeting_driver_assoc
from app.api.session.models import Session, session_driver_assoc
from app.api.team.models import Team, team_driver_assoc
from app.api.event.models import Event
from app.db.core import Base
from app.models import QueryModel, RequestModel, ResponseModel


class Driver(Base):
    __tablename__ = "driver"
    __table_args__ = (
        UniqueConstraint(
            ("year", "number"),
            name="uq_driver_year_and_number"
        )
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    year: Mapped[int]
    number: Mapped[int]
    acronym: Mapped[str] = mapped_column(String(length=3))
    first_name: Mapped[str]
    last_name: Mapped[str]
    full_name: Mapped[str]
    broadcast_name: Mapped[str]
    image_url: Mapped[str]

    # Many-to-one rel with country as parent
    country_id: Mapped[int] = mapped_column(ForeignKey(column="country.id"))
    country: Mapped[Country] = relationship(back_populates="drivers")

    meetings: Mapped[list[Meeting]] = relationship(
        secondary=meeting_driver_assoc, back_populates="drivers", cascade="all, delete-orphan"
    )

    sessions: Mapped[list[Session]] = relationship(
        secondary=session_driver_assoc, back_populates="drivers", cascade="all, delete-orphan"
    )

    teams: Mapped[list[Team]] = relationship(
        secondary=team_driver_assoc, back_populates="drivers", cascade="all, delete-orphan"
    )

    events: Mapped[list[Event | None]] = relationship(back_populates="driver", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"Driver(id={self.id!r}, year={self.year!r}, number={self.number!r}, acronym={self.acronym!r}, first_name={self.first_name!r}, last_name={self.last_name!r}, full_name={self.full_name!r}, broadcast_name={self.broadcast_name!r}, image_url={self.image_url!r}, country_id={self.country_id!r}"
    

class DriverFilterParams(RequestModel):
    driver_id: int | None = None
    year: int | None = None
    driver_number: int | None = None
    driver_acronym: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    full_name: str | None = None
    broadcast_name: str | None = None
    image_url: str | None = None
    country_id: int | None = None
    country_code: str | None = None


class DriverColumns(QueryModel):
    id: int | None = None
    year: int | None = None
    number: int | None = None
    acronym: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    full_name: str | None = None
    broadcast_name: str | None = None
    image_url: str | None = None


class DriverResponse(ResponseModel):
    driver_id: int
    team_id: int
    year: int
    driver_number: int
    driver_acronym: str
    last_name: str
    full_name: str
    broadcast_name: str
    image_url: str
    country_id: int
    country_code: str