from datetime import datetime as dt
from typing import Optional

from sqlmodel import Column, DateTime, Enum, Field

from app.definitions import EmissionType, EnergyCategory
from app.definitions.general import EnergyLocation
from app.models.base import BaseSQLModel


class Energy(BaseSQLModel, table=True):
    quantity: float = Field(default=None, nullable=False)
    description: Optional[str] = Field(default=None, nullable=True)
    datetime: dt = Field(
        default=None, sa_column=Column(DateTime(timezone=True), nullable=False)
    )

    location: EnergyLocation = Field(
        sa_column=Column(Enum(EnergyLocation)),
        nullable=False,
    )

    energy_category: EnergyCategory = Field(
        sa_column=Column(Enum(EnergyCategory)),
        nullable=False,
    )

    emission_type: EmissionType = Field(
        sa_column=Column(Enum(EmissionType)),
        nullable=False,
    )
