"""
Module containing repositories that the Actions use to persist data or to retrieve it
"""
from typing import Dict, Any, List

from pydantic import BaseModel
from sqlalchemy import Column, Integer, String

from lilly.repositories import Repository
from lilly.datasources import DataSource

from .datasources import Base, NamesDb
from .dtos import NameRecordDTO


class Name(Base):
    __tablename__ = "names"
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)


class NamesRepository(Repository):
    """Repository for saving and retrieving random names"""
    _names_db = NamesDb()

    def _to_output_dto(self, record: Any) -> BaseModel:
        return NameRecordDTO.from_orm(record)

    @property
    def _datasource(self) -> DataSource:
        return self._names_db

    def _get_one(self, datasource_connection: Any, record_id: Any, **kwargs) -> Any:
        return datasource_connection.query(Name).get(record_id)

    def _get_many(self, datasource_connection: Any, skip: int, limit: int, filters: Dict[Any, Any], **kwargs) -> List[
        Any]:
        return datasource_connection.query(Name).filter_by(**filters).offset(skip).limit(limit).all()

    def _create_one(self, datasource_connection: Any, record: Any, **kwargs) -> Any:
        record = Name(**record)
        datasource_connection.add(record)
        datasource_connection.commit()
        return record

    def _create_many(self, datasource_connection: Any, records: List[Any], **kwargs) -> List[Any]:
        record_objects = [Name(**record) for record in records]
        datasource_connection.bulk_save_objects(record_objects)
        return record_objects

    def _update_one(self, datasource_connection: Any, record_id: Any, new_record: Any, **kwargs) -> Any:
        record = datasource_connection.query(Name).get(record_id)
        if record is None:
            raise KeyError(f"record with id: {record_id} not found")

        for field, value in new_record.items():
            setattr(record, field, value)

        datasource_connection.add(record)
        datasource_connection.commit()
        return record

    def _update_many(self, datasource_connection: Any, new_record: Any, filters: Dict[Any, Any], **kwargs) -> Any:
        pass

    def _remove_one(self, datasource_connection: Any, record_id: Any, **kwargs) -> Any:
        record = datasource_connection.query(Name).get(record_id)
        if record is None:
            raise KeyError(f"record with id: {record_id} not found")
        datasource_connection.delete(record)
        datasource_connection.commit()
        return record

    def _remove_many(self, datasource_connection: Any, filters: Dict[Any, Any], **kwargs) -> Any:
        pass
