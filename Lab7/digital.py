from product import Product

class DigitalProduct(Product):
    def __init__(self, product_id: str, name: str, price: float, stock: int, type: str, download_size: float):
        super().__init__(product_id, name, price, stock)
        self.__download_size = download_size  # in MB
        self.__type = type

    def get_download_size(self) -> float:
        return self.__download_size

    def get_type(self) -> str:
        return self.__type

    def display_product_info(self):
        super().display_product_info()
        print(f" | Download Size: {self.__download_size} MB")

    @staticmethod
    def get_fulfilment_info():
        return "This product is a digital item and will be delivered digitally, to be downloaded."

    def to_dict(self):
        product_dict = super().to_dict()
        product_dict["type"] = "digital"
        product_dict["download_size"] = self.__download_size
        return product_dict