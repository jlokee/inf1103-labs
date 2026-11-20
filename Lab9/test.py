from product import Product
from supplier import Supplier
from digital import DigitalProduct
from physical import PhysicalProduct
from product_factory import ProductFactory
from inventory import Inventory
from orderline import OrderLine
from order import Order


def show_product_details(product: Product) -> None:
    """Works with ANY Product (LSP): only uses behaviour defined on Product."""
    product.display_information()
    print(f"Fulfilment Info: {product.get_fulfilment_info()}")


def heading(title: str) -> None:
    print(f"\n{'=' * 60}\n{title}\n{'=' * 60}")


def make_products(supplier: Supplier) -> tuple[PhysicalProduct, DigitalProduct]:
    laptop = ProductFactory.create("physical", "P001", "Laptop", 1200.0, 15, supplier, weight=2.5)
    office = ProductFactory.create("digital", "P005", "Microsoft Office", 100.0, 40, supplier, download_size=200.0)
    return laptop, office


def test_association() -> None:
    heading("Section 2: Association (Supplier <-> Product)")
    supplier = Supplier("SUP001", "Global Tech WholeSale", "supply@globaltech.com")
    laptop, office = make_products(supplier)

    print("Supplier info via each product:")
    laptop.supplier.display_information()
    office.supplier.display_information()
    print("Same Supplier object shared:", laptop.supplier is office.supplier is supplier)

    del supplier  # removes only the variable name, not the object
    print("\nAfter 'del supplier':")
    laptop.supplier.display_information()
    office.supplier.display_information()


def test_aggregation() -> None:
    heading("Section 3: Aggregation (Inventory <> Product)")
    supplier = Supplier("SUP001", "Global Tech WholeSale", "supply@globaltech.com")
    laptop, _ = make_products(supplier)   # product exists BEFORE any inventory

    inventory_a, inventory_b = Inventory(), Inventory()
    inventory_a.add_product(laptop)
    print("In A:", len(inventory_a), "| In B:", len(inventory_b))

    removed = inventory_a.remove_product("P001")
    print("In A:", len(inventory_a), "| Same object returned:", removed is laptop)
    print("Product still usable after removal:")
    laptop.display_information()

    inventory_b.add_product(laptop)
    print("In A:", len(inventory_a), "| In B:", len(inventory_b))
    print("B holds the very same object:", inventory_b.find_product("P001") is laptop)


def test_composition() -> None:
    heading("Section 4: Composition (Order 1 <#> OrderLine)")
    supplier = Supplier("SUP001", "Global Tech WholeSale", "supply@globaltech.com")
    laptop, office = make_products(supplier)

    order1, order2 = Order("ORD001"), Order("ORD002")
    order1.add_order_line(laptop, 2)
    order1.add_order_line(office, 3)
    order1.display_order_summary()

    order2.add_order_line(laptop, 1)   # same Product, different Order
    print()
    order2.display_order_summary()

    line_a, line_b = order1.order_lines[0], order2.order_lines[0]
    print("\nSame Product object in both lines:", line_a.product is line_b.product)
    print("Same OrderLine object in both orders:", line_a is line_b)
    print("Each order created its own OrderLine:", isinstance(line_a, OrderLine) and line_a is not line_b)

    print("\nRemoving the laptop line from ORD001 via Order method:")
    order1.remove_order_line("P001")
    order1.display_order_summary()
    print("Laptop still exists, stock now:", laptop.get_stock())

    print("\nInvalid orders:")
    try:
        order1.add_order_line(laptop, 0)
    except ValueError as error:
        print(f"Rejected: {error}")
    order1.add_order_line(laptop, 999)


def test_lsp_and_polymorphism() -> None:
    heading("Sections 6 & 7: LSP and Polymorphism")
    supplier = Supplier("SUP001", "Global Tech WholeSale", "supply@globaltech.com")
    laptop, office = make_products(supplier)

    print("show_product_details() with each subtype:\n")
    for product in (laptop, office):
        show_product_details(product)
        print()

    inventory = Inventory()
    inventory.add_product(laptop)
    inventory.add_product(office)

    print("One loop over Product references (no isinstance):\n")
    for product in inventory.products:
        product.display_information()
        print(product.get_fulfilment_info())
        print()

    print("update_stock() keeps the same meaning for every Product:")
    for product in inventory.products:
        product.update_stock(7)
        try:
            product.update_stock(-1)
            bad = "accepted"
        except ValueError:
            bad = "rejected"
        print(f"  {product.get_name()}: valid -> ok, negative -> {bad}, stock = {product.get_stock()}")


if __name__ == "__main__":
    test_association()
    test_aggregation()
    test_composition()
    test_lsp_and_polymorphism()
