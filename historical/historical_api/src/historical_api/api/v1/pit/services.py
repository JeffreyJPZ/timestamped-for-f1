from datetime import datetime

from historical_api.api.v1.pit.models import Pit
from historical_api.api.v1.event.models import Event
from historical_api.core.db import AsyncSession, select


async def get(db_session: AsyncSession, event_id: int) -> Pit | None:
    """
    Returns a pit with the given event id and date, or None if the pit does not exist.
    """
    
    return (
        await db_session.execute(
            select(Pit)
            .select_from(Pit)
            .join(Event, Pit.event_id == Event.id)
            .filter(Pit.event_id == event_id)
        )
    ).scalars().one_or_none()