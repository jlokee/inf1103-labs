import json
from digital import DigitalProduct
from physical import PhysicalProduct
from inventory import Inventory
from supplier import Supplier

FILE_NAME = "OOP_inventory.json"
DEFAULT_SUPPLIER = Supplier("SUP001", "Global Tech WholeSale", "supply@globaltech.com")


def load_inventory(inventory: Inventory) -> bool:
    try:
        with open(FILE_NAME, 'r') as file: 
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return False
    for product_id, product_data in data.items():
        product_type = product_data.get("type", "generic")
        if product_type == "physical":
            inventory.add_product(PhysicalProduct(
                product_id=product_id,
                name=product_data["name"],
                price=product_data["price"],
                stock=product_data["stock"],
                supplier=DEFAULT_SUPPLIER,
                type=product_data["type"],
                weight=product_data["weight"],
            ))

        elif product_type == "digital":
            inventory.add_product(DigitalProduct(
                product_id=product_id,
                name=product_data["name"],
                price=product_data["price"],
                stock=product_data["stock"],
                supplier=DEFAULT_SUPPLIER,
                type=product_data["type"],
                download_size=product_data["download_size"]
            ))
        else:
            # Product is abstract, so an unknown type cannot be instantiated
            print(f"Skipping {product_id}: unknown product type '{product_type}'.")
    return True

def print_inventory(inventory: Inventory) -> None:
    print("--------------------------------------")
    inventory.display_inventory()
    print("--------------------------------------")

def user_input(inventory: Inventory) -> None:
    while True:
        user_option = input("\nEnter option: ")
        print()
        if user_option == "1":
            print_inventory(inventory)
        elif user_option == "2":
            add_product(inventory)
        elif user_option == "3":
            update_stock(inventory)
        elif user_option == "4":
            find_product(inventory)
        elif user_option == "5":
            print("Saving inventory...")
            save_inventory(inventory)
            print("Inventory saved successfully!")
        elif user_option == "6":
            print("Saving inventory before exit...")
            save_inventory(inventory)
            print("Inventory saved successfully!\n\nThank you for using the Inventory Management System. \nProgram terminated.")
            break
        else:
            print("Invalid option. Please try again.")

def add_product(inventory: Inventory) -> None:
    print("Add New Product")
    product_id = input("Enter Product ID: ")
    name = input("Enter Product Name: ")
    try:
        price = float(input("Enter Product Price: "))
        stock = int(input("Enter Product Stock: "))
    except ValueError:
        print("Invalid input. Please enter valid numbers for price and stock.")
        return
    if price < 0 or stock < 0:
        print("Price and stock cannot be negative.")
        return
    product_type = input("Enter Product Type (physical/digital): ").strip().lower()
    if product_type == "physical":
        info = PhysicalProduct.get_fulfilment_info()
        print(info)
        try:
            weight = float(input("Enter Product Weight (in kg): "))
        except ValueError:
            print("Invalid input. Please enter a valid number for weight.")
            return
        if weight < 0:
            print("Weight cannot be negative.")
            return
        inventory.add_product(PhysicalProduct(product_id, name, price, stock, DEFAULT_SUPPLIER, product_type, weight))
        print("\nPhysical product added successfully!")
    elif product_type == "digital":
        info = DigitalProduct.get_fulfilment_info()
        print(info)
        try:
            download_size = float(input("Enter Download Size (in MB): "))
        except ValueError:
            print("Invalid input. Please enter a valid number for download size.")
            return
        if download_size < 0:
            print("Download size cannot be negative.")
            return
        inventory.add_product(DigitalProduct(product_id, name, price, stock, DEFAULT_SUPPLIER, product_type, download_size))
        print("\nDigital product added successfully!")
    else:
        print("Invalid product type. Please enter 'physical' or 'digital'.")

def update_stock(inventory: Inventory) -> None:
    print("Update Product Stock")
    product_id = input("Enter Product ID:")
    print()
    status = "update"
    product = inventory.find_product(product_id)
    if product is None:
        print("Product ID Not Found.")
        return
    product.display_details(status)
    try:
        new_stock = int(input("\nNew stock quantity: "))
    except ValueError:
        print("Invalid input. Please enter a valid number for stock quantity.")
        return
    if product.update_stock(new_stock):
        save_inventory(inventory)
        print("Stock updated successfully!")
    else:
        print("Invalid stock quantity. Stock cannot be negative.")


def find_product(inventory: Inventory) -> None:
    print("Find Product")
    product_id = input("Enter Product ID: ")
    print()
    status = "search"
    product = inventory.find_product(product_id)
    if product:
        product.display_details(status)
    else:
        print("Product ID not found.")

def save_inventory(inventory: Inventory) -> None:
    data = {p.get_product_id(): p.to_dict() for p in inventory.get_inventory()}
    with open("OOP_inventory.json", 'w') as file:
        json.dump(data, file, indent=4)

def print_menu() -> None:
    print("----------- MENU -----------\n",
          "1. Display All Products\n",
          "2. Add Product\n",
          "3. Update Stock\n",
          "4. Search Product\n",
          "5. Save Inventory\n",
          "6. Exit\n"
          "----------------------------",)


def main() -> None:
    print("==================================\n Welcome to the Inventory Manager\n==================================\n")
    inventory = Inventory()
    if load_inventory(inventory):
        print("OOP_inventory.json found.\nInventory loaded successfully!\n")
    else:
        print("No existing inventory found. Starting with an empty inventory.")
    print_menu()
    user_input(inventory)

if __name__ == "__main__":
    main()




