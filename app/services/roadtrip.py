# isort:skip_file
from typing import Union

from fastapi import Depends
from fastapi.encoders import jsonable_encoder

from app.core import get_logger
from app.models import Roadtrip
from app.repositories import RoadtripRepository
from app.schemas import RoadtripCreateSchema, RoadtripUpdateSchema
from app.utils.errors import AppError, DatabaseError, ErrorType

logger = get_logger(__name__)


class RoadtripService:
    def __init__(self, roadtrip_repository: RoadtripRepository = Depends()):
        self.roadtrip_repository = roadtrip_repository

    def get(self, id: int) -> Union[Roadtrip, AppError]:
        event = self.roadtrip_repository.get(id)
        if not event:
            logger.error(f"Roadtrip not found with id: {id}")
            return None
        return event

    def get_all(self) -> Union[list[Roadtrip], AppError]:
        try:
            return self.roadtrip_repository.get_all()
        except DatabaseError as err:
            logger.error(f"Error while fetching all Roadtrips, error: {err}")
            return AppError(
                error_type=ErrorType.DATASOURCE_ERROR,
                message="DB Error while fetching all Roadtrips",
            )

    def create(
        self, roadtrip: RoadtripCreateSchema
    ) -> Union[Roadtrip, AppError]:
        roadtrip = Roadtrip(**roadtrip.dict())
        try:
            return self.roadtrip_repository.create(roadtrip)
        except DatabaseError as err:
            logger.error(f"DB Error while creating Roadtrip, error: {err}")
            return AppError(
                error_type=ErrorType.DATASOURCE_ERROR,
                message="Error while creating Roadtrip",
            )

    def bulk_create(self, roadtrips: list[RoadtripCreateSchema]) -> bool:
        roadtrips = [Roadtrip(**event.dict()) for event in roadtrips]
        try:
            return self.roadtrip_repository.bulk_create(roadtrips)
        except DatabaseError as err:
            logger.error(f"DB Error while creating Events, error: {err}")
            return False

    def update(self, id: int, roadtrip: RoadtripUpdateSchema) -> Roadtrip:
        try:
            roadtrip_in_db = self.roadtrip_repository.get(id)
        except DatabaseError as err:
            logger.error(f"DB Error while fetching Roadtrip, error: {err}")
            return AppError(
                error_type=ErrorType.DATASOURCE_ERROR,
                message="Error while fetching Roadtrip",
            )

        if not roadtrip_in_db:
            return AppError(
                error_type=ErrorType.NOT_FOUND, message="Roadtrip not found"
            )

        obj_data = jsonable_encoder(roadtrip_in_db)
        if isinstance(roadtrip, dict):
            update_data = roadtrip
        else:
            update_data = roadtrip.dict(exclude_unset=True)

        # This is an iterator over the fields of the model to be updated
        for field in obj_data:
            if field in update_data:
                setattr(roadtrip_in_db, field, update_data[field])
        try:
            return self.roadtrip_repository.update(roadtrip_in_db)
        except DatabaseError as err:
            logger.error(f"DB Error while updating Roadtrip, error: {err}")
            return AppError(
                error_type=ErrorType.DATASOURCE_ERROR,
                message="Error while updating Roadtrip",
            )

    def delete(self, id: str) -> Roadtrip:
        try:
            roadtrip_in_db = self.roadtrip_repository.get(id)
        except DatabaseError as err:
            logger.error(f"DB Error while fetching Roadtrip, error: {err}")
            return AppError(
                error_type=ErrorType.DATASOURCE_ERROR,
                message="Error while fetching Roadtrip",
            )

        if isinstance(roadtrip_in_db, AppError):
            return roadtrip_in_db

        if not roadtrip_in_db:
            return AppError(
                error_type=ErrorType.NOT_FOUND, message="Roadtrip not found"
            )

        try:
            return self.roadtrip_repository.delete(roadtrip_in_db)
        except DatabaseError as err:
            logger.error(f"DB Error while deleting Roadtrip, error: {err}")
            return AppError(
                error_type=ErrorType.DATASOURCE_ERROR,
                message="Error while deleting Roadtrip",
            )
