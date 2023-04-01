# isort: skip_file
import json
from datetime import datetime as dt

from fastapi import APIRouter, Depends, HTTPException, Response, status

from app.core import get_logger
from app.models import Fuel
from app.schemas.fuel_schema import (
    FuelCreateSchema,
    FuelUpdateSchema,
)
from app.services.fuel import FuelService
from app.utils.errors import AppError


logger = get_logger(__name__)
fuel_router = APIRouter()


@fuel_router.get("/", response_model=list[Fuel])
async def list_fuels(
    fuel_service: FuelService = Depends(),
) -> list[Fuel]:
    result = fuel_service.get_all()
    if isinstance(result, AppError):
        raise HTTPException(
            status_code=result.error_type,
            detail=result.message,
        )
    return result


@fuel_router.get("/consumo_anual_por_categoria/")
async def consumo_anual_por_categoria(
    year: int,
    fuel_service: FuelService = Depends(),
) -> list[Fuel]:
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

    result = fuel_service.get_consumed_fuel_percentage_by_year(year)
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


@fuel_router.get("/consumo_promedio_mensual/")
async def consumo_promedio_mensual(
    year: int,
    fuel_service: FuelService = Depends(),
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

    result = fuel_service.get_average_monthly_consumption(year)
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


@fuel_router.get("/porcentaje_por_segmento_anual/")
async def porcentaje_por_segmento_anual(
    year: int,
    fuel_service: FuelService = Depends(),
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

    result = fuel_service.get_most_impactful_emission_type(year)
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


@fuel_router.get("/{id}", response_model=Fuel)
async def retrieve_fuel(
    id: str,
    fuel_service: FuelService = Depends(),
) -> Fuel:
    fuel = fuel_service.get(id)
    if fuel:
        return fuel
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Fuel not found"
        )


@fuel_router.post("/", response_model=Fuel)
async def create_event(
    fuel: FuelCreateSchema,
    fuel_service: FuelService = Depends(),
) -> Fuel:
    result = fuel_service.create(fuel)
    if isinstance(result, AppError):
        raise HTTPException(
            detail=result.message, status_code=result.error_type
        )

    return result


@fuel_router.post("/bulk_create")
async def bulk_create_fuels(
    fuels: list[FuelCreateSchema],
    fuel_service: FuelService = Depends(),
) -> Response:
    result = fuel_service.bulk_create(fuels)
    if isinstance(result, AppError):
        raise HTTPException(
            detail=result.message, status_code=result.error_type
        )

    return Response(
        content=json.dumps({"data": "Fuels created succesfully"}),
        status_code=201,
        headers={"Content-Type": "application/json"},
    )


@fuel_router.put("/{id}", response_model=Fuel)
async def update_fuel(
    id: str,
    fuel: FuelUpdateSchema,
    fuel_service: FuelService = Depends(),
) -> Fuel:
    result = fuel_service.update(id, fuel)

    if isinstance(result, AppError):
        raise HTTPException(
            detail=result.message, status_code=result.error_type
        )

    return result


@fuel_router.delete("/{id}")
async def delete_event(
    id: str,
    fuel_service: FuelService = Depends(),
) -> Fuel:
    result = fuel_service.delete(id)

    if isinstance(result, AppError):
        raise HTTPException(
            detail=result.message, status_code=result.error_type
        )

    return Response(
        content=json.dumps({"data": "Fuel deleted succesfully"}),
        status_code=200,
        headers={"Content-Type": "application/json"},
    )
