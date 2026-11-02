class Product:
    def __init__(self, product_id: str, name: str, price: float, stock: int):
        self.__product_id = str(product_id)
        self.__name = str(name)
        self.__price = float(price)
        self.__stock = int(stock)

    def get_product_id(self):
        return self.__product_id


    def get_name(self):
        return self.__name

    def get_price(self):
        return self.__price

    def get_stock(self):
        return self.__stock

    def update_stock(self, quantity: int):
        if quantity < 0:
            return False
        self.__stock = quantity
        return True

    def display_product_info(self):
        print(f"ID: {self.__product_id} | "
              f"Name: {self.__name} | "
              f"Price: ${self.__price:.2f} | "
              f"Stock: {self.__stock}")

    def display_details(self):
        print ("Product Found:\n"
                f"Name: {self.__name}\n"
                f"Current Stock: {self.__stock}\n")

    def to_dict(self):
        return {
            "product_id": self.__product_id,
            "name": self.__name,
            "price": self.__price,
            "stock": self.__stock
        }