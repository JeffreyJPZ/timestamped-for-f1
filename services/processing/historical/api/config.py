import os
from pathlib import Path
from pydantic import BaseModel, DirectoryPath, AnyUrl
from pydantic_settings import BaseSettings


class SQLAlchemyModel(BaseModel):
    url: AnyUrl = os.environ.get('SQLALCHEMY_URL', default='')


class AlembicModel(BaseModel):
    migrations_path: DirectoryPath = Path(__file__).parent.joinpath('migrations').absolute()


class Settings(BaseSettings):
    sqlalchemy: SQLAlchemyModel = SQLAlchemyModel()
    alembic: AlembicModel = AlembicModel()


def get_settings() -> Settings:
    return Settings()