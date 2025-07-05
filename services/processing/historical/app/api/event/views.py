from typing import Annotated

import asyncio
from fastapi import APIRouter, Depends, Query

from app.api.circuit import services as circuit_services
from app.api.event import services as event_services
from app.api.event_role import services as event_role_services
from app.api.location import services as location_services
from app.api.event_role.models import EventRoleResponse
from app.api.location.models import LocationResponse
from app.db.core import AsyncSession, get_db_session
from .enums import EventCauseEnum
from .models import (
    Event,
    EventGet,
    EventResponse,
    EventDataResponse
)

router = APIRouter()


@router.get(
    path="/",
    response_model=list[EventResponse]
)
async def get_events(
    params: Annotated[EventGet, Query()],
    db_session: AsyncSession = Depends(get_db_session)
):
    
    events = await event_services.get_all(
        db_session=db_session,
        id=params.event_id,
        meeting_id=params.meeting_id,
        session_name=params.session_name,
        date=params.date,
        elapsed_time=params.elapsed_time,
        lap_number=params.lap_number,
        category=params.category,
        cause=params.cause,
    )

    roles = await asyncio.gather(*[
        event_role_services.get_all_by_event_id(
            db_session=db_session,
            event_id=event.id
        ) for event in events
    ])

    circuits = await asyncio.gather(*[
        circuit_services.get_by_meeting_id(
            db_session=db_session,
            meeting_id=event.meeting_id
        ) for event in events
    ])

    response = []

    for idx, event in enumerate(events):
        event_roles = roles[idx]
        event_circuit = circuits[idx]

        details_response = None

        # TODO: handle different causes
        if event.cause == EventCauseEnum.OVERTAKE:
            location = await location_services.get(
                db_session=db_session,
                event_id=event.id
            )

            details_response = LocationResponse(
                date=location.date,
                x=location.x,
                y=location.y
            )
        
        event_roles_response = list(map(lambda event_role : EventRoleResponse(driver_id=event_role.driver_id, role=event_role.role), event_roles))

        event_data_response = EventDataResponse(
            date=event.date,
            elapsed_time=event.elapsed_time,
            lap_number=event.lap_number,
            category=event.category,
            cause=event.cause,
            roles=event_roles_response,
            details=details_response
        )

        response.append(
            EventResponse(
                event_id=event.id,
                circuit_id=event_circuit.id,
                meeting_id=event.meeting_id,
                session_name=event.session_name,
                data=event_data_response
            )
        )

    return response


@router.get(
    path="/{event_id}",
    response_model=EventResponse
)
async def get_event(
    event_id: int,
    db_session: AsyncSession = Depends(get_db_session)
):
    
    event = await event_services.get(
        db_session=db_session,
        id=event_id
    )

    roles = await event_role_services.get_all_by_event_id(
        db_session=db_session,
        event_id=event.id
    )

    circuit = await circuit_services.get_by_meeting_id(
        db_session=db_session,
        meeting_id=event.meeting_id
    )

    details_response = None

    # TODO: handle different causes
    if event.cause == EventCauseEnum.OVERTAKE:
        location = await location_services.get(
            db_session=db_session,
            event_id=event.id
        )

        details_response = LocationResponse(
            date=location.date,
            x=location.x,
            y=location.y
        )
    
    event_roles_response = list(map(lambda event_role : EventRoleResponse(driver_id=event_role.driver_id, role=event_role.role), roles))

    event_data_response = EventDataResponse(
        date=event.date,
        elapsed_time=event.elapsed_time,
        lap_number=event.lap_number,
        category=event.category,
        cause=event.cause,
        roles=event_roles_response,
        details=details_response
    )

    return EventResponse(
        event_id=event.id,
        circuit_id=circuit.id,
        meeting_id=event.meeting_id,
        session_name=event.session_name,
        data=event_data_response
    )