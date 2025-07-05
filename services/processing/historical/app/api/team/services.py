from app.api.team.models import Team
from app.api.driver.models import Driver
from app.api.meeting.models import Meeting
from app.api.session.models import Session
from app.db.core import AsyncSession, select
from app.utils import get_non_empty_entries


async def get(db_session: AsyncSession, id: int) -> Team | None:
    """
    Returns a team with the given id, or None if the team does not exist.
    """
    
    return (
        await db_session.execute(
            select(Team)
            .filter(Team.id == id)
        )
    ).scalars().one_or_none()


async def get_all(db_session: AsyncSession, **filters) -> list[Team]:
    """
    Returns all teams with attributes matching the given filters, in ascending order by year and name.
    """
    
    non_empty_filters = get_non_empty_entries(**filters)

    return (
        await db_session.execute(
            select(Team)
            .filter_by(**non_empty_filters)
            .order_by(Team.year, Team.name)
        )
    ).scalars().all()


async def get_all_by_driver_id(db_session: AsyncSession, driver_id: int, **filters) -> list[Team]:
    """
    Returns all teams that a driver has driven for in a year using the given driver id and additional filters, in ascending order by team name.
    """
    
    non_empty_filters = get_non_empty_entries(**filters)

    return (
        await db_session.execute(
            select(Team)
            .select_from(Team)
            .join(Driver, Team.drivers)
            .filter(Driver.id == driver_id)
            .filter_by(**non_empty_filters)
            .order_by(Team.name)
        )
    ).scalars().all()


async def get_all_by_meeting_id(db_session: AsyncSession, meeting_id: int, **filters) -> list[Team]:
    """
    Returns all teams that have participated in a meeting using the given meeting id and additional filters, in ascending order by team name.
    """
    
    non_empty_filters = get_non_empty_entries(**filters)

    return (
        await db_session.execute(
            select(Team)
            .select_from(Team)
            .join(Meeting, Team.meetings)
            .filter(Meeting.id == meeting_id)
            .filter_by(**non_empty_filters)
            .order_by(Team.name)
        )
    ).scalars().all()


async def get_all_by_meeting_id_and_session_name(db_session: AsyncSession, meeting_id: int, session_name: str, **filters) -> list[Team]:
    """
    Returns all teams that have participated in a session using the given meeting id, session name, and additional filters, in ascending order by team name.
    """
    
    non_empty_filters = get_non_empty_entries(**filters)

    return (
        await db_session.execute(
            select(Team)
            .select_from(Team)
            .join(Session, Team.sessions)
            .filter(Session.meeting_id == meeting_id)
            .filter(Session.name == session_name)
            .filter_by(**non_empty_filters)
            .order_by(Team.name)
        )
    ).scalars().all()