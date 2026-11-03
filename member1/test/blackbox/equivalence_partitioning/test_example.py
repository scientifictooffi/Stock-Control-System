"""Technique: Black-box / Equivalence Partitioning
Tool: unittest
Function: stock_control/products/catalogue.py::add_product (P1)
"""
import unittest

from stock_control.products.catalogue import add_product
from stock_control.store import Store


class TestAddProductExample(unittest.TestCase):

    def test_skeleton_raises_not_implemented(self):
        store = Store()
        with self.assertRaises(NotImplementedError):
            add_product(store, "ABC-0001", "Copper pipe", "Plumbing", 9.99)


if __name__ == "__main__":
    unittest.main()
