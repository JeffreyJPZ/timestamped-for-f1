from fastapi import FastAPI
from .routes import router


app = FastAPI(
    root_path="/api/v1"
)

app.include_router(router)