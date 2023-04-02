# Python Imports
from typing import Optional, Union

# Third Party Imports
from fastapi import Depends
from sqlalchemy import func
from sqlmodel import Session, column, select

# Local Imports
from app.core import get_logger
from app.definitions.general import EmissionType, FuelType
from app.infrastructure import get_db_session
from app.models import Fuel
from app.schemas.fuel_schema import FuelPercentageDB
from app.utils.errors import DatabaseError, handle_database_error

logger = get_logger(__name__)


class FuelRepository:
    def __init__(self, session: Session = Depends(get_db_session)):
        self.session = session

    @handle_database_error
    def get(self, id: str) -> Union[Fuel, DatabaseError]:
        """
        Get an Fuel by id.

        Parameters
        ----------
        `id` : str
            The id of the fuel to get

        Returns
        -------
        `Union[Fuel, DatabaseError]`
            The fuel if found, otherwise an DatabaseError
        """
        try:
            statement = select(Fuel).where(Fuel.id == id)
            return self.session.exec(statement).first()
        except Exception as err:
            logger.error(f"Error getting Fuel, Error: {err}")
            raise err

    @handle_database_error
    def get_all(self) -> Union[list[Fuel], DatabaseError]:
        """
        Get all Fuels.

        Returns
        -------
        `Union[list[Fuel], DatabaseError]`
            A list of fuels if found, otherwise an DatabaseError
        """
        statement = select(Fuel)
        try:
            return self.session.exec(statement).fetchall()
        except Exception as err:
            logger.error(f"Error while fetching all Fuels, error: {err}")
            raise err

    @handle_database_error
    def create(self, fuel: Fuel) -> Union[Fuel, DatabaseError]:
        """
        Create a fuel

        Parameters
        ----------
        `fuel` : Fuel
            The fuel to create

        Returns
        -------
        `Union[Fuel, DatabaseError]`
            The created Fuel if successful, otherwise an DatabaseError
        """

        try:
            self.session.add(fuel)
            self.session.commit()
            self.session.refresh(fuel)
            return fuel
        except Exception as err:
            logger.error(f"Error while creating Fuel, error: {err}")
            self.session.rollback()
            raise err

    @handle_database_error
    def bulk_create(self, fuels: list[Fuel]) -> Union[bool, DatabaseError]:
        """
        Create multiple fuels

        Parameters
        ----------
        `fuels` : list[Fuel]
            The Fuels to create

        Returns
        -------
        `Union[bool, DatabaseError]`
            True if successful, otherwise an DatabaseError
        """

        try:
            self.session.add_all(fuels)
            self.session.commit()
            return True
        except Exception as err:
            logger.error(f"Error while creating Fuels, error: {err}")
            self.session.rollback()
            raise err

    @handle_database_error
    def update(self, fuel: Fuel) -> Union[Fuel, DatabaseError]:
        try:
            self.session.add(fuel)
            self.session.commit()
            self.session.refresh(fuel)
        except Exception as err:
            logger.error(f"Error while updating Fuel, error: {err}")
            self.session.rollback()
            raise err
        return fuel

    @handle_database_error
    def delete(self, fuel: Fuel) -> Union[bool, DatabaseError]:
        try:
            self.session.delete(fuel)
            self.session.commit()
            return True
        except Exception as err:
            logger.error(f"Error while deleting Fuel, error: {err}")
            self.session.rollback()
            raise err

    @handle_database_error
    def get_consumed_fuel_percentage_by_year(
        self, year: int
    ) -> Union[int, DatabaseError]:
        subquery = (
            select(func.sum(Fuel.quantity).label("total"))
            .where(
                Fuel.datetime >= f"{year}-01-01 00:00:00",
                Fuel.datetime <= f"{year}-12-31 23:59:59",
            )
            .subquery()
        )

        statement = (
            select(
                Fuel.fuel_type,
                (func.sum(Fuel.quantity) * 100.0 / subquery.c.total).label(
                    "percentage"
                ),
            )
            .join(subquery, True)
            .where(
                Fuel.datetime >= f"{year}-01-01 00:00:00",
                Fuel.datetime <= f"{year}-12-31 23:59:59",
            )
            .group_by(Fuel.fuel_type, subquery.c.total)
        )

        try:
            result: list[FuelPercentageDB] = self.session.exec(
                statement
            ).fetchall()
        except Exception as err:
            logger.error(
                f"Error while fetching consumed fuel by year and fuel type, error: {err}"
            )
            raise err

        if not result:
            return {
                FuelType.COMBUSTIBLE_ADMINISTRATIVO: 0,
                FuelType.COMBUSTIBLE_INDIRECTO_DE_PROVEEDOR: 0,
                FuelType.COMBUSTIBLE_DE_LOGISTICA: 0,
            }

        response = {}
        for row in result:
            response[row.fuel_type] = round((row.percentage / 100), 2)

        return response

    @handle_database_error
    def get_average_monthly_consumption(
        self, year: int
    ) -> Union[int, DatabaseError]:
        statement = select(
            func.avg(Fuel.quantity).label("avg_monthly_consumption"),
        ).where(
            Fuel.datetime >= f"{year}-01-01 00:00:00",
            Fuel.datetime <= f"{year}-12-31 23:59:59",
        )

        try:
            result = self.session.exec(statement).first()
        except Exception as err:
            logger.error(
                f"Error while fetching consumed fuel by year and fuel type, error: {err}"
            )
            raise err
        return result

    @handle_database_error
    def get_most_impactful_emission_type(self, year: int):
        subquery = (
            select(func.sum(Fuel.quantity).label("total"))
            .where(
                Fuel.datetime >= f"{year}-01-01 00:00:00",
                Fuel.datetime <= f"{year}-12-31 23:59:59",
            )
            .subquery()
        )

        statement = (
            select(
                Fuel.emission_type,
                (func.sum(Fuel.quantity) * 100.0 / subquery.c.total).label(
                    "percentage"
                ),
            )
            .join(subquery, True)
            .where(
                Fuel.datetime >= f"{year}-01-01 00:00:00",
                Fuel.datetime <= f"{year}-12-31 23:59:59",
            )
            .group_by(Fuel.emission_type, subquery.c.total)
        )

        try:
            result = self.session.exec(statement).fetchall()
        except Exception as err:
            logger.error(
                f"Error while fetching consumed fuel by year and fuel type, error: {err}"
            )
            raise err

        if not result:
            return {
                EmissionType.EMISIONES_DIRECTAS: 0,
                EmissionType.EMISIONES_INDIRECTAS: 0,
                EmissionType.OTRAS_EMISIONES_INDIRECTAS: 0,
            }

        response = {}
        for row in result:
            response[row.emission_type] = round((row.percentage / 100), 2)

        return response

    @handle_database_error
    def get_fuel_sum_by_year(
        self, year: int
    ) -> Union[Optional[float], DatabaseError]:
        statement = select(
            func.sum(Fuel.quantity).label("total"),
        ).where(
            Fuel.datetime >= f"{year}-01-01 00:00:00",
            Fuel.datetime <= f"{year}-12-31 23:59:59",
        )

        try:
            result = self.session.exec(statement).first()
        except Exception as err:
            logger.error(
                f"Error while fetching consumed fuel by year and fuel type, error: {err}"
            )
            raise err

        return result

    @handle_database_error
    def get_min_and_max_fuel_by_year(
        self, year: int
    ) -> Union[dict[str, float], DatabaseError]:
        # Get the moth with the lowest consumption
        lowest_fuel_month = (
            select(
                func.date_trunc("month", Fuel.datetime).label("month"),
                func.sum(Fuel.quantity).label("total_quantity"),
            )
            .where(
                Fuel.datetime >= f"{year}-01-01 00:00:00",
                Fuel.datetime <= f"{year}-12-31 23:59:59",
            )
            .group_by("month")
            .order_by(column("total_quantity"))
            .limit(1)
        )

        try:
            lowest_result = self.session.exec(lowest_fuel_month).first()
        except Exception as err:
            logger.error(
                f"Error while fetching consumed fuel by year and fuel type, error: {err}"
            )
            raise err

        highest_fuel_month = (
            select(
                func.date_trunc("month", Fuel.datetime).label("month"),
                func.sum(Fuel.quantity).label("total_quantity"),
            )
            .where(
                Fuel.datetime >= f"{year}-01-01 00:00:00",
                Fuel.datetime <= f"{year}-12-31 23:59:59",
            )
            .group_by("month")
            .order_by(column("total_quantity").desc())
            .limit(1)
        )

        try:
            highest_result = self.session.exec(highest_fuel_month).first()
        except Exception as err:
            logger.error(
                f"Error while fetching consumed fuel by year and fuel type, error: {err}"
            )
            raise err

        if not lowest_result or not highest_result:
            return None
        return {
            "lowest": lowest_result.month.strftime("%B"),
            "highest": highest_result.month.strftime("%B"),
        }
