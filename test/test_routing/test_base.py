"""
Module containing tests for the base RouteSet
"""
from unittest import main

from unittest import TestCase
from unittest.mock import patch, Mock

from lilly.actions import Action
from lilly.routing import RouteSet


class TestRouteSet(TestCase):
    """Test for the RouteSet class"""

    @patch.object(Action, "run")
    @patch.object(Action, "__init__", return_value=None)
    def test_do(self, mock_action_init: Mock, mock_action_run: Mock):
        """the _do method makes a call to the Action"""
        expected = "foo bar"
        mock_action_run.return_value = expected
        args = ["some", "stuff"]
        kwargs = {"other": "stuff"}

        route_set = RouteSet()
        response = route_set._do(Action, *args, **kwargs)

        mock_action_init.assert_called_with(*args, **kwargs)
        mock_action_run.assert_called_once()
        self.assertEqual(expected, response)


if __name__ == '__main__':
    main()
