"""Some common utilitly functions"""
from fastapi import FastAPI, APIRouter

# the universal route for the entire app
_router = APIRouter()


def register_router(app: FastAPI):
    """
    Registers the router given an app instance
    Since _router is protected, we need this public method to register the router
    """
    app.include_router(_router)
