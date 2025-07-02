from fastapi import APIRouter

from app.api.circuit.views import router as circuit_router
from app.api.driver.views import router as driver_router
from app.api.event.views import router as event_router
from app.api.meeting.views import router as meeting_router
from app.api.session.views import router as session_router
from app.api.team.views import router as team_router


router = APIRouter()

router.include_router(
    router=circuit_router,
    prefix="/circuits"
)

router.include_router(
    router=driver_router,
    prefix="/drivers"
)

router.include_router(
    router=event_router,
    prefix="/events"
)

router.include_router(
    router=meeting_router,
    prefix="/meetings"
)

router.include_router(
    router=session_router,
    prefix="/sessions"
)

router.include_router(
    router=team_router,
    prefix="/teams"
)