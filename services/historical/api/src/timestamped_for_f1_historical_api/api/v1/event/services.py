from timestamped_for_f1_historical_api.api.v1.event.models import Event
from timestamped_for_f1_historical_api.api.v1.meeting.models import Meeting
from timestamped_for_f1_historical_api.api.v1.session.models import Session
from timestamped_for_f1_historical_api.core.db import AsyncSession, select
from timestamped_for_f1_historical_api.utils import get_non_empty_entries


async def get(db_session: AsyncSession, id: int) -> Event | None:
    """
    Returns an event with the given id, or None if the event does not exist.
    """
    
    return (
        await db_session.execute(
            select(Event)
            .filter(Event.id == id)
        )
    ).scalars().one_or_none()


async def get_all(db_session: AsyncSession, **filters) -> list[Event]:
    """
    Returns all events with attributes matching the given filters, in ascending order by date.
    """
    
    non_empty_filters = get_non_empty_entries(**filters)

    return (
        await db_session.execute(
            select(Event)
            .filter_by(**non_empty_filters)
            .order_by(Event.date)
        )
    ).scalars().all()


async def get_all_by_meeting_id(db_session: AsyncSession, meeting_id: int, **filters) -> list[Event]:
    """
    Returns all events for a meeting using the given meeting id and additional filters, in ascending order by date.
    """
    
    non_empty_filters = get_non_empty_entries(**filters)

    return (
        await db_session.execute(
            select(Event)
            .select_from(Meeting)
            .join(Session, Meeting.sessions)
            .join(Event, Session.id == Event.session_id)
            .filter(Meeting.id == meeting_id)
            .filter_by(**non_empty_filters)
            .order_by(Event.date)
        )
    ).scalars().all()


async def get_all_by_session_id(db_session: AsyncSession, session_id: int, **filters) -> list[Event]:
    """
    Returns all events for a session using the given session id and additional filters, in ascending order by date.
    """
    
    non_empty_filters = get_non_empty_entries(**filters)

    return (
        await db_session.execute(
            select(Event)
            .select_from(Meeting)
            .join(Session, Meeting.sessions)
            .join(Event, Session.id == Event.session_id)
            .filter(Session.id == session_id)
            .filter_by(**non_empty_filters)
            .order_by(Event.date)
        )
    ).scalars().all()


async def get_all_by_meeting_id_and_session_name(db_session: AsyncSession, meeting_id: int, session_name: str, **filters) -> list[Event]:
    """
    Returns all events for a session using the given meeting id, session name, and additional filters, in ascending order by date.
    """
    
    non_empty_filters = get_non_empty_entries(**filters)

    return (
        await db_session.execute(
            select(Event)
            .select_from(Meeting)
            .join(Session, Meeting.sessions)
            .join(Event, Session.id == Event.session_id)
            .filter(Session.meeting_id == meeting_id)
            .filter(Session.name == session_name)
            .filter_by(**non_empty_filters)
            .order_by(Event.date)
        )
    ).scalars().all()