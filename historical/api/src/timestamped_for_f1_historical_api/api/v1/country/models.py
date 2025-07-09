from typing import Optional, TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from timestamped_for_f1_historical_api.core.db import Base
# Prevent circular imports for SQLAlchemy models since we are using type annotation
if TYPE_CHECKING:
    from timestamped_for_f1_historical_api.api.v1.circuit.models import Circuit
    from timestamped_for_f1_historical_api.api.v1.driver.models import Driver
    

class Country(Base):
    __tablename__ = "country"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    code: Mapped[str] = mapped_column(String(length=3), unique=True)
    name: Mapped[Optional[str]] = mapped_column(unique=True) # Driver data only comes with country code

    circuits: Mapped[list["Circuit"]] = relationship(
        back_populates="country", cascade="save-update, merge"
    )

    drivers: Mapped[list["Driver"]] = relationship(
        back_populates="country", cascade="save-update, merge"
    )

    def __repr__(self) -> str:  
        return f"Country(id={self.id!r}, code={self.code!r}, name={self.name!r}"