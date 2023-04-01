from datetime import datetime as dt
from typing import Optional

from sqlmodel import Column, DateTime, Enum, Field

from app.definitions import EmissionType, FuelType
from app.models.base import BaseSQLModel


class Fuel(BaseSQLModel, table=True):
    quantity: float = Field(default=None, nullable=False)
    description: Optional[str] = Field(default=None, nullable=True)
    datetime: dt = Field(
        default=None, sa_column=Column(DateTime(timezone=True), nullable=False)
    )
    fuel_type: FuelType = Field(
        sa_column=Column(Enum(FuelType)),
        nullable=False,
    )
    emission_type: EmissionType = Field(
        sa_column=Column(Enum(EmissionType)),
        nullable=False,
    )
