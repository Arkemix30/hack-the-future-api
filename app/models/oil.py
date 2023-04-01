from datetime import datetime as dt
from typing import Optional

from sqlmodel import Column, DateTime, Enum, Field

from app.definitions import EmissionType, OilType
from app.models.base import BaseSQLModel


class Oil(BaseSQLModel, table=True):
    quantity: float = Field(default=None, nullable=False)
    description: Optional[str] = Field(default=None, nullable=True)
    datetime: dt = Field(
        default=None, sa_column=Column(DateTime(timezone=True), nullable=False)
    )
    oil_type: OilType = Field(
        sa_column=Column(Enum(OilType)),
        nullable=False,
    )
    emission_type: EmissionType = Field(
        sa_column=Column(Enum(EmissionType)),
        nullable=False,
    )
