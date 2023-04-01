# Python Imports
from typing import Union

# Third Party Imports
from fastapi import Depends
from sqlmodel import Session, select

# Local Imports
from app.core import get_logger
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
