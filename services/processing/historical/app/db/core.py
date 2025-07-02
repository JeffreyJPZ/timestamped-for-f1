import os
from pathlib import Path

from collections.abc import AsyncIterator
from fastapi import Depends
from pydantic import BaseModel, DirectoryPath, AnyUrl
from pydantic_settings import BaseSettings
from sqlalchemy import Subquery, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy_helpers.aio import Base
from sqlalchemy_helpers.fastapi import AsyncDatabaseManager, make_db_session, manager_from_config


class SQLAlchemyModel(BaseModel):
    url: AnyUrl = os.environ.get('SQLALCHEMY_URL', default='')


class AlembicModel(BaseModel):
    migrations_path: DirectoryPath = Path(__file__).parent.joinpath('migrations').absolute()


class DatabaseSettings(BaseSettings):
    sqlalchemy: SQLAlchemyModel = SQLAlchemyModel()
    alembic: AlembicModel = AlembicModel()


def get_db_settings() -> DatabaseSettings:
    return DatabaseSettings()


async def get_db_manager() -> AsyncDatabaseManager:
    db_settings = get_db_settings().sqlalchemy
    return manager_from_config(db_settings)


async def get_db_session(
    db_manager: AsyncDatabaseManager = Depends(get_db_manager),
) -> AsyncIterator[AsyncSession]:
    async for session in make_db_session(db_manager):
        yield session