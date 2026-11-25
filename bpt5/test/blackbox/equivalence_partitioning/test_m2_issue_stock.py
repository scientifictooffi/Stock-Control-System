import unittest
from bpt5.test.m2_fixtures import (
    MAIN_QTY, SKU, TODAY, UNKNOWN_SKU, batch, make_store, snapshot)
from stock_control.movements.issuing import issue_stock


class TestIssueStockValidClasses(unittest.TestCase):
    def setUp(self):
        self.store = make_store()

    def test_valid_class_all_rules_pass(self):
        self.assertEqual(issue_stock(self.store, SKU, 5, "MAIN", TODAY), 5)
        product = self.store.products[SKU]
        self.assertEqual(product.quantity, MAIN_QTY - 5)
        self.assertEqual(product.stock_by_warehouse["MAIN"], MAIN_QTY - 5)

    def test_valid_class_part_order(self):
        self.assertEqual(
            issue_stock(self.store, SKU, 15, "MAIN", TODAY, True), MAIN_QTY)
        self.assertEqual(self.store.products[SKU].stock_by_warehouse["MAIN"],
                         0)

    def test_valid_class_earliest_use_by_first(self):
        issue_stock(self.store, SKU, 3, "MAIN", TODAY)
        self.assertEqual(batch(self.store, "B0002").quantity, 0)
        self.assertEqual(batch(self.store, "B0001").quantity, 4)
        self.assertEqual(batch(self.store, "B0003").quantity, 2)

    def test_valid_class_other_products_untouched(self):
        issue_stock(self.store, SKU, 5, "MAIN", TODAY)
        self.assertEqual(batch(self.store, "B0004").quantity, 5)

    def test_valid_class_saved_in_history(self):
        issue_stock(self.store, SKU, 5, "MAIN", TODAY, user="christen")
        movement = self.store.movements[-1]
        self.assertEqual(
            (movement.sku, movement.movement_type, movement.quantity,
             movement.warehouse, movement.date, movement.user),
            (SKU, "issue", 5, "MAIN", TODAY, "christen"))
        self.assertEqual(movement.reason, "issued from B0002:3, B0001:2")


class TestIssueStockInvalidClasses(unittest.TestCase):
    def setUp(self):
        self.store = make_store()
        self.before = snapshot(self.store)

    def assert_refused(self, error, *args):
        with self.assertRaises(error):
            issue_stock(self.store, *args)
        self.assertEqual(self.store, self.before)

    def test_unknown_product(self):
        self.assert_refused(KeyError, UNKNOWN_SKU, 1, "MAIN", TODAY)

    def test_quantity_not_positive(self):
        self.assert_refused(ValueError, SKU, -2, "MAIN", TODAY)

    def test_quantity_not_whole_number(self):
        self.assert_refused(ValueError, SKU, 2.5, "MAIN", TODAY)

    def test_quantity_is_text(self):
        self.assert_refused(ValueError, SKU, "3", "MAIN", TODAY)

    def test_quantity_not_int(self):
        self.assert_refused(ValueError, SKU, True, "MAIN", TODAY)

    def test_unknown_warehouse(self):
        self.assert_refused(ValueError, SKU, 1, "EAST", TODAY)

    def test_not_enough_stock(self):
        self.assert_refused(ValueError, SKU, 15, "MAIN", TODAY)

    def test_part_order_with_no_stock(self):
        self.assert_refused(ValueError, SKU, 1, "NORTH", TODAY, True)


if __name__ == "__main__":
    unittest.main()
