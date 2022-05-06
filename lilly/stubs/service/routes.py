"""
Module containing the basic public API of the service.
These can be exposed as REST API endpoints or websockets
"""
from typing import List, Optional

from lilly.routing import RouteSet
from lilly.routing.ext import routeset, get, post, put, delete, patch

from .dtos import (
    RandomNameCreationRequestDTO,
    MessageDTO,
    NameRecordDTO,
    NameCreationRequestDTO,
)
from .actions import (
    GenerateRandomName,
    CreateOneName,
    CreateManyNames,
    ReadOneName,
    ReadManyNames,
    UpdateOneName,
    UpdateManyNames,
    DeleteOneName,
    DeleteManyNames,
)


@routeset
class HelloWorld(RouteSet):
    """Collection of routes for the Hello World domain"""

    @get("/hello/{name}", response_model=MessageDTO)
    def say_hello(self, name: str):
        return {"message": f"Hi {name}"}

    @post("/random-names/", response_model=NameRecordDTO)
    def create_random_name(self, request: RandomNameCreationRequestDTO):
        return self._do(GenerateRandomName, length=request.length)

    @post("/names/", response_model=NameRecordDTO)
    def create_name(self, body: NameCreationRequestDTO):
        return self._do(CreateOneName, body)

    @post("/admin/names/", response_model=List[NameRecordDTO])
    def create_many_names(self, body: List[NameCreationRequestDTO]):
        return self._do(CreateManyNames, body)

    @get("/names/{record_id}", response_model=NameRecordDTO)
    def read_name(self, record_id: int):
        return self._do(ReadOneName, record_id)

    @get("/names/", response_model=List[NameRecordDTO])
    def read_many_names(self, skip: int = 0, limit: Optional[int] = None, q: Optional[str] = None):
        criteria = []
        if q is not None:
            criteria.append(f"title LIKE '%{q}%'")

        return self._do(ReadManyNames, *criteria, skip=skip, limit=limit, )

    @put("/names/{record_id}", response_model=NameRecordDTO)
    def update_name(self, record_id: int, body: NameRecordDTO):
        return self._do(UpdateOneName, record_id, body)

    @put("/admin/names/", response_model=List[NameRecordDTO])
    def update_many_names(self, body: NameCreationRequestDTO, q: str = ""):
        return self._do(UpdateManyNames, body, f"title LIKE '%{q}%'", )

    @patch("/names/{record_id}", response_model=NameRecordDTO)
    def update_name_partially(self, record_id: int, body: NameCreationRequestDTO):
        return self._do(UpdateOneName, record_id, body)

    @delete("/names/{record_id}", response_model=NameRecordDTO)
    def delete_name(self, record_id: int):
        return self._do(DeleteOneName, record_id)

    @delete("/admin/names/", response_model=List[NameRecordDTO])
    def delete_many_names(self, q: str = ""):
        return self._do(DeleteManyNames, f"title LIKE '%{q}%'", )
