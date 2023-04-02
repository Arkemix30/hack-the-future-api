# Python Imports
from typing import Union

# Third Party Imports
from fastapi import Depends
from sqlalchemy import func
from sqlmodel import Session, select

# Local Imports
from app.core import get_logger
from app.definitions import RoadtripGroupType
from app.infrastructure import get_db_session
from app.models import Roadtrip
from app.schemas.roadtrip_schema import RoadtripPercentageDB
from app.utils.errors import DatabaseError, handle_database_error

logger = get_logger(__name__)


class RoadtripRepository:
    def __init__(self, session: Session = Depends(get_db_session)):
        self.session = session

    @handle_database_error
    def get(self, id: str) -> Union[Roadtrip, DatabaseError]:
        """
        Get an Roadtrip by id.

        Parameters
        ----------
        `id` : str
            The id of the roadtrip to get

        Returns
        -------
        `Union[Roadtrip, DatabaseError]`
            The roadtrip if found, otherwise an DatabaseError
        """
        try:
            statement = select(Roadtrip).where(Roadtrip.id == id)
            return self.session.exec(statement).first()
        except Exception as err:
            logger.error(f"Error getting Roadtrip, Error: {err}")
            raise err

    @handle_database_error
    def get_all(self) -> Union[list[Roadtrip], DatabaseError]:
        """
        Get all Roadtrips.

        Returns
        -------
        `Union[list[Roadtrip], DatabaseError]`
            A list of roadtrips if found, otherwise an DatabaseError
        """
        statement = select(Roadtrip)
        try:
            return self.session.exec(statement).fetchall()
        except Exception as err:
            logger.error(f"Error while fetching all Roadtrips, error: {err}")
            raise err

    @handle_database_error
    def create(self, roadtrip: Roadtrip) -> Union[Roadtrip, DatabaseError]:
        """
        Create a roadtrip

        Parameters
        ----------
        `roadtrip` : Roadtrip
            The roadtrip to create

        Returns
        -------
        `Union[Roadtrip, DatabaseError]`
            The created Roadtrip if successful, otherwise an DatabaseError
        """

        try:
            self.session.add(roadtrip)
            self.session.commit()
            self.session.refresh(roadtrip)
            return roadtrip
        except Exception as err:
            logger.error(f"Error while creating Roadtrip, error: {err}")
            self.session.rollback()
            raise err

    @handle_database_error
    def bulk_create(
        self, roadtrips: list[Roadtrip]
    ) -> Union[bool, DatabaseError]:
        """
        Create multiple roadtrips

        Parameters
        ----------
        `roadtrips` : list[Roadtrip]
            The Roadtrips to create

        Returns
        -------
        `Union[bool, DatabaseError]`
            True if successful, otherwise an DatabaseError
        """

        try:
            self.session.add_all(roadtrips)
            self.session.commit()
            return True
        except Exception as err:
            logger.error(f"Error while creating Roadtrips, error: {err}")
            self.session.rollback()
            raise err

    @handle_database_error
    def update(self, roadtrip: Roadtrip) -> Union[Roadtrip, DatabaseError]:
        try:
            self.session.add(roadtrip)
            self.session.commit()
            self.session.refresh(roadtrip)
        except Exception as err:
            logger.error(f"Error while updating Roadtrip, error: {err}")
            self.session.rollback()
            raise err
        return roadtrip

    @handle_database_error
    def delete(self, roadtrip: Roadtrip) -> Union[bool, DatabaseError]:
        try:
            self.session.delete(roadtrip)
            self.session.commit()
            return True
        except Exception as err:
            logger.error(f"Error while deleting Roadtrip, error: {err}")
            self.session.rollback()
            raise err

    @handle_database_error
    def get_average_monthly_comparative_percentage(
        self, year: int
    ) -> Union[float, DatabaseError]:
        """
        Get the average monthly comparative percentage for a location

        Parameters
        ----------
        `location` : str
            The location to get the average monthly comparative percentage for

        Returns
        -------
        `Union[float, DatabaseError]`
            The average monthly comparative percentage if successful, otherwise an DatabaseError
        """
        statement = (
            select(
                Roadtrip.group, (func.sum(Roadtrip.quantity) / 12).label("sum")
            )
            .where(Roadtrip.datetime >= f"{year}-01-01")
            .where(Roadtrip.datetime <= f"{year}-12-31")
            .group_by(Roadtrip.group)
        )

        try:
            result: list[RoadtripPercentageDB] = self.session.exec(
                statement
            ).fetchall()
        except Exception as err:
            logger.error(
                f"Error while fetching consumed fuel by year and fuel type, error: {err}"
            )
            raise err

        if not result:
            return {
                RoadtripGroupType.EQUIPO_ADMINISTRATIVO: 0,
                RoadtripGroupType.EQUIPO_DE_VENTAS: 0,
            }

        response = {}
        for row in result:
            response[row.group] = row.sum

        return response
