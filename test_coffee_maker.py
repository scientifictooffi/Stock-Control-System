import unittest

from coffee_maker import CoffeeMaker

#test123

# Unit tests for CoffeeMaker class.
class TestCoffeeMaker(unittest.TestCase):

    def test_add_ingredients(self):
        cm = CoffeeMaker()
        cm.add_ingredients(20, 10)
        self.assertEqual(20, cm.get_coffee())
        self.assertEqual(10, cm.get_milk())

    def test_add_ingredients_exception(self):
        cm = CoffeeMaker()
        with self.assertRaises(Exception):
            cm.add_ingredients(4, -1)

    def test_make_espresso_without_ingredients(self):
        cm = CoffeeMaker()
        self.assertEqual(5, cm.make_espresso(5))

    def test_make_latte_without_ingredients(self):
        cm = CoffeeMaker()
        self.assertEqual(5, cm.make_latte(5))

    def test_make_espresso(self):
        cm = CoffeeMaker()
        cm.add_ingredients(10, 10)
        self.assertEqual(4, cm.make_espresso(5))

    def test_make_latte(self):
        cm = CoffeeMaker()
        cm.add_ingredients(10, 10)
        self.assertEqual(3, cm.make_latte(5))

