from typing import Annotated, Any

from fastapi import APIRouter, Depends, Query

from app.db.core import AsyncSession, Subquery, get_db_session, select
from app.utils import get_non_empty_keys
from .models import (
    Circuit,
    CircuitFilterParams
)


router = APIRouter()


# async def create_circuit_response(circuit_result_obj: dict[str, Any], circuit_query: Subquery, turn_query: Subquery, db_session: AsyncSession) -> CircuitResponse:

#     turn_results = await db_session.execute(
#         select(
#             turn_query.c[TurnColumnNamesToResponseNames.number],
#             turn_query.c[TurnColumnNamesToResponseNames.angle],
#             turn_query.c[TurnColumnNamesToResponseNames.length],
#             turn_query.c[TurnColumnNamesToResponseNames.x],
#             turn_query.c[TurnColumnNamesToResponseNames.y]
#         )
#         .select_from(turn_query)
#         .join(
#             circuit_query,
#             turn_query.c[TurnColumnNamesToResponseNames.circuit_id] == circuit_result_obj[CircuitColumnNamesToResponseNames.id]
#         )
#     )

#     turns = []

#     for turn_result in turn_results:
#         turn_result_obj = turn_result._asdict()
#         turn_response = TurnResponse(**turn_result_obj)
#         turns.append(turn_response)

#     return CircuitResponse(
#         turns=turns,
#         **circuit_result_obj
#     )


# @router.get(
#     "/",
#     response_model=list[CircuitResponse]
# )
# async def get_circuits(
#     params: Annotated[CircuitFilterParams, Query()],
#     db_session: AsyncSession = Depends(get_db_session)
# ):
#     circuit_filters = CircuitColumns(
#         id=params.circuit_id,
#         year=params.year,
#         name=params.circuit_name,
#         location=params.circuit_location,
#         rotation=params.circuit_rotation
#     ).model_dump()
#     non_empty_circuit_filters = get_non_empty_keys(**circuit_filters)

#     country_filters = CountryColumns(
#         id=params.country_id,
#         code=params.country_code,
#         name=params.country_name
#     ).model_dump()
#     non_empty_country_filters = get_non_empty_keys(**country_filters)

#     circuit_query = select(
#         db_Circuit.id.label(CircuitColumnNamesToResponseNames.id),
#         db_Circuit.year.label(CircuitColumnNamesToResponseNames.year),
#         db_Circuit.name.label(CircuitColumnNamesToResponseNames.name),
#         db_Circuit.location.label(CircuitColumnNamesToResponseNames.location),
#         db_Circuit.rotation.label(CircuitColumnNamesToResponseNames.rotation)
#     ).filter_by(**non_empty_circuit_filters).subquery()

#     country_query = select(
#         db_Country.id.label(CountryColumnNamesToResponseNames.id),
#         db_Country.code.label(CountryColumnNamesToResponseNames.code),
#         db_Country.name.label(CountryColumnNamesToResponseNames.name)
#     ).filter_by(**non_empty_country_filters).subquery()

#     turn_query = select(
#         db_Turn.number.label(TurnColumnNamesToResponseNames.number),
#         db_Turn.angle.label(TurnColumnNamesToResponseNames.angle),
#         db_Turn.length.label(TurnColumnNamesToResponseNames.length),
#         db_Turn.x.label(TurnColumnNamesToResponseNames.x),
#         db_Turn.y.label(TurnColumnNamesToResponseNames.y)
#     ).subquery()

    
#     circuit_results = await db_session.execute(
#         select(
#             circuit_query.c[CircuitColumnNamesToResponseNames.id],
#             circuit_query.c[CircuitColumnNamesToResponseNames.year],
#             circuit_query.c[CircuitColumnNamesToResponseNames.name],
#             circuit_query.c[CircuitColumnNamesToResponseNames.location],
#             country_query.c[CountryColumnNamesToResponseNames.id],
#             country_query.c[CountryColumnNamesToResponseNames.code],
#             country_query.c[CountryColumnNamesToResponseNames.name]
#         )
#         .select_from(circuit_query)
#         .join(
#             country_query,
#             circuit_query.c[CircuitColumnNamesToResponseNames.country_id] == country_query.c[CountryColumnNamesToResponseNames.id]
#         )
#         .order_by(
#             circuit_query.c[CircuitColumnNamesToResponseNames.year],
#             circuit_query.c[CircuitColumnNamesToResponseNames.name]
#         )
#     )

#     # Query all circuits and get all turns for each circuit
#     circuits = await asyncio.gather(*[
#         create_circuit_response(
#             circuit_result_obj=circuit_result._asdict(),
#             circuit_query=circuit_query,
#             turn_query=turn_query,
#             db_session=db_session
#         ) for circuit_result in circuit_results
#     ])

#     return circuits


@router.get("/{id}")
async def get_circuit(
    id: int,
    db_session: AsyncSession = Depends(get_db_session)
):
    result = await db_session.get(entity=Circuit, ident=id)
    return None