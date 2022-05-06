"""DataSource from SQLAlchemy"""
from typing import Optional

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker, DeclarativeMeta

from .base import DataSource


class SQLAlchemySessionContextManager:
    """This is a special context manager to ensure the created session is closed when used"""

    def __init__(self, engine: Engine):
        self.__engine = engine
        self.__session: Optional[Session] = None

    def __enter__(self) -> Session:
        self.__session = sessionmaker(bind=self.__engine, autocommit=False, autoflush=False)()
        return self.__session

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__session.close()


class SQLAlchemyDataSource(DataSource):
    """The data source that connects to relational databases via SQLAlchemy"""
    _is_initialized: bool = False

    def __init__(self, declarative_meta: DeclarativeMeta, db_uri: str, **options):
        self._declarative_meta = declarative_meta

        if db_uri.startswith("sqlite"):
            # remove the same_thread_check done by sqlite
            connect_args = options.get("connect_args", {})
            connect_args.update({"check_same_thread": False})
            options["connect_args"] = connect_args

        self._engine = create_engine(db_uri, **options)

    def connect(self) -> SQLAlchemySessionContextManager:
        """Connects to the database and returns a session to use for making queries"""
        if not self._is_initialized:
            self.initialize_db()

        return SQLAlchemySessionContextManager(self._engine)

    def initialize_db(self):
        """Does any tasks to prepare the database for use"""
        self._declarative_meta.metadata.create_all(bind=self._engine)
        self._is_initialized = True

    def clear_db(self):
        """Clears the whole database, removing the associated tables"""
        self._declarative_meta.metadata.drop_all(bind=self._engine)
        self._is_initialized = False
