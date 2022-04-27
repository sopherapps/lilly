"""
Module containing the datasources to save and retrieve information from
"""
from sqlalchemy.orm import declarative_base

from lilly.datasources import SQLAlchemyDataSource
from lilly.conf import settings

Base = declarative_base()


class NamesDb(SQLAlchemyDataSource):
    """This is a connection to a database via SQLAlchemy"""

    def __init__(self):
        super().__init__(declarative_meta=Base, db_uri=settings.DATABASE_URL)
