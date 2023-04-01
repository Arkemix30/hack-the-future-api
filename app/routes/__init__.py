from fastapi import APIRouter

from .energy_routes import energy_router
from .fuel_routes import fuel_router

api_router = APIRouter()
api_router.include_router(fuel_router, prefix="/fuel", tags=["fuel"])
api_router.include_router(energy_router, prefix="/energy", tags=["energy"])