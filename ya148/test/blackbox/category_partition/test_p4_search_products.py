import unittest

from stock_control.models import Category, Product
from stock_control.products.search import search_products
from stock_control.store import Store


def make_store():
    store = Store()
    store.categories["Plumbing"] = Category("Plumbing")
    store.categories["Tools"] = Category("Tools")
    store.products["PIP-0001"] = Product("PIP-0001", "Copper pipe",
                                         "Plumbing", 8.5, 4.0, 40,
                                         min_level=5)
    store.products["TAP-0001"] = Product("TAP-0001", "Brass tap",
                                         "Plumbing", 12.0, 6.0, 3,
                                         min_level=5)
    store.products["DRL-0001"] = Product("DRL-0001", "Cordless drill",
                                         "Tools", 89.0, 55.0, 0,
                                         min_level=1)
    store.products["CUT-0001"] = Product("CUT-0001", "Pipe cutter",
                                         "Tools", 15.0, 7.0, 10,
                                         min_level=5)
    store.products["OLD-0001"] = Product("OLD-0001", "Old pipe valve",
                                         "Plumbing", 3.0, 1.0, 9,
                                         status="archived")
    return store


def names(products):
    return [product.name for product in products]


class TestSearchProductsCategoryPartition(unittest.TestCase):

    def test_frame_01_name_not_string_error(self):
        with self.assertRaises(ValueError):
            search_products(make_store(), 12)

    def test_frame_02_unknown_category_error(self):
        with self.assertRaises(ValueError):
            search_products(make_store(), category="Garden")

    def test_frame_03_min_above_max_error(self):
        with self.assertRaises(ValueError):
            search_products(make_store(), min_price=50, max_price=10)

    def test_frame_04_negative_price_error(self):
        with self.assertRaises(ValueError):
            search_products(make_store(), max_price=-5)

    def test_frame_05_name_no_match_single(self):
        with self.assertRaises(LookupError):
            search_products(make_store(), "hammer")

    def test_frame_06_min_only_single(self):
        self.assertEqual(["Cordless drill", "Pipe cutter"],
                         names(search_products(make_store(), min_price=15)))

    def test_frame_07_max_only_single(self):
        self.assertEqual(["Brass tap", "Copper pipe"],
                         names(search_products(make_store(), max_price=12)))

    def test_frame_08_low_single(self):
        self.assertEqual(["Brass tap"],
                         names(search_products(make_store(),
                                               availability="low")))

    def test_frame_09_empty_none_none_none(self):
        self.assertEqual(4, len(search_products(make_store())))

    def test_frame_10_empty_none_none_in_stock(self):
        self.assertEqual(["Copper pipe", "Pipe cutter"],
                         names(search_products(make_store(),
                                               availability="in_stock")))

    def test_frame_11_empty_none_none_out(self):
        self.assertEqual(["Cordless drill"],
                         names(search_products(make_store(),
                                               availability="out")))

    def test_frame_12_empty_none_range_none(self):
        self.assertEqual(["Brass tap", "Copper pipe", "Pipe cutter"],
                         names(search_products(make_store(), min_price=5,
                                               max_price=20)))

    def test_frame_13_empty_none_range_in_stock(self):
        self.assertEqual(["Copper pipe", "Pipe cutter"],
                         names(search_products(make_store(), min_price=5,
                                               max_price=20,
                                               availability="in_stock")))

    def test_frame_14_empty_none_range_out(self):
        with self.assertRaises(LookupError):
            search_products(make_store(), min_price=5, max_price=20,
                            availability="out")

    def test_frame_15_empty_cat_none_none(self):
        self.assertEqual(["Brass tap", "Copper pipe"],
                         names(search_products(make_store(),
                                               category="Plumbing")))

    def test_frame_16_empty_cat_none_in_stock(self):
        self.assertEqual(["Copper pipe"],
                         names(search_products(make_store(),
                                               category="Plumbing",
                                               availability="in_stock")))

    def test_frame_17_empty_cat_none_out(self):
        self.assertEqual(["Cordless drill"],
                         names(search_products(make_store(),
                                               category="Tools",
                                               availability="out")))

    def test_frame_18_empty_cat_range_none(self):
        self.assertEqual(["Pipe cutter"],
                         names(search_products(make_store(),
                                               category="Tools", min_price=10,
                                               max_price=20)))

    def test_frame_19_empty_cat_range_in_stock(self):
        self.assertEqual(["Pipe cutter"],
                         names(search_products(make_store(),
                                               category="Tools", min_price=10,
                                               max_price=20,
                                               availability="in_stock")))

    def test_frame_20_empty_cat_range_out(self):
        self.assertEqual(["Cordless drill"],
                         names(search_products(make_store(),
                                               category="Tools", min_price=50,
                                               max_price=100,
                                               availability="out")))

    def test_frame_21_part_none_none_none(self):
        self.assertEqual(["Copper pipe", "Pipe cutter"],
                         names(search_products(make_store(), "pipe")))

    def test_frame_22_part_none_none_in_stock(self):
        self.assertEqual(["Copper pipe", "Pipe cutter"],
                         names(search_products(make_store(), "pipe",
                                               availability="in_stock")))

    def test_frame_23_part_none_none_out(self):
        self.assertEqual(["Cordless drill"],
                         names(search_products(make_store(), "drill",
                                               availability="out")))

    def test_frame_24_part_none_range_none(self):
        self.assertEqual(["Pipe cutter"],
                         names(search_products(make_store(), "pipe",
                                               min_price=10, max_price=20)))

    def test_frame_25_part_none_range_in_stock(self):
        self.assertEqual(["Copper pipe"],
                         names(search_products(make_store(), "pipe",
                                               min_price=0, max_price=10,
                                               availability="in_stock")))

    def test_frame_26_part_none_range_out(self):
        with self.assertRaises(LookupError):
            search_products(make_store(), "pipe", min_price=0,
                            max_price=100, availability="out")

    def test_frame_27_part_cat_none_none(self):
        self.assertEqual(["Copper pipe"],
                         names(search_products(make_store(), "pipe",
                                               "Plumbing")))

    def test_frame_28_part_cat_none_in_stock(self):
        self.assertEqual(["Copper pipe"],
                         names(search_products(make_store(), "pipe",
                                               "Plumbing",
                                               availability="in_stock")))

    def test_frame_29_part_cat_none_out(self):
        with self.assertRaises(LookupError):
            search_products(make_store(), "tap", "Plumbing",
                            availability="out")

    def test_frame_30_part_cat_range_none(self):
        self.assertEqual(["Brass tap"],
                         names(search_products(make_store(), "tap",
                                               "Plumbing", 10, 20)))

    def test_frame_31_part_cat_range_in_stock(self):
        self.assertEqual(["Pipe cutter"],
                         names(search_products(make_store(), "cutter",
                                               "Tools", 10, 20, "in_stock")))

    def test_frame_32_part_cat_range_out(self):
        self.assertEqual(["Cordless drill"],
                         names(search_products(make_store(), "drill",
                                               "Tools", 50, 100, "out")))


if __name__ == "__main__":
    unittest.main()
