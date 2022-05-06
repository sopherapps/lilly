"""Module contains CRUD related actions"""
from abc import abstractmethod
from typing import Any, List, Optional

from pydantic import BaseModel

from .base import Action
from ..repositories import Repository


class CreateOneAction(Action):
    """Action to create one item in a repository"""

    def __init__(self, record: BaseModel, **kwargs):
        """
        Arguments:
            record (BaseModel): the record to be created
            **kwargs (Any): any extra key-word arguments you may need to pass in your particular implementation
        """
        self._record = record
        self._options = kwargs

    @property
    @abstractmethod
    def _repository(self) -> Repository:
        """The repository that this action connects to when creating the record"""
        raise NotImplementedError("_repository should be implemented")

    def run(self) -> BaseModel:
        """
        Runs the Action

        Returns:
            BaseModel: the record's DTO
        """
        return self._repository.create_one(self._record, **self._options)


class CreateManyAction(Action):
    """Action to create many items in the associated repository"""

    def __init__(self, records: List[BaseModel], **kwargs):
        """
        Arguments:
            records (list[BaseModel]): the records' DTO to be created
            **kwargs (Any): any extra key-word arguments you may need to pass in your particular implementation
        """
        self._records = records
        self._options = kwargs

    @property
    @abstractmethod
    def _repository(self) -> Repository:
        """The repository that this action connects to when creating the records"""
        raise NotImplementedError("_repository should be implemented")

    def run(self) -> List[BaseModel]:
        """
        Runs the Action

        Returns:
            list[BaseModel]: the records' DTOs
        """
        return self._repository.create_many(self._records, **self._options)


class ReadOneAction(Action):
    """Action to read one from the associated repository"""

    def __init__(self, record_id: Any, **kwargs):
        """
        Arguments:
            record_id (Any): the ID of the record to be retrieved
            **kwargs (Any): any extra key-word arguments you may need to pass in your particular implementation
        """
        self._record_id = record_id
        self._options = kwargs

    @property
    @abstractmethod
    def _repository(self) -> Repository:
        """The repository that this action connects to when reading the record"""
        raise NotImplementedError("_repository should be implemented")

    def run(self) -> BaseModel:
        """
        Runs the Action

        Returns:
            BaseModel: the record's DTO
        """
        return self._repository.get_one(self._record_id, **self._options)


class ReadManyAction(Action):
    """Action to read many from the associated repository"""

    def __init__(self, *criterion, skip: int = 0, limit: Optional[int] = None, **filters):
        """
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
        """
        self._criterion = criterion
        self._filters = filters
        self._limit = limit
        self._skip = skip

    @property
    @abstractmethod
    def _repository(self) -> Repository:
        """The repository that this action connects to when reading the records"""
        raise NotImplementedError("_repository should be implemented")

    def run(self) -> List[BaseModel]:
        """
        Runs the Action

        Returns:
            list[BaseModel]: the records' DTOs
        """
        return self._repository.get_many(*self._criterion, skip=self._skip, limit=self._limit, **self._filters)


class UpdateOneAction(Action):
    """Action to update one record in the associated repository"""

    def __init__(self, record_id: Any, new_record: BaseModel, **kwargs):
        """
        Arguments:
            record_id (Any): the ID of the record to be replaced
            new_record (BaseModel): the record's DTO to replace the old record
            **kwargs (Any): any extra key-word arguments you may need to pass in your particular implementation
        """
        self._record_id = record_id
        self._new_record = new_record
        self._options = kwargs

    @property
    @abstractmethod
    def _repository(self) -> Repository:
        """The repository that this action connects to when updating the record"""
        raise NotImplementedError("_repository should be implemented")

    def run(self) -> BaseModel:
        """
        Runs the Action

        Returns:
            BaseModel: the updated record's DTO
        """
        return self._repository.update_one(self._record_id, self._new_record, **self._options)


class UpdateManyAction(Action):
    """Action to update many records in the associated repository"""

    def __init__(self, new_record: BaseModel, *criterion, **filters):
        """
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
        """
        self._new_record = new_record
        self._criterion = criterion
        self._filters = filters

    @property
    @abstractmethod
    def _repository(self) -> Repository:
        """The repository that this action connects to when updating the records"""
        raise NotImplementedError("_repository should be implemented")

    def run(self) -> List[BaseModel]:
        """
        Runs the Action

        Returns:
            list[BaseModel]: the updated records' DTOs
        """
        return self._repository.update_many(self._new_record, *self._criterion, **self._filters)


class DeleteOneAction(Action):
    """Action to delete one record in the associated repository"""

    def __init__(self, record_id: Any, **kwargs):
        """
        Arguments:
            record_id (Any): the ID of the record to be removed
            **kwargs (Any): any extra key-word arguments you may need to pass in your particular implementation
        """
        self._record_id = record_id
        self._options = kwargs

    @property
    @abstractmethod
    def _repository(self) -> Repository:
        """The repository that this action connects to when deleting the record"""
        raise NotImplementedError("_repository should be implemented")

    def run(self) -> BaseModel:
        """
        Runs the Action

        Returns:
            BaseModel: the deleted record's DTO
        """
        return self._repository.remove_one(self._record_id, **self._options)


class DeleteManyAction(Action):
    """Action to delete many records in the associated repository"""

    def __init__(self, *criterion, **filters):
        """
        Arguments:
            *criterion (Any): any SQLAlchemy SQL expression object applicable to the WHERE clause of a select.

                e.g.::

                    MyClass.name == 'some name'

                - Multiple criteria may be specified as comma separated; the effect
                  is that they will be joined together using the :func:`.and_`
                - the :func:`.or_` can be also used to combine multiple criterion and passed as a single criterion

            **filters (Any): key-word arguments where the key corresponds to the field name on the model
                            in the repository and the argument is the value that field should have
        """
        self._criterion = criterion
        self._filters = filters

    @property
    @abstractmethod
    def _repository(self) -> Repository:
        """The repository that this action connects to when deleting the records"""
        raise NotImplementedError("_repository should be implemented")

    def run(self) -> List[BaseModel]:
        """
        Runs the Action

        Returns:
            list[BaseModel]: the deleted records' DTOs
        """
        return self._repository.remove_many(*self._criterion, **self._filters)
