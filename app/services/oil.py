# isort:skip_file
from typing import Union

from fastapi import Depends
from fastapi.encoders import jsonable_encoder

from app.core import get_logger
from app.models import Oil
from app.repositories import OilRepository
from app.schemas import OilCreateSchema, OilUpdateSchema
from app.utils.errors import AppError, DatabaseError, ErrorType

logger = get_logger(__name__)


class OilService:
    def __init__(self, oil_repository: OilRepository = Depends()):
        self.oil_repository = oil_repository

    def get(self, id: int) -> Union[Oil, AppError]:
        event = self.oil_repository.get(id)
        if not event:
            logger.error(f"Oil not found with id: {id}")
            return None
        return event

    def get_all(self) -> Union[list[Oil], AppError]:
        try:
            return self.oil_repository.get_all()
        except DatabaseError as err:
            logger.error(f"Error while fetching all Oils, error: {err}")
            return AppError(
                error_type=ErrorType.DATASOURCE_ERROR,
                message="DB Error while fetching all Oils",
            )

    def create(self, oil: OilCreateSchema) -> Union[Oil, AppError]:
        oil = Oil(**oil.dict())
        try:
            return self.oil_repository.create(oil)
        except DatabaseError as err:
            logger.error(f"DB Error while creating Oil, error: {err}")
            return AppError(
                error_type=ErrorType.DATASOURCE_ERROR,
                message="Error while creating Oil",
            )

    def bulk_create(self, oils: list[OilCreateSchema]) -> bool:
        oils = [Oil(**event.dict()) for event in oils]
        try:
            return self.oil_repository.bulk_create(oils)
        except DatabaseError as err:
            logger.error(f"DB Error while creating Events, error: {err}")
            return False

    def update(self, id: int, oil: OilUpdateSchema) -> Oil:
        try:
            oil_in_db = self.oil_repository.get(id)
        except DatabaseError as err:
            logger.error(f"DB Error while fetching Oil, error: {err}")
            return AppError(
                error_type=ErrorType.DATASOURCE_ERROR,
                message="Error while fetching Oil",
            )

        if not oil_in_db:
            return AppError(
                error_type=ErrorType.NOT_FOUND, message="Oil not found"
            )

        obj_data = jsonable_encoder(oil_in_db)
        if isinstance(oil, dict):
            update_data = oil
        else:
            update_data = oil.dict(exclude_unset=True)

        # This is an iterator over the fields of the model to be updated
        for field in obj_data:
            if field in update_data:
                setattr(oil_in_db, field, update_data[field])
        try:
            return self.oil_repository.update(oil_in_db)
        except DatabaseError as err:
            logger.error(f"DB Error while updating Oil, error: {err}")
            return AppError(
                error_type=ErrorType.DATASOURCE_ERROR,
                message="Error while updating Oil",
            )

    def delete(self, id: str) -> Oil:
        try:
            oil_in_db = self.oil_repository.get(id)
        except DatabaseError as err:
            logger.error(f"DB Error while fetching Oil, error: {err}")
            return AppError(
                error_type=ErrorType.DATASOURCE_ERROR,
                message="Error while fetching Oil",
            )

        if isinstance(oil_in_db, AppError):
            return oil_in_db

        if not oil_in_db:
            return AppError(
                error_type=ErrorType.NOT_FOUND, message="Oil not found"
            )

        try:
            return self.oil_repository.delete(oil_in_db)
        except DatabaseError as err:
            logger.error(f"DB Error while deleting Oil, error: {err}")
            return AppError(
                error_type=ErrorType.DATASOURCE_ERROR,
                message="Error while deleting Oil",
            )
