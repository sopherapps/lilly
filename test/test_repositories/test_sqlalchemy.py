"""Tests for the SQLAlchemyRepository code"""
import os
import unittest
from typing import Type, List, Dict, Any
from unittest.mock import MagicMock, PropertyMock, patch

from pydantic import BaseModel
from dotenv import load_dotenv
from sqlalchemy import Column, Integer, String, Table
from sqlalchemy.orm import declarative_base, DeclarativeMeta

from lilly.datasources import SQLAlchemyDataSource
from lilly.repositories import SQLAlchemyRepository
from test.assets.mock_internals import NameTestDTO, MOCK_NAME_RECORDS, NameTestCreationDTO

root_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
test_env_path = os.path.join(root_path, ".env")
load_dotenv(test_env_path)

Base = declarative_base()

sqlite_test_db = SQLAlchemyDataSource(declarative_meta=Base, db_uri="sqlite://")
pq_test_db = SQLAlchemyDataSource(declarative_meta=Base, db_uri=os.environ.get("TEST_DATABASE_URL"))


class NameTest(Base):
    __tablename__ = "names"
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)


class NamesTestRepository(SQLAlchemyRepository):
    """Repository for saving and retrieving random names"""

    def __init__(self, db_source: SQLAlchemyDataSource):
        self.db_source = db_source

    @property
    def _model_cls(self) -> Type[DeclarativeMeta]:
        return NameTest

    @property
    def _dto_cls(self) -> Type[BaseModel]:
        return NameTestDTO

    @property
    def _datasource(self) -> SQLAlchemyDataSource:
        return self.db_source


