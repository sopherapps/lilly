"""Module defines the DataSource class"""
from abc import abstractmethod
from typing import Any


class DataSource:
    """
    Class responsible for connecting to any data source e.g. database, rest api, File system
    to enable the app persist data or retrieve data
    """

    @abstractmethod
    def connect(self) -> Any:
        """
        This should connect to the actual source of data and return an appropriate connection instance
        For instance, this could return an SQL alchemy db session
        """
        raise NotImplementedError()
