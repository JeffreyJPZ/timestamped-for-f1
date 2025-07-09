from typing import Annotated

import asyncio
from fastapi import APIRouter, Depends, Query

from timestamped_for_f1_historical_api.api.v1.country import services as country_services
from timestamped_for_f1_historical_api.api.v1.circuit import services as circuit_services
from timestamped_for_f1_historical_api.api.v1.event.enums import EventCauseEnum
from timestamped_for_f1_historical_api.api.v1.team import services as team_services
from timestamped_for_f1_historical_api.api.v1.driver import services as driver_services
from timestamped_for_f1_historical_api.api.v1.event import services as event_services
from timestamped_for_f1_historical_api.api.v1.event_role import services as event_role_services
from timestamped_for_f1_historical_api.api.v1.location import services as location_services
from timestamped_for_f1_historical_api.api.v1.session import services as session_services
from timestamped_for_f1_historical_api.api.v1.team.models import TeamResponse
from timestamped_for_f1_historical_api.api.v1.driver.models import DriverResponse
from timestamped_for_f1_historical_api.api.v1.event.models import EventResponse, EventDataResponse
from timestamped_for_f1_historical_api.api.v1.event_role.models import EventRoleResponse
from timestamped_for_f1_historical_api.api.v1.location.models import LocationResponse
from timestamped_for_f1_historical_api.core.db import AsyncSession, get_db_session

from .models import MeetingGet, MeetingResponse
from .services import get, get_all


router = APIRouter()


@router.get(
    path="",
    response_model=list[MeetingResponse]
)
async def get_meetings(
    params: Annotated[MeetingGet, Query()],
    db_session: AsyncSession = Depends(get_db_session)
):
    
    meetings = await get_all(
        db_session=db_session,
        id=params.meeting_id,
        year=params.year,
        name=params.meeting_name,
        official_name=params.meeting_official_name,
        start_date=params.start_date,
        utc_offset=params.utc_offset
    )

    if not meetings:
        return []
    
    circuits = await asyncio.gather(*[
        circuit_services.get(
            db_session=db_session,
            id=meeting.circuit_id
        ) for meeting in meetings
    ])

    sessions = await asyncio.gather(*[
        session_services.get_all_by_meeting_id(
            db_session=db_session,
            meeting_id=meeting.id
        ) for meeting in meetings
    ])
  
    response = []

    for idx, meeting in enumerate(meetings):
        meeting_circuit = circuits[idx]
        meeting_sessions = sessions[idx]

        # Get list of session ids
        meeting_session_ids = list(map(lambda session : session.id, meeting_sessions))

        response.append(
            MeetingResponse(
                meeting_id=meeting.id,
                session_ids=meeting_session_ids,
                circuit_id=meeting_circuit.id,
                year=meeting.year,
                meeting_name=meeting.name,
                meeting_official_name=meeting.official_name,
                start_date=meeting.start_date,
                utc_offset=meeting.utc_offset
            )
        )

    return response


@router.get(
    path="/{meeting_id}",
    response_model=MeetingResponse
)
async def get_meeting(
    meeting_id: int,
    db_session: AsyncSession = Depends(get_db_session)
):
    
    meeting = await get(
        db_session=db_session,
        id=meeting_id
    )

    circuit = await circuit_services.get(
        db_session=db_session,
        id=meeting.circuit_id
    )

    sessions = await session_services.get_all_by_meeting_id(
        db_session=db_session,
        meeting_id=meeting.id
    )
    
    session_ids = list(map(lambda session : session.id, sessions))

    return MeetingResponse(
        meeting_id=meeting.id,
        session_ids=session_ids,
        circuit_id=circuit.id,
        year=meeting.year,
        meeting_name=meeting.name,
        meeting_official_name=meeting.official_name,
        start_date=meeting.start_date,
        utc_offset=meeting.utc_offset
    )


@router.get(
    path="/{meeting_id}/teams",
    response_model=list[TeamResponse]
)
async def get_teams_by_meeting(
    meeting_id: int,
    db_session: AsyncSession = Depends(get_db_session)
):
    
    meeting = await get(
        db_session=db_session,
        id=meeting_id
    )

    teams = await team_services.get_all_by_meeting_id(
        db_session=db_session,
        meeting_id=meeting.id
    )

    if not teams:
        return []

    drivers = await asyncio.gather(*[
        driver_services.get_all_by_team_id_and_meeting_id(
            db_session=db_session,
            team_id=team.id,
            meeting_id=meeting.id
        ) for team in teams
    ])
        
    response = []

    for idx, team in enumerate(teams):
        team_drivers = drivers[idx]

        # Get a list of driver ids
        team_driver_ids = list(map(lambda driver : driver.id, team_drivers))

        response.append(
            TeamResponse(
                driver_ids=team_driver_ids,
                team_id=team.id,
                year=team.year,
                team_name=team.name,
                team_color=team.color
            )
        )

    return response


@router.get(
    path="/{meeting_id}/drivers",
    response_model=list[DriverResponse]
)
async def get_drivers_by_meeting(
    meeting_id: int,
    db_session: AsyncSession = Depends(get_db_session)
):
    
    meeting = await get(
        db_session=db_session,
        id=meeting_id
    )

    drivers = await driver_services.get_all_by_meeting_id(
        db_session=db_session,
        meeting_id=meeting.id
    )

    if not drivers:
        return []

    teams = await asyncio.gather(*[
        team_services.get_all_by_driver_id(
            db_session=db_session,
            driver_id=driver.id
        ) for driver in drivers
    ])

    countries = await asyncio.gather(*[
        country_services.get(
            db_session=db_session,
            id=driver.country_id
        ) for driver in drivers
    ])

    response = []

    for idx, driver in enumerate(drivers):
        driver_country = countries[idx]
        driver_teams = teams[idx]

        # Get a list of team ids
        driver_team_ids = list(map(lambda team : team.id, driver_teams))

        response.append(
            DriverResponse(
                team_ids=driver_team_ids,
                driver_id=driver.id,
                year=driver.year,
                driver_number=driver.number,
                driver_acronym=driver.acronym,
                first_name=driver.first_name,
                last_name=driver.last_name,
                full_name=driver.full_name,
                broadcast_name=driver.broadcast_name,
                image_url=driver.image_url,
                country_id=driver_country.id,
                country_code=driver_country.code
            )
        )

    return response


@router.get(
    path="/{meeting_id}/events",
    response_model=list[EventResponse]
)
async def get_events_by_meeting(
    meeting_id: int,
    db_session: AsyncSession = Depends(get_db_session)
):
    
    meeting = await get(
        db_session=db_session,
        id=meeting_id
    )

    events = await event_services.get_all_by_meeting_id(
        db_session=db_session,
        meeting_id=meeting.id
    )

    if not events:
        return []

    roles = await asyncio.gather(*[
        event_role_services.get_all_by_event_id(
            db_session=db_session,
            event_id=event.id
        ) for event in events
    ])

    circuit = await circuit_services.get_by_meeting_id(
        db_session=db_session,
        meeting_id=meeting.id
    )

    response = []

    for idx, event in enumerate(events):
        event_roles = roles[idx]

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
                circuit_id=circuit.id,
                meeting_id=meeting.id,
                session_id=event.session_id,
                data=event_data_response
            )
        )

    return response


