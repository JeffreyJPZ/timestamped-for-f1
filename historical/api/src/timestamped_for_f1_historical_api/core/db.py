import os
from pathlib import Path

from collections.abc import AsyncIterator
from fastapi import Depends
from pydantic import BaseModel, DirectoryPath
from pydantic_settings import BaseSettings
from sqlalchemy import MetaData, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy_helpers.aio import Base
from sqlalchemy_helpers.fastapi import AsyncDatabaseManager, make_db_session, manager_from_config


class SQLAlchemyModel(BaseModel):
    url: str = os.environ.get('SQLALCHEMY_URL', default='')


class AlembicModel(BaseModel):
    migrations_path: DirectoryPath = Path(__file__).parent.parent.joinpath('migrations').absolute()


class DatabaseConfig(BaseSettings):
    sqlalchemy: SQLAlchemyModel = SQLAlchemyModel()
    alembic: AlembicModel = AlembicModel()


def get_db_config() -> DatabaseConfig:
    return DatabaseConfig()


async def get_db_manager() -> AsyncDatabaseManager:
    db_config = get_db_config()
    return manager_from_config(db_config)


async def get_db_session(
    db_manager: AsyncDatabaseManager = Depends(get_db_manager),
) -> AsyncIterator[AsyncSession]:
    async for session in make_db_session(db_manager):
        yield session