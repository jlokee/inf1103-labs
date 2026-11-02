import json
from product import Product
from inventory import Inventory

user_option = 0
FILE_NAME = "OOP_inventory.json"


def load_inventory(inventory):
    try:
        with open(FILE_NAME, 'r') as file: 
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return False
    for product_id, product_data in data.items():
        inventory.add_product(Product(product_id, product_data["name"], product_data["price"], product_data["stock"]))
    return True

def print_inventory(inventory):
    print("--------------------------------------")
    inventory.display_inventory()
    print("--------------------------------------")

def user_input(inventory):
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
            search_product(inventory)
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

def add_product(inventory):
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
    inventory.add_product(Product(product_id, name, price, stock))
    print("\nProduct added successfully!")

def update_stock(inventory):
    print("Update Product Stock")
    product_id = input("Enter Product ID:")
    print()
    status = "update"
    product = inventory.search_product(product_id)
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


def search_product(inventory):
    print("Search Product")
    product_id = input("Enter Product ID: ")
    print()
    status = "search"
    product = inventory.search_product(product_id)
    if product:
        product.display_details(status)
    else:
        print("Product ID not found.")

def save_inventory(inventory):
    data = {p.get_product_id(): p.to_dict() for p in inventory.get_inventory()}
    with open("OOP_inventory.json", 'w') as file:
        json.dump(data, file, indent=4)

def print_menu():
    print("----------- MENU -----------\n",
          "1. Display All Products\n",
          "2. Add Product\n",
          "3. Update Stock\n",
          "4. Search Product\n",
          "5. Save Inventory\n",
          "6. Exit\n"
          "----------------------------",)


def main():
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




