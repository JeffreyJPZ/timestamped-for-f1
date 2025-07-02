from typing import Annotated

from fastapi import APIRouter, Depends, Query

from app.db.core import AsyncSession, get_db_session, select
from app.utils import get_non_empty_keys
from .models import (
    Meeting,
    MeetingFilterParams
)


router = APIRouter()


@router.get("/")
async def get_meetings(
    params: Annotated[MeetingFilterParams, Query()],
    db_session: AsyncSession = Depends(get_db_session)
):
    non_empty_params = get_non_empty_keys(**params.model_dump())
    result = await db_session.scalars(select(Meeting).filter_by(**non_empty_params)).all()
    return None


@router.get("/{id}")
async def get_meeting(
    id: int,
    db_session: AsyncSession = Depends(get_db_session)
):
    return None