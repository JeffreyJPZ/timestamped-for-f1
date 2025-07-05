from typing import Annotated

from fastapi import APIRouter, Depends, Query

from app.db.core import AsyncSession, get_db_session, select
from app.utils import get_non_empty_entries
from .models import Session, SessionGet


router = APIRouter()


@router.get("/")
async def get_sessions(
    params: Annotated[SessionFilterParams, Query()],
    db_session: AsyncSession = Depends(get_db_session)
):
    non_empty_params = get_non_empty_keys(**params.model_dump())
    result = await db_session.scalars(select(Meeting).join(Meeting.sessions).filter_by(**non_empty_params)).all()
    return None


@router.get("/{id}")
async def get_session(
    id: int,
    db_session: AsyncSession = Depends(get_db_session)
):
    result = await db_session.get(entity=Session, ident=id)
    return None


@router.get("/{}/teams")
async def get_teams_by_session(
    params: Annotated[SessionGet, Query()],
    db_session: AsyncSession = Depends(get_db_session)
):
    non_empty_params = get_non_empty_entries(**params.model_dump())
    result = await db_session.scalars(select(Meeting).filter_by(**non_empty_params)).all()
    return None


@router.get("/{meeting_id}/drivers")
async def get_drivers_by_meeting(
    params: Annotated[MeetingFilterParams, Query()],
    db_session: AsyncSession = Depends(get_db_session)
):
    non_empty_params = get_non_empty_entries(**params.model_dump())
    result = await db_session.scalars(select(Meeting).filter_by(**non_empty_params)).all()
    return None


@router.get("/{meeting_id}/events")
async def get_events_by_meeting(
    params: Annotated[MeetingFilterParams, Query()],
    db_session: AsyncSession = Depends(get_db_session)
):
    non_empty_params = get_non_empty_entries(**params.model_dump())
    result = await db_session.scalars(select(Meeting).filter_by(**non_empty_params)).all()
    return None