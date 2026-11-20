class Supplier:
    def __init__(self, supplier_id: str, name: str, contact_email: str):
        self.supplier_id: str = str(supplier_id)
        self.name: str = str(name)
        self.contact_email: str = str(contact_email)

    def display_information(self) -> None:
        print(f"Supplier ID: {self.supplier_id} | "
              f"Name: {self.name} | "
              f"Contact Email: {self.contact_email}")
