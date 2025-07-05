from datetime import datetime, timedelta
from typing import Annotated, Any

import asyncio
from fastapi import APIRouter, Depends, Query

import models
import db_models
from app.db.core import AsyncSession, Subquery, get_db_session, select
from app.utils import get_non_empty_entries


router = APIRouter(prefix="/api/v1")

async def create_circuit_response(circuit_result_obj: dict[str, Any], circuit_query: Subquery, turn_query: Subquery, db_session: AsyncSession) -> models.CircuitResponse:

    turn_results = await db_session.execute(
        select(
            turn_query.c[models.TurnColumnNamesToResponseNames.number],
            turn_query.c[models.TurnColumnNamesToResponseNames.angle],
            turn_query.c[models.TurnColumnNamesToResponseNames.length],
            turn_query.c[models.TurnColumnNamesToResponseNames.x],
            turn_query.c[models.TurnColumnNamesToResponseNames.y]
        )
        .select_from(turn_query)
        .join(
            circuit_query,
            turn_query.c[models.TurnColumnNamesToResponseNames.circuit_id] == circuit_result_obj[models.CircuitColumnNamesToResponseNames.id]
        )
    )

    turns = []

    for turn_result in turn_results:
        turn_result_obj = turn_result._asdict()
        turn_response = models.TurnResponse(**turn_result_obj)
        turns.append(turn_response)

    return models.CircuitResponse(
        turns=turns,
        **circuit_result_obj
    )


@router.get(
    "/circuits",
    response_model=list[models.CircuitResponse]
)
async def get_circuits(
    params: Annotated[models.CircuitFilterParams, Query()],
    db_session: AsyncSession = Depends(get_db_session)
):
    circuit_filters = models.CircuitColumns(
        id=params.circuit_id,
        year=params.year,
        name=params.circuit_name,
        location=params.circuit_location,
        rotation=params.circuit_rotation
    ).model_dump()
    non_empty_circuit_filters = get_non_empty_entries(**circuit_filters)

    country_filters = models.CountryColumns(
        id=params.country_id,
        code=params.country_code,
        name=params.country_name
    ).model_dump()
    non_empty_country_filters = get_non_empty_entries(**country_filters)

    circuit_query = select(
        db_models.Circuit.id.label(models.CircuitColumnNamesToResponseNames.id),
        db_models.Circuit.year.label(models.CircuitColumnNamesToResponseNames.year),
        db_models.Circuit.name.label(models.CircuitColumnNamesToResponseNames.name),
        db_models.Circuit.location.label(models.CircuitColumnNamesToResponseNames.location),
        db_models.Circuit.rotation.label(models.CircuitColumnNamesToResponseNames.rotation)
    ).filter_by(**non_empty_circuit_filters).subquery()

    country_query = select(
        db_models.Country.id.label(models.CountryColumnNamesToResponseNames.id),
        db_models.Country.code.label(models.CountryColumnNamesToResponseNames.code),
        db_models.Country.name.label(models.CountryColumnNamesToResponseNames.name)
    ).filter_by(**non_empty_country_filters).subquery()

    turn_query = select(
        db_models.Turn.number.label(models.TurnColumnNamesToResponseNames.number),
        db_models.Turn.angle.label(models.TurnColumnNamesToResponseNames.angle),
        db_models.Turn.length.label(models.TurnColumnNamesToResponseNames.length),
        db_models.Turn.x.label(models.TurnColumnNamesToResponseNames.x),
        db_models.Turn.y.label(models.TurnColumnNamesToResponseNames.y)
    ).subquery()

    
    circuit_results = await db_session.execute(
        select(
            circuit_query.c[models.CircuitColumnNamesToResponseNames.id],
            circuit_query.c[models.CircuitColumnNamesToResponseNames.year],
            circuit_query.c[models.CircuitColumnNamesToResponseNames.name],
            circuit_query.c[models.CircuitColumnNamesToResponseNames.location],
            country_query.c[models.CountryColumnNamesToResponseNames.id],
            country_query.c[models.CountryColumnNamesToResponseNames.code],
            country_query.c[models.CountryColumnNamesToResponseNames.name]
        )
        .select_from(circuit_query)
        .join(
            country_query,
            circuit_query.c[models.CircuitColumnNamesToResponseNames.country_id] == country_query.c[models.CountryColumnNamesToResponseNames.id]
        )
        .order_by(
            circuit_query.c[models.CircuitColumnNamesToResponseNames.year],
            circuit_query.c[models.CircuitColumnNamesToResponseNames.name]
        )
    )

    # Query all circuits and get all turns for each circuit
    circuits = await asyncio.gather(*[
        create_circuit_response(
            circuit_result_obj=circuit_result._asdict(),
            circuit_query=circuit_query,
            turn_query=turn_query,
            db_session=db_session
        ) for circuit_result in circuit_results
    ])

    return circuits


