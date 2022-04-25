"""
Module containing the datasources to save and retrieve information from
"""
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker, declarative_base

from lilly.datasources import DataSource
from lilly.conf import settings

Base = declarative_base()


class NamesDb(DataSource):
    """This is a connection to a database via SQLAlchemy"""
    _is_initialized: bool = False

    def __init__(self):
        db_uri = settings.DATABASE_URL
        options = {}

        if _is_db_sqlite(db_uri=db_uri):
            # remove the same_thread_check done by sqlite
            connect_args = options.get("connect_args", {})
            connect_args.update({'check_same_thread': False})
            options["connect_args"] = connect_args

        self.engine = create_engine(db_uri, **options)

    def connect(self) -> Session:
        """Connects to the database and returns a session to use for making queries"""
        if not self._is_initialized:
            self._initialize_db()
        return next(self._sessions())

    def _initialize_db(self):
        """Does any tasks to prepare the database for use"""
        Base.metadata.create_all(bind=self.engine)
        self._is_initialized = True

    def _sessions(self, **kwargs) -> Generator[Session, None, None]:
        """
        generates sessions on the fly, yielding them and closing them after use
        """
        db = sessionmaker(bind=self.engine, autocommit=False, autoflush=False)()
        try:
            yield db
        finally:
            db.close()


def _is_db_sqlite(db_uri: str) -> bool:
    """Checks if the database is an sqlite one."""
    return db_uri.split(":")[0].lower() == "sqlite"
