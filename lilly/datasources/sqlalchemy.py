"""DataSource from SQLAlchemy"""
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker, DeclarativeMeta

from .base import DataSource


class SQLAlchemyDataSource(DataSource):
    """The data source that connects to relational databases via SQLAlchemy"""
    _is_initialized: bool = False

    def __init__(self, declarative_meta: DeclarativeMeta, db_uri: str, **options):
        self._declarative_meta = declarative_meta

        if _is_db_sqlite(db_uri=db_uri):
            # remove the same_thread_check done by sqlite
            connect_args = options.get("connect_args", {})
            connect_args.update({"check_same_thread": False})
            options["connect_args"] = connect_args

        self._engine = create_engine(db_uri, **options)

    def connect(self) -> Session:
        """Connects to the database and returns a session to use for making queries"""
        if not self._is_initialized:
            self.initialize_db()
        return next(self._sessions())

    def initialize_db(self):
        """Does any tasks to prepare the database for use"""
        self._declarative_meta.metadata.create_all(bind=self._engine)
        self._is_initialized = True

    def clear_db(self):
        """Clears the whole database, removing the associated tables"""
        self._declarative_meta.metadata.drop_all(bind=self._engine)
        self._is_initialized = False

    def _sessions(self, **kwargs) -> Generator[Session, None, None]:
        """
        generates sessions on the fly, yielding them and closing them after use
        """
        db = sessionmaker(bind=self._engine, autocommit=False, autoflush=False)()
        try:
            yield db
        finally:
            db.close()


def _is_db_sqlite(db_uri: str) -> bool:
    """Checks if the database is an sqlite one."""
    return db_uri.split(":")[0].lower() == "sqlite"
