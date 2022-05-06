"""
Module containing repositories that the Actions use to persist data or to retrieve it
"""
from typing import Type

from pydantic import BaseModel
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import DeclarativeMeta

from lilly.repositories import SQLAlchemyRepository
from lilly.datasources import SQLAlchemyDataSource

from .datasources import Base, NamesDb
from .dtos import NameRecordDTO


class Name(Base):
    __tablename__ = "names"
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)


class NamesRepository(SQLAlchemyRepository):
    """Repository for saving and retrieving random names"""
    _names_db = NamesDb()

    @property
    def _model_cls(self) -> Type[DeclarativeMeta]:
        return Name

    @property
    def _dto_cls(self) -> Type[BaseModel]:
        return NameRecordDTO

    @property
    def _datasource(self) -> SQLAlchemyDataSource:
        return self._names_db
