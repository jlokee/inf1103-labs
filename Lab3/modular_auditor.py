inventory = 0
total_inventory = 0
rej_inventory = 0
tax = 0.0
total_tax = 0.0

def get_valid_input():
    inventory = input("Enter the number of items in inventory (or type 'quit' to exit): ")
    if inventory.isdigit():  
        return int(inventory)
    elif inventory == "quit":
        return "quit"
    elif inventory.startswith("-") and inventory[1:].isdigit():
        print("Inventory cannot be negative. Please enter a valid number.")
        return "rejected"
    elif inventory == "report":
        generate_report(total_inventory, rej_inventory)
    else:
        print("Invalid input. Please enter a valid number.")
        return "rejected"

def process_delivery(current_total, new_value):
    current_total += new_value
    return current_total

def calculate_tax(amount):
    tax_rate = 0.10  # 10% tax rate
    tax_amount = amount * tax_rate
    return tax_amount

def generate_report(total_units, failed_attempts):
    print("Total Units Processed is", total_units, "items.")
    print("Rejected Entries is", failed_attempts)

while True:
    inventory = get_valid_input()
    if inventory == "quit":
        print("Exiting... Total Units Processed is", total_inventory, "items.")
        print("Rejected Entries is", rej_inventory)
        break
    elif isinstance(inventory, int):
        total_inventory = process_delivery(total_inventory, inventory)
        if total_inventory >500:
            print("Alert: Inventory exceeds 500 items. Please check your stock.")
            break
        else:
            tax = round(calculate_tax(inventory),2)
            total_tax += tax
            print("You have", total_inventory, "items in inventory.")
            print("Tax for this transaction is $", tax)
    elif inventory == "rejected":
        rej_inventory += 1
    

print("Total Units Processed is", total_inventory, "items.")
print("Total tax collected is $", total_tax)