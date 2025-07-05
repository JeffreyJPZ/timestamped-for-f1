from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.api.circuit.models import Circuit
from app.api.driver.models import Driver
from app.db.core import Base


class Country(Base):
    __tablename__ = "country"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    code: Mapped[str] = mapped_column(String(3), unique=True)
    name: Mapped[str | None] = mapped_column(unique=True) # Driver data only comes with country code

    circuits: Mapped[list[Circuit]] = relationship(
        back_populates="country", cascade="all, delete-orphan"
    )

    drivers: Mapped[list[Driver]] = relationship(
        back_populates="country", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"Country(id={self.id!r}, code={self.code!r}, name={self.name!r}"