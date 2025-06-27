from datetime import datetime, timedelta

from fastapi import APIRouter, Depends

import models
from db import AsyncSession, gen_db_session


router = APIRouter(prefix='/api/v1')


@router.get('/circuits')
async def get_circuits(
    id: int,
    year: int,
    circuit_name: str,
    country_code: str,
    country_name: str,
    location: str,
    rotation: int,
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
    id: int,
    year: int,
    meeting_name: str,
    meeting_official_name: str,
    start_date: datetime,
    utc_offset: timedelta,
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
    id: int,
    year: int,
    meeting_name: str,
    session_name: str,
    session_type: str,
    start_date: datetime,
    end_date: datetime,
    utc_offset: timedelta,
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
    id: int,
    year: int,
    name: str,
    color: str,
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
    id: int,
    year: int,
    driver_number: int,
    acronym: str,
    first_name: str,
    last_name: str,
    full_name: str,
    broadcast_name: str,
    image_url: str,
    country_code: str,
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
    id: int,
    date: datetime,
    elapsed_time: timedelta,
    lap_number: int,
    category: str,
    cause: str,
    db_session: AsyncSession = Depends(gen_db_session)
):
    return None


@router.get('/event{id}')
async def get_event(
    id: int,
    db_session: AsyncSession = Depends(gen_db_session)
):
    return None