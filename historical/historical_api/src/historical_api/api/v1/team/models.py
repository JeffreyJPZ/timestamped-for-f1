from sqlalchemy import Table, Column, ForeignKey, PrimaryKeyConstraint, UniqueConstraint, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from historical_api.api.v1.meeting.models import Meeting, meeting_team_assoc
from historical_api.api.v1.session.models import Session, session_team_assoc
from historical_api.api.v1.driver.models import Driver
from historical_api.core.db import Base
from historical_api.core.models import QueryModel, ResourceModel, ResponseModel


team_driver_assoc = Table(
    Column("team_id", ForeignKey("team.id")),
    Column("driver_id", ForeignKey("driver.id")),
    PrimaryKeyConstraint(
        ("team_id", "driver_id"),
        name="pk_team_driver_team_id_and_driver_id"
    ),
    name="team_driver",
    metadata=Base.metadata
)


class Team(Base):
    __tablename__ = "team"
    __table_args__ = (
        UniqueConstraint(
            ("year", "name"),
            name="uq_team_year_and_name"
        )
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    year: Mapped[int]
    name: Mapped[str]
    color: Mapped[str] = mapped_column(String(length=6))

    meetings: Mapped[list[Meeting]] = relationship(
        secondary=meeting_team_assoc, back_populates="teams", cascade="all, delete-orphan"
    )

    sessions: Mapped[list[Session]] = relationship(
        secondary=session_team_assoc, back_populates="teams", cascade="all, delete-orphan"
    )

    drivers: Mapped[list[Driver]] = relationship(
        secondary=team_driver_assoc, back_populates="teams", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"Team(id={self.id!r}, year={self.year!r}, name={self.name!r}, color={self.color!r}"
    

class TeamResource(ResourceModel):
    """
    Base Pydantic model for team actions.
    """

    team_id: int | None = None
    year: int | None = None
    team_name: str | None = None
    team_color: str | None = None


class TeamGet(TeamResource):
    """
    Pydantic model for retrieving teams.
    """

    pass


class TeamResponse(ResponseModel):
    # NOTE: The length of driver_ids depends on the endpoint used - for example, the /sessions/:id/teams endpoint returns several driver ids at most (for the given session),
    # but the /teams endpoint can return several or more driver ids.
    driver_ids: list[int] 
    team_id: int
    year: int
    team_name: str
    team_color: str