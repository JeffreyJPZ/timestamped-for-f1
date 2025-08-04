from timestamped_for_f1_historical_api.api.v1.location.models import Location
from timestamped_for_f1_historical_api.api.v1.event.models import Event
from timestamped_for_f1_historical_api.core.db import AsyncSession, select


async def get(db_session: AsyncSession, event_id: int) -> Location | None:
    """
    Returns a location with the given event id, or None if the location does not exist.
    """
    
    return (
        await db_session.execute(
            select(Location)
            .select_from(Location)
            .join(Event, Location.event_id == Event.id)
            .filter(Location.event_id == event_id)
        )
    ).scalars().one_or_none()