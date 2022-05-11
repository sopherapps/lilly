"""Module containing REST RouteSet for CRUD-related actions"""
from abc import abstractmethod
from typing import Type, List, Optional, Any

from fastapi import APIRouter
from pydantic import BaseModel

from lilly.actions import (
    CreateOneAction,
    CreateManyAction,
    ReadOneAction,
    ReadManyAction,
    UpdateOneAction,
    UpdateManyAction,
    DeleteOneAction,
    DeleteManyAction
)
from lilly.routing._base import RouteSet


class CRUDRouteSetSettings(BaseModel):
    """
    The settings for CRUD Route sets
        # TODO: There is need for searching even number fields, or even searching for less or greater

        * id_type (Type[Any]): the data type of the id field for the given DTO in the repository
        * base_path (str) (required): the base path in the REST API for this route set
        * base_path_for_multiple_items (str) (required): the base path in the REST API for this route set when multiple items are considered e.g. create_many
        * response_model (Type[BaseModel]) (required): the BaseModel subclass representing a single returned entity in this route set's response
        * creation_request_model (Type[BaseModel]) (required): the BaseModel subclass representing the REST API request body sent when creating an instance in the associated repository
        * create_one_action (Type[CreateOneAction]): the :ref:`CreateOneAction <lilly.actions.CreateOneAction>` subclass to be used to create a single instance in the repository
        * create_many_action (Type[CreateManyAction]): the :ref:`CreateManyAction <lilly.actions.CreateManyAction>` subclass to be used to create multiple instances in the repository
        * read_one_action (Type[ReadOneAction]): the :ref:`ReadOneAction <lilly.actions.ReadOneAction>` subclass to be used to read a single instance from the repository
        * read_many_action (Type[ReadManyAction]): the :ref:`ReadManyAction <lilly.actions.ReadManyAction>` subclass to be used to read multiple instances from the repository
        * update_one_action (Type[UpdateOneAction]): the :ref:`UpdateOneAction <lilly.actions.UpdateOneAction>` subclass to be used to update a single instance in the repository
        * update_many_action (Type[UpdateManyAction]): the :ref:`UpdateManyAction <lilly.actions.UpdateManyAction>` subclass to be used to update multiple instances in the repository
        * delete_one_action (Type[DeleteOneAction]): the :ref:`DeleteOneAction <lilly.actions.DeleteOneAction>` subclass to be used to delete a single instances from the repository
        * delete_many_action (Type[DeleteManyAction]): the :ref:`DeleteManyAction <lilly.actions.DeleteManyAction>` subclass to be used to delete multiple instances in the repository
        * string_searchable_fields (List[str]): the list of fields that can be searched as strings during filtering
    """
    id_type: Type[Any] = int
    base_path: str
    base_path_for_multiple_items: str
    response_model: Type[BaseModel]
    creation_request_model: Type[BaseModel]
    create_one_action: Optional[Type[CreateOneAction]] = None
    create_many_action: Optional[Type[CreateManyAction]] = None
    read_one_action: Optional[Type[ReadOneAction]] = None
    read_many_action: Optional[Type[ReadManyAction]] = None
    update_one_action: Optional[Type[UpdateOneAction]] = None
    update_many_action: Optional[Type[UpdateManyAction]] = None
    delete_one_action: Optional[Type[DeleteOneAction]] = None
    delete_many_action: Optional[Type[DeleteManyAction]] = None
    string_searchable_fields: List[str] = []


class CRUDRouteSet(RouteSet):
    """
    Base Routeset for CRUD route sets
    """

    @classmethod
    @abstractmethod
    def get_settings(cls) -> CRUDRouteSetSettings:
        """
        The settings for CRUD Route sets

        Returns:
            CRUDRouteSetSettings: the settings for this CRUD Route set
        """
        raise NotImplementedError("get_settings is required")


def _generate_crud_route_set(router: APIRouter, cls: Type[CRUDRouteSet]) -> Type[CRUDRouteSet]:
    _settings = cls.get_settings()

    class _CRUDRouteSet(cls):
        """The CRUD routeset"""

        @classmethod
        def get_settings(cls) -> CRUDRouteSetSettings:
            return _settings

        @router.post(f"{_settings.base_path}/", response_model=_settings.response_model)
        def create_one(self, body: _settings.creation_request_model):
            return self._do(_settings.create_one_action, body)

        @router.post(f"{_settings.base_path_for_multiple_items}/", response_model=List[_settings.response_model])
        def create_many(self, body: List[_settings.creation_request_model]):
            return self._do(_settings.create_many_action, body)

        @router.get(f"{_settings.base_path}/{{record_id}}", response_model=_settings.response_model)
        def read_one(self, record_id: _settings.id_type):
            return self._do(_settings.read_one_action, record_id)

        @router.get(f"{_settings.base_path}/", response_model=List[_settings.response_model])
        def read_many(self, skip: int = 0, limit: Optional[int] = None, q: Optional[str] = None):
            criteria = []

            if q is not None:
                query = _extract_sql_query_string(fields=_settings.string_searchable_fields, q=q)
                criteria.append(query)

            return self._do(_settings.read_many_action, *criteria, skip=skip, limit=limit, )

        @router.put(f"{_settings.base_path}/{{record_id}}", response_model=_settings.response_model)
        def update_one(self, record_id: _settings.id_type, body: _settings.response_model):
            return self._do(_settings.update_one_action, record_id, body)

        @router.patch(f"{_settings.base_path}/{{record_id}}", response_model=_settings.response_model)
        def update_partial(self, record_id: _settings.id_type, body: _settings.creation_request_model):
            return self._do(_settings.update_one_action, record_id, body)

        @router.put(f"{_settings.base_path_for_multiple_items}/", response_model=List[_settings.response_model])
        def update_many(self, body: _settings.creation_request_model, q: str = ""):
            query = _extract_sql_query_string(fields=_settings.string_searchable_fields, q=q)
            return self._do(_settings.update_many_action, body, query, )

        @router.delete(f"{_settings.base_path}/{{record_id}}", response_model=_settings.response_model)
        def delete_one(self, record_id: _settings.id_type):
            return self._do(_settings.delete_one_action, record_id)

        @router.delete(f"{_settings.base_path_for_multiple_items}/", response_model=List[_settings.response_model])
        def delete_many(self, q: str = ""):
            query = _extract_sql_query_string(fields=_settings.string_searchable_fields, q=q)
            return self._do(_settings.delete_many_action, query, )

    _remove_routes_for_undefined_actions(_CRUDRouteSet, settings=_settings)

    return _CRUDRouteSet


def _extract_sql_query_string(fields: List[str], q: str):
    """Generates the search query to be sent to the repository for filtering using SQL-like syntax"""
    str_search = ""
    for field in fields:
        str_search += f"{field} LIKE '%{q}%' OR"
    return str_search.rstrip(" OR")


def _remove_routes_for_undefined_actions(cls: Type[CRUDRouteSet], settings: CRUDRouteSetSettings):
    """Removes the routes from the CRUDRouteSet for which actions have not been defined"""
    if settings.read_one_action is None:
        delattr(cls, "read_one")

    if settings.read_many_action is None:
        delattr(cls, "read_many")

    if settings.create_one_action is None:
        delattr(cls, "create_one")

    if settings.create_many_action is None:
        delattr(cls, "create_many")

    if settings.update_one_action is None:
        delattr(cls, "update_one")
        delattr(cls, "update_partial")

    if settings.update_many_action is None:
        delattr(cls, "update_many")

    if settings.delete_one_action is None:
        delattr(cls, "delete_one")

    if settings.delete_many_action is None:
        delattr(cls, "delete_many")
