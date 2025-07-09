import asyncio
from fastapi import FastAPI

from timestamped_for_f1_historical_api.core.db import get_db_manager

from .routes import router


# Initialize database tables if necessary and apply migrations
db_manager = asyncio.run(get_db_manager())
asyncio.run(db_manager.sync())

# Create FastAPI app
app = FastAPI(
    root_path="/api/v1"
)
app.include_router(router)