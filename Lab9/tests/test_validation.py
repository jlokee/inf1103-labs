import unittest

from order import Order
from orderline import OrderLine
from product_factory import ProductFactory
from supplier import Supplier


class TestValidation(unittest.TestCase):
    def setUp(self):
        self.supplier = Supplier("SUP001", "Test Supplier", "test@example.com")

    def make(self, product_type="physical", price=10.0, stock=5):
        return ProductFactory.create(product_type, "X1", "Item", price, stock, self.supplier)

    def test_price_must_be_greater_than_zero(self):
        for bad_price in (0, -1, -0.01):
            with self.subTest(price=bad_price):
                with self.assertRaises(ValueError):
                    self.make(price=bad_price)

    def test_initial_stock_cannot_be_negative(self):
        with self.assertRaises(ValueError):
            self.make(stock=-1)

    def test_zero_stock_is_allowed(self):
        self.assertEqual(self.make(stock=0).get_stock(), 0)

    def test_update_stock_rejects_negative_and_keeps_old_value(self):
        product = self.make(stock=5)
        with self.assertRaises(ValueError):
            product.update_stock(-3)
        self.assertEqual(product.get_stock(), 5)

    def test_every_product_type_enforces_the_same_stock_rule(self):
        """LSP: a DigitalProduct must not weaken the rule defined on Product."""
        for product_type in ("physical", "digital"):
            with self.subTest(product_type=product_type):
                with self.assertRaises(ValueError):
                    self.make(product_type, stock=-1)
                with self.assertRaises(ValueError):
                    self.make(product_type).update_stock(-1)

    def test_order_line_quantity_must_be_greater_than_zero(self):
        product = self.make()
        for bad_quantity in (0, -2):
            with self.subTest(quantity=bad_quantity):
                with self.assertRaises(ValueError):
                    OrderLine(product, bad_quantity)

    def test_order_rejects_bad_quantity_and_leaves_stock_alone(self):
        product = self.make(stock=5)
        order = Order("ORD1")
        with self.assertRaises(ValueError):
            order.add_order_line(product, 0)
        self.assertEqual(product.get_stock(), 5)
        self.assertEqual(order.order_lines, [])


if __name__ == "__main__":
    unittest.main()
