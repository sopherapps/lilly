"""
Module for testing the CRUDRouteSet
"""
import json
import unittest
from unittest.mock import patch, PropertyMock, MagicMock

from fastapi.testclient import TestClient

from lilly import Lilly
from test.assets.mock_internals import NameTestDTO, MockRepository, NameTestCreationDTO
from test.assets.mock_services.crud.routes import MockCRUDRouteSet


class TestCRUDRouteSet(unittest.TestCase):
    """Tests for the CRUD RouteSet"""

    def setUp(self):
        """Initialize some common variables"""
        self.headers = {
            "Content-Type": "application/json"
        }
        # importing this registers it with the router
        self.mock_route_set_cls = MockCRUDRouteSet
        self.route_settings = self.mock_route_set_cls.get_settings()

    @patch("lilly.applications.Lilly._register_routes")
    @patch("lilly.applications.Lilly._register_settings")
    @patch("test.assets.mock_internals.MockRepository.create_one")
    @patch("lilly.actions.CreateOneAction._repository", new_callable=PropertyMock)
    def test_create_one_action(self, mock_repo: PropertyMock, mock_create_one: MagicMock, *args):
        """The call to create one should return the repository's create_one method's response"""
        app = Lilly()
        client = TestClient(app=app)
        expected_response = NameTestDTO(id=1, title="Some Name")
        request = NameTestCreationDTO(title="Some Name")

        mock_create_one.return_value = expected_response
        mock_repo.return_value = MockRepository()

        response_json = client.post(
            f"{self.route_settings.base_path}/", data=request.json(), headers=self.headers).json()

        got = NameTestDTO(**response_json)

        mock_create_one.assert_called_with(request)
        self.assertEqual(expected_response, got)

    @patch("lilly.applications.Lilly._register_routes")
    @patch("lilly.applications.Lilly._register_settings")
    @patch("test.assets.mock_internals.MockRepository.create_many")
    @patch("lilly.actions.CreateManyAction._repository", new_callable=PropertyMock)
    def test_create_many_action(self, mock_repo: PropertyMock, mock_create_many: MagicMock, *args):
        """The call to create many should return the repository's create_many method's response"""
        app = Lilly()
        client = TestClient(app=app)
        expected_response = [NameTestDTO(id=1, title="Some Name")]
        request = [NameTestCreationDTO(title="Some Name")]
        request_json = json.dumps([record.dict() for record in request])

        mock_create_many.return_value = expected_response
        mock_repo.return_value = MockRepository()

        response_json = client.post(
            f"{self.route_settings.base_path_for_multiple_items}/",
            data=request_json, headers=self.headers).json()

        got = [NameTestDTO(**record) for record in response_json]

        mock_create_many.assert_called_with(request)
        self.assertListEqual(expected_response, got)

    @patch("lilly.applications.Lilly._register_routes")
    @patch("lilly.applications.Lilly._register_settings")
    @patch("test.assets.mock_internals.MockRepository.get_one")
    @patch("lilly.actions.ReadOneAction._repository", new_callable=PropertyMock)
    def test_read_one_action(self, mock_repo: PropertyMock, mock_get_one: MagicMock, *args):
        """A call to read one  should return the repository's get_one method's response"""
        app = Lilly()
        client = TestClient(app=app)
        expected_response = NameTestDTO(id=1, title="Some Name")
        record_id = 6

        mock_get_one.return_value = expected_response
        mock_repo.return_value = MockRepository()

        response_json = client.get(f"{self.route_settings.base_path}/{record_id}", headers=self.headers).json()

        got = NameTestDTO(**response_json)

        mock_get_one.assert_called_with(record_id)
        self.assertEqual(expected_response, got)

    @patch("lilly.applications.Lilly._register_routes")
    @patch("lilly.applications.Lilly._register_settings")
    @patch("test.assets.mock_internals.MockRepository.get_many")
    @patch("lilly.actions.ReadManyAction._repository", new_callable=PropertyMock)
    def test_read_many_action(self, mock_repo: PropertyMock, mock_get_many: MagicMock, *args):
        """A call to the read many action should return the repository's get_many method's response"""
        app = Lilly()
        client = TestClient(app=app)
        expected_response = [NameTestDTO(id=1, title="Some Name")]
        q = "doe"
        skip = 6
        limit = 3

        mock_get_many.return_value = expected_response
        mock_repo.return_value = MockRepository()

        response_json = client.get(f"{self.route_settings.base_path}/?skip={skip}&limit={limit}&q={q}",
                                   headers=self.headers).json()

        got = [NameTestDTO(**record) for record in response_json]

        mock_get_many.assert_called_with(f"title LIKE '%{q}%'", skip=skip, limit=limit)
        self.assertListEqual(expected_response, got)

    @patch("lilly.applications.Lilly._register_routes")
    @patch("lilly.applications.Lilly._register_settings")
    @patch("test.assets.mock_internals.MockRepository.update_one")
    @patch("lilly.actions.UpdateOneAction._repository", new_callable=PropertyMock)
    def test_update_one_action(self, mock_repo: PropertyMock, mock_update_one: MagicMock, *args):
        """Call to update one should return the repository's update_one method's response"""
        app = Lilly()
        client = TestClient(app=app)
        expected_response = NameTestDTO(id=1, title="Some Name")
        record_id = 6
        new_record = NameTestDTO(id=1, title="Some Change")

        mock_update_one.return_value = expected_response
        mock_repo.return_value = MockRepository()

        response_json = client.put(
            f"{self.route_settings.base_path}/{record_id}", data=new_record.json(), headers=self.headers).json()

        got = NameTestDTO(**response_json)

        mock_update_one.assert_called_with(record_id, new_record)
        self.assertEqual(expected_response, got)

    @patch("lilly.applications.Lilly._register_routes")
    @patch("lilly.applications.Lilly._register_settings")
    @patch("test.assets.mock_internals.MockRepository.update_many")
    @patch("lilly.actions.UpdateManyAction._repository", new_callable=PropertyMock)
    def test_update_many_action(self, mock_repo: PropertyMock, mock_update_many: MagicMock, *args):
        """A call to the update many action should return the repository's update_many method's response"""
        app = Lilly()
        client = TestClient(app=app)
        expected_response = [NameTestDTO(id=1, title="Some Name")]
        new_record = NameTestCreationDTO(title="Some Change")
        q = "doe"

        mock_update_many.return_value = expected_response
        mock_repo.return_value = MockRepository()

        response_json = client.put(f"{self.route_settings.base_path_for_multiple_items}/?q={q}",
                                   data=new_record.json(),
                                   headers=self.headers).json()

        got = [NameTestDTO(**record) for record in response_json]

        mock_update_many.assert_called_with(new_record, f"title LIKE '%{q}%'")
        self.assertListEqual(expected_response, got)

    @patch("lilly.applications.Lilly._register_routes")
    @patch("lilly.applications.Lilly._register_settings")
    @patch("test.assets.mock_internals.MockRepository.remove_one")
    @patch("lilly.actions.DeleteOneAction._repository", new_callable=PropertyMock)
    def test_delete_one_action(self, mock_repo: PropertyMock, mock_remove_one: MagicMock, *args):
        """A call to delete one should return the repository's remove_one method's response"""
        app = Lilly()
        client = TestClient(app=app)
        expected_response = NameTestDTO(id=1, title="Some Name")
        record_id = 6

        mock_remove_one.return_value = expected_response
        mock_repo.return_value = MockRepository()

        response_json = client.delete(f"{self.route_settings.base_path}/{record_id}", headers=self.headers).json()

        got = NameTestDTO(**response_json)

        mock_remove_one.assert_called_with(record_id)
        self.assertEqual(expected_response, got)

    @patch("lilly.applications.Lilly._register_routes")
    @patch("lilly.applications.Lilly._register_settings")
    @patch("test.assets.mock_internals.MockRepository.remove_many")
    @patch("lilly.actions.DeleteManyAction._repository", new_callable=PropertyMock)
    def test_delete_many_action(self, mock_repo: PropertyMock, mock_remove_many: MagicMock, *args):
        """A call to delete many should return the repository's remove_many method's response"""
        app = Lilly()
        client = TestClient(app=app)
        expected_response = [NameTestDTO(id=1, title="Some Name")]
        q = "doe"

        mock_remove_many.return_value = expected_response
        mock_repo.return_value = MockRepository()

        response_json = client.delete(
            f"{self.route_settings.base_path_for_multiple_items}/?q={q}", headers=self.headers).json()

        got = [NameTestDTO(**record) for record in response_json]

        mock_remove_many.assert_called_with(f"title LIKE '%{q}%'")
        self.assertListEqual(expected_response, got)


if __name__ == '__main__':
    unittest.main()
