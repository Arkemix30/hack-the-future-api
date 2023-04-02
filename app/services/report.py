# isort:skip_file
from typing import Optional, Union

from fastapi import Depends

from app.core import get_logger
from app.repositories import FuelRepository, EnergyRepository
from app.repositories.oil_repo import OilRepository

# from app.schemas import FuelCreateSchema, FuelUpdateSchema
from app.utils.errors import AppError, DatabaseError, ErrorType

logger = get_logger(__name__)


class ReportService:
    def __init__(
        self,
        fuel_repository: FuelRepository = Depends(),
        oil_repository: OilRepository = Depends(),
        energy_repository: EnergyRepository = Depends(),
    ):
        self.fuel_repository = fuel_repository
        self.oil_repository = oil_repository
        self.energy_repository = energy_repository

    def get_comparative_energy_fuel_by_year(
        self, year: int
    ) -> Union[dict[str, float], AppError]:
        try:
            fuel_sum = self.fuel_repository.get_fuel_sum_by_year(year)
            energy_sum = self.energy_repository.get_energy_sum_by_year(year)
        except DatabaseError as err:
            logger.error(f"Error while fetching all Fuels, error: {err}")
            return AppError(
                error_type=ErrorType.DATASOURCE_ERROR,
                message="Error while fetching all Fuels",
            )

        if fuel_sum is None:
            fuel_sum = 0

        if energy_sum is None:
            energy_sum = 0

        try:
            fuel_percentage = fuel_sum / (fuel_sum + energy_sum)
            energy_percentage = energy_sum / (fuel_sum + energy_sum)
        except Exception as err:
            logger.error(f"Error while calculating percentages, error: {err}")
            return AppError(
                error_type=ErrorType.NOT_FOUND,
                message="No data found for requested year",
            )

        return {
            "fuel_percentage": round(fuel_percentage, 2),
            "energy_percentage": round(energy_percentage, 2),
        }

    def get_average_consumption_by_year(
        self, year: int
    ) -> Union[dict[str, float], AppError]:
        try:
            fuel_average: Optional[
                int
            ] = self.fuel_repository.get_average_monthly_consumption(year)
            oil_average: dict[
                str, int
            ] = self.oil_repository.get_average_compsution_for_every_type(year)
        except DatabaseError as err:
            logger.error(
                f"Error while fetching all average consumption for every oil type, error: {err}"
            )
            return AppError(
                error_type=ErrorType.DATASOURCE_ERROR,
                message="Error while fetching all average consumption for every oil type",
            )

        if fuel_average is None:
            fuel_average = 0

        return {
            **oil_average,
            "COMBUSTIBLE": round(fuel_average, 2),
        }