class TestSQLAlchemyRepository(unittest.TestCase):
    """Tests related to the repository-related code"""

    def setUp(self) -> None:
        """Initialize some common variables"""
        sqlite_test_db.clear_db()
        sqlite_test_db.initialize_db()

        pq_test_db.clear_db()
        pq_test_db.initialize_db()

        self.sqlite_name_repo = NamesTestRepository(sqlite_test_db)
        self.pq_name_repo = NamesTestRepository(pq_test_db)

    @staticmethod
    def _add_dummy_data(db_source: SQLAlchemyDataSource, records: List[Dict[str, Any]]):
        """Adds dummy data to the database"""
        with db_source.connect() as db:
            names_table: Table = NameTest.__table__
            stmt = names_table.insert().values(records)
            db.execute(stmt)
            db.commit()

    def test_get_one(self):
        """get_one returns a single record of given id from the database"""
        self._test_get_one(self.sqlite_name_repo)
        self._test_get_one(self.pq_name_repo)

    def test_get_many(self):
        """get_many returns a list of records that fulfill given criteria and filters"""
        self._test_get_many(self.sqlite_name_repo)
        self._test_get_many(self.pq_name_repo)

    def test_update_one(self):
        """update_one updates the record of record_id passed"""
        self._test_update_one(self.sqlite_name_repo)
        self._test_update_one(self.pq_name_repo)

    def test_update_many(self):
        """update_many updates many records that fulfill the criteria and filters"""
        self._test_update_many(self.sqlite_name_repo)
        self._test_update_many(self.pq_name_repo)

    def test_remove_one(self):
        """remove_one removes the record with the given record_id"""
        self._test_remove_one(self.sqlite_name_repo)
        self._test_remove_one(self.pq_name_repo)

    def test_remove_many(self):
        """remove_many removes the records that fulfill the given criteria and filters"""
        self._test_remove_many(self.sqlite_name_repo)
        self._test_remove_many(self.pq_name_repo)

    def test_create_one(self):
        """create_one creates a record in the database"""
        self._test_create_one(self.sqlite_name_repo)
        self._test_create_one(self.pq_name_repo)

    def test_create_many(self):
        """create_many creates many records in the database"""
        self._test_create_many(self.sqlite_name_repo)
        self._test_create_many(self.pq_name_repo)

    def test_required_datasource_attribute(self):
        """Throws NotImplementedError when used without _datasource defined on the class"""
        mock_repo = SQLAlchemyRepository()
        mock_repo._to_output_dto = MagicMock(return_value="to_output_dto")

        self.assertRaises(NotImplementedError, mock_repo.get_one, 1)

    @patch("lilly.repositories.SQLAlchemyRepository._datasource", new_callable=PropertyMock)
    def test_required_to_output_dto(self, mock_repo_datasource: PropertyMock):
        """Throws NotImplementedError when used without _dto_cls defined on the class"""
        mock_repo_datasource.return_value = self.sqlite_name_repo.db_source
        mock_repo = SQLAlchemyRepository()
        self.assertRaises(NotImplementedError, mock_repo.get_one, 1)

    @patch("lilly.repositories.SQLAlchemyRepository._dto_cls", new_callable=PropertyMock)
    @patch("lilly.repositories.SQLAlchemyRepository._datasource", new_callable=PropertyMock)
    def test_required_to_output_dto(self, mock_repo_datasource: PropertyMock, mock_dto_cls):
        """Throws NotImplementedError when used without _dto_cls defined on the class"""
        mock_repo_datasource.return_value = self.sqlite_name_repo.db_source
        mock_dto_cls.return_value = NameTestDTO
        mock_repo = SQLAlchemyRepository()
        self.assertRaises(NotImplementedError, mock_repo.get_one, 1)

    def _test_get_one(self, repo: NamesTestRepository):
        """get_one returns a single record of given id from the database"""
        self._add_dummy_data(repo.db_source, MOCK_NAME_RECORDS)

        for index, record in enumerate(MOCK_NAME_RECORDS):
            record_id = index + 1

            expected = NameTestDTO(id=record_id, **record)
            got = repo.get_one(record_id=record_id)
            self.assertEqual(expected, got)

    def _test_get_many(self, repo: NamesTestRepository):
        """get_many returns a list of records that fulfill given criteria and filters"""
        self._add_dummy_data(repo.db_source, MOCK_NAME_RECORDS)

        expected = [
            NameTestDTO(id=7, title="Roe"),
            NameTestDTO(id=8, title="Roe"),
        ]
        got = repo.get_many(NameTest.id < 10, "id > 2", skip=1, limit=2, title="Roe")
        self.assertListEqual(expected, got)

    def _test_update_one(self, repo: NamesTestRepository):
        """update_one updates the record of record_id passed"""
        self._add_dummy_data(repo.db_source, MOCK_NAME_RECORDS)
        test_data: List[NameTestDTO] = [
            NameTestDTO(id=2, title="Foo bar"),
            NameTestDTO(id=5, title="Pao al"),
            NameTestDTO(id=1, title="Shingie"),
        ]
        with repo.db_source.connect() as session:
            for expected in test_data:
                got_after_update = repo.update_one(expected.id, expected)
                got_after_get = session.query(NameTest).get(expected.id)

                self.assertEqual(expected, got_after_update)
                self.assertEqual(expected, NameTestDTO.from_orm(got_after_get))

    def _test_update_many(self, repo: NamesTestRepository):
        """update_many updates many records that fulfill the criteria and filters"""
        expected_after_update = [
            NameTestDTO(id=4, title="Rene"),
            NameTestDTO(id=7, title="Rene"),
            NameTestDTO(id=8, title="Rene"),
        ]
        expected_after_get = [
            NameTestDTO(id=1, title="Doe"),
            NameTestDTO(id=2, title="Roe"),
            NameTestDTO(id=3, title="Doe"),
            NameTestDTO(id=4, title="Rene"),
            NameTestDTO(id=5, title="Doe"),
            NameTestDTO(id=6, title="Doe"),
            NameTestDTO(id=7, title="Rene"),
            NameTestDTO(id=8, title="Rene"),
            NameTestDTO(id=9, title="Doe"),
            NameTestDTO(id=10, title="Roe"),
        ]
        new_data = NameTestCreationDTO(title="Rene")

        with repo.db_source.connect() as session:
            self._add_dummy_data(repo.db_source, MOCK_NAME_RECORDS)
            got_after_update = repo.update_many(new_data, NameTest.id < 10, "id > 2", title="Roe")
            got_after_get = [NameTestDTO.from_orm(record) for record in
                             session.query(NameTest).order_by(NameTest.id).all()]

        self.assertListEqual(expected_after_update, got_after_update)
        self.assertListEqual(expected_after_get, got_after_get)

    def _test_remove_one(self, repo: NamesTestRepository):
        """remove_one removes the record with the given record_id"""
        with repo.db_source.connect() as session:
            self._add_dummy_data(repo.db_source, MOCK_NAME_RECORDS)

            for index, record in enumerate(MOCK_NAME_RECORDS):
                record_id = index + 1

                expected = NameTestDTO(id=record_id, **record)
                got = repo.remove_one(record_id=record_id)
                self.assertEqual(expected, got)

                got_from_get = session.query(NameTest).get(record_id)
                self.assertIsNone(got_from_get)

    def _test_remove_many(self, repo: NamesTestRepository):
        """remove_many removes the records that fulfill the given criteria and filters"""
        with repo.db_source.connect() as session:
            self._add_dummy_data(repo.db_source, MOCK_NAME_RECORDS)

            expected_after_update = [
                NameTestDTO(id=4, title="Roe"),
                NameTestDTO(id=7, title="Roe"),
                NameTestDTO(id=8, title="Roe"),
            ]
            expected_after_get = [
                NameTestDTO(id=1, title="Doe"),
                NameTestDTO(id=2, title="Roe"),
                NameTestDTO(id=3, title="Doe"),
                NameTestDTO(id=5, title="Doe"),
                NameTestDTO(id=6, title="Doe"),
                NameTestDTO(id=9, title="Doe"),
                NameTestDTO(id=10, title="Roe"),
            ]

            got_after_delete = repo.remove_many(NameTest.id < 10, "id > 2", title="Roe")
            got_after_get = [NameTestDTO.from_orm(record) for record in
                             session.query(NameTest).order_by(NameTest.id).all()]

            self.assertListEqual(expected_after_update, got_after_delete)
            self.assertListEqual(expected_after_get, got_after_get)

    def _test_create_one(self, repo: NamesTestRepository):
        """get_one creates ibe record in the database"""
        for index, record in enumerate(MOCK_NAME_RECORDS):
            record_id = index + 1

            expected = NameTestDTO(id=record_id, **record)
            got = repo.create_one(NameTestCreationDTO(**record))
            self.assertEqual(expected, got)

    def _test_create_many(self, repo: NamesTestRepository):
        """create_many creates many records in the database"""
        records = [NameTestCreationDTO(**record) for record in MOCK_NAME_RECORDS]
        expected = [
            NameTestDTO(id=1, title="Doe"),
            NameTestDTO(id=2, title="Roe"),
            NameTestDTO(id=3, title="Doe"),
            NameTestDTO(id=4, title="Roe"),
            NameTestDTO(id=5, title="Doe"),
            NameTestDTO(id=6, title="Doe"),
            NameTestDTO(id=7, title="Roe"),
            NameTestDTO(id=8, title="Roe"),
            NameTestDTO(id=9, title="Doe"),
            NameTestDTO(id=10, title="Roe"),
        ]

        with repo.db_source.connect() as session:
            got_after_create = repo.create_many(records=records)
            got_after_get = [NameTestDTO.from_orm(record) for record in
                             session.query(NameTest).order_by(NameTest.id).all()]

            self.assertListEqual([], got_after_create)
            self.assertListEqual(expected, got_after_get)


if __name__ == '__main__':
    unittest.main()
