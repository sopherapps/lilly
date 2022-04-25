"""
Module containing actions.
These are the business logic components called by routes to do a specific task by using the _do() call
"""
import random
import string

from pydantic import BaseModel

from lilly.actions import Action

from .repositories import NamesRepository


class GenerateRandomName(Action):
    """
    Generates a random string and persists it in the data source
    """
    _vowels = "aeiou"
    _consonants = "".join(set(string.ascii_lowercase) - set("aeiou"))
    _name_repository = NamesRepository()

    def __init__(self, length: int = 7):
        self._length = length

    def run(self) -> BaseModel:
        """Actual method that is run"""
        name = self._generate_random_word()
        return self._name_repository.create_one({"title": name})

    def _generate_random_word(self):
        """Generates a random word"""
        word = ""
        for i in range(self._length):
            if i % 2 == 0:
                word += random.choice(self._consonants)
            else:
                word += random.choice(self._vowels)
        return word
