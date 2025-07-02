from fastapi import FastAPI
from views import router


app = FastAPI(
    root_path="/api/v1"
)

app.include_router(router)