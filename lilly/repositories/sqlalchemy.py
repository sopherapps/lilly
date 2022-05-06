"""
SQLAlchemyRepository, available for inheritance
"""
from abc import abstractmethod
from typing import Any, Type, Dict, List, Optional

from pydantic import BaseModel
from sqlalchemy.orm import DeclarativeMeta, Session
from sqlalchemy import insert, select, update, delete, text

from .base import Repository
from lilly.datasources import SQLAlchemyDataSource


class SQLAlchemyRepository(Repository):
    """Repository for saving and retrieving random names"""

    @property
    @abstractmethod
    def _model_cls(self) -> Type[DeclarativeMeta]:
        """The SqlAlchemy Declarative model class to be used. It must be a subclass of sqlalchemy.orm.DeclarativeMeta"""
        raise NotImplementedError("an SQLAlchemy declarative model class should be returned")

    @property
    @abstractmethod
    def _dto_cls(self) -> Type[BaseModel]:
        """The Data Transfer Object (DTO) class to output data in. It must be a subclass of pydantic.BaseModel"""
        raise NotImplementedError("A DTO class is required.")

    @property
    @abstractmethod
    def _datasource(self) -> SQLAlchemyDataSource:
        raise NotImplementedError("a datasource that is an SQLAlchemyDataSource needs to be returned from _datasource")

    def _to_output_dto(self, record: Any) -> BaseModel:
        return self._dto_cls.from_orm(record)

    def _get_one(self, datasource_connection: Session, record_id: Any, **kwargs) -> DeclarativeMeta:
        return datasource_connection.query(self._model_cls).get(record_id)

    def create_many(self, records: List[BaseModel], **kwargs) -> List[Any]:
        """
        method to create many records.
        This will always return an empty list as it is quite impossible to return the multiple records inserted
        with their ids

        This should be overridden.

        Arguments:
            records (list[BaseModel]): the records to be created
            **kwargs (Any): any extra key-word arguments you may need to pass in your particular implementation

        Returns:
            list: an empty list when successful
        """
        return super().create_many(records=records, **kwargs)

    def _get_many(self,
                  datasource_connection: Any,
                  *criterion,
                  skip: int = 0,
                  limit: Optional[int] = None,
                  **filters) -> List[DeclarativeMeta]:
        coerced_criteria = self.__coerce_string_criteria(*criterion)

        query = datasource_connection.query(self._model_cls).filter(*coerced_criteria).filter_by(**filters).offset(skip)

        if limit is not None:
            query = query.limit(limit)

        data = query.all()
        return data

    def _create_one(self, datasource_connection: Session, record: BaseModel, **kwargs) -> DeclarativeMeta:
        record = self._model_cls(**record.dict())
        datasource_connection.add(record)
        datasource_connection.commit()
        return record

    def _create_many(self, datasource_connection: Session, records: List[BaseModel], **kwargs) -> List[
        DeclarativeMeta]:
        stmt = insert(self._model_cls)

        datasource_connection.execute(stmt, [record.dict() for record in records])
        datasource_connection.commit()

        # return empty because it is currently quite hard to return the inserted records with their data
        # unless one is to use the inefficient method of multiple calls to session.add()
        return []

    def _update_one(self, datasource_connection: Any, record_id: Any, new_record: BaseModel,
                    **kwargs) -> DeclarativeMeta:
        record = datasource_connection.query(self._model_cls).get(record_id)
        if record is None:
            raise KeyError(f"record with id: {record_id} not found")

        for field, value in iter(new_record):
            setattr(record, field, value)

        datasource_connection.add(record)
        datasource_connection.commit()
        return record

    def _update_many(self, datasource_connection: Session, new_record: BaseModel, *criterion, **filters) -> List[
        DeclarativeMeta]:
        coerced_criteria = self.__coerce_string_criteria(*criterion)
        new_data = new_record.dict()

        stmt = update(self._model_cls).filter(*coerced_criteria).filter_by(**filters).values(new_data) \
            .execution_options(synchronize_session="fetch")

        affected_records = self._get_affected_records(
            datasource_connection, *coerced_criteria, new_data=new_data, **filters)

        datasource_connection.execute(stmt)
        datasource_connection.commit()

        return affected_records

    def _remove_one(self, datasource_connection: Session, record_id: Any, **kwargs) -> DeclarativeMeta:
        record = datasource_connection.query(self._model_cls).get(record_id)
        if record is None:
            raise KeyError(f"record with id: {record_id} not found")
        datasource_connection.delete(record)
        datasource_connection.commit()
        return record

    def _remove_many(self, datasource_connection: Session, *criterion, **filters) -> List[DeclarativeMeta]:
        coerced_criteria = self.__coerce_string_criteria(*criterion)

        stmt = delete(self._model_cls).filter(*coerced_criteria).filter_by(**filters) \
            .execution_options(synchronize_session="fetch")
        affected_records = self._get_affected_records(
            datasource_connection, *coerced_criteria, **filters)

        datasource_connection.execute(stmt)
        datasource_connection.commit()

        return affected_records

    def _get_affected_records(self,
                              datasource_connection: Session,
                              *criterion,
                              new_data: Optional[Dict[str, Any]] = None,
                              **filters):
        """
        Gets the records that are affected by the given criteria and filters,
        and updated them with new data if new_data is set
        """
        affected_records = datasource_connection.execute(
            select(self._model_cls).filter(*criterion).filter_by(**filters)
        ).scalars().all()

        if new_data is not None:
            return [_update_orm_instance(record, new_data=new_data) for record in affected_records]

        return affected_records

    @staticmethod
    def __coerce_string_criteria(*criteria):
        """
        Wraps any string criteria for filtering in a text()

        e.g.::
         "title LIKE '%t'" becomes text("title LIKE '%t'")
        """
        return [text(criterion) if isinstance(criterion, str) else criterion for criterion in criteria]


def _update_orm_instance(orm_instance: DeclarativeMeta, new_data: Dict[str, Any]):
    """Updates the orm instance in place and returns it"""
    for field, value in new_data.items():
        setattr(orm_instance, field, value)
    return orm_instance
