"""
Package containing base class for all route sets and any utilities connected to routing e.g. decorators
Route sets are collections of related routes that expose the app to its clients.
We use Class Based Views in order to be cleaner and to use the private _do() method to call an action
"""
from typing import Type

from lilly.actions import Action


class RouteSet:
    """
    Base class for all RouteSets
    Route sets are collections of related routes that expose the app to its clients.
    We use Class Based Views in order to be cleaner and to use the private _do() method to call an action

    - They must be decorated by @service
    - Their methods that are endpoints should be decorated by @get(), @post(), @patch() etc,
      all having the same signature as normal FastAPI route decorators
    - Any dependencies can be passed in as class attributes
    """

    @staticmethod
    def _do(action_cls: Type[Action], *args, **kwargs):
        """
        This instantiates Action instance, passing in *args and *kwargs,
        then calls the action's `run()` method to run the action
        """
        action = action_cls(*args, **kwargs)
        return action.run()
