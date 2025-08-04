from typing import Annotated

import asyncio
from fastapi import APIRouter, Depends, Query

from timestamped_for_f1_historical_api.api.v1.driver import services as driver_services
from timestamped_for_f1_historical_api.core.db import AsyncSession, get_db_session

from .models import TeamGet, TeamResponse
from .services import get, get_all


router = APIRouter()


@router.get(
    path="",
    response_model=list[TeamResponse]
)
async def get_teams(
    params: Annotated[TeamGet, Query()],
    db_session: AsyncSession = Depends(get_db_session)
):
    
    teams = await get_all(
        db_session=db_session,
        id=params.team_id,
        year=params.year,
        name=params.team_name,
        color=params.team_color
    )

    if not teams:
        return []
    
    drivers = await asyncio.gather(*[
        driver_services.get_all_by_team_id(
            db_session=db_session,
            team_id=team.id
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
    path="/{id}",
    response_model=TeamResponse
)
async def get_team(
    id: int,
    db_session: AsyncSession = Depends(get_db_session)
):
    
    team = await get(
        db_session=db_session,
        id=id
    )

    drivers = await driver_services.get_all_by_team_id(
        db_session=db_session,
        team_id=team.id
    )

    driver_ids = list(map(lambda driver : driver.id, drivers))

    return TeamResponse(
        driver_ids=driver_ids,
        team_id=team.id,
        year=team.year,
        team_name=team.name,
        team_color=team.color
    )