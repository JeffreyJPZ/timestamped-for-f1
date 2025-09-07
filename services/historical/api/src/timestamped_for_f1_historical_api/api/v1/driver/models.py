from typing import Optional, TYPE_CHECKING

from sqlalchemy import ForeignKey, UniqueConstraint, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from timestamped_for_f1_historical_api.core.db import Base
from timestamped_for_f1_historical_api.core.models import ResourceModel, ResponseModel
from timestamped_for_f1_historical_api.api.v1.meeting.models import meeting_driver_assoc
from timestamped_for_f1_historical_api.api.v1.session.models import session_driver_assoc
from timestamped_for_f1_historical_api.api.v1.team.models import team_driver_assoc
# Prevent circular imports for SQLAlchemy models since we are using type annotation
if TYPE_CHECKING:
    from timestamped_for_f1_historical_api.api.v1.country.models import Country
    from timestamped_for_f1_historical_api.api.v1.meeting.models import Meeting
    from timestamped_for_f1_historical_api.api.v1.session.models import Session, session_driver_assoc
    from timestamped_for_f1_historical_api.api.v1.team.models import Team, team_driver_assoc
    from timestamped_for_f1_historical_api.api.v1.event.models import Event


class Driver(Base):
    __tablename__ = "driver"
    __table_args__ = (
        UniqueConstraint("year", "number"),
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
    country_id: Mapped[Optional[int]] = mapped_column(ForeignKey("country.id"))
    country: Mapped[Optional["Country"]] = relationship(back_populates="drivers")

    meetings: Mapped[list["Meeting"]] = relationship(
        secondary=meeting_driver_assoc, back_populates="drivers", cascade="save-update, merge"
    )

    sessions: Mapped[list["Session"]] = relationship(
        secondary=session_driver_assoc, back_populates="drivers", cascade="save-update, merge"
    )

    teams: Mapped[list["Team"]] = relationship(
        secondary=team_driver_assoc, back_populates="drivers", cascade="save-update, merge"
    )

    # Many-to-many rel with events
    events: Mapped[list["Event"]] = relationship(
        back_populates="driver", cascade="save-update, merge"
    )

    def __repr__(self) -> str:
        return f"Driver(id={self.id!r}, year={self.year!r}, number={self.number!r}, acronym={self.acronym!r}, first_name={self.first_name!r}, last_name={self.last_name!r}, full_name={self.full_name!r}, broadcast_name={self.broadcast_name!r}, image_url={self.image_url!r}, country_id={self.country_id!r}"
    

class DriverResource(ResourceModel):
    """
    Base Pydantic model for driver actions
    """

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


class DriverGet(DriverResource):
    """
    Pydantic model for retrieving drivers.
    """

    pass


class DriverResponse(ResponseModel):
    # NOTE: The length of team_ids depends on the endpoint used - for example, the /sessions/:id/drivers endpoint returns at most one team id (for the given session),
    # but the /drivers endpoint can return multiple team ids.
    team_ids: list[int] 
    driver_id: int
    year: int
    driver_number: int
    driver_acronym: str
    first_name: str
    last_name: str
    full_name: str
    broadcast_name: str
    image_url: str
    country_id: int
    country_code: str