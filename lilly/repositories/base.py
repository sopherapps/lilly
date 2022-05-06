"""
Module defines the Repository Base class which is to be inherited by all repository classes
Repositories are responsible for data preparation when saving to a data source or retireiving data from
a data source
"""
from abc import abstractmethod
from typing import Any, List, Optional, ContextManager

from pydantic import BaseModel

from lilly.datasources import DataSource


class Repository:
    """
    The Repository Base class which is to be inherited by all repository classes
    Repositories are responsible for data preparation when saving to a data source or retrieving data from
    a data source

        e.g.::

        They will do a `get_many` or `create_one` etc.
    """

    @abstractmethod
    def _get_one(self, datasource_connection: Any, record_id: Any, **kwargs) -> Any:
        """
        method to get one record of id `record_id`.

        This should be overridden

        Arguments:
            datasource_connection (Any): the connection to the data source as got from DataSource.connect()
            record_id (Any): the ID of the record to be retrieved
            **kwargs (Any): any extra key-word arguments you may need to pass in your particular implementation

        Returns:
            Any: the record whose ID is `record_id`
        """
        raise NotImplementedError()

    def get_one(self, record_id: Any, **kwargs) -> BaseModel:
        """
        method to get one record of id `record_id`.

        Arguments:
            record_id (Any): the ID of the record to be retrieved
            **kwargs (Any): any extra key-word arguments you may need to pass in your particular implementation

        Returns:
            BaseModel: the record DTO whose ID is `record_id`
        """
        with self._get_connection() as connection:
            record = self._get_one(connection, record_id=record_id, **kwargs)
            return self._to_output_dto(record)

    @abstractmethod
    def _get_many(self,
                  datasource_connection: Any,
                  *criterion,
                  skip: int = 0,
                  limit: Optional[int] = None,
                  **filters) -> List[
        Any]:
        """
        method to get many records that fulfil the `criterion` and `filters`.

        This should be overridden

        Arguments:
            datasource_connection (Any): the connection to the data source as got from DataSource.connect()
            *criterion (Any): any SQLAlchemy SQL expression object applicable to the WHERE clause of a select.

                e.g.::

                    MyClass.name == 'some name'

                - Multiple criteria may be specified as comma separated; the effect
                  is that they will be joined together using the :func:`.and_`
                - the :func:`.or_` can be also used to combine multiple criterion and passed as a single criterion

            skip (int): the number of records to skip in the query set. Default is `0`
            limit (Optional[int]): the maximum number of records to return. Default is `None`
            **filters (Any): key-word arguments where the key corresponds to the field name on the model
                            in the repository and the argument is the value that field should have

        Returns:
            list[Any]: the records
        """
        raise NotImplementedError()

    def get_many(self, *criterion, skip: int = 0, limit: Optional[int] = None, **filters) -> List[BaseModel]:
        """
        method to get many records that fulfil the `criterion` and `filters`.

        Arguments:
            *criterion (Any): any SQLAlchemy SQL expression object applicable to the WHERE clause of a select.

                e.g.::

                    MyClass.name == 'some name'

                - Multiple criteria may be specified as comma separated; the effect
                  is that they will be joined together using the :func:`.and_`
                - the :func:`.or_` can be also used to combine multiple criterion and passed as a single criterion

            skip (int): the number of records to skip in the query set. Default is `0`
            limit (Optional[int]): the maximum number of records to return. Default is `None`
            **filters (Any): key-word arguments where the key corresponds to the field name on the model
                            in the repository and the argument is the value that field should have

        Returns:
            list[BaseModel]: the records' DTOs
        """
        with self._get_connection() as connection:
            records = self._get_many(connection, skip=skip, limit=limit, *criterion, **filters)
            return [self._to_output_dto(record) for record in records]

    @abstractmethod
    def _create_one(self, datasource_connection: Any, record: BaseModel, **kwargs) -> Any:
        """
        method to create one record.

        This should be overridden

        Arguments:
            datasource_connection (Any): the connection to the data source as got from DataSource.connect()
            record (BaseModel): the record DTO to be created
            **kwargs (Any): any extra key-word arguments you may need to pass in your particular implementation

        Returns:
            Any: the created record
        """
        raise NotImplementedError()

    def create_one(self, record: BaseModel, **kwargs) -> BaseModel:
        """
        method to create one record.

        Arguments:
            record (BaseModel): the record DTO to be created
            **kwargs (Any): any extra key-word arguments you may need to pass in your particular implementation

        Returns:
            BaseModel: the created record DTO
        """
        with self._get_connection() as connection:
            record = self._create_one(connection, record=record, **kwargs)
            return self._to_output_dto(record)

    @abstractmethod
    def _create_many(self, datasource_connection: Any, records: List[BaseModel], **kwargs) -> List[Any]:
        """
        method to create many records.

        This should be overridden.

        Arguments:
            datasource_connection (Any): the connection to the data source as got from DataSource.connect()
            records (list[BaseModel]): the records' DTOs to be created
            **kwargs (Any): any extra key-word arguments you may need to pass in your particular implementation

        Returns:
            list[Any]: the created records
        """
        raise NotImplementedError()

    def create_many(self, records: List[BaseModel], **kwargs) -> List[BaseModel]:
        """
        method to create many records.

        Arguments:
            records (list[BaseModel]): the records' DTOs to be created
            **kwargs (Any): any extra key-word arguments you may need to pass in your particular implementation

        Returns:
            list[BaseModel]: the created records' DTOs
        """
        with self._get_connection() as connection:
            records = self._create_many(connection, records=records, **kwargs)
            return [self._to_output_dto(record) for record in records]

    @abstractmethod
    def _update_one(self, datasource_connection: Any, record_id: Any, new_record: BaseModel, **kwargs) -> Any:
        """
        method to update one record of id `record_id`.

        This should be overridden

        Arguments:
            datasource_connection (Any): the connection to the data source as got from DataSource.connect()
            record_id (Any): the ID of the record to be replaced
            new_record (BaseModel): the record's DTO to replace the old record
            **kwargs (Any): any extra key-word arguments you may need to pass in your particular implementation

        Returns:
            Any: the updated record
        """
        raise NotImplementedError()

    def update_one(self, record_id: Any, new_record: BaseModel, **kwargs) -> BaseModel:
        """
        method to update one record of id `record_id`.

        Arguments:
            record_id (Any): the ID of the record to be replaced
            new_record (BaseModel): the record's DTO to replace the old record
            **kwargs (Any): any extra key-word arguments you may need to pass in your particular implementation

        Returns:
            BaseModel: the updated record's DTO
        """
        with self._get_connection() as connection:
            record = self._update_one(connection, record_id=record_id, new_record=new_record, **kwargs)
            return self._to_output_dto(record)

    @abstractmethod
    def _update_many(self, datasource_connection: Any, new_record: BaseModel, *criterion, **filters) -> List[Any]:
        """
        method to update many records that fulfil the `criterion` and `filters`.

        This should be overridden

        Arguments:
            datasource_connection (Any): the connection to the data source as got from DataSource.connect()
            new_record (BaseModel): the new record's DTO that should replace the records
            *criterion (Any): any SQLAlchemy SQL expression object applicable to the WHERE clause of a select.

                e.g.::

                    MyClass.name == 'some name'

                - Multiple criteria may be specified as comma separated; the effect
                  is that they will be joined together using the :func:`.and_`
                - the :func:`.or_` can be also used to combine multiple criterion and passed as a single criterion

            **filters (Any): key-word arguments where the key corresponds to the field name on the model
                            in the repository and the argument is the value that field should have

        Returns:
            list[Any]: the updated records
        """
        raise NotImplementedError()

    def update_many(self, new_record: BaseModel, *criterion, **filters) -> List[BaseModel]:
        """
        method to update many records that fulfil the `criterion` and `filters`.

        Arguments:
            new_record (BaseModel): the new record's DTO that should replace the records
            *criterion (Any): any SQLAlchemy SQL expression object applicable to the WHERE clause of a select.

                e.g.::

                    MyClass.name == 'some name'

                - Multiple criteria may be specified as comma separated; the effect
                  is that they will be joined together using the :func:`.and_`
                - the :func:`.or_` can be also used to combine multiple criterion and passed as a single criterion

            **filters (Any): key-word arguments where the key corresponds to the field name on the model
                            in the repository and the argument is the value that field should have

        Returns:
            list[BaseModel]: the updated records' DTOs
        """
        with self._get_connection() as connection:
            records = self._update_many(connection, new_record, *criterion, **filters)
            return [self._to_output_dto(record) for record in records]

    @abstractmethod
    def _remove_one(self, datasource_connection: Any, record_id: Any, **kwargs) -> Any:
        """
        method to remove one record of id `record_id`.

        This should be overridden

        Arguments:
            datasource_connection (Any): the connection to the data source as got from DataSource.connect()
            record_id (Any): the ID of the record to be removed
            **kwargs (Any): any extra key-word arguments you may need to pass in your particular implementation

        Returns:
            Any: the removed record
        """
        raise NotImplementedError()

    def remove_one(self, record_id: Any, **kwargs) -> BaseModel:
        """
        method to remove one record of id `record_id`.

        Arguments:
            record_id (Any): the ID of the record to be removed
            **kwargs (Any): any extra key-word arguments you may need to pass in your particular implementation

        Returns:
            Any: the removed record's DTO
        """
        with self._get_connection() as connection:
            record = self._remove_one(connection, record_id=record_id, **kwargs)
            return self._to_output_dto(record)

    @abstractmethod
    def _remove_many(self, datasource_connection: Any, *criterion, **filters) -> List[Any]:
        """
        method to remove many records that fulfil the `criterion` and `filters`.

        This should be overridden.

        Arguments:
            datasource_connection (Any): the connection to the data source as got from DataSource.connect()
            *criterion (Any): any SQLAlchemy SQL expression object applicable to the WHERE clause of a select.

                e.g.::

                    MyClass.name == 'some name'

                - Multiple criteria may be specified as comma separated; the effect
                  is that they will be joined together using the :func:`.and_`
                - the :func:`.or_` can be also used to combine multiple criterion and passed as a single criterion

            **filters (Any): key-word arguments where the key corresponds to the field name on the model
                            in the repository and the argument is the value that field should have

        Returns:
            list[Any]: the removed records
        """
        raise NotImplementedError()

    def remove_many(self, *criterion, **filters) -> List[BaseModel]:
        """
        method to remove many records that fulfil the `criterion` and `filters`.

        Arguments:
            *criterion (Any): any SQLAlchemy SQL expression object applicable to the WHERE clause of a select.

                e.g.::

                    MyClass.name == 'some name'

                - Multiple criteria may be specified as comma separated; the effect
                  is that they will be joined together using the :func:`.and_`
                - the :func:`.or_` can be also used to combine multiple criterion and passed as a single criterion

            **filters (Any): key-word arguments where the key corresponds to the field name on the model
                            in the repository and the argument is the value that field should have

        Returns:
            list[BaseModel]: the removed records' DTOs
        """
        with self._get_connection() as connection:
            records = self._remove_many(connection, *criterion, **filters)
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

    def _get_connection(self) -> ContextManager:
        """
        Returns the context manager to the connection to the data source by calling `DataSource.connect()`
        """
        return self._datasource.connect()
