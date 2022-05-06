"""Module defines the DataSource base class"""
from abc import abstractmethod
from typing import ContextManager


class DataSource:
    """
    Class responsible for connecting to any data source e.g. database, rest api, File system
    to enable the app persist data or retrieve data
    """

    @abstractmethod
    def connect(self) -> ContextManager:
        """
        This should connect to the actual source of data and return a context manager to
        an appropriate connection instance

        This is to allow for cleanup tasks to be done after each operation within the __exit__
        The __enter__ should return the actual connection object e.g. a session for a SQLAlchemy

        eg.::

        class SQLAlchemySessionContextManager:
            def __init__(self, engine: Engine):
                self.__engine = engine
                self.__session: Optional[Session] = None

            def __enter__(self) -> Session:
                self.__session = sessionmaker(bind=self.__engine, autocommit=False, autoflush=False)()
                return self.__session

            def __exit__(self, exc_type, exc_val, exc_tb):
                self.__session.close()

        """
        raise NotImplementedError()
