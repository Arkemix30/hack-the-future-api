from datetime import datetime as dt
from typing import Optional

from pydantic import BaseModel

from app.definitions import EmissionType, OilCategory, OilType


class OilBaseSchema(BaseModel):
    quantity: Optional[float]
    description: Optional[str]
    datetime: Optional[dt]
    oil_type: Optional[OilType]
    oil_category: Optional[OilCategory]
    emission_type: Optional[EmissionType]


class OilCreateSchema(OilBaseSchema):
    quantity: float
    datetime: dt
    oil_type: OilType
    oil_category: OilCategory
    emission_type: EmissionType


class OilUpdateSchema(OilBaseSchema):
    pass
