from typing import Annotated

import asyncio
from fastapi import APIRouter, Depends, Query

from timestamped_for_f1_historical_api.api.v1.circuit import services as circuit_services
from timestamped_for_f1_historical_api.api.v1.event import services as event_services
from timestamped_for_f1_historical_api.api.v1.event_role import services as event_role_services
from timestamped_for_f1_historical_api.api.v1.location import services as location_services
from timestamped_for_f1_historical_api.api.v1.session import services as session_services
from timestamped_for_f1_historical_api.api.v1.meeting import services as meeting_services
from timestamped_for_f1_historical_api.api.v1.event_role.models import EventRoleResponse
from timestamped_for_f1_historical_api.api.v1.location.models import LocationResponse
from timestamped_for_f1_historical_api.core.db import AsyncSession, get_db_session

from .enums import EventCauseEnum
from .models import (
    EventGet,
    EventResponse,
    EventDataResponse
)


router = APIRouter()


@router.get(
    path="",
    response_model=list[EventResponse]
)
async def get_events(
    params: Annotated[EventGet, Query()],
    db_session: AsyncSession = Depends(get_db_session)
):
    
    events = await event_services.get_all(
        db_session=db_session,
        id=params.event_id,
        session_id=params.session_id,
        date=params.date,
        elapsed_time=params.elapsed_time,
        lap_number=params.lap_number,
        category=params.category,
        cause=params.cause,
    )

    if not events:
        return []

    sessions = await asyncio.gather(*[
        session_services.get(
            db_session=db_session,
            id=event.session_id
        ) for event in events
    ])

    meetings = await asyncio.gather(*[
        meeting_services.get(
            db_session=db_session,
            id=session.meeting_id
        ) for session in sessions
    ])

    roles = await asyncio.gather(*[
        event_role_services.get_all_by_event_id(
            db_session=db_session,
            event_id=event.id
        ) for event in events
    ])

    circuits = await asyncio.gather(*[
        circuit_services.get_by_session_id(
            db_session=db_session,
            session_id=event.session_id
        ) for event in events
    ])

    response = []

    for idx, event in enumerate(events):
        event_session = sessions[idx]
        event_meeting = meetings[idx]
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
                meeting_id=event_meeting.id,
                session_id=event_session.id,
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

    session = await session_services.get(
        db_session=db_session,
        id=event.session_id
    )

    meeting = await meeting_services.get(
        db_session=db_session,
        id=session.meeting_id
    )

    roles = await event_role_services.get_all_by_event_id(
        db_session=db_session,
        event_id=event.id
    )

    circuit = await circuit_services.get_by_session_id(
        db_session=db_session,
        session_id=event.session_id
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
        meeting_id=meeting.id,
        session_id=session.id,
        data=event_data_response
    )