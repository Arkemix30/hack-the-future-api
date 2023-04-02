# isort: skip_file
import json
from datetime import datetime as dt

from fastapi import APIRouter, Depends, HTTPException, Response, status

from app.core import get_logger
from app.services import ReportService
from app.utils.errors import AppError


logger = get_logger(__name__)
report_router = APIRouter()


@report_router.get("/comparativa_energia_combustible", response_model=dict)
async def comparativa_energia_combustible(
    year: int,
    report_service: ReportService = Depends(),
) -> Response:
    if year < 2000 or year > dt.now().year:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El año debe ser mayor a 2000 y menor al año actual",
        )

    comparative_energy_fuel = (
        report_service.get_comparative_energy_fuel_by_year(year)
    )

    if isinstance(comparative_energy_fuel, AppError):
        raise HTTPException(
            status_code=comparative_energy_fuel.error_type,
            detail=comparative_energy_fuel.message,
        )

    return Response(
        content=json.dumps({"data": comparative_energy_fuel}),
        media_type="application/json",
    )


@report_router.get("/promedio_mensual_petroleo")
async def promedio_mensual_petroleo(
    year: int,
    report_service: ReportService = Depends(),
) -> Response:
    if year < 1900 or year > dt.now().year:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El año debe ser mayor a 1900 y menor al año actual",
        )

    monthly_average_oil = report_service.get_average_consumption_by_year(year)

    if isinstance(monthly_average_oil, AppError):
        raise HTTPException(
            status_code=monthly_average_oil.error_type,
            detail=monthly_average_oil.message,
        )

    return Response(
        content=json.dumps({"data": monthly_average_oil}),
        media_type="application/json",
    )
