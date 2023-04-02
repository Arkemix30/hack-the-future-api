from fastapi import APIRouter

from .energy_routes import energy_router
from .fuel_routes import fuel_router
from .oil_routes import oil_router
from .report_routes import report_router
from .roadtrip_routes import roadtrip_router

api_router = APIRouter()
api_router.include_router(energy_router, prefix="/energy", tags=["energy"])
api_router.include_router(fuel_router, prefix="/fuel", tags=["fuel"])
api_router.include_router(oil_router, prefix="/oil", tags=["oil"])
api_router.include_router(
    roadtrip_router, prefix="/roadtrip", tags=["roadtrip"]
)
api_router.include_router(report_router, tags=["report"])
