"""
Unit tests for main.py
"""
import unittest
from src.main import add, is_number

class TestMain(unittest.TestCase):
    """
    Test cases for main.py
    """
    def test_is_number(self):
        """
        Test is_number function
        :return:
        """
        self.assertTrue(is_number('1'))
        self.assertTrue(is_number('1.0'))
        self.assertTrue(is_number('1.0e-10'))
        self.assertFalse(is_number('a'))
        self.assertFalse(is_number('1a'))

    def test_add(self):
        """
        Test add function
        """
        self.assertEqual(add('1', '2', '3'), 6)
        self.assertEqual(add('1.0', '2.0', '3.0'), 6)
        self.assertEqual(add('1', '2', 'a'), 'Error: arguments must be numbers')
        self.assertEqual(add('1', '2', '3a'), 'Error: arguments must be numbers')

