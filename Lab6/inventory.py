from product import Product


class Inventory:
    def __init__(self):
        self.__products = []

    def add_product(self, product: Product):
        existing_product = self.search_product(product.get_product_id())
        if existing_product:
            print(f"Product with ID {product.get_product_id()} already exists. Updating stock instead.")
            self.update_stock(existing_product.get_product_id(), product.get_stock())
        else:
            self.__products.append(product)


    def search_product(self, product_id: str):
        for product in self.__products:
            if product.get_product_id() == product_id:
                return product
        return None

    def display_inventory(self):
        if not self.__products:
            print("Inventory is empty.")
            return
        print("Current Inventory:\n")
        for product in self.__products:
            product.display_product_info()

    def get_inventory(self):
        return list(self.__products)

    def __len__(self):
        return len(self.__products)