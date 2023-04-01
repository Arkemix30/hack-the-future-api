from datetime import datetime as dt
from typing import Optional

from pydantic import BaseModel

from app.definitions import EmissionType, OilCategory


class OilBaseSchema(BaseModel):
    quantity: Optional[float]
    description: Optional[str]
    datetime: Optional[dt]
    oil_type: Optional[OilCategory]
    emission_type: Optional[EmissionType]


class OilCreateSchema(OilBaseSchema):
    quantity: float
    datetime: dt
    oil_type: OilCategory
    emission_type: EmissionType


class OilUpdateSchema(OilBaseSchema):
    pass
