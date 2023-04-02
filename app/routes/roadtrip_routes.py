# isort: skip_file
import json
from datetime import datetime as dt

from fastapi import APIRouter, Depends, HTTPException, Response, status

from app.core import get_logger
from app.models import Roadtrip
from app.schemas.roadtrip_schema import (
    RoadtripCreateSchema,
    RoadtripUpdateSchema,
)
from app.services.roadtrip import RoadtripService
from app.utils.errors import AppError


logger = get_logger(__name__)
roadtrip_router = APIRouter()


@roadtrip_router.get("/", response_model=list[Roadtrip])
async def list_energies(
    roadtrip_service: RoadtripService = Depends(),
) -> list[Roadtrip]:
    result = roadtrip_service.get_all()
    if isinstance(result, AppError):
        raise HTTPException(
            status_code=result.error_type,
            detail=result.message,
        )
    return result


@roadtrip_router.get("/comparativa_promedio_mensual")
async def comparativa_promedio_mensual(
    year: int,
    roadtrip_service: RoadtripService = Depends(),
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

    result = roadtrip_service.get_average_monthly_comparative_percentage(year)
    if isinstance(result, AppError):
        raise HTTPException(
            status_code=result.error_type,
            detail=result.message,
        )
    return Response(
        content=json.dumps({"data": result}),
        status_code=200,
        headers={"Content-Type": "application/json"},
    )


@roadtrip_router.get("/{id}", response_model=Roadtrip)
async def retrieve_roadtrip(
    id: str,
    roadtrip_service: RoadtripService = Depends(),
) -> Roadtrip:
    roadtrip = roadtrip_service.get(id)
    if roadtrip:
        return roadtrip
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Roadtrip not found"
        )


@roadtrip_router.post("/", response_model=Roadtrip)
async def create_roadtrip(
    roadtrip: RoadtripCreateSchema,
    roadtrip_service: RoadtripService = Depends(),
) -> Roadtrip:
    result = roadtrip_service.create(roadtrip)
    if isinstance(result, AppError):
        raise HTTPException(
            detail=result.message, status_code=result.error_type
        )

    return result


@roadtrip_router.post("/bulk_create")
async def bulk_create_energies(
    energies: list[RoadtripCreateSchema],
    roadtrip_service: RoadtripService = Depends(),
) -> Response:
    result = roadtrip_service.bulk_create(energies)
    if isinstance(result, AppError):
        raise HTTPException(
            detail=result.message, status_code=result.error_type
        )

    return Response(
        content=json.dumps({"data": "Roadtrips created succesfully"}),
        status_code=200,
        headers={"Content-Type": "application/json"},
    )


@roadtrip_router.put("/{id}", response_model=Roadtrip)
async def update_roadtrip(
    id: str,
    roadtrip: RoadtripUpdateSchema,
    roadtrip_service: RoadtripService = Depends(),
) -> Roadtrip:
    result = roadtrip_service.update(id, roadtrip)

    if isinstance(result, AppError):
        raise HTTPException(
            detail=result.message, status_code=result.error_type
        )

    return result


@roadtrip_router.delete("/{id}")
async def delete_event(
    id: str,
    roadtrip_service: RoadtripService = Depends(),
) -> Roadtrip:
    result = roadtrip_service.delete(id)

    if isinstance(result, AppError):
        raise HTTPException(
            detail=result.message, status_code=result.error_type
        )

    return Response(
        content=json.dumps({"data": "Roadtrip deleted succesfully"}),
        status_code=200,
        headers={"Content-Type": "application/json"},
    )
