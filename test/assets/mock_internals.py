"""Module containing mocks of all relevant internal classes"""
from typing import Any, List, ContextManager, Dict

from pydantic import BaseModel

from lilly.datasources import DataSource
from lilly.repositories import Repository

MOCK_NAME_RECORDS: List[Dict[str, Any]] = [
    {"title": "Doe"},
    {"title": "Roe"},
    {"title": "Doe"},
    {"title": "Roe"},
    {"title": "Doe"},
    {"title": "Doe"},
    {"title": "Roe"},
    {"title": "Roe"},
    {"title": "Doe"},
    {"title": "Roe"},
]


class NameTestDTO(BaseModel):
    id: int
    title: str

    class Config:
        orm_mode = True


class NameTestCreationDTO(BaseModel):
    title: str


class MockConnectionContextManager:
    """A mock context manager for the connection to a data source"""

    def __init__(self, connection: Any):
        self._connection = connection

    def __enter__(self):
        return self._connection

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


class MockDataSource(DataSource):
    """Mock DataSource"""

    def connect(self) -> ContextManager:
        return MockConnectionContextManager("connected")


class MockRepository(Repository):
    """A mock repo"""
    @property
    def _datasource(self) -> DataSource:
        return MockDataSource()

    def _to_output_dto(self, record: Any) -> BaseModel:
        return NameTestDTO(**record)
