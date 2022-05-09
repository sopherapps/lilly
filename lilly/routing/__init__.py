"""
Package containing base class for all route sets and any utilities connected to routing e.g. decorators
Route sets are collections of related routes that expose the app to its clients.
We use Class Based Views in order to be cleaner and to use the private _do() method to call an action
"""
from ._base import RouteSet
from ._crud import CRUDRouteSetSettings, CRUDRouteSet
from ._decorators import routeset, get, post, put, patch, delete, options, head
from ._router import register_router

__all__ = [
    RouteSet,
    CRUDRouteSetSettings,
    CRUDRouteSet,
    routeset,
    get,
    post,
    put,
    patch,
    delete,
    options,
    head,
    register_router
]
