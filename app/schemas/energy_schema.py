from datetime import datetime as dt
from typing import Optional

from pydantic import BaseModel

from app.definitions import EmissionType, EnergyCategory, EnergyLocation


class EnergyBaseSchema(BaseModel):
    quantity: Optional[float]
    description: Optional[str]
    datetime: Optional[dt]
    location: Optional[EnergyLocation]
    energy_category: Optional[EnergyCategory]
    emission_type: Optional[EmissionType]


class EnergyCreateSchema(EnergyBaseSchema):
    quantity: float
    datetime: dt
    location: EnergyLocation
    energy_category: EnergyCategory
    emission_type: EmissionType


class EnergyUpdateSchema(EnergyBaseSchema):
    pass
