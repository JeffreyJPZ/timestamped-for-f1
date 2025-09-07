from timestamped_for_f1_historical_api.api.v1.pit.models import Pit
from timestamped_for_f1_historical_api.api.v1.event.models import Event
from timestamped_for_f1_historical_api.core.db import AsyncSession, select


async def get(db_session: AsyncSession, event_id: int) -> Pit | None:
    """
    Returns a pit with the given event id, or None if the pit does not exist.
    """
    
    return (
        await db_session.execute(
            select(Pit)
            .select_from(Pit)
            .join(Event, Pit.event_id == Event.id)
            .filter(Pit.event_id == event_id)
        )
    ).scalars().one_or_none()