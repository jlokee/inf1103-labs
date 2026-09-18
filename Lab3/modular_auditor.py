inventory = 0
total_inventory = 0
rej_inventory = 0

def get_valid_input():
    inventory = input("Enter the number of items in inventory (or type 'quit' to exit): ")
    if inventory.isdigit():  
        return int(inventory)
    elif inventory == "quit":
        return "quit"
    elif inventory.startswith("-") and inventory[1:].isdigit():
        print("Inventory cannot be negative. Please enter a valid number.")
        return "rejected"
    else:
        print("Invalid input. Please enter a valid number.")
        return "rejected"

while True:
    inventory = get_valid_input()
    if inventory == "quit":
        print("Exiting... Total Units Processed is", total_inventory, "items.")
        print("Rejected Entries is", rej_inventory)
        break
    elif isinstance(inventory, int):
        total_inventory += inventory
        if total_inventory >500:
            print("Alert: Inventory exceeds 500 items. Please check your stock.")
            break
        else:
            print("You have", total_inventory, "items in inventory.")
    elif inventory == "rejected":
        rej_inventory += 1

