import json

json_check = False
user_option = 0

def load_inventory():
    global json_check
    with open("inventory.json", 'r') as file: 
        json_check = True
        return json.load(file)
    print()

def print_inventory(inventory):
    print("Current Inventory:\n")
    for product_id, product_info in inventory.items():
        print(f"ID: {product_id} | Name: {product_info['name']} | Price: ${product_info['price']:.2f} | Stock: {product_info['stock']}")

def user_input():
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
    price = float(input("Enter Product Price: "))
    stock = int(input("Enter Product Stock: "))

    inventory[product_id] = {
        "name": name,
        "price": price,
        "stock": stock
    }
    print("\nProduct added successfully!")

def update_stock(inventory):
    print("Update Product Stock")
    product_id = input("Enter Product ID:")
    print()
    if product_id in inventory:
        print(f"Product Found: \nName: {inventory[product_id]['name']}\nCurrent Stock: {inventory[product_id]['stock']}")
        new_stock = int(input("\nNew stock quantity: "))
        if new_stock >= 0:
            inventory[product_id]['stock'] = new_stock
            save_inventory(inventory)
            print("Stock updated successfully!")
        else:
            print("Stock quantity cannot be negative.")
    else:
        print("Product ID not found.")

def search_product(inventory):
    print("Search Product")
    product_id = input("Enter Product ID: ")
    print()
    if product_id in inventory:
        product_info = inventory[product_id]
        print(f"Product Found:\n-------------------\nName: {product_info['name']}\nPrice: ${product_info['price']:.2f}\nStock: {product_info['stock']}\n-------------------")
    else:
        print("Product ID not found.")

def save_inventory(inventory):
    with open("inventory.json", 'w') as file:
        json.dump(inventory, file, indent=4)

print("==================================\n Welcome to the Inventory Manager\n==================================\n")
inventory = load_inventory()
if json_check == True:
    print("inventory.json found.\nInventory loaded successfully.\n")
else:
    print("inventory.json not found.\nStarting with an empty inventory.")
print("----------- MENU -----------\n",
"1. Display All Products\n",
"2. Add Product\n",
"3. Update Stock\n",
"4. Search Product\n",
"5. Save Inventory\n",
"6. Exit\n"
"----------------------------",)
user_input()


