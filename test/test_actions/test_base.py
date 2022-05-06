"""Module to test the Base Action class"""
import unittest

from lilly.actions import Action


class TestAction(unittest.TestCase):
    """Test for the base Action class"""

    def test_run(self):
        """run() should be overridden"""
        self.assertRaises(NotImplementedError, Action().run)


if __name__ == '__main__':
    unittest.main()
