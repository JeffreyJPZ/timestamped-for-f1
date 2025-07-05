from app.api.v1.country.models import Country
from app.db.core import AsyncSession, select


async def get(db_session: AsyncSession, id: int) -> Country | None:
    """
    Returns a country with the given id, or None if the country does not exist.
    """

    return (
        await db_session.execute(
            select(Country)
            .filter(Country.id == id)
        )
    ).scalars().one_or_none()