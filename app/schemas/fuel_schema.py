from datetime import datetime as dt
from typing import Optional

from pydantic import BaseModel

from app.definitions import EmissionType, FuelType


class FuelBaseSchema(BaseModel):
    quantity: Optional[float]
    description: Optional[str]
    datetime: Optional[dt]
    fuel_type: Optional[FuelType]
    emission_type: Optional[EmissionType]


class FuelCreateSchema(FuelBaseSchema):
    quantity: float
    datetime: dt
    fuel_type: FuelType
    emission_type: EmissionType


class FuelUpdateSchema(FuelBaseSchema):
    pass


class FuelPercentageByYearResponseSchema(BaseModel):
    combustible_administrativo: float
    combustible_indirecto_de_proveedor: float
    combustible_de_logistica: float


class FuelPercentageDB(BaseModel):
    fuel_type: FuelType
    percentage: float
