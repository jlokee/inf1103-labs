from supplier import Supplier
from product import Product
from canbeship import CanBeShipped


class PhysicalProduct(Product, CanBeShipped):
    def __init__(self, product_id: str, name: str, price: float, stock: int,
                 supplier: Supplier, type: str, weight: float):
        super().__init__(product_id, name, price, stock, supplier)
        self.__type: str = type
        self.__weight: float = weight

    def get_type(self) -> str:
        return self.__type

    def get_weight(self) -> float:
        return self.__weight

    def display_information(self) -> None:
        super().display_information()
        print(f"  Weight: {self.__weight} kg | Shipping Cost: ${self.calculate_shipping_cost():.2f}")

    @staticmethod
    def get_fulfilment_info() -> str:
        return ("This product is a physical item and will require shipping.\n"
                "Shipping cost will be calculated based on the weight of the product.\n"
                "Base Cost: $5.00 | Cost per kg: $2.00")

    def calculate_shipping_cost(self) -> float:
        base_cost = 5.00      # Base shipping cost
        cost_per_kg = 2.00    # Cost per kilogram
        return base_cost + (cost_per_kg * self.__weight)

    def to_dict(self) -> dict:
        product_dict = super().to_dict()
        product_dict["type"] = "physical"
        product_dict["weight"] = self.__weight
        return product_dict
