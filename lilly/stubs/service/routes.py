"""
Module containing the basic public API of the service.
These can be exposed as REST API endpoints or websockets
"""
from lilly.routing import CRUDRouteSet, CRUDRouteSetSettings, routeset, get, post, RouteSet

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
class NormalRouteSet(RouteSet):
    """
    A basic Class based route that can have any method as an endpoint and can have common variables in the init
    attached to self
    """

    def __init__(self):
        self.name = "Lilly"

    @get("/", response_model=MessageDTO)
    def home(self):
        """Home"""
        return {"message": f"Welcome to {self.name}"}

    @get("/login", response_model=MessageDTO)
    def login(self):
        """Login"""
        return {"message": f"{self.name} invites you to login"}


@routeset
class HelloWorld(CRUDRouteSet):
    """
    Class Based Route set that handles CRUD functionality out of the box
    """

    @classmethod
    def get_settings(cls) -> CRUDRouteSetSettings:
        # When an action is not defined, the dependant routes will not be shown
        return CRUDRouteSetSettings(
            id_type=int,
            base_path="/names",
            base_path_for_multiple_items="/admin/names",
            response_model=NameRecordDTO,
            creation_request_model=NameCreationRequestDTO,
            create_one_action=CreateOneName,
            create_many_action=CreateManyNames,
            read_one_action=ReadOneName,
            read_many_action=ReadManyNames,
            update_one_action=UpdateOneName,
            update_many_action=UpdateManyNames,
            delete_one_action=DeleteOneName,
            delete_many_action=DeleteManyNames,
            string_searchable_fields=["title"],
        )

    # You can add even more routes on the CRUD routeset

    @get("/hello/{name}", response_model=MessageDTO)
    def say_hello(self, name: str):
        return {"message": f"Hi {name}"}

    @post("/random-names/", response_model=NameRecordDTO)
    def create_random_name(self, request: RandomNameCreationRequestDTO):
        return self._do(GenerateRandomName, length=request.length)
