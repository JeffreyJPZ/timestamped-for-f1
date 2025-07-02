from typing import Annotated

from fastapi import APIRouter, Depends, Query

from app.db.core import AsyncSession, get_db_session, select
from app.utils import get_non_empty_keys
from .models import (
    Team,
    TeamFilterParams
)


router = APIRouter()


@router.get("/")
async def get_teams(
    params: Annotated[TeamFilterParams, Query()],
    db_session: AsyncSession = Depends(get_db_session)
):
    non_empty_params = get_non_empty_keys(**params.model_dump())
    result = await db_session.scalars(select(Team).filter_by(**non_empty_params)).all()
    return None


@router.get("/{id}")
async def get_team(
    id: int,
    db_session: AsyncSession = Depends(get_db_session)
):
    result = await db_session.get(entity=Team, ident=id)
    return None