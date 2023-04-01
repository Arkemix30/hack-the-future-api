# Python Imports
from typing import Union

# Third Party Imports
from fastapi import Depends
from sqlalchemy import func
from sqlmodel import Session, select

# Local Imports
from app.core import get_logger
from app.definitions.general import EnergyLocation
from app.infrastructure import get_db_session
from app.models import Energy
from app.utils.errors import DatabaseError, handle_database_error

logger = get_logger(__name__)


class EnergyRepository:
    def __init__(self, session: Session = Depends(get_db_session)):
        self.session = session

    @handle_database_error
    def get(self, id: str) -> Union[Energy, DatabaseError]:
        """
        Get an Energy by id.

        Parameters
        ----------
        `id` : str
            The id of the energy to get

        Returns
        -------
        `Union[Energy, DatabaseError]`
            The energy if found, otherwise an DatabaseError
        """
        try:
            statement = select(Energy).where(Energy.id == id)
            return self.session.exec(statement).first()
        except Exception as err:
            logger.error(f"Error getting Energy, Error: {err}")
            raise err

    @handle_database_error
    def get_all(self) -> Union[list[Energy], DatabaseError]:
        """
        Get all Energys.

        Returns
        -------
        `Union[list[Energy], DatabaseError]`
            A list of energys if found, otherwise an DatabaseError
        """
        statement = select(Energy)
        try:
            return self.session.exec(statement).fetchall()
        except Exception as err:
            logger.error(f"Error while fetching all Energys, error: {err}")
            raise err

    @handle_database_error
    def create(self, energy: Energy) -> Union[Energy, DatabaseError]:
        """
        Create a energy

        Parameters
        ----------
        `energy` : Energy
            The energy to create

        Returns
        -------
        `Union[Energy, DatabaseError]`
            The created Energy if successful, otherwise an DatabaseError
        """

        try:
            self.session.add(energy)
            self.session.commit()
            self.session.refresh(energy)
            return energy
        except Exception as err:
            logger.error(f"Error while creating Energy, error: {err}")
            self.session.rollback()
            raise err

    @handle_database_error
    def bulk_create(self, energys: list[Energy]) -> Union[bool, DatabaseError]:
        """
        Create multiple energys

        Parameters
        ----------
        `energys` : list[Energy]
            The Energys to create

        Returns
        -------
        `Union[bool, DatabaseError]`
            True if successful, otherwise an DatabaseError
        """

        try:
            self.session.add_all(energys)
            self.session.commit()
            return True
        except Exception as err:
            logger.error(f"Error while creating Energys, error: {err}")
            self.session.rollback()
            raise err

    @handle_database_error
    def update(self, energy: Energy) -> Union[Energy, DatabaseError]:
        try:
            self.session.add(energy)
            self.session.commit()
            self.session.refresh(energy)
        except Exception as err:
            logger.error(f"Error while updating Energy, error: {err}")
            self.session.rollback()
            raise err
        return energy

    @handle_database_error
    def delete(self, energy: Energy) -> Union[bool, DatabaseError]:
        try:
            self.session.delete(energy)
            self.session.commit()
            return True
        except Exception as err:
            logger.error(f"Error while deleting Energy, error: {err}")
            self.session.rollback()
            raise err

    @handle_database_error
    def get_average_monthly_by_location_and_year(
        self,
        year: int,
        location: EnergyLocation,
    ) -> Union[list[Energy], DatabaseError]:
        """
        Get the average monthly energy consumption for a location and year.

        Parameters
        ----------
        `location` : str
            The location to get the average monthly energy consumption for
        `year` : int
            The year to get the average monthly energy consumption for

        Returns
        -------
        `Union[list[Energy], DatabaseError]`
            A list of energys if found, otherwise an DatabaseError
        """
        statement = (
            select(
                func.date_trunc("month", Energy.datetime).label("month"),
                func.avg(Energy.quantity).label("avg_monthly_consumption"),
            )
            .where(
                Energy.location == location,
                Energy.datetime >= f"{year}-01-01 00:00:00",
                Energy.datetime <= f"{year}-12-31 23:59:59",
            )
            .group_by("month")
            .order_by("month")
        )

        try:
            result = self.session.exec(statement).fetchall()
            result = [dict(row) for row in result]
        except Exception as err:
            logger.error(
                f"Error while fetching consumed energy by year and energy type, error: {err}"
            )
            raise err

        if not result:
            return {str(i): 0 for i in range(1, 13)}

        # Convert datetime to string
        response = {}
        for row in result:
            response[int(row["month"].strftime("%m"))] = round(
                row["avg_monthly_consumption"], 2
            )

        # Fill the missing months with 0
        for month in range(1, 13):
            if month not in response:
                response[month] = 0

        return response
