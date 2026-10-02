import json



def load_inventory():
    with open("Lab5/inventory.json", 'r') as file:  
        return json.load(file)
    print()

def save_inventory(inventory):
    with open("Lab5/inventory.json", 'w') as file:
        json.dump(inventory, file, indent=4)
    print("Product added successfully")

def print_inventory(inventory):
    print("Current Inventory:\n")
    for product_id, product_info in inventory.items():
        print(f"Product ID: {product_id}")
        print(f"Name: {product_info['name']}")
        print(f"Price: ${product_info['price']:.2f}")
        print(f"Stock: {product_info['stock']}")
        print()


print("==================================\n Welcome to the Inventory Manager\n==================================\n\n")
inventory = load_inventory()
print_inventory(inventory)
