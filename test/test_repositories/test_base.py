"""Tests for the base Repository class"""

import unittest
from unittest.mock import MagicMock, PropertyMock, patch, call

from lilly.datasources import DataSource
from lilly.repositories import Repository
from test.assets.mock_internals import MockConnectionContextManager


class TestRepository(unittest.TestCase):
    """Tests related to the repository-related code"""

    def setUp(self) -> None:
        """Initialize some common variables"""
        self.connection = "connected"
        self.mock_datasource = DataSource()
        self.mock_datasource.connect = MagicMock(return_value=MockConnectionContextManager(self.connection))

    @patch("lilly.repositories.Repository._datasource", new_callable=PropertyMock)
    def test_get_one(self, mock_repo_datasource: PropertyMock):
        """get_one calls _get_one with datasource_connection got from self._datasource.connect()"""
        mock_repo_datasource.return_value = self.mock_datasource
        item = "_get_one"
        item_dto = "to_output_dto"
        record_id = 34

        mock_repo = Repository()
        mock_repo._to_output_dto = MagicMock(return_value=item_dto)
        mock_repo._get_one = MagicMock(return_value=item)
        random_kwargs = {"hello": "world", "yei": "yoohoo"}

        value = mock_repo.get_one(record_id=record_id, **random_kwargs)

        mock_repo._get_one.assert_called_with(self.connection, record_id=record_id, **random_kwargs)
        mock_repo._to_output_dto.assert_called_with(item)
        self.assertEqual(value, item_dto)

    @patch("lilly.repositories.Repository._datasource", new_callable=PropertyMock)
    def test_get_many(self, mock_repo_datasource: PropertyMock):
        """get_many calls _get_many with datasource_connection got from self._datasource.connect()"""
        mock_repo_datasource.return_value = self.mock_datasource
        items = ["_get_many", "_another"]
        item_dto = "to_output_dto"

        mock_repo = Repository()
        mock_repo._to_output_dto = MagicMock(return_value=item_dto)
        mock_repo._get_many = MagicMock(return_value=items)
        random_kwargs = {"hello": "world", "yei": "yoohoo"}
        skip = 6
        limit = 4
        filters = {"some": "stuff"}

        values = mock_repo.get_many(skip=skip, limit=limit, filters=filters, **random_kwargs)

        mock_repo._get_many.assert_called_with(self.connection, skip=skip, limit=limit, filters=filters,
                                               **random_kwargs)
        mock_repo._to_output_dto.assert_has_calls([call(item) for item in items])
        self.assertListEqual(values, [item_dto for _ in items])

    @patch("lilly.repositories.Repository._datasource", new_callable=PropertyMock)
    def test_update_one(self, mock_repo_datasource: PropertyMock):
        """update_one calls _update_one with datasource_connection got from self._datasource.connect()"""
        mock_repo_datasource.return_value = self.mock_datasource
        item = "_update_one"
        item_dto = "to_output_dto"
        record_id = 34

        mock_repo = Repository()
        mock_repo._to_output_dto = MagicMock(return_value=item_dto)
        mock_repo._update_one = MagicMock(return_value=item)
        random_kwargs = {"hello": "world", "yei": "yoohoo"}
        new_record = "stuff"

        value = mock_repo.update_one(record_id=record_id, new_record=new_record, **random_kwargs)

        mock_repo._update_one.assert_called_with(
            self.connection, record_id=record_id, new_record=new_record, **random_kwargs)
        mock_repo._to_output_dto.assert_called_with(item)
        self.assertEqual(value, item_dto)

    @patch("lilly.repositories.Repository._datasource", new_callable=PropertyMock)
    def test_update_many(self, mock_repo_datasource: PropertyMock):
        """update_many calls _update_many with datasource_connection got from self._datasource.connect()"""
        mock_repo_datasource.return_value = self.mock_datasource
        items = ["_update_many", "_another"]
        item_dto = "to_output_dto"

        mock_repo = Repository()
        mock_repo._to_output_dto = MagicMock(return_value=item_dto)
        mock_repo._update_many = MagicMock(return_value=items)
        random_kwargs = {"hello": "world", "yei": "yoohoo"}
        new_record = "stuff"
        filters = {"some": "stuff"}

        values = mock_repo.update_many(new_record=new_record, filters=filters, **random_kwargs)

        mock_repo._update_many.assert_called_with(
            self.connection, new_record, filters=filters, **random_kwargs)
        mock_repo._to_output_dto.assert_has_calls([call(item) for item in items])
        self.assertListEqual(values, [item_dto for _ in items])

    @patch("lilly.repositories.Repository._datasource", new_callable=PropertyMock)
    def test_remove_one(self, mock_repo_datasource: PropertyMock):
        """remove_one calls _remove_one with datasource_connection got from self._datasource.connect()"""
        mock_repo_datasource.return_value = self.mock_datasource
        item = "_delete_one"
        item_dto = "to_output_dto"
        record_id = 34

        mock_repo = Repository()
        mock_repo._to_output_dto = MagicMock(return_value=item_dto)
        mock_repo._remove_one = MagicMock(return_value=item)
        random_kwargs = {"hello": "world", "yei": "yoohoo"}

        value = mock_repo.remove_one(record_id=record_id, **random_kwargs)

        mock_repo._remove_one.assert_called_with(self.connection, record_id=record_id, **random_kwargs)
        mock_repo._to_output_dto.assert_called_with(item)
        self.assertEqual(value, item_dto)

    @patch("lilly.repositories.Repository._datasource", new_callable=PropertyMock)
    def test_remove_many(self, mock_repo_datasource: PropertyMock):
        """remove_many calls _remove_many with datasource_connection got from self._datasource.connect()"""
        mock_repo_datasource.return_value = self.mock_datasource
        items = ["_remove_many", "_another"]
        item_dto = "to_output_dto"

        mock_repo = Repository()
        mock_repo._to_output_dto = MagicMock(return_value=item_dto)
        mock_repo._remove_many = MagicMock(return_value=items)
        random_kwargs = {"hello": "world", "yei": "yoohoo"}
        filters = {"some": "stuff"}

        values = mock_repo.remove_many(filters=filters, **random_kwargs)

        mock_repo._remove_many.assert_called_with(self.connection, filters=filters, **random_kwargs)
        mock_repo._to_output_dto.assert_has_calls([call(item) for item in items])
        self.assertListEqual(values, [item_dto for _ in items])

    @patch("lilly.repositories.Repository._datasource", new_callable=PropertyMock)
    def test_create_one(self, mock_repo_datasource: PropertyMock):
        """create_one calls _create_one with datasource_connection got from self._datasource.connect()"""
        mock_repo_datasource.return_value = self.mock_datasource
        item = "_create_one"
        item_dto = "to_output_dto"

        mock_repo = Repository()
        mock_repo._to_output_dto = MagicMock(return_value=item_dto)
        mock_repo._create_one = MagicMock(return_value=item)
        random_kwargs = {"hello": "world", "yei": "yoohoo"}

        value = mock_repo.create_one(record=item, **random_kwargs)

        mock_repo._create_one.assert_called_with(self.connection, record=item, **random_kwargs)
        mock_repo._to_output_dto.assert_called_with(item)
        self.assertEqual(value, item_dto)

    @patch("lilly.repositories.Repository._datasource", new_callable=PropertyMock)
    def test_create_many(self, mock_repo_datasource: PropertyMock):
        """create_many calls _create_many with datasource_connection got from self._datasource.connect()"""
        mock_repo_datasource.return_value = self.mock_datasource
        items = ["_create_many", "_another"]
        item_dto = "to_output_dto"

        mock_repo = Repository()
        mock_repo._to_output_dto = MagicMock(return_value=item_dto)
        mock_repo._create_many = MagicMock(return_value=items)
        random_kwargs = {"hello": "world", "yei": "yoohoo"}

        values = mock_repo.create_many(records=items, **random_kwargs)

        mock_repo._create_many.assert_called_with(self.connection, records=items, **random_kwargs)
        mock_repo._to_output_dto.assert_has_calls([call(item) for item in items])
        self.assertListEqual(values, [item_dto for _ in items])

    def test_required_datasource_attribute(self):
        """Throws NotImplementedError when used without _datasource defined on the class"""
        mock_repo = Repository()
        mock_repo._to_output_dto = MagicMock(return_value="to_output_dto")

        self.assertRaises(NotImplementedError, mock_repo.get_one, 1)

    @patch("lilly.repositories.Repository._datasource", new_callable=PropertyMock)
    def test_required_to_output_dto(self, mock_repo_datasource: PropertyMock):
        """Throws NotImplementedError when used without to_output_dto defined on the class"""
        mock_repo_datasource.return_value = self.mock_datasource
        mock_repo = Repository()
        self.assertRaises(NotImplementedError, mock_repo.get_one, 1)


if __name__ == '__main__':
    unittest.main()
