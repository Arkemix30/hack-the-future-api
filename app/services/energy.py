# isort:skip_file
from typing import Optional, Union

from fastapi import Depends
from fastapi.encoders import jsonable_encoder

from app.core import get_logger
from app.definitions.general import EnergyLocation
from app.models import Energy
from app.repositories import EnergyRepository
from app.schemas import EnergyCreateSchema, EnergyUpdateSchema
from app.utils.errors import AppError, DatabaseError, ErrorType

logger = get_logger(__name__)


class EnergyService:
    def __init__(self, energy_repository: EnergyRepository = Depends()):
        self.energy_repository = energy_repository

    def get(self, id: int) -> Union[Energy, AppError]:
        event = self.energy_repository.get(id)
        if not event:
            logger.error(f"Energy not found with id: {id}")
            return None
        return event

    def get_all(self) -> Union[list[Energy], AppError]:
        try:
            return self.energy_repository.get_all()
        except DatabaseError as err:
            logger.error(f"Error while fetching all Energys, error: {err}")
            return AppError(
                error_type=ErrorType.DATASOURCE_ERROR,
                message="DB Error while fetching all Energys",
            )

    def create(self, energy: EnergyCreateSchema) -> Union[Energy, AppError]:
        energy = Energy(**energy.dict())
        try:
            return self.energy_repository.create(energy)
        except DatabaseError as err:
            logger.error(f"DB Error while creating Energy, error: {err}")
            return AppError(
                error_type=ErrorType.DATASOURCE_ERROR,
                message="Error while creating Energy",
            )

    def bulk_create(self, energys: list[EnergyCreateSchema]) -> bool:
        energys = [Energy(**event.dict()) for event in energys]
        try:
            return self.energy_repository.bulk_create(energys)
        except DatabaseError as err:
            logger.error(f"DB Error while creating Events, error: {err}")
            return False

    def update(self, id: int, energy: EnergyUpdateSchema) -> Energy:
        try:
            energy_in_db = self.energy_repository.get(id)
        except DatabaseError as err:
            logger.error(f"DB Error while fetching Energy, error: {err}")
            return AppError(
                error_type=ErrorType.DATASOURCE_ERROR,
                message="Error while fetching Energy",
            )

        if not energy_in_db:
            return AppError(
                error_type=ErrorType.NOT_FOUND, message="Energy not found"
            )

        obj_data = jsonable_encoder(energy_in_db)
        if isinstance(energy, dict):
            update_data = energy
        else:
            update_data = energy.dict(exclude_unset=True)

        # This is an iterator over the fields of the model to be updated
        for field in obj_data:
            if field in update_data:
                setattr(energy_in_db, field, update_data[field])
        try:
            return self.energy_repository.update(energy_in_db)
        except DatabaseError as err:
            logger.error(f"DB Error while updating Energy, error: {err}")
            return AppError(
                error_type=ErrorType.DATASOURCE_ERROR,
                message="Error while updating Energy",
            )

    def delete(self, id: str) -> Energy:
        try:
            energy_in_db = self.energy_repository.get(id)
        except DatabaseError as err:
            logger.error(f"DB Error while fetching Energy, error: {err}")
            return AppError(
                error_type=ErrorType.DATASOURCE_ERROR,
                message="Error while fetching Energy",
            )

        if isinstance(energy_in_db, AppError):
            return energy_in_db

        if not energy_in_db:
            return AppError(
                error_type=ErrorType.NOT_FOUND, message="Energy not found"
            )

        try:
            return self.energy_repository.delete(energy_in_db)
        except DatabaseError as err:
            logger.error(f"DB Error while deleting Energy, error: {err}")
            return AppError(
                error_type=ErrorType.DATASOURCE_ERROR,
                message="Error while deleting Energy",
            )

    def get_average_monthly_by_location_and_year(
        self,
        year: int,
        location: Optional[EnergyLocation] = EnergyLocation.PLANTA_DE_ENVASADO,
    ) -> Union[dict, AppError]:
        try:
            result = self.energy_repository.get_average_monthly_by_location_and_year(
                year, location
            )
        except DatabaseError as err:
            logger.error(
                f"DB Error while fetching average monthly Energy by location and year, error: {err}"
            )
            return AppError(
                error_type=ErrorType.DATASOURCE_ERROR,
                message="Error while fetching average monthly Energy by location and year",
            )

        if not result:
            return 0

        return round(result, 2)
