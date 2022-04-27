"""Module contains definition of the Action base class which is responsible for any business logic"""
from abc import abstractmethod


class Action:
    """
    Base class for all Action classes that do the business logic of the app;
    often connecting the routes (the presentation) to the persistence layer (the repositories)
    """

    @abstractmethod
    def run(self):
        """This does the actual business logic. It is called by the route's _do() method"""
        raise NotImplementedError()
