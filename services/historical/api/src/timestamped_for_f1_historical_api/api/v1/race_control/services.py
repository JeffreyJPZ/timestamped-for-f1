from timestamped_for_f1_historical_api.api.v1.race_control.models import RaceControl
from timestamped_for_f1_historical_api.api.v1.event.models import Event
from timestamped_for_f1_historical_api.core.db import AsyncSession, select


async def get(db_session: AsyncSession, event_id: int) -> RaceControl | None:
    """
    Returns a race control message with the given event id, or None if the message does not exist.
    """
    
    return (
        await db_session.execute(
            select(RaceControl)
            .select_from(RaceControl)
            .join(Event, RaceControl.event_id == Event.id)
            .filter(RaceControl.event_id == event_id)
        )
    ).scalars().one_or_none()