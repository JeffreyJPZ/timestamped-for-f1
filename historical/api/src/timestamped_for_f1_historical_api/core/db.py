import os
from pathlib import Path

from collections.abc import AsyncIterator
from fastapi import Depends
from pydantic import BaseModel, DirectoryPath, AnyUrl
from pydantic_settings import BaseSettings
from sqlalchemy import MetaData, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy_helpers.aio import Base
from sqlalchemy_helpers.fastapi import AsyncDatabaseManager, make_db_session, manager_from_config


class SQLAlchemyModel(BaseModel):
    url: AnyUrl = os.environ.get('SQLALCHEMY_URL', default='')


class AlembicModel(BaseModel):
    migrations_path: DirectoryPath = Path(__file__).parent.parent.joinpath('migrations').absolute()


class DatabaseConfig(BaseSettings):
    sqlalchemy: SQLAlchemyModel = SQLAlchemyModel()
    alembic: AlembicModel = AlembicModel()


def get_db_config() -> DatabaseConfig:
    return DatabaseConfig()


async def get_db_manager() -> AsyncDatabaseManager:
    db_config = get_db_config().sqlalchemy
    return manager_from_config(db_config)


async def get_db_session(
    db_manager: AsyncDatabaseManager = Depends(get_db_manager),
) -> AsyncIterator[AsyncSession]:
    async for session in make_db_session(db_manager):
        yield session

    
def get_base_metadata() -> MetaData:
    """
    Returns constraint naming conventions for SQLAlchemy models.
    """

    return MetaData(naming_convention={
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_`%(constraint_name)s`",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s"
    })