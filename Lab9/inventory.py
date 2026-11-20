from product import Product


class Inventory:
    """Aggregation: holds references to Product objects but does not own their lifecycle."""

    def __init__(self):
        self.products: list[Product] = []

    def add_product(self, product: Product) -> None:
        existing_product = self.find_product(product.get_product_id())
        if existing_product:
            print(f"Product with ID {product.get_product_id()} already exists. Updating stock instead.")
            existing_product.update_stock(product.get_stock())
        else:
            self.products.append(product)

    def find_product(self, product_id: str) -> Product | None:
        for product in self.products:
            if product.get_product_id() == product_id:
                return product
        return None

    def display_inventory(self) -> None:
        if not self.products:
            print("Inventory is empty.")
            return
        print("Current Inventory:\n")
        for product in self.products:
            product.display_information()

    def get_inventory(self) -> list[Product]:
        return list(self.products)

    def remove_product(self, product_id: str) -> Product | None:
        """Remove the reference from this inventory and return the Product.

        The Product itself is NOT destroyed - the caller can keep using it
        or add it to another Inventory.
        """
        product = self.find_product(product_id)
        if product:
            self.products.remove(product)
            print(f"Product with ID {product_id} has been removed from the inventory.")
        else:
            print(f"No product found with ID {product_id}.")
        return product

    def __len__(self) -> int:
        return len(self.products)
