"""
Module containing actions.
These are the business logic components called by routes to do a specific task by using the _do() call
"""
import random
import string

from pydantic import BaseModel

from lilly.actions import (
    Action,
    ReadOneAction,
    ReadManyAction,
    CreateOneAction,
    CreateManyAction,
    UpdateOneAction,
    UpdateManyAction,
    DeleteOneAction,
    DeleteManyAction,
)
from lilly.repositories import Repository

from .dtos import NameCreationRequestDTO
from .repositories import NamesRepository

_names_repo = NamesRepository()


class GenerateRandomName(Action):
    """
    Generates a random string and persists it in the data source
    """
    _vowels = "aeiou"
    _consonants = "".join(set(string.ascii_lowercase) - set("aeiou"))

    def __init__(self, length: int = 7):
        self._length = length

    def run(self) -> BaseModel:
        """Actual method that is run"""
        name = self._generate_random_word()
        return _names_repo.create_one(NameCreationRequestDTO(title=name))

    def _generate_random_word(self):
        """Generates a random word"""
        word = ""
        for i in range(self._length):
            if i % 2 == 0:
                word += random.choice(self._consonants)
            else:
                word += random.choice(self._vowels)
        return word


class CreateOneName(CreateOneAction):
    """Create a single Name record in the repository"""

    @property
    def _repository(self) -> Repository:
        return _names_repo


class CreateManyNames(CreateManyAction):
    """Create a list of name records in the repository"""

    @property
    def _repository(self) -> Repository:
        return _names_repo


class ReadOneName(ReadOneAction):
    """Reads a single Name record from the repository"""

    @property
    def _repository(self) -> Repository:
        return _names_repo


class ReadManyNames(ReadManyAction):
    """Reads a list of name records from the repository"""

    @property
    def _repository(self) -> Repository:
        return _names_repo


class UpdateOneName(UpdateOneAction):
    """Updates a single Name record in the repository"""

    @property
    def _repository(self) -> Repository:
        return _names_repo


class UpdateManyNames(UpdateManyAction):
    """Updates a list of name records in the repository"""

    @property
    def _repository(self) -> Repository:
        return _names_repo


class DeleteOneName(DeleteOneAction):
    """Deletes a single Name record in the repository"""

    @property
    def _repository(self) -> Repository:
        return _names_repo


class DeleteManyNames(DeleteManyAction):
    """
    Deletes a list of name records in the repository basing on the Criteria passed
    """

    @property
    def _repository(self) -> Repository:
        return _names_repo
