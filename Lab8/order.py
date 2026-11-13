from product import Product
from orderline import OrderLine


class Order:
    """Composition: an Order creates and manages its own OrderLine objects."""

    def __init__(self, order_id: str):
        self.order_id: str = order_id
        self.order_lines: list[OrderLine] = []

    def add_order_line(self, product: Product, quantity: int) -> None:
        if quantity <= 0:
            print("Quantity must be greater than zero.")
            return
        if product.get_stock() < quantity:
            print(f"Not enough stock for product {product.get_name()}. Available stock: {product.get_stock()}.")
            return
        line = OrderLine(product, quantity)   # the Order creates the line itself
        self.order_lines.append(line)
        product.update_stock(product.get_stock() - quantity)

    def remove_order_line(self, product_id: str) -> bool:
        """Remove the line for a product and return its quantity to stock."""
        for line in self.order_lines:
            if line.product.get_product_id() == product_id:
                self.order_lines.remove(line)
                line.product.update_stock(line.product.get_stock() + line.quantity)
                return True
        print(f"No order line found for product {product_id}.")
        return False

    def calculate_total(self) -> float:
        return sum(line.calculate_subtotal() for line in self.order_lines)

    def display_order_summary(self) -> None:
        print(f"Order ID: {self.order_id}")
        print("Order Summary:")
        for line in self.order_lines:
            line.display_line()
        print(f"Total Amount: ${self.calculate_total():.2f}")
