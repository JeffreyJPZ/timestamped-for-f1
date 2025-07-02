from typing import ClassVar

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.api.country.models import Country
from app.api.meeting.models import Meeting
from app.api.turn.models import Turn, TurnResponse
from app.db.core import Base
from app.models import RequestModel, QueryModel, MappingModel, ResponseModel


class Circuit(Base):
    __tablename__ = "circuit"
    __table_args__ = (
        UniqueConstraint(
            ("year", "name"),
            name="uq_circuit_year_and_name"
        )
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    year: Mapped[int]
    name: Mapped[str]
    location: Mapped[str]
    rotation: Mapped[int]

    # Many-to-one rel with country as parent
    country_id: Mapped[int] = mapped_column(ForeignKey(column="country.id"))
    country: Mapped[Country] = relationship(back_populates="circuits")
    
    meetings: Mapped[list[Meeting]] = relationship(
        back_populates="circuit", cascade="all, delete-orphan"
    )

    turns: Mapped[list[Turn]] = relationship(
        back_populates="circuit", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"Circuit(id={self.id!r}, year={self.year!r}, name={self.name!r}, country_id={self.country_id!r}, location={self.location!r}, rotation={self.rotation!r})"
    

class CircuitFilterParams(RequestModel):
    circuit_id: int | None = None
    year: int | None = None
    circuit_name: str | None = None
    circuit_location: str | None = None
    circuit_rotation: int | None = None
    country_id: str | None = None
    country_code: str | None = None
    country_name: str | None = None


class CircuitColumns(QueryModel):
    id: int | None = None
    year: int | None = None
    name: str | None = None
    location: str | None = None
    rotation: int | None = None
    country_id: int | None = None


class CircuitColumnNamesToResponseNames(MappingModel):
    id: ClassVar[str] = "circuit_id"
    year: ClassVar[str] = "year"
    name: ClassVar[str] = "circuit_name"
    location: ClassVar[str] = "circuit_location"
    rotation: ClassVar[str] = "circuit_rotation"
    country_id: ClassVar[str] = "country_id"


class CircuitResponse(ResponseModel):
    circuit_id: int
    year: int
    circuit_name: str
    circuit_location: str
    circuit_rotation: int
    turns: list[TurnResponse]
    country_id: int
    country_code: str
    country_name: str