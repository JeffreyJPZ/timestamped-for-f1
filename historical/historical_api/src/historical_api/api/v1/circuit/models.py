from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from historical_api.api.v1.country.models import Country
from historical_api.api.v1.meeting.models import Meeting
from historical_api.api.v1.turn.models import Turn, TurnResponse
from historical_api.core.db import Base
from historical_api.core.models import ResourceModel, ResponseModel


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
    

class CircuitResource(ResourceModel):
    """
    Base Pydantic model for circuit actions.
    """

    circuit_id: int | None = None
    year: int | None = None
    circuit_name: str | None = None
    circuit_location: str | None = None
    circuit_rotation: int | None = None
    country_id: str | None = None
    country_code: str | None = None
    country_name: str | None = None


class CircuitGet(CircuitResource):
    """
    Pydantic model for retrieving circuits.
    """

    pass


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