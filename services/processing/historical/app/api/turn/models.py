from decimal import Decimal
from typing import ClassVar

from sqlalchemy import ForeignKey, PrimaryKeyConstraint, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.api.circuit.models import Circuit
from app.db.core import Base
from app.models import QueryModel, ResponseModel, MappingModel


class Turn(Base):
    __tablename__ = "turn"
    __table_args__ = (
        PrimaryKeyConstraint(
            ("circuit_id", "number"),
            name="pk_turn_circuit_id_and_number"
        )
    )

    number: Mapped[int]
    angle: Mapped[Numeric] = mapped_column(Numeric(precision=18, scale=15))
    length: Mapped[Numeric] = mapped_column(Numeric(precision=20, scale=15))
    x: Mapped[Numeric] = mapped_column(Numeric(precision=20, scale=15))
    y: Mapped[Numeric] = mapped_column(Numeric(precision=20, scale=15))

    # Many-to-one weak rel with circuit as owner
    circuit_id: Mapped[int] = mapped_column(ForeignKey(column="circuit.id"))
    circuit: Mapped[Circuit] = relationship(back_populates="turns")

    def __repr__(self) -> str:
        return f"Turn(number={self.number!r}, angle={self.angle!r}, length={self.length}, x={self.x!r}, location={self.y!r}, circuit_id={self.circuit_id!r})"
    
    
class TurnColumns(QueryModel):
    number: int | None = None
    angle: Decimal | None = None
    length: Decimal | None = None
    x: Decimal | None = None
    y: Decimal | None = None
    circuit_id: int | None = None


class TurnColumnNamesToResponseNames(MappingModel):
    number: ClassVar[str] = "number"
    angle: ClassVar[str] = "angle"
    length: ClassVar[str] = "length"
    x: ClassVar[str] = "x"
    y: ClassVar[str] = "y"
    circuit_id: ClassVar[str] = "circuit_id"


class TurnResponse(ResponseModel):
    number: int
    angle: Decimal
    length: Decimal
    x: Decimal
    y: Decimal