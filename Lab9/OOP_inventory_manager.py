import csv
import json
from digital import DigitalProduct      # only used for get_fulfilment_info(); products are built by the factory
from physical import PhysicalProduct    # only used for get_fulfilment_info(); products are built by the factory
from inventory import Inventory
from product_factory import ProductFactory
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
        try:
            inventory.add_product(ProductFactory.create(
                product_type=product_data.get("type", "generic"),
                product_id=product_id,
                name=product_data["name"],
                price=product_data["price"],
                stock_quantity=product_data["stock"],
                supplier=DEFAULT_SUPPLIER,
                weight=product_data.get("weight", 0.0),
                download_size=product_data.get("download_size", 0.0),
            ))
        except (ValueError, KeyError) as error:
            print(f"Skipping {product_id}: {error}")
    return True

def get_positive_float(prompt: str) -> float:
    """Keep asking until the user enters a number greater than zero."""
    while True:
        try:
            value = float(input(prompt))
            if value <= 0:
                print("Please enter a number greater than zero.")
                continue
            return value
        except ValueError:
            print("Please enter a valid number, e.g. 12.50")


def get_non_negative_int(prompt: str) -> int:
    """Keep asking until the user enters a whole number that is zero or more."""
    while True:
        try:
            value = int(input(prompt))
            if value < 0:
                print("Please enter zero or a positive whole number.")
                continue
            return value
        except ValueError:
            print("Please enter a valid whole number, e.g. 10")


def load_products(path: str, inventory: Inventory, supplier: Supplier) -> None:
    """Load products from a CSV file, skipping (and reporting) any bad rows."""
    loaded = 0
    try:
        file = open(path, newline="")
    except FileNotFoundError:
        print(f"Products file not found: {path}")
    else:
        with file:
            reader = csv.reader(file)
            next(reader, None)  # skip the header row
            for line_number, row in enumerate(reader, start=2):
                try:
                    product_type, product_id, name, price, stock_quantity = row
                    product = ProductFactory.create(product_type, product_id, name,
                                                    float(price), int(stock_quantity), supplier)
                    inventory.add_product(product)
                    loaded += 1
                except ValueError as error:
                    print(f"Skipping row {line_number}: {error}")
        print(f"{loaded} products loaded.")
    finally:
        print("Load attempt finished.")


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
    price = get_positive_float("Enter Product Price: ")
    stock = get_non_negative_int("Enter Product Stock: ")
    product_type = input("Enter Product Type (physical/digital): ").strip().lower()
    if product_type == "physical":
        print(PhysicalProduct.get_fulfilment_info())
        try:
            weight = float(input("Enter Product Weight (in kg): "))
        except ValueError:
            print("Invalid input. Please enter a valid number for weight.")
            return
        if weight < 0:
            print("Weight cannot be negative.")
            return
        extra = {"weight": weight}
    elif product_type == "digital":
        print(DigitalProduct.get_fulfilment_info())
        try:
            download_size = float(input("Enter Download Size (in MB): "))
        except ValueError:
            print("Invalid input. Please enter a valid number for download size.")
            return
        if download_size < 0:
            print("Download size cannot be negative.")
            return
        extra = {"download_size": download_size}
    else:
        print("Invalid product type. Please enter 'physical' or 'digital'.")
        return
    try:
        inventory.add_product(ProductFactory.create(product_type, product_id, name, price,
                                                    stock, DEFAULT_SUPPLIER, **extra))
    except ValueError as error:
        print(f"Could not add product: {error}")
        return
    print(f"\n{product_type.capitalize()} product added successfully!")

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
    try:
        product.update_stock(new_stock)
    except ValueError:
        print("Invalid stock quantity. Stock cannot be negative.")
        return
    save_inventory(inventory)
    print("Stock updated successfully!")


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
