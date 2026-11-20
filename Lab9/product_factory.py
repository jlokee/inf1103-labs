from product import Product
from physical import PhysicalProduct
from digital import DigitalProduct
from supplier import Supplier


class ProductFactory:
    """Owns the decision of which concrete Product class to build.

    weight is used for physical products and download_size (MB) for digital ones.
    Both default to 0.0 so callers that only have the common fields (e.g. the
    products.csv file) can still create a product.
    """

    @staticmethod
    def create(product_type: str, product_id: str, name: str, price: float,
               stock_quantity: int, supplier: Supplier,
               weight: float = 0.0, download_size: float = 0.0) -> Product:
        kind = str(product_type).strip().lower()
        if kind == "physical":
            return PhysicalProduct(product_id, name, price, stock_quantity, supplier, kind, weight)
        elif kind == "digital":
            return DigitalProduct(product_id, name, price, stock_quantity, supplier, kind, download_size)
        else:
            raise ValueError(f"Unknown product type: {product_type}")
