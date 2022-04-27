"""Tests for the SQLAlchemy based DataSources"""

from unittest import main, TestCase
from unittest.mock import patch

from sqlalchemy.orm import declarative_base, Session
from sqlalchemy.exc import OperationalError
from sqlalchemy import Column, Integer, String

from lilly.datasources import SQLAlchemyDataSource, sqlalchemy

Base = declarative_base()


class Name(Base):
    """Model for names"""
    __tablename__ = "names"

    id = Column(Integer, primary_key=True)
    title = Column(String)


class TestSQLAlchemy(TestCase):
    """Tests for SQLAlchemy based data sources"""

    def setUp(self) -> None:
        """Initialize some common variables"""
        self.db_uri = "sqlite://"
        self.sqlalchemy_datasource = SQLAlchemyDataSource(declarative_meta=Base, db_uri=self.db_uri)

    def test_connect(self):
        """Connect should return a Session object and set _is_initialized as True"""
        initial_is_initialized = self.sqlalchemy_datasource._is_initialized

        session: Session = self.sqlalchemy_datasource.connect()
        final_is_initialized = self.sqlalchemy_datasource._is_initialized
        records = session.query(Name).all()

        self.assertIsInstance(session, Session)
        self.assertEqual(str(session.bind.url), self.db_uri)
        self.assertListEqual(records, [])
        self.assertFalse(initial_is_initialized)
        self.assertTrue(final_is_initialized)

    def test_initialize_db(self):
        """initialize_db should create all the tables in database"""
        session = next(self.sqlalchemy_datasource._sessions())
        initial_is_initialized = self.sqlalchemy_datasource._is_initialized

        self.sqlalchemy_datasource.initialize_db()
        final_is_initialized = self.sqlalchemy_datasource._is_initialized
        records = session.query(Name).all()

        self.assertFalse(initial_is_initialized)
        self.assertTrue(final_is_initialized)
        self.assertListEqual(records, [])

    def test_clear_db(self):
        """clear_db should clear all the tables in the database"""
        session = next(self.sqlalchemy_datasource._sessions())

        self.sqlalchemy_datasource.clear_db()
        final_is_initialized = self.sqlalchemy_datasource._is_initialized

        self.assertRaises(OperationalError, session.query(Name).all)
        self.assertFalse(final_is_initialized)

    def test_sqlite_engine_no_thread_check(self):
        """For sqlite databases only, the engine is instantiated with a check_same_thread in connect_args as False"""
        with patch.object(sqlalchemy, "create_engine", wraps=sqlalchemy.create_engine) as mock_create_engine:
            sqlalchemy_datasource = SQLAlchemyDataSource(declarative_meta=Base, db_uri=self.db_uri)
            options = {"connect_args": {"check_same_thread": False}}
            mock_create_engine.assert_called_with(self.db_uri, **options)


if __name__ == '__main__':
    main()
