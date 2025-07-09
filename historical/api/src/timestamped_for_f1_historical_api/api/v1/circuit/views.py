from typing import Annotated

import asyncio
from fastapi import APIRouter, Depends, Query

from timestamped_for_f1_historical_api.api.v1.country import services as country_services
from timestamped_for_f1_historical_api.api.v1.turn import services as turn_services
from timestamped_for_f1_historical_api.api.v1.turn.models import TurnResponse
from timestamped_for_f1_historical_api.core.db import AsyncSession, get_db_session

from .models import CircuitGet, CircuitResponse
from .services import get, get_all


router = APIRouter()


@router.get(
    path="",
    response_model=list[CircuitResponse]
)
async def get_circuits(
    params: Annotated[CircuitGet, Query()],
    db_session: AsyncSession = Depends(get_db_session)
):
    
    circuits = await get_all(
        db_session=db_session,
        id=params.circuit_id,
        year=params.year,
        name=params.circuit_name,
        location=params.circuit_location,
        rotation=params.circuit_rotation
    )

    if not circuits:
        return []
    
    # gather should return results in the order of returned circuits
    # TODO: handle exception
    countries = await asyncio.gather(*[
        country_services.get(
            db_session=db_session,
            id=circuit.id
        ) for circuit in circuits
    ])

    turns = await asyncio.gather(*[
        turn_services.get_all_by_circuit_id(
            db_session=db_session,
            circuit_id=circuit.id
        ) for circuit in circuits
    ])
        
    response = []

    for idx, circuit in enumerate(circuits):
        circuit_country = countries[idx]
        circuit_turns = turns[idx]

        response.append(
            CircuitResponse(
                circuit_id=circuit.id,
                year=circuit.year,
                circuit_name=circuit.name,
                circuit_location=circuit.location,
                circuit_rotation=circuit.rotation,
                turns=circuit_turns,
                country_id=circuit_country.id,
                country_code=circuit_country.code,
                country_name=circuit_country.name
            )
        )

    return response
        

@router.get(
    path="/{circuit_id}",
    response_model=CircuitResponse
)
async def get_circuit(
    circuit_id: int,
    db_session: AsyncSession = Depends(get_db_session)
):
    
    circuit = await get(
        db_session=db_session,
        id=circuit_id
    )

    country = await country_services.get(
        db_session=db_session,
        id=circuit.country_id
    )

    turns = await turn_services.get_all_by_circuit_id(
        db_session=db_session,
        circuit_id=circuit_id
    )

    # Create turn response
    turn_data = list(map(lambda turn: TurnResponse(number=turn.number, angle=turn.angle, length=turn.length, x=turn.x, y=turn.y), turns))

    return CircuitResponse(
        circuit_id=circuit.id,
        year=circuit.year,
        circuit_name=circuit.name,
        circuit_location=circuit.location,
        circuit_rotation=circuit.rotation,
        turns=turn_data,
        country_id=country.id,
        country_code=country.code,
        country_name=country.name
    )