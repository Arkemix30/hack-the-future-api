from datetime import datetime as dt
from typing import Optional

from pydantic import BaseModel

from app.definitions import EmissionType


class RoadtripBaseSchema(BaseModel):
    quantity: Optional[int]
    description: Optional[str]
    datetime: Optional[dt]
    emission_type: Optional[EmissionType]


class RoadtripCreateSchema(RoadtripBaseSchema):
    quantity: int
    datetime: dt
    emission_type: EmissionType


class RoadtripUpdateSchema(RoadtripBaseSchema):
    pass
