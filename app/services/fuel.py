# isort:skip_file
from typing import Union

from fastapi import Depends
from fastapi.encoders import jsonable_encoder

from app.core import get_logger
from app.models import Fuel
from app.repositories import FuelRepository
from app.schemas import FuelCreateSchema, FuelUpdateSchema
from app.utils.errors import AppError, DatabaseError, ErrorType

logger = get_logger(__name__)


class FuelService:
    def __init__(self, fuel_repository: FuelRepository = Depends()):
        self.fuel_repository = fuel_repository

    def get(self, id: int) -> Union[Fuel, AppError]:
        event = self.fuel_repository.get(id)
        if not event:
            logger.error(f"Fuel not found with id: {id}")
            return None
        return event

    def get_all(self) -> Union[list[Fuel], AppError]:
        try:
            return self.fuel_repository.get_all()
        except DatabaseError as err:
            logger.error(f"Error while fetching all Fuels, error: {err}")
            return AppError(
                error_type=ErrorType.DATASOURCE_ERROR,
                message="DB Error while fetching all Fuels",
            )

    def create(self, fuel: FuelCreateSchema) -> Union[Fuel, AppError]:
        fuel = Fuel(**fuel.dict())
        try:
            return self.fuel_repository.create(fuel)
        except DatabaseError as err:
            logger.error(f"DB Error while creating Fuel, error: {err}")
            return AppError(
                error_type=ErrorType.DATASOURCE_ERROR,
                message="Error while creating Fuel",
            )

    def bulk_create(self, fuels: list[FuelCreateSchema]) -> bool:
        fuels = [Fuel(**event.dict()) for event in fuels]
        try:
            return self.fuel_repository.bulk_create(fuels)
        except DatabaseError as err:
            logger.error(f"DB Error while creating Events, error: {err}")
            return False

    def update(self, id: int, fuel: FuelUpdateSchema) -> Fuel:
        try:
            fuel_in_db = self.fuel_repository.get(id)
        except DatabaseError as err:
            logger.error(f"DB Error while fetching Fuel, error: {err}")
            return AppError(
                error_type=ErrorType.DATASOURCE_ERROR,
                message="Error while fetching Fuel",
            )

        if not fuel_in_db:
            return AppError(
                error_type=ErrorType.NOT_FOUND, message="Fuel not found"
            )

        obj_data = jsonable_encoder(fuel_in_db)
        if isinstance(fuel, dict):
            update_data = fuel
        else:
            update_data = fuel.dict(exclude_unset=True)

        # This is an iterator over the fields of the model to be updated
        for field in obj_data:
            if field in update_data:
                setattr(fuel_in_db, field, update_data[field])
        try:
            return self.fuel_repository.update(fuel_in_db)
        except DatabaseError as err:
            logger.error(f"DB Error while updating Fuel, error: {err}")
            return AppError(
                error_type=ErrorType.DATASOURCE_ERROR,
                message="Error while updating Fuel",
            )

    def delete(self, id: str) -> Fuel:
        try:
            fuel_in_db = self.fuel_repository.get(id)
        except DatabaseError as err:
            logger.error(f"DB Error while fetching Fuel, error: {err}")
            return AppError(
                error_type=ErrorType.DATASOURCE_ERROR,
                message="Error while fetching Fuel",
            )

        if isinstance(fuel_in_db, AppError):
            return fuel_in_db

        if not fuel_in_db:
            return AppError(
                error_type=ErrorType.NOT_FOUND, message="Fuel not found"
            )

        try:
            return self.fuel_repository.delete(fuel_in_db)
        except DatabaseError as err:
            logger.error(f"DB Error while deleting Fuel, error: {err}")
            return AppError(
                error_type=ErrorType.DATASOURCE_ERROR,
                message="Error while deleting Fuel",
            )

    def get_consumed_fuel_percentage_by_year(
        self, year: int
    ) -> Union[dict, AppError]:
        try:
            result = self.fuel_repository.get_consumed_fuel_percentage_by_year(
                year
            )
        except DatabaseError as err:
            logger.error(
                f"DB Error while fetching consumed fuel by year and fuel type, error: {err}"
            )
            return AppError(
                error_type=ErrorType.DATASOURCE_ERROR,
                message="Error while fetching consumed fuel by year and fuel type",
            )

        return result

    def get_average_monthly_consumption(
        self, year: int
    ) -> Union[list[dict], AppError]:
        try:
            result = self.fuel_repository.get_average_monthly_consumption(year)
        except DatabaseError as err:
            logger.error(
                f"DB Error while fetching consumed fuel by year and fuel type, error: {err}"
            )
            return AppError(
                error_type=ErrorType.DATASOURCE_ERROR,
                message="Error while fetching consumed fuel by year and fuel type",
            )

        return result

    def get_most_impactful_emission_type(
        self, year: int
    ) -> Union[list[dict], AppError]:
        try:
            result = self.fuel_repository.get_most_impactful_emission_type(
                year
            )
        except DatabaseError as err:
            logger.error(
                f"DB Error while fetching consumed fuel by year and fuel type, error: {err}"
            )
            return AppError(
                error_type=ErrorType.DATASOURCE_ERROR,
                message="Error while fetching consumed fuel by year and fuel type",
            )

        return result
