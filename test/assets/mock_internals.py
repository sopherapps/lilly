"""Module containing mocks of all relevant internal classes"""
from typing import Any, List, Optional, ContextManager, Dict

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

    def _get_one(self, datasource_connection: Any, record_id: int, **kwargs) -> Any:
        index = record_id - 1
        return MOCK_NAME_RECORDS[index]

    def _get_many(self, datasource_connection: Any, *criterion, skip: int = 0, limit: Optional[int] = None,
                  **filters) -> List[
        Any]:
        return MOCK_NAME_RECORDS

    def _create_one(self, datasource_connection: Any, record: Dict[str, Any], **kwargs) -> Any:
        return {"id": 1, **record}

    def _create_many(self, datasource_connection: Any, records: List[Dict[str, Any]], **kwargs) -> List[Any]:
        return [{"id": index + 1, **record} for index, record in enumerate(records)]

    def _update_one(self, datasource_connection: Any, record_id: int, new_record: Dict[str, Any], **kwargs) -> Any:
        return {"id": record_id, **new_record}

    def _update_many(self, datasource_connection: Any, new_record: Dict[str, Any], *criterion, **filters) -> List[Any]:
        filtered_records = self.__get_filtered_records(*criterion, **filters)
        return [{**record, **new_record} for record in filtered_records]

    def _remove_one(self, datasource_connection: Any, record_id: int, **kwargs) -> Any:
        return MOCK_NAME_RECORDS[record_id - 1]

    def _remove_many(self, datasource_connection: Any, *criterion, **filters) -> List[Any]:
        return self.__get_filtered_records(*criterion, **filters)

    def __get_filtered_records(self, *criterion, **filters) -> List[Any]:
        """Filters the records and returns them"""
        if len(criterion) > 0:
            raise NotImplementedError("filtering by criterion is not implemented in the mock")
        records = [{"id": index + 1, **record} for index, record in enumerate(MOCK_NAME_RECORDS)]
        return list(filter(lambda item: all([item[field] == value for field, value in filters.items()]), records))

    @property
    def _datasource(self) -> DataSource:
        return MockDataSource()

    def _to_output_dto(self, record: Any) -> BaseModel:
        return NameTestDTO(**record)
