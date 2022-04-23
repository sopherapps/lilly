"""Tests for the repository-related code"""

import unittest
from typing import Dict, Any, List

from lilly.repositories import Repository


class TestRepository(unittest.TestCase):
    """Tests related to the repository-related code"""
    def test_required_datasource_attribute(self):
        """Throws AttributeError during initialization if datasource is not set on class"""
        class Sample(Repository):
            pass

        self.assertRaises(AttributeError, Sample)


if __name__ == '__main__':
    unittest.main()