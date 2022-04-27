import unittest

from lilly import Lilly, conf
from fastapi.testclient import TestClient


class TestLilly(unittest.TestCase):
    """Tests for the Lilly class"""

    def setUp(self) -> None:
        """Initialize some common variables"""
        self.app = Lilly(settings_path="assets.mock_settings", services_path="assets.mock_services")

    def test_mount(self):
        """A call to mount should raise NotImplementedError exception"""
        another_app = Lilly(settings_path="assets.mock_settings", services_path="assets.mock_services")
        self.assertRaises(NotImplementedError, self.app.mount, "/another", another_app)

    def test_register_settings(self):
        """Initializing the app with a given path to the settings module registers its settings"""
        self.assertEqual(conf.settings.TEST_APP, "True")

    def test_register_services(self):
        """Initializing the app with a given import path to the services package registers the routes in each service"""
        client = TestClient(app=self.app)
        name = "Joe"
        headers = {"Content-Type": "application/json"}
        expected = {"message": f"Hi {name}"}

        first_service_response = client.get(f"/first/{name}", headers=headers).json()
        second_service_response = client.get(f"/second/{name}", headers=headers).json()

        self.assertDictEqual(first_service_response, expected)
        self.assertDictEqual(second_service_response, expected)


if __name__ == '__main__':
    unittest.main()
