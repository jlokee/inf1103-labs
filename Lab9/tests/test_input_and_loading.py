import contextlib
import io
import os
import tempfile
import unittest
from unittest.mock import patch

from inventory import Inventory
from OOP_inventory_manager import get_positive_float, load_products
from supplier import Supplier

CSV_TEXT = """product_type,product_id,name,price,stock_quantity
physical,P001,Desk Lamp,25.00,10
digital,D001,Photo Editor,49.90,100
service,S001,Installation,30.00,5
physical,P002,Office Chair,abc,3
physical,P003,Monitor Stand,39.50,7
"""


def run_quietly(func, *args):
    """Run func, returning everything it printed."""
    buffer = io.StringIO()
    with contextlib.redirect_stdout(buffer):
        func(*args)
    return buffer.getvalue()


class TestGetPositiveFloat(unittest.TestCase):
    def test_asks_again_until_valid(self):
        buffer = io.StringIO()
        with patch("builtins.input", side_effect=["abc", "-5", "12.50"]), contextlib.redirect_stdout(buffer):
            result = get_positive_float("Price: ")
        self.assertEqual(result, 12.5)
        self.assertEqual(buffer.getvalue().splitlines(),
                         ["Please enter a valid number, e.g. 12.50",
                          "Please enter a number greater than zero."])

    def test_zero_is_rejected(self):
        with patch("builtins.input", side_effect=["0", "3"]), contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(get_positive_float("Price: "), 3.0)


class TestLoadProducts(unittest.TestCase):
    def setUp(self):
        self.supplier = Supplier("SUP001", "Test Supplier", "test@example.com")
        self.inventory = Inventory()
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.path = os.path.join(self.directory.name, "products.csv")
        with open(self.path, "w", newline="") as file:
            file.write(CSV_TEXT)

    def test_valid_rows_load_and_bad_rows_are_skipped(self):
        output = run_quietly(load_products, self.path, self.inventory, self.supplier)
        self.assertEqual(len(self.inventory), 3)
        for product_id in ("P001", "D001", "P003"):
            self.assertIsNotNone(self.inventory.find_product(product_id))
        self.assertIsNone(self.inventory.find_product("S001"))
        self.assertIsNone(self.inventory.find_product("P002"))
        self.assertIn("Unknown product type: service", output)
        self.assertIn("3 products loaded.", output)

    def test_finally_message_prints_last(self):
        output = run_quietly(load_products, self.path, self.inventory, self.supplier)
        self.assertEqual(output.splitlines()[-1], "Load attempt finished.")

    def test_missing_file_is_handled_without_crashing(self):
        missing = os.path.join(self.directory.name, "nope.csv")
        output = run_quietly(load_products, missing, self.inventory, self.supplier)
        self.assertIn(f"Products file not found: {missing}", output)
        self.assertIn("Load attempt finished.", output)
        self.assertNotIn("products loaded", output)
        self.assertEqual(len(self.inventory), 0)


if __name__ == "__main__":
    unittest.main()
