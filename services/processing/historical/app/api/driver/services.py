from app.api.driver.models import Driver
from app.api.team.models import Team
from app.api.meeting.models import Meeting
from app.api.session.models import Session
from app.db.core import AsyncSession, select
from app.utils import get_non_empty_entries


async def get(db_session: AsyncSession, id: int) -> Driver | None:
    """
    Returns a driver with the given id, or None if the driver does not exist.
    """
    
    return (
        await db_session.execute(
            select(Driver)
            .filter(Driver.id == id)
        )
    ).scalars().one_or_none()


async def get_all(db_session: AsyncSession, **filters) -> list[Driver]:
    """
    Returns all drivers with attributes matching the given filters, in ascending order by year and last name.
    """
    
    non_empty_filters = get_non_empty_entries(**filters)

    return (
        await db_session.execute(
            select(Driver)
            .filter_by(**non_empty_filters)
            .order_by(Driver.year, Driver.last_name)
        )
    ).scalars().all()


async def get_all_by_team_id(db_session: AsyncSession, team_id: int, **filters) -> list[Team]:
    """
    Returns all drivers that a team has had in a given year using the given team id and additional filters, in ascending order by driver last name.
    """
    
    non_empty_filters = get_non_empty_entries(**filters)

    return (
        await db_session.execute(
            select(Driver)
            .select_from(Driver)
            .join(Team, Driver.teams)
            .filter(Team.id == team_id)
            .filter_by(**non_empty_filters)
            .order_by(Driver.last_name)
        )
    ).scalars().all()


async def get_all_by_meeting_id(db_session: AsyncSession, meeting_id: int, **filters) -> list[Driver]:
    """
    Returns all drivers that have participated in a given meeting using the given meeting id and additional filters, in ascending order by driver last name.
    """
    
    non_empty_filters = get_non_empty_entries(**filters)

    return (
        await db_session.execute(
            select(Driver)
            .select_from(Driver)
            .join(Meeting, Driver.meetings)
            .filter(Meeting.id == meeting_id)
            .filter_by(**non_empty_filters)
            .order_by(Driver.last_name)
        )
    ).scalars().all()


async def get_all_by_meeting_id_and_session_name(db_session: AsyncSession, meeting_id: int, session_name: str, **filters) -> list[Driver]:
    """
    Returns all drivers that have participated in a given session using the given meeting id, session name, and additional filters, in ascending order by driver last name.
    """
    
    non_empty_filters = get_non_empty_entries(**filters)

    return (
        await db_session.execute(
            select(Driver)
            .select_from(Driver)
            .join(Session, Driver.sessions)
            .filter(Session.meeting_id == meeting_id)
            .filter(Session.name == session_name)
            .filter_by(**non_empty_filters)
            .order_by(Driver.last_name)
        )
    ).scalars().all()