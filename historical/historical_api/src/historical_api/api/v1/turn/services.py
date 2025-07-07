from historical_api.api.v1.turn.models import Turn
from historical_api.core.db import AsyncSession, select


async def get_all_by_circuit_id(db_session: AsyncSession, circuit_id: int) -> list[Turn]:
    """
    Returns turns belonging to a given circuit, in ascending order by turn number.
    """

    return (
        await db_session.execute(
            select(Turn)
            .filter(Turn.circuit_id == circuit_id)
            .order_by(Turn.number)
        )
    ).scalars().all()