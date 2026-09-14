inventory = 0
total_inventory = 0
rej_inventory = 0

while True:
    inventory = input("Enter the number of items in inventory (or type 'quit' to exit): ")
    if inventory.isdigit():  
        total_inventory += int(inventory)
        if total_inventory >500:
            print("Alert: Inventory exceeds 500 items. Please check your stock.")
            break
        else:
            print("You have", total_inventory, "items in inventory.")
    elif inventory == "quit":
        print("Exiting... Total Units Processed is", total_inventory, "items.")
        print("Rejected Entries is", rej_inventory)
        break
    elif inventory.startswith("-") and inventory[1:].isdigit():
        rej_inventory += 1
        print("Inventory cannot be negative. Please enter a valid number.")
    else:
        rej_inventory += 1
        print("Invalid input. Please enter a valid number")
