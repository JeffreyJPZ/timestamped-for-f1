from typing import Annotated

from fastapi import APIRouter, Depends, Query

from app.db.core import AsyncSession, get_db_session, select
from app.utils import get_non_empty_keys
from .models import (
    Event,
    EventFilterParams
)

router = APIRouter()


@router.get("/")
async def get_events(
    params: Annotated[EventFilterParams, Query()],
    db_session: AsyncSession = Depends(get_db_session)
):
    non_empty_params = get_non_empty_keys(**params.model_dump())
    result = await db_session.scalars(select(Event).join(Event.location).filter_by(**non_empty_params)).all()
    return None


@router.get("/{id}")
async def get_event(
    id: int,
    db_session: AsyncSession = Depends(get_db_session)
):
    result = await db_session.get(entity=Event, ident=id)
    return None