from typing import Literal, TYPE_CHECKING

from sqlalchemy import ForeignKey, PrimaryKeyConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from timestamped_for_f1_historical_api.core.db import Base
from timestamped_for_f1_historical_api.core.models import ResponseModel
# Prevent circular imports for SQLAlchemy models since we are using type annotation
if TYPE_CHECKING:
    from timestamped_for_f1_historical_api.api.v1.event.models import Event
    from timestamped_for_f1_historical_api.api.v1.driver.models import Driver

from .enums import EventRoleEnum


class EventRole(Base):
    __tablename__ = "event_role"
    __table_args__ = (
        PrimaryKeyConstraint("event_id", "driver_id"),
    )

    event_id: Mapped[int] = mapped_column(ForeignKey("event.id"))
    driver_id: Mapped[int] = mapped_column(ForeignKey("driver.id"))
    role: Mapped[str] # One of: "initiator" or "participant"

    event: Mapped["Event"] = relationship(back_populates="drivers")
    driver: Mapped["Driver"] = relationship(back_populates="events")

    def __repr__(self) -> str:
        return f"EventRole(event_id={self.event_id!r}, driver_id={self.driver_id!r}, role={self.role!r})"


class EventRoleResponse(ResponseModel):
    driver_id: int
    role: EventRoleEnum