from typing import TYPE_CHECKING

from timestamped_for_f1_historical_api.api.v1.country.models import Country
from timestamped_for_f1_historical_api.core.db import AsyncSession, select


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