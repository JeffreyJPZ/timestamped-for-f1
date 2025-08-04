from fastapi import APIRouter

from timestamped_for_f1_historical_api.api.v1.circuit.views import router as circuit_router
from timestamped_for_f1_historical_api.api.v1.driver.views import router as driver_router
from timestamped_for_f1_historical_api.api.v1.event.views import router as event_router
from timestamped_for_f1_historical_api.api.v1.meeting.views import router as meeting_router
from timestamped_for_f1_historical_api.api.v1.session.views import router as session_router
from timestamped_for_f1_historical_api.api.v1.team.views import router as team_router


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