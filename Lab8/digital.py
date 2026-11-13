from supplier import Supplier
from product import Product


class DigitalProduct(Product):
    def __init__(self, product_id: str, name: str, price: float, stock: int,
                 supplier: Supplier, type: str, download_size: float):
        super().__init__(product_id, name, price, stock, supplier)
        self.__download_size: float = download_size  # in MB
        self.__type: str = type

    def get_download_size(self) -> float:
        return self.__download_size

    def get_type(self) -> str:
        return self.__type

    def display_information(self) -> None:
        super().display_information()
        print(f"  Download Size: {self.__download_size} MB")

    @staticmethod
    def get_fulfilment_info() -> str:
        return "This product is a digital item and will be delivered digitally, to be downloaded."

    def to_dict(self) -> dict:
        product_dict = super().to_dict()
        product_dict["type"] = "digital"
        product_dict["download_size"] = self.__download_size
        return product_dict
