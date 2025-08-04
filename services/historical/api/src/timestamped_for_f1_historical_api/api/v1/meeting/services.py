from timestamped_for_f1_historical_api.api.v1.meeting.models import Meeting
from timestamped_for_f1_historical_api.core.db import AsyncSession, select
from timestamped_for_f1_historical_api.utils import get_non_empty_entries


async def get(db_session: AsyncSession, id: int) -> Meeting | None:
    """
    Returns a meeting with the given id, or None if the meeting does not exist.
    """
    
    return (
        await db_session.execute(
            select(Meeting)
            .filter(Meeting.id == id)
        )
    ).scalars().one_or_none()


async def get_all(db_session: AsyncSession, **filters) -> list[Meeting]:
    """
    Returns all meetings with attributes matching the given filters, in ascending order by year and name.
    """
    
    non_empty_filters = get_non_empty_entries(**filters)

    return (
        await db_session.execute(
            select(Meeting)
            .filter_by(**non_empty_filters)
            .order_by(Meeting.year, Meeting.name)
        )
    ).scalars().all()