from sqlalchemy import Table, Column, ForeignKey, PrimaryKeyConstraint, UniqueConstraint, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.api.meeting.models import Meeting, meeting_team_assoc
from app.api.session.models import Session, session_team_assoc
from app.api.driver.models import Driver
from app.db.core import Base
from app.models import QueryModel, RequestModel, ResponseModel


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
    

class TeamFilterParams(RequestModel):
    team_id: int | None = None
    year: int | None = None
    team_name: str | None = None
    team_color: str | None = None


class TeamColumns(QueryModel):
    id: int | None = None
    year: int | None = None
    name: str | None = None
    color: str | None = None


class TeamResponse(ResponseModel):
    team_id: int
    year: int
    team_name: str
    team_color: str