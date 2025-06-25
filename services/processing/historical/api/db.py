from collections.abc import AsyncIterator
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy_helpers.fastapi import AsyncDatabaseManager, make_db_session, manager_from_config
from sqlalchemy_helpers.aio import Base
from config import get_settings


async def gen_db_manager() -> AsyncDatabaseManager:
    db_settings = get_settings().sqlalchemy
    return manager_from_config(db_settings)


async def gen_db_session(
    db_manager: AsyncDatabaseManager = Depends(gen_db_manager),
) -> AsyncIterator[AsyncSession]:
    async for session in make_db_session(db_manager):
        yield session