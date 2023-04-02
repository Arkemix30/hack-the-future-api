# Python Imports
from typing import Union

# Third Party Imports
from fastapi import Depends
from sqlalchemy import func
from sqlmodel import Session, select

# Local Imports
from app.core import get_logger
from app.definitions import OilType
from app.infrastructure import get_db_session
from app.models import Oil
from app.utils.errors import DatabaseError, handle_database_error

logger = get_logger(__name__)


class OilRepository:
    def __init__(self, session: Session = Depends(get_db_session)):
        self.session = session

    @handle_database_error
    def get(self, id: str) -> Union[Oil, DatabaseError]:
        """
        Get an Oil by id.

        Parameters
        ----------
        `id` : str
            The id of the oil to get

        Returns
        -------
        `Union[Oil, DatabaseError]`
            The oil if found, otherwise an DatabaseError
        """
        try:
            statement = select(Oil).where(Oil.id == id)
            return self.session.exec(statement).first()
        except Exception as err:
            logger.error(f"Error getting Oil, Error: {err}")
            raise err

    @handle_database_error
    def get_all(self) -> Union[list[Oil], DatabaseError]:
        """
        Get all Oils.

        Returns
        -------
        `Union[list[Oil], DatabaseError]`
            A list of oils if found, otherwise an DatabaseError
        """
        statement = select(Oil)
        try:
            return self.session.exec(statement).fetchall()
        except Exception as err:
            logger.error(f"Error while fetching all Oils, error: {err}")
            raise err

    @handle_database_error
    def create(self, oil: Oil) -> Union[Oil, DatabaseError]:
        """
        Create a oil

        Parameters
        ----------
        `oil` : Oil
            The oil to create

        Returns
        -------
        `Union[Oil, DatabaseError]`
            The created Oil if successful, otherwise an DatabaseError
        """

        try:
            self.session.add(oil)
            self.session.commit()
            self.session.refresh(oil)
            return oil
        except Exception as err:
            logger.error(f"Error while creating Oil, error: {err}")
            self.session.rollback()
            raise err

    @handle_database_error
    def bulk_create(self, oils: list[Oil]) -> Union[bool, DatabaseError]:
        """
        Create multiple oils

        Parameters
        ----------
        `oils` : list[Oil]
            The Oils to create

        Returns
        -------
        `Union[bool, DatabaseError]`
            True if successful, otherwise an DatabaseError
        """

        try:
            self.session.add_all(oils)
            self.session.commit()
            return True
        except Exception as err:
            logger.error(f"Error while creating Oils, error: {err}")
            self.session.rollback()
            raise err

    @handle_database_error
    def update(self, oil: Oil) -> Union[Oil, DatabaseError]:
        try:
            self.session.add(oil)
            self.session.commit()
            self.session.refresh(oil)
        except Exception as err:
            logger.error(f"Error while updating Oil, error: {err}")
            self.session.rollback()
            raise err
        return oil

    @handle_database_error
    def delete(self, oil: Oil) -> Union[bool, DatabaseError]:
        try:
            self.session.delete(oil)
            self.session.commit()
            return True
        except Exception as err:
            logger.error(f"Error while deleting Oil, error: {err}")
            self.session.rollback()
            raise err

    @handle_database_error
    def get_monthly_consumption_by_type_and_year(
        self, year: int, oil_type: OilType
    ) -> Union[int, DatabaseError]:
        """
        Get the monthly consumption of a oil type for a given year

        Parameters
        ----------
        `year` : int
            The year to get the monthly consumption for
        `oil_type` : OilType
            The type of oil to get the monthly consumption for

        Returns
        -------
        `Union[int, DatabaseError]`
            The monthly consumption if found, otherwise an DatabaseError
        """
        try:
            statement = (
                select(
                    func.date_trunc("month", Oil.datetime).label("month"),
                    func.sum(Oil.quantity).label("quantity"),
                )
                .where(
                    Oil.oil_type == oil_type,
                    Oil.datetime >= f"{year}-01-01 00:00:00",
                    Oil.datetime <= f"{year}-12-31 23:59:59",
                )
                .group_by("month")
                .order_by("month")
            )
            result = self.session.exec(statement).fetchall()
            result = [dict(row) for row in result]
        except Exception as err:
            logger.error(f"Error getting monthly consumption, Error: {err}")
            raise err

        if not result:
            return {str(i): 0 for i in range(1, 13)}

        response = {}
        for row in result:
            response[int(row["month"].strftime("%m"))] = row["quantity"]

        # Fill in missing months
        for i in range(1, 13):
            if i not in response:
                response[i] = 0

        return response

    @handle_database_error
    def get_min_loss_by_type_and_year(
        self, year: int, oil_type: OilType
    ) -> Union[str, DatabaseError]:
        """
        Get the minimum loss of a oil type for a given year

        Parameters
        ----------
        `year` : int
            The year to get the minimum loss for
        `oil_type` : OilType
            The type of oil to get the minimum loss for

        Returns
        -------
        `Union[str, DatabaseError]`
            The minimum loss if found, otherwise an DatabaseError
        """
        try:
            statement = (
                select(
                    func.date_trunc("month", Oil.datetime).label("month"),
                    func.min(Oil.quantity).label("quantity"),
                )
                .where(
                    Oil.oil_type == oil_type,
                    Oil.datetime >= f"{year}-01-01 00:00:00",
                    Oil.datetime <= f"{year}-12-31 23:59:59",
                )
                .group_by("month")
                .order_by("month")
            )
            result = self.session.exec(statement).first()
        except Exception as err:
            logger.error(f"Error getting minimum loss, Error: {err}")
            raise err

        if not result:
            return None

        return result.month.strftime("%B")

    @handle_database_error
    def get_average_compsution_for_every_type(
        self, year: int
    ) -> Union[dict[str, int], DatabaseError]:
        """
        Get the average monthly consumption for every oil type for a given year

        Parameters
        ----------
        `year` : int
            The year to get the average monthly consumption for

        Returns
        -------
        `Union[dict[str, int], DatabaseError]`
            The average monthly consumption for every oil type if found, otherwise an DatabaseError
        """

        statement = (
            select(
                Oil.oil_type,
                func.avg(Oil.quantity).label("avg_monthly_consumption"),
            ).where(
                Oil.datetime >= f"{year}-01-01 00:00:00",
                Oil.datetime <= f"{year}-12-31 23:59:59",
            )
        ).group_by(Oil.oil_type)

        try:
            result = self.session.exec(statement).fetchall()
        except Exception as err:
            logger.error(
                f"Error while fetching consumed fuel by year and fuel type, error: {err}"
            )
            raise err

        if not result:
            return {
                OilType.ACEITE: 0,
                OilType.REFRIGERANTE: 0,
            }

        return {
            row.oil_type: round(row.avg_monthly_consumption, 2)
            for row in result
        }
