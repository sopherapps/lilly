"""
Test routes
"""
from lilly.routing import routeset, get, RouteSet

from .dtos import MessageDTO


@routeset
class First(RouteSet):
    """Collection of routes for the First domain"""

    @get("/first/{name}", response_model=MessageDTO)
    def say_hello(self, name: str):
        return {"message": f"Hi {name}"}
