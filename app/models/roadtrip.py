from datetime import datetime as dt
from typing import Optional

from sqlmodel import Column, DateTime, Enum, Field

from app.definitions import EmissionType
from app.models.base import BaseSQLModel


class Roadtrip(BaseSQLModel, table=True):
    quantity: int = Field(default=None, nullable=False)
    description: Optional[str] = Field(default=None, nullable=True)
    datetime: dt = Field(
        default=None, sa_column=Column(DateTime(timezone=True), nullable=False)
    )
    emission_type: EmissionType = Field(
        sa_column=Column(Enum(EmissionType)),
        nullable=False,
    )
