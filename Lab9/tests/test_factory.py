import inspect
import unittest

import OOP_inventory_manager
from digital import DigitalProduct
from physical import PhysicalProduct
from product import Product
from product_factory import ProductFactory
from supplier import Supplier


class TestProductFactory(unittest.TestCase):
    def setUp(self):
        self.supplier = Supplier("SUP001", "Test Supplier", "test@example.com")

    def test_creates_physical_product(self):
        product = ProductFactory.create("physical", "P1", "Lamp", 25.0, 10, self.supplier, weight=2.0)
        self.assertIsInstance(product, PhysicalProduct)
        self.assertIsInstance(product, Product)
        self.assertEqual(product.get_weight(), 2.0)

    def test_creates_digital_product(self):
        product = ProductFactory.create("digital", "D1", "Editor", 49.9, 100, self.supplier, download_size=300.0)
        self.assertIsInstance(product, DigitalProduct)
        self.assertEqual(product.get_download_size(), 300.0)

    def test_type_is_case_and_space_insensitive(self):
        self.assertIsInstance(ProductFactory.create(" Physical ", "P1", "Lamp", 25.0, 1, self.supplier),
                              PhysicalProduct)

    def test_unknown_type_raises_value_error_with_clear_message(self):
        with self.assertRaises(ValueError) as context:
            ProductFactory.create("service", "S1", "Installation", 30.0, 5, self.supplier)
        self.assertEqual(str(context.exception), "Unknown product type: service")

    def test_manager_does_not_create_products_directly(self):
        source = inspect.getsource(OOP_inventory_manager)
        self.assertNotIn("PhysicalProduct(", source)
        self.assertNotIn("DigitalProduct(", source)


if __name__ == "__main__":
    unittest.main()
