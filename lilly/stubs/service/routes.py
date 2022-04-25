"""
Module containing the basic public API of the service.
These can be exposed as REST API endpoints or websockets
"""
from lilly.routing import RouteSet
from lilly.routing.ext import routeset, get, post

from .dtos import NameCreationRequestDTO, MessageDTO, NameRecordDTO
from .actions import GenerateRandomName


@routeset
class HelloWorld(RouteSet):
    """Collection of routes for the Hello World domain"""

    @get("/hello/{name}", response_model=MessageDTO)
    def say_hello(self, name: str):
        return {"message": f"Hi {name}"}

    @post("/names/", response_model=NameRecordDTO)
    def create_random_name(self, request: NameCreationRequestDTO):
        return self._do(GenerateRandomName, length=request.length)
