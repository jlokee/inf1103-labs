from abc import ABC, abstractmethod
from supplier import Supplier


class Product(ABC):
    def __init__(self, product_id: str, name: str, price: float, stock: int, supplier: Supplier):
        self.__product_id: str = str(product_id)
        self.__name: str = str(name)
        self.__price: float = float(price)
        self.__stock: int = int(stock)
        # Association: the Supplier is created independently and only referenced here
        self.supplier: Supplier = supplier

    def get_product_id(self) -> str:
        return self.__product_id

    @abstractmethod
    def get_type(self) -> str:
        pass

    def get_name(self) -> str:
        return self.__name

    def get_price(self) -> float:
        return self.__price

    def get_stock(self) -> int:
        return self.__stock

    @staticmethod
    @abstractmethod
    def get_fulfilment_info() -> str:
        pass

    def update_stock(self, quantity: int) -> bool:
        """Set the stock level. Returns False (and changes nothing) if quantity is negative."""
        if quantity < 0:
            return False
        self.__stock = quantity
        return True

    def display_information(self) -> None:
        print(f"ID: {self.__product_id} | "
              f"Name: {self.__name} | "
              f"Price: ${self.__price:.2f} | "
              f"Stock: {self.__stock}")
        if self.supplier:
            print(f"  Supplier: {self.supplier.name}")

    def display_details(self, status: str) -> None:
        if status == "update":
            print("Product Found:\n"
                  f"Name: {self.__name}\n"
                  f"Current Stock: {self.__stock}\n")
        else:
            print("Product Found:\n"
                  "---------------------------------\n"
                  f"ID: {self.__product_id}\n"
                  f"Name: {self.__name}\n"
                  f"Price: ${self.__price:.2f}\n"
                  f"Current Stock: {self.__stock}\n"
                  "---------------------------------\n")

    def to_dict(self) -> dict:
        return {
            "product_id": self.__product_id,
            "name": self.__name,
            "price": self.__price,
            "stock": self.__stock,
            "supplier_id": self.supplier.supplier_id if self.supplier else None
        }
