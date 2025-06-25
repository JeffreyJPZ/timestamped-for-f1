from fastapi import FastAPI
from views import router

app = FastAPI()
app.include_router(router)