@router.get("/circuits/{id}")
async def get_circuit(
    id: int,
    db_session: AsyncSession = Depends(get_db_session)
):
    result = await db_session.get(entity=db_models.Circuit, ident=id)
    return None


@router.get("/meetings")
async def get_meetings(
    params: Annotated[models.MeetingFilterParams, Query()],
    db_session: AsyncSession = Depends(get_db_session)
):
    non_empty_params = get_non_empty_entries(**params.model_dump())
    result = await db_session.scalars(select(db_models.Meeting).filter_by(**non_empty_params)).all()
    return None


@router.get("/meetings/{id}")
async def get_meeting(
    id: int,
    db_session: AsyncSession = Depends(get_db_session)
):
    return None


@router.get("/sessions")
async def get_sessions(
    params: Annotated[models.SessionFilterParams, Query()],
    db_session: AsyncSession = Depends(get_db_session)
):
    non_empty_params = get_non_empty_entries(**params.model_dump())
    result = await db_session.scalars(select(db_models.Meeting).join(db_models.Meeting.sessions).filter_by(**non_empty_params)).all()
    return None


@router.get("/sessions/{id}")
async def get_session(
    id: int,
    db_session: AsyncSession = Depends(get_db_session)
):
    result = await db_session.get(entity=db_models.Session, ident=id)
    return None


@router.get("/teams")
async def get_teams(
    params: Annotated[models.TeamFilterParams, Query()],
    db_session: AsyncSession = Depends(get_db_session)
):
    non_empty_params = get_non_empty_entries(**params.model_dump())
    result = await db_session.scalars(select(db_models.Team).filter_by(**non_empty_params)).all()
    return None


@router.get("/teams/{id}")
async def get_team(
    id: int,
    db_session: AsyncSession = Depends(get_db_session)
):
    result = await db_session.get(entity=db_models.Team, ident=id)
    return None


@router.get("/drivers")
async def get_drivers(
    params: Annotated[models.DriverFilterParams, Query()],
    db_session: AsyncSession = Depends(get_db_session)
):
    non_empty_params = get_non_empty_entries(**params.model_dump())
    result = await db_session.scalars(select(db_models.Driver).filter_by(**non_empty_params)).all()
    return None


@router.get("/drivers/{id}")
async def get_driver(
    id: int,
    db_session: AsyncSession = Depends(get_db_session)
):
    result = await db_session.get(entity=db_models.Driver, ident=id)
    return None


@router.get("/events")
async def get_events(
    params: Annotated[models.EventFilterParams, Query()],
    db_session: AsyncSession = Depends(get_db_session)
):
    non_empty_params = get_non_empty_entries(**params.model_dump())
    result = await db_session.scalars(select(db_models.Event).join(db_models.Event.location).filter_by(**non_empty_params)).all()
    return None


@router.get("/event{id}")
async def get_event(
    id: int,
    db_session: AsyncSession = Depends(get_db_session)
):
    result = await db_session.get(entity=db_models.Event, ident=id)
    return None