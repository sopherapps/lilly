"""
Tests for the CRUD actions
"""
import unittest
from unittest.mock import PropertyMock, patch, MagicMock

from lilly.actions import (
    CreateOneAction,
    CreateManyAction,
    ReadOneAction,
    ReadManyAction,
    UpdateOneAction,
    UpdateManyAction,
    DeleteOneAction,
    DeleteManyAction,
)
from test.assets.mock_internals import MockRepository, NameTestDTO


class TestCRUD(unittest.TestCase):
    """Tests for the CRUD actions"""

    def setUp(self) -> None:
        """Initialize some common variables"""
        self.sample_kwargs = {
            "foo": "bar",
            "potato": 8
        }

    @patch("test.assets.mock_internals.MockRepository.create_one")
    @patch("lilly.actions.CreateOneAction._repository", new_callable=PropertyMock)
    def test_create_one_action(self, mock_repo: PropertyMock, mock_create_one: MagicMock):
        """CreateOneAction instance should return the repository's create_one method's response"""
        expected_response = NameTestDTO(id=1, title="Some Name")
        record = {"id": 7}

        mock_create_one.return_value = expected_response
        mock_repo.return_value = MockRepository()

        got = CreateOneAction(record, **self.sample_kwargs).run()

        mock_create_one.assert_called_with(record, **self.sample_kwargs)
        self.assertEqual(expected_response, got)

    @patch("test.assets.mock_internals.MockRepository.create_many")
    @patch("lilly.actions.CreateManyAction._repository", new_callable=PropertyMock)
    def test_create_many_action(self, mock_repo: PropertyMock, mock_create_many: MagicMock):
        """CreateManyAction instance should return the repository's create_many method's response"""
        expected_response = [NameTestDTO(id=1, title="Some Name")]
        records = [{"id": 7}]

        mock_create_many.return_value = expected_response
        mock_repo.return_value = MockRepository()

        got = CreateManyAction(records, **self.sample_kwargs).run()

        mock_create_many.assert_called_with(records, **self.sample_kwargs)
        self.assertListEqual(expected_response, got)

    @patch("test.assets.mock_internals.MockRepository.get_one")
    @patch("lilly.actions.ReadOneAction._repository", new_callable=PropertyMock)
    def test_read_one_action(self, mock_repo: PropertyMock, mock_get_one: MagicMock):
        """ReadOneAction instance should return the repository's get_one method's response"""
        expected_response = NameTestDTO(id=1, title="Some Name")
        record_id = 6

        mock_get_one.return_value = expected_response
        mock_repo.return_value = MockRepository()

        got = ReadOneAction(record_id, **self.sample_kwargs).run()

        mock_get_one.assert_called_with(record_id, **self.sample_kwargs)
        self.assertEqual(expected_response, got)

    @patch("test.assets.mock_internals.MockRepository.get_many")
    @patch("lilly.actions.ReadManyAction._repository", new_callable=PropertyMock)
    def test_read_many_action(self, mock_repo: PropertyMock, mock_get_many: MagicMock):
        """ReadManyAction instance should return the repository's get_many method's response"""
        expected_response = [NameTestDTO(id=1, title="Some Name")]
        criteria = [8, 5]
        filters = {"y": "i", "e": "l", "d": "."}
        skip = 6
        limit = 3

        mock_get_many.return_value = expected_response
        mock_repo.return_value = MockRepository()

        got = ReadManyAction(*criteria, skip=skip, limit=limit, **filters).run()

        mock_get_many.assert_called_with(*criteria, skip=skip, limit=limit, **filters)
        self.assertListEqual(expected_response, got)

    @patch("test.assets.mock_internals.MockRepository.update_one")
    @patch("lilly.actions.UpdateOneAction._repository", new_callable=PropertyMock)
    def test_update_one_action(self, mock_repo: PropertyMock, mock_update_one: MagicMock):
        """UpdateOneAction instance should return the repository's update_one method's response"""
        expected_response = NameTestDTO(id=1, title="Some Name")
        record_id = 6
        new_record = {"i": "j"}

        mock_update_one.return_value = expected_response
        mock_repo.return_value = MockRepository()

        got = UpdateOneAction(record_id, new_record, **self.sample_kwargs).run()

        mock_update_one.assert_called_with(record_id, new_record, **self.sample_kwargs)
        self.assertEqual(expected_response, got)

    @patch("test.assets.mock_internals.MockRepository.update_many")
    @patch("lilly.actions.UpdateManyAction._repository", new_callable=PropertyMock)
    def test_update_many_action(self, mock_repo: PropertyMock, mock_update_many: MagicMock):
        """UpdateManyAction instance should return the repository's update_many method's response"""
        expected_response = [NameTestDTO(id=1, title="Some Name")]
        new_record = {"i": "j"}
        criteria = [8, 5]
        filters = {"y": "i", "e": "l", "d": "."}

        mock_update_many.return_value = expected_response
        mock_repo.return_value = MockRepository()

        got = UpdateManyAction(new_record, *criteria, **filters).run()

        mock_update_many.assert_called_with(new_record, *criteria, **filters)
        self.assertListEqual(expected_response, got)

    @patch("test.assets.mock_internals.MockRepository.remove_one")
    @patch("lilly.actions.DeleteOneAction._repository", new_callable=PropertyMock)
    def test_delete_one_action(self, mock_repo: PropertyMock, mock_remove_one: MagicMock):
        """DeleteOneAction instance should return the repository's remove_one method's response"""
        expected_response = NameTestDTO(id=1, title="Some Name")
        record_id = 6

        mock_remove_one.return_value = expected_response
        mock_repo.return_value = MockRepository()

        got = DeleteOneAction(record_id, **self.sample_kwargs).run()

        mock_remove_one.assert_called_with(record_id, **self.sample_kwargs)
        self.assertEqual(expected_response, got)

    @patch("test.assets.mock_internals.MockRepository.remove_many")
    @patch("lilly.actions.DeleteManyAction._repository", new_callable=PropertyMock)
    def test_update_many_action(self, mock_repo: PropertyMock, mock_remove_many: MagicMock):
        """DeleteManyAction instance should return the repository's remove_many method's response"""
        expected_response = [NameTestDTO(id=1, title="Some Name")]
        criteria = [8, 5]
        filters = {"y": "i", "e": "l", "d": "."}

        mock_remove_many.return_value = expected_response
        mock_repo.return_value = MockRepository()

        got = DeleteManyAction(*criteria, **filters).run()

        mock_remove_many.assert_called_with(*criteria, **filters)
        self.assertListEqual(expected_response, got)


if __name__ == '__main__':
    unittest.main()
