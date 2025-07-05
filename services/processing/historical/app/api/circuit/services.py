from app.api.circuit.models import Circuit
from app.api.meeting.models import Meeting
from app.db.core import AsyncSession, select
from app.utils import get_non_empty_entries


async def get(db_session: AsyncSession, id: int) -> Circuit | None:
    """
    Returns a circuit with the given id, or None if the circuit does not exist.
    """
    
    return (
        await db_session.execute(
            select(Circuit)
            .filter(Circuit.id == id)
        )
    ).scalars().one_or_none()


async def get_by_meeting_id(db_session: AsyncSession, meeting_id: int) -> Circuit | None:
    """
    Returns a circuit where the meeting with the given meeting id takes place, or None if the circuit does not exist.
    """
    
    return (
        await db_session.execute(
            select(Circuit)
            .select_from(Meeting)
            .join(Circuit, Meeting.circuit_id == Circuit.id)
            .filter(Meeting.id == meeting_id)
        )
    ).scalars().one_or_none()


async def get_all(db_session: AsyncSession, **filters) -> list[Circuit]:
    """
    Returns all circuits with attributes matching the given filters, in ascending order by year and name.
    """
    
    non_empty_filters = get_non_empty_entries(**filters)

    return (
        await db_session.execute(
            select(Circuit)
            .filter_by(**non_empty_filters)
            .order_by(Circuit.year, Circuit.name)
        )
    ).scalars().all()