"""
Module defines the Repository Base class which is to be inherited by all repository classes
Repositories are responsible for data preparation when saving to a data source or retireiving data from
a data source
"""
from abc import abstractmethod
from typing import Type, Any, Dict, List

from pydantic import BaseModel

from lilly.datasources import DataSource


class Repository:
    """
    The Repository Base class which is to be inherited by all repository classes
    Repositories are responsible for data preparation when saving to a data source or retrieving data from
    a data source

    e.g. They will do a `get_many` or `create_one` etc.
    """

    @abstractmethod
    def _get_one(self, datasource_connection: Any, record_id: Any, **kwargs) -> Any:
        """method to get one record of id `record_id`. This should be overridden"""
        raise NotImplementedError()

    def get_one(self, record_id: Any, **kwargs) -> BaseModel:
        """method to get one record of id `record_id`"""
        connection = self._get_connection()
        record = self._get_one(connection, record_id=record_id, **kwargs)
        return self._to_output_dto(record)

    @abstractmethod
    def _get_many(self, datasource_connection: Any, skip: int, limit: int, filters: Dict[Any, Any], **kwargs) -> List[
        Any]:
        """method to get many records that fulfil the `filters`. This should be overridden"""
        raise NotImplementedError()

    def get_many(self, skip: int, limit: int, filters: Dict[Any, Any], **kwargs) -> List[BaseModel]:
        """method to get many records that fulfil the `filters`"""
        connection = self._get_connection()
        records = self._get_many(connection, skip=skip, limit=limit, filters=filters, **kwargs)
        return [self._to_output_dto(record) for record in records]

    @abstractmethod
    def _create_one(self, datasource_connection: Any, record: Any, **kwargs) -> Any:
        """method to create one record. This should be overridden. Returns the created record."""
        raise NotImplementedError()

    def create_one(self, record: Any, **kwargs) -> BaseModel:
        """method to create one record, returning the created record"""
        connection = self._get_connection()
        record = self._create_one(connection, record=record, **kwargs)
        return self._to_output_dto(record)

    @abstractmethod
    def _create_many(self, datasource_connection: Any, records: List[Any], **kwargs) -> List[Any]:
        """method to create many records. This should be overridden. Returns the created records."""
        raise NotImplementedError()

    def create_many(self, records: List[Any], **kwargs) -> List[BaseModel]:
        """method to create many records. Returning the created records."""
        connection = self._get_connection()
        records = self._create_many(connection, records=records, **kwargs)
        return [self._to_output_dto(record) for record in records]

    @abstractmethod
    def _update_one(self, datasource_connection: Any, record_id: Any, new_record: Any, **kwargs) -> Any:
        """
        method to update one record of id `record_id`. This should be overridden
        It should return the updated record.
        """
        raise NotImplementedError()

    def update_one(self, record_id: Any, new_record: Any, **kwargs) -> BaseModel:
        """method to update one record of id `record_id`. Returning the updated record."""
        connection = self._get_connection()
        record = self._update_one(connection, record_id=record_id, new_record=new_record, **kwargs)
        return self._to_output_dto(record)

    @abstractmethod
    def _update_many(self, datasource_connection: Any, new_record: Any, filters: Dict[Any, Any], **kwargs) -> List[Any]:
        """
        method to update many records that fulfil the `filters`. This should be overridden
        It should return the updated records.
        """
        raise NotImplementedError()

    def update_many(self, new_record: Any, filters: Dict[Any, Any], **kwargs) -> List[BaseModel]:
        """method to update many records that fulfil the `filters`. Returning the updated records"""
        connection = self._get_connection()
        records = self._update_many(connection, new_record=new_record, filters=filters, **kwargs)
        return [self._to_output_dto(record) for record in records]

    @abstractmethod
    def _remove_one(self, datasource_connection: Any, record_id: Any, **kwargs) -> Any:
        """
        method to remove one record of id `record_id`. This should be overridden
        It should return the removed record.
        """
        raise NotImplementedError()

    def remove_one(self, record_id: Any, **kwargs) -> BaseModel:
        """
        method to remove one record of id `record_id`, returning the deleted record
        """
        connection = self._get_connection()
        record = self._remove_one(connection, record_id=record_id, **kwargs)
        return self._to_output_dto(record)

    @abstractmethod
    def _remove_many(self, datasource_connection: Any, filters: Dict[Any, Any], **kwargs) -> List[Any]:
        """
        method to remove many records that fulfil the `filters`. This should be overridden
        It should return the removed records.
        """
        raise NotImplementedError()

    def remove_many(self, filters: Dict[Any, Any], **kwargs) -> List[BaseModel]:
        """method to remove many records that fulfil the `filters`, returning the deleted records"""
        connection = self._get_connection()
        records = self._remove_many(connection, filters=filters, **kwargs)
        return [self._to_output_dto(record) for record in records]

    @property
    @abstractmethod
    def _datasource(self) -> DataSource:
        """Gets the datasource to be used in the repository"""
        raise NotImplementedError()

    @abstractmethod
    def _to_output_dto(self, record: Any) -> BaseModel:
        """Converts the given data into the appropriate data transfer object"""
        raise NotImplementedError()

    def _get_connection(self) -> Any:
        """Returns the connection to the data source"""
        return self._datasource.connect()
