# isort: skip_file
import json
from typing import Union
from datetime import datetime as dt

from fastapi import APIRouter, Depends, HTTPException, Response, status

from app.core import get_logger
from app.definitions.general import EnergyLocation
from app.models import Energy
from app.schemas.energy_schema import (
    EnergyCreateSchema,
    EnergyUpdateSchema,
)
from app.services.energy import EnergyService
from app.utils.errors import AppError


logger = get_logger(__name__)
energy_router = APIRouter()


@energy_router.get("/", response_model=list[Energy])
async def list_energies(
    energy_service: EnergyService = Depends(),
) -> list[Energy]:
    result = energy_service.get_all()
    if isinstance(result, AppError):
        raise HTTPException(
            status_code=result.error_type,
            detail=result.message,
        )
    return result


@energy_router.get("/consumo_promedio_mensual/")
async def consumo_promedio_mensual(
    year: int,
    location: Union[EnergyLocation, None] = EnergyLocation.PLANTA_DE_ENVASADO,
    energy_service: EnergyService = Depends(),
) -> Response:
    if year is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Year is required",
        )

    if year < 1900 or year > dt.now().year:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Year must be between 1900 and {dt.now().year}",
        )

    result = energy_service.get_average_monthly_by_location_and_year(
        year, location
    )
    if isinstance(result, AppError):
        raise HTTPException(
            status_code=result.error_type,
            detail=result.message,
        )
    return result


@energy_router.get("/{id}", response_model=Energy)
async def retrieve_energy(
    id: str,
    energy_service: EnergyService = Depends(),
) -> Energy:
    energy = energy_service.get(id)
    if energy:
        return energy
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Energy not found"
        )


@energy_router.post("/", response_model=Energy)
async def create_event(
    energy: EnergyCreateSchema,
    energy_service: EnergyService = Depends(),
) -> Energy:
    result = energy_service.create(energy)
    if isinstance(result, AppError):
        raise HTTPException(
            detail=result.message, status_code=result.error_type
        )

    return result


@energy_router.post("/bulk_create")
async def bulk_create_energies(
    energies: list[EnergyCreateSchema],
    energy_service: EnergyService = Depends(),
) -> Response:
    result = energy_service.bulk_create(energies)
    if isinstance(result, AppError):
        raise HTTPException(
            detail=result.message, status_code=result.error_type
        )

    return Response(
        content=json.dumps({"data": "Energys created succesfully"}),
        status_code=201,
        headers={"Content-Type": "application/json"},
    )


@energy_router.put("/{id}", response_model=Energy)
async def update_energy(
    id: str,
    energy: EnergyUpdateSchema,
    energy_service: EnergyService = Depends(),
) -> Energy:
    result = energy_service.update(id, energy)

    if isinstance(result, AppError):
        raise HTTPException(
            detail=result.message, status_code=result.error_type
        )

    return result


@energy_router.delete("/{id}")
async def delete_event(
    id: str,
    energy_service: EnergyService = Depends(),
) -> Energy:
    result = energy_service.delete(id)

    if isinstance(result, AppError):
        raise HTTPException(
            detail=result.message, status_code=result.error_type
        )

    return Response(
        content=json.dumps({"data": "Energy deleted succesfully"}),
        status_code=200,
        headers={"Content-Type": "application/json"},
    )
