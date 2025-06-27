from datetime import datetime, timedelta

from fastapi import APIRouter, Depends

import models
from db import AsyncSession, gen_db_session


router = APIRouter(prefix='/api/v1')


@router.get('/circuits')
async def get_circuits(
    id: int | None = None,
    year: int | None = None,
    circuit_name: str | None = None,
    country_code: str | None = None,
    country_name: str | None = None,
    location: str | None = None,
    rotation: int | None = None,
    db_session: AsyncSession = Depends(gen_db_session)
):
    return None


@router.get('/circuits/{id}')
async def get_circuit(
    id: int,
    db_session: AsyncSession = Depends(gen_db_session)
):
    return None


@router.get('/meetings')
async def get_meetings(
    id: int | None = None,
    year: int | None = None,
    meeting_name: str | None = None,
    meeting_official_name: str | None = None,
    start_date: datetime | None = None,
    utc_offset: timedelta | None = None,
    db_session: AsyncSession = Depends(gen_db_session)
):
    return None


@router.get('/meetings/{id}')
async def get_meeting(
    id: int,
    db_session: AsyncSession = Depends(gen_db_session)
):
    return None


@router.get('/sessions')
async def get_sessions(
    id: int | None = None,
    year: int | None = None,
    meeting_name: str | None = None,
    session_name: str | None = None,
    session_type: str | None = None,
    start_date: datetime | None = None,
    end_date: datetime | None = None,
    utc_offset: timedelta | None = None,
    db_session: AsyncSession = Depends(gen_db_session)
):
    return None


@router.get('/sessions/{id}')
async def get_session(
    id: int,
    db_session: AsyncSession = Depends(gen_db_session)
):
    return None


@router.get('/teams')
async def get_teams(
    id: int | None = None,
    year: int | None = None,
    name: str | None = None,
    color: str | None = None,
    db_session: AsyncSession = Depends(gen_db_session)
):
    return None


@router.get('/teams/{id}')
async def get_team(
    id: int,
    db_session: AsyncSession = Depends(gen_db_session)
):
    return None


@router.get('/drivers')
async def get_drivers(
    id: int | None = None,
    year: int | None = None,
    driver_number: int | None = None,
    acronym: str | None = None,
    first_name: str | None = None,
    last_name: str | None = None,
    full_name: str | None = None,
    broadcast_name: str | None = None,
    image_url: str | None = None,
    country_code: str | None = None,
    db_session: AsyncSession = Depends(gen_db_session)
):
    return None


@router.get('/drivers/{id}')
async def get_driver(
    id: int,
    db_session: AsyncSession = Depends(gen_db_session)
):
    return None


@router.get('/events')
async def get_events(
    id: int | None = None,
    date: datetime | None = None,
    elapsed_time: timedelta | None = None,
    lap_number: int | None = None,
    category: str | None = None,
    cause: str | None = None,
    db_session: AsyncSession = Depends(gen_db_session)
):
    return None


@router.get('/event{id}')
async def get_event(
    id: int,
    db_session: AsyncSession = Depends(gen_db_session)
):
    return None