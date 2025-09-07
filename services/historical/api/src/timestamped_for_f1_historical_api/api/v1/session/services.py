from timestamped_for_f1_historical_api.api.v1.session.models import Session
from timestamped_for_f1_historical_api.api.v1.meeting.models import Meeting
from timestamped_for_f1_historical_api.core.db import AsyncSession, select
from timestamped_for_f1_historical_api.utils import get_non_empty_entries


async def get(db_session: AsyncSession, id: int) -> Session | None:
    """
    Returns a session with the given id, or None if the session does not exist.
    """
    
    return (
        await db_session.execute(
            select(Session)
            .filter(Session.id == id)
        )
    ).scalars().one_or_none()


async def get_by_meeting_id_and_name(db_session: AsyncSession, meeting_id: int, name: str) -> Session | None:
    """
    Returns a session with the given meeting id and name, or None if the session does not exist.
    """
    
    return (
        await db_session.execute(
            select(Session)
            .filter(Session.meeting_id == meeting_id)
            .filter(Session.name == name)
        )
    ).scalars().one_or_none()


async def get_all(db_session: AsyncSession, **filters) -> list[Session]:
    """
    Returns all sessions with attributes matching the given filters, in ascending order by meeting id and name.
    """
    
    non_empty_filters = get_non_empty_entries(**filters)

    return (
        await db_session.execute(
            select(Session)
            .filter_by(**non_empty_filters)
            .order_by(Session.meeting_id, Session.name)
        )
    ).scalars().all()


async def get_all_by_meeting_id(db_session: AsyncSession, meeting_id: int, **filters) -> list[Session]:
    """
    Returns all sessions belonging to a meeting with the given meeting id and optional filters, in ascending order by meeting id and session name.
    """
    
    non_empty_filters = get_non_empty_entries(**filters)

    return (
        await db_session.execute(
            select(Session)
            .select_from(Session)
            .join(Meeting, Session.meeting_id == Meeting.id)
            .filter(Session.meeting_id == meeting_id)
            .filter_by(**non_empty_filters)
            .order_by(Session.meeting_id, Session.name)
        )
    ).scalars().all()