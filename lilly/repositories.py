"""
Module defines the Repository Base class which is to be inherited by all repository classes
Repositories are responsible for data preparation when saving to a data source or retireiving data from
a data source
"""
from abc import abstractmethod
from typing import Type, Any, Dict, List

from lilly.datasources import DataSource


class Repository:
    """
    The Repository Base class which is to be inherited by all repository classes
    Repositories are responsible for data preparation when saving to a data source or retireiving data from
    a data source

    e.g. They will do a `get_many` or `create_one` etc.
    """
    datasourceCls: Type[DataSource]

    def __init__(self):
        self._datasource: DataSource = self.datasourceCls()

    @abstractmethod
    def get_one(self, record_id: Any, **kwargs) -> Any:
        """method to get one record of id `record_id`"""
        raise NotImplemented()

    @abstractmethod
    def get_many(self, skip: int, limit: int, filters: Dict[Any, Any], **kwargs) -> List[Any]:
        """method to get many records that fulfil the `filters`"""
        raise NotImplemented()

    @abstractmethod
    def create_one(self, record: Any, **kwargs) -> Any:
        """method to create one record"""
        raise NotImplemented()

    @abstractmethod
    def create_many(self, records: List[Any], **kwargs) -> List[Any]:
        """method to create many records"""
        raise NotImplemented()

    @abstractmethod
    def update_one(self, record_id: Any, new_record: Any, **kwargs) -> Any:
        """method to update one record of id `record_id`"""
        raise NotImplemented()

    @abstractmethod
    def update_many(self, new_record: Any, filters: Dict[Any, Any], **kwargs) -> Any:
        """method to update many records that fulfil the `filters`"""
        raise NotImplemented()

    @abstractmethod
    def remove_one(self, record_id: Any, **kwargs) -> Any:
        """method to remove one record of id `record_id`"""
        raise NotImplemented()

    @abstractmethod
    def remove_many(self, filters: Dict[Any, Any], **kwargs) -> Any:
        """method to remove many records that fulfil the `filters`"""
        raise NotImplemented()
