import inspect
import unittest

from discount import (BulkDiscount, DiscountStrategy, NoDiscount,
                      PercentageDiscount, StudentDiscount)
from order import Order
from product_factory import ProductFactory
from supplier import Supplier


def make_order(total: float, discount: DiscountStrategy | None = None) -> Order:
    supplier = Supplier("SUP001", "Test Supplier", "test@example.com")
    product = ProductFactory.create("physical", "P1", "Item", total, 10, supplier)
    order = Order("ORD1", discount)
    order.add_order_line(product, 1)
    return order


class TestStrategies(unittest.TestCase):
    def test_no_discount_returns_total_unchanged(self):
        self.assertEqual(NoDiscount().apply(100), 100)

    def test_percentage_discount(self):
        self.assertAlmostEqual(PercentageDiscount(10).apply(250), 225)

    def test_bulk_discount_at_and_above_threshold(self):
        self.assertEqual(BulkDiscount(200, 20).apply(200), 180)
        self.assertEqual(BulkDiscount(200, 20).apply(250), 230)

    def test_bulk_discount_below_threshold(self):
        self.assertEqual(BulkDiscount(200, 20).apply(199.99), 199.99)

    def test_student_discount_is_five_percent(self):
        self.assertAlmostEqual(StudentDiscount().apply(200), 190)

    def test_invalid_percentage_rejected(self):
        with self.assertRaises(ValueError):
            PercentageDiscount(150)

    def test_base_class_cannot_be_instantiated(self):
        with self.assertRaises(TypeError):
            DiscountStrategy()


class TestOrderUsesStrategy(unittest.TestCase):
    def test_default_is_no_discount(self):
        self.assertEqual(make_order(250).calculate_total(), 250)

    def test_order_total_goes_through_strategy(self):
        self.assertEqual(make_order(250, BulkDiscount(200, 20)).calculate_total(), 230)

    def test_set_discount_changes_strategy_on_existing_order(self):
        order = make_order(250, BulkDiscount(200, 20))
        order.set_discount(PercentageDiscount(10))
        self.assertAlmostEqual(order.calculate_total(), 225)

    def test_new_strategy_works_without_changing_order(self):
        class FlatTenOff(DiscountStrategy):          # defined here, Order knows nothing about it
            def apply(self, total: float) -> float:
                return total - 10

        self.assertEqual(make_order(100, FlatTenOff()).calculate_total(), 90)

    def test_one_strategy_object_can_be_shared_by_orders(self):
        shared = PercentageDiscount(10)
        self.assertIs(make_order(100, shared).discount, make_order(200, shared).discount)

    def test_calculate_total_has_no_discount_branching(self):
        source = inspect.getsource(Order.calculate_total)
        self.assertNotIn("if ", source)
        self.assertNotIn("elif", source)


if __name__ == "__main__":
    unittest.main()
