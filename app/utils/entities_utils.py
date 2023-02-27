import re
from datetime import datetime as dt
from typing import Optional

from sqlalchemy import func
from sqlalchemy.ext.declarative import declared_attr
from sqlmodel import Column, DateTime, Field, SQLModel


def model_class_name_to_lower(class_name: str) -> str:
    """
    Convert a model class name to lower case.
    If the class name is like: `"SomethingSomething"`, the function will return `"something_something"`.

    Parameters
    ----------
    `class_name` : str
        The class name to convert.

    Returns
    -------
    `str`
        The class name converted to lower case.
    """

    # Split the class name by capital letters
    class_name_list = re.findall(r"[A-Z][^A-Z]*", class_name)
    # Convert the class name list to lower case
    class_name_list = [name.lower() for name in class_name_list]
    # Join the class name list with an underscore
    class_name = "_".join(class_name_list)
    return class_name


class BaseSQLModel(SQLModel):
    id: Optional[int] = Field(default=None, primary_key=True)

    created_at: Optional[dt] = Field(
        sa_column=Column(
            DateTime(timezone=True), nullable=True, server_default=func.now()
        )
    )
    updated_at: Optional[dt] = Field(
        sa_column=Column(
            DateTime(timezone=True), nullable=True, onupdate=func.now()
        )
    )

    # This is a declarative attribute, it will be used to set the table name
    @declared_attr
    def __tablename__(cls):
        return model_class_name_to_lower(cls.__name__)
