from datetime import datetime as dt
from typing import Optional

from sqlalchemy import func
from sqlalchemy.ext.declarative import declared_attr
from sqlmodel import Column, DateTime, Field, SQLModel

from app.utils.entities_utils import model_class_name_to_lower


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
