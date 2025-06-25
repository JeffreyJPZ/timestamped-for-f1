from fastapi import APIRouter, Depends
from db import AsyncSession, gen_db_session
import models

router = APIRouter(prefix="/v1")

@router.get("/circuits/{name}")
async def get_circuit(name: str, db_session: AsyncSession = Depends(gen_db_session)):
    return None