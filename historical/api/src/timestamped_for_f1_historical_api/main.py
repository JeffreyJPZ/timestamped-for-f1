from contextlib import asynccontextmanager
from fastapi import FastAPI

from timestamped_for_f1_historical_api.core.db import get_db_manager

from .routes import router


@asynccontextmanager
async def lifespan(app: FastAPI):

    # Initialize database tables if necessary and apply migrations before handling requests
    db_manager = await get_db_manager()
    await db_manager.sync()

    yield


app = FastAPI(
    root_path="/api/v1",
    lifespan=lifespan
)

app.include_router(router)