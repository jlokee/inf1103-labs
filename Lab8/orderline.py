from product import Product


class OrderLine:
    """Part of an Order (composition). Should only be created by Order.add_order_line()."""

    def __init__(self, product: Product, quantity: int):
        self.product: Product = product      # association: OrderLine does not own the Product
        self.quantity: int = quantity

    def calculate_subtotal(self) -> float:
        return self.product.get_price() * self.quantity

    def display_line(self) -> None:
        print(f"Product: {self.product.get_name()}, Quantity: {self.quantity}, "
              f"Subtotal: ${self.calculate_subtotal():.2f}")
