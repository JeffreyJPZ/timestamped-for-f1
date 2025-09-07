from typing import Annotated

import asyncio
from fastapi import APIRouter, Depends, Query

from timestamped_for_f1_historical_api.api.v1.country import services as country_services
from timestamped_for_f1_historical_api.api.v1.team import services as team_services
from timestamped_for_f1_historical_api.core.db import AsyncSession, get_db_session

from .models import DriverGet, DriverResponse
from .services import get, get_all


router = APIRouter()


@router.get(
    path="",
    response_model=list[DriverResponse]
)
async def get_drivers(
    params: Annotated[DriverGet, Query()],
    db_session: AsyncSession = Depends(get_db_session)
):
    
    drivers = await get_all(
        db_session=db_session,
        id=params.driver_id,
        year=params.year,
        number=params.driver_number,
        acronym=params.driver_acronym,
        first_name=params.first_name,
        last_name=params.last_name,
        full_name=params.full_name,
        broadcast_name=params.broadcast_name,
        image_url=params.image_url,
        country_id=params.country_id,
        country_code=params.country_code
    )

    if not drivers:
        return []
    
    teams = await asyncio.gather(*[
        team_services.get_all_by_driver_id(
            db_session=db_session,
            driver_id=driver.id,
            year=driver.year
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


@router.get("/{driver_id}")
async def get_driver(
    driver_id: int,
    db_session: AsyncSession = Depends(get_db_session)
):
    driver = await get(
        db_session=db_session,
        id=driver_id
    )

    teams = await team_services.get_all_by_driver_id(
        db_session=db_session,
        driver_id=driver.id,
        year=driver.year
    )

    country = await country_services.get(
        db_session=db_session,
        id=driver.country_id
    )

    team_ids = list(map(lambda team : team.id, teams))

    return DriverResponse(
        driver_id=driver.id,
        team_ids=team_ids,
        year=driver.year,
        number=driver.number,
        acronym=driver.acronym,
        first_name=driver.first_name,
        last_name=driver.last_name,
        full_name=driver.full_name,
        broadcast_name=driver.broadcast_name,
        image_url=driver.image_url,
        country_id=country.id,
        country_code=country.code
    )