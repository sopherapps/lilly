"""
Module containing extensions specific to routes and route sets e.g. decorators
"""
from fastapi import APIRouter, FastAPI
from fastapi_utils.cbv import cbv

_router = APIRouter()

# decorators
get = _router.get
post = _router.post
patch = _router.patch
delete = _router.delete
put = _router.put
options = _router.options
head = _router.head
websocket = _router.websocket
routeset = cbv(_router)


def register_router(app: FastAPI):
    """
    Registers the router given an app instance
    Since _router is protected, we need this public method to register the router
    """
    app.include_router(_router)
