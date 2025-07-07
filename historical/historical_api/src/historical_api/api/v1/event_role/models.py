from typing import Literal

from sqlalchemy import ForeignKey, PrimaryKeyConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from historical_api.api.v1.event.models import Event
from historical_api.api.v1.driver.models import Driver
from historical_api.core.db import Base
from historical_api.core.models import ResponseModel


class EventRole(Base):
    __tablename__ = "event_role"
    __table_args__ = (
        PrimaryKeyConstraint(
            ("event_id", "driver_id"),
            name="pk_event_role_event_id_and_driver_id"
        )
    )

    event_id: Mapped[int] = mapped_column(ForeignKey(column="event.id"))
    driver_id: Mapped[int] = mapped_column(ForeignKey(column="driver.id"))
    role: Mapped[str] # One of: "initiator" or "participant"

    event: Mapped[Event] = relationship(back_populates="drivers", cascade="all, delete-orphan")
    driver: Mapped[Driver] = relationship(back_populates="events", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"EventRole(event_id={self.event_id!r}, driver_id={self.driver_id!r}, role={self.role!r})"


class EventRoleResponse(ResponseModel):
    driver_id: int
    role: Literal["initiator"] | Literal["participant"]