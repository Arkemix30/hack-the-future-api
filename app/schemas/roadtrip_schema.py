from datetime import datetime as dt
from typing import Optional

from pydantic import BaseModel

from app.definitions import EmissionType, RoadtripGroupType


class RoadtripBaseSchema(BaseModel):
    quantity: Optional[int]
    description: Optional[str]
    datetime: Optional[dt]
    group: Optional[RoadtripGroupType]
    emission_type: Optional[EmissionType]


class RoadtripCreateSchema(RoadtripBaseSchema):
    quantity: int
    datetime: dt
    group: RoadtripGroupType
    emission_type: EmissionType


class RoadtripUpdateSchema(RoadtripBaseSchema):
    pass


class RoadtripPercentageDB(BaseModel):
    group: RoadtripGroupType
    sum: float
