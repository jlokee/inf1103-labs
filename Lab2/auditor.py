inventory = 0
total_inventory = 0
rej_inventory = 0

while inventory != "quit":
    inventory = str(input("Enter the number of items in inventory (or type 'quit' to exit): "))

    if inventory.isdigit() == True:  
        total_inventory += int(inventory)
        if int(inventory) < 0:
            print("Inventory cannot be negative. Please enter a valid number.")
            rej_inventory += 1
        elif int(inventory) > 0 and int(total_inventory) <= 500:
            print("You have", total_inventory, "items in inventory.")
        elif int(total_inventory) >500:
            print("Alert: Inventory exceeds 500 items. Please check your stock.")
            inventory = "quit"
            break
    elif inventory == "quit":
        print("Exiting... Total Units Processed is", total_inventory, "items.")
        print("Rejected Entries is", rej_inventory)
    else:
        print("Invalid input. Please enter a valid number")
