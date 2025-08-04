from typing import TYPE_CHECKING
from decimal import Decimal

from sqlalchemy import ForeignKey, UniqueConstraint, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship

from timestamped_for_f1_historical_api.core.db import Base
from timestamped_for_f1_historical_api.core.models import ResponseModel
# Prevent circular imports for SQLAlchemy models since we are using type annotation
if TYPE_CHECKING:
    from timestamped_for_f1_historical_api.api.v1.circuit.models import Circuit


class Turn(Base):
    __tablename__ = "turn"
    __table_args__ = (
        UniqueConstraint("circuit_id", "number"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    number: Mapped[int]
    angle: Mapped[Decimal] = mapped_column(Numeric(precision=18, scale=15))
    length: Mapped[Decimal] = mapped_column(Numeric(precision=20, scale=15))
    x: Mapped[Decimal] = mapped_column(Numeric(precision=20, scale=15))
    y: Mapped[Decimal] = mapped_column(Numeric(precision=20, scale=15))

    # Many-to-one weak rel with circuit as owner
    circuit_id: Mapped[int] = mapped_column(ForeignKey("circuit.id"))
    circuit: Mapped["Circuit"] = relationship(back_populates="turns")

    def __repr__(self) -> str:
        return f"Turn(id={self.id!r}, number={self.number!r}, angle={self.angle!r}, length={self.length}, x={self.x!r}, location={self.y!r}, circuit_id={self.circuit_id!r})"


class TurnResponse(ResponseModel):
    number: int
    angle: Decimal
    length: Decimal
    x: Decimal
    y: Decimal