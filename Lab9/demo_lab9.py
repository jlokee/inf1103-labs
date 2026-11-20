"""Runs the 'Predict first' scenarios from Lab 9 so you can compare output with your predictions."""
from unittest.mock import patch

from discount import BulkDiscount, PercentageDiscount, StudentDiscount
from inventory import Inventory
from order import Order
from OOP_inventory_manager import DEFAULT_SUPPLIER, get_positive_float, load_products
from product_factory import ProductFactory


def heading(title: str) -> None:
    print(f"\n{'=' * 60}\n{title}\n{'=' * 60}")


def demo_strategy() -> None:
    heading("2.3 / 2.4 Strategy: order total of 250")
    product = ProductFactory.create("physical", "P100", "Test Item", 250.0, 5, DEFAULT_SUPPLIER)
    order = Order("ORD100", BulkDiscount(200, 20))
    order.add_order_line(product, 1)
    print("BulkDiscount(200, 20):      ", order.calculate_total())
    order.set_discount(PercentageDiscount(10))
    print("then PercentageDiscount(10):", order.calculate_total())
    order.set_discount(StudentDiscount())
    print("then StudentDiscount():     ", order.calculate_total())


def demo_factory() -> None:
    heading("3.2 Factory: unknown product type")
    try:
        ProductFactory.create("service", "S001", "Installation", 30.0, 5, DEFAULT_SUPPLIER)
    except ValueError as error:
        print(f"ValueError: {error}")


def demo_input() -> None:
    heading("5.1 get_positive_float: abc, -5, 12.50")
    with patch("builtins.input", side_effect=["abc", "-5", "12.50"]):
        print("Returned:", get_positive_float("Price: "))


def demo_loading() -> None:
    heading("5.2 load_products: products.csv")
    inventory = Inventory()
    load_products("products.csv", inventory, DEFAULT_SUPPLIER)
    heading("5.2 load_products: file missing")
    load_products("products_renamed.csv", Inventory(), DEFAULT_SUPPLIER)


if __name__ == "__main__":
    demo_strategy()
    demo_factory()
    demo_input()
    demo_loading()
