# isort: skip_file
import json
from datetime import datetime as dt

from fastapi import APIRouter, Depends, HTTPException, Response, status

from app.core import get_logger
from app.models import Oil
from app.schemas.oil_schema import (
    OilCreateSchema,
    OilUpdateSchema,
)
from app.services.oil import OilService
from app.utils.errors import AppError


logger = get_logger(__name__)
oil_router = APIRouter()


@oil_router.get("/", response_model=list[Oil])
async def list_energies(
    oil_service: OilService = Depends(),
) -> list[Oil]:
    result = oil_service.get_all()
    if isinstance(result, AppError):
        raise HTTPException(
            status_code=result.error_type,
            detail=result.message,
        )
    return result


@oil_router.get("/consumo_mensual_aceite")
async def consumo_mensual_aceite(
    year: int, oil_service: OilService = Depends()
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

    result = oil_service.get_monthly_consumption_by_type_and_year(year)
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


@oil_router.get("/mes_menos_perdida_refrigerante")
async def mes_menos_perdida_refrigerante(
    year: int, oil_service: OilService = Depends()
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

    result = oil_service.get_min_loss_by_type_and_year(year)
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


@oil_router.get("/{id}", response_model=Oil)
async def retrieve_oil(
    id: str,
    oil_service: OilService = Depends(),
) -> Oil:
    oil = oil_service.get(id)
    if oil:
        return oil
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Oil not found"
        )


@oil_router.post("/", response_model=Oil)
async def create_event(
    oil: OilCreateSchema,
    oil_service: OilService = Depends(),
) -> Oil:
    result = oil_service.create(oil)
    if isinstance(result, AppError):
        raise HTTPException(
            detail=result.message, status_code=result.error_type
        )

    return result


@oil_router.post("/bulk_create")
async def bulk_create_energies(
    energies: list[OilCreateSchema],
    oil_service: OilService = Depends(),
) -> Response:
    result = oil_service.bulk_create(energies)
    if isinstance(result, AppError):
        raise HTTPException(
            detail=result.message, status_code=result.error_type
        )

    return Response(
        content=json.dumps({"data": "Oils created succesfully"}),
        status_code=200,
        headers={"Content-Type": "application/json"},
    )


@oil_router.put("/{id}", response_model=Oil)
async def update_oil(
    id: str,
    oil: OilUpdateSchema,
    oil_service: OilService = Depends(),
) -> Oil:
    result = oil_service.update(id, oil)

    if isinstance(result, AppError):
        raise HTTPException(
            detail=result.message, status_code=result.error_type
        )

    return result


@oil_router.delete("/{id}")
async def delete_event(
    id: str,
    oil_service: OilService = Depends(),
) -> Oil:
    result = oil_service.delete(id)

    if isinstance(result, AppError):
        raise HTTPException(
            detail=result.message, status_code=result.error_type
        )

    return Response(
        content=json.dumps({"data": "Oil deleted succesfully"}),
        status_code=200,
        headers={"Content-Type": "application/json"},
    )
