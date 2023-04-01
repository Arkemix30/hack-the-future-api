from datetime import datetime as dt
from typing import Optional

from pydantic import BaseModel

from app.definitions import EmissionType, EnergyCategory


class EnergyBaseSchema(BaseModel):
    quantity: Optional[float]
    description: Optional[str]
    datetime: Optional[dt]
    energy_type: Optional[EnergyCategory]
    emission_type: Optional[EmissionType]


class EnergyCreateSchema(EnergyBaseSchema):
    quantity: float
    datetime: dt
    energy_type: EnergyCategory
    emission_type: EmissionType


class EnergyUpdateSchema(EnergyBaseSchema):
    pass
