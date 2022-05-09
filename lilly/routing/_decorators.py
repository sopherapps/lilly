"""
Module containing decorators specific to routes and route sets
"""
from typing import TypeVar, Type

from fastapi_utils.cbv import cbv
from ._crud import _generate_crud_route_set, CRUDRouteSet
from ._router import _router

T = TypeVar("T")

get = _router.get
post = _router.post
patch = _router.patch
delete = _router.delete
put = _router.put
options = _router.options
head = _router.head
websocket = _router.websocket


def routeset(cls: Type[T]) -> Type[T]:
    """
    Decorator to make Class Based Views work

    Example:

        @routeset
        class SomeRoutes(RouteSet):
            @get("home", response_model=SomeDTO)
            def home(self):
                return {"message": "home"}
        ```
    """
    route_set_cls = cls
    if issubclass(cls, CRUDRouteSet):
        route_set_cls = _generate_crud_route_set(router=_router, cls=cls)

    return cbv(_router)(route_set_cls)
