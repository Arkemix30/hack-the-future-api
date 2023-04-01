# Python Imports
from typing import Union

# Third Party Imports
from fastapi import Depends
from sqlmodel import Session, select

# Local Imports
from app.core import get_logger
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
