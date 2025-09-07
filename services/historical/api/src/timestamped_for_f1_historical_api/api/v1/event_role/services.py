from timestamped_for_f1_historical_api.api.v1.event_role.models import EventRole
from timestamped_for_f1_historical_api.core.db import AsyncSession, select
from timestamped_for_f1_historical_api.utils import get_non_empty_entries


async def get_all_by_event_id(db_session: AsyncSession, event_id: int, **filters) -> list[EventRole]:
    """
    Returns all event roles for a given event id, in ascending order by driver id.
    """
    
    non_empty_filters = get_non_empty_entries(**filters)

    return (
        await db_session.execute(
            select(EventRole)
            .filter(EventRole.event_id == event_id)
            .filter_by(**non_empty_filters)
            .order_by(EventRole.driver_id)
        )
    ).scalars().all()