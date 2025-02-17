from decimal import Decimal, InvalidOperation
import ast

class Product:
    def __init__(self, data):
        self.__dict__.update(data)
        try:
            # Remove currency symbols and whitespace if present
            price_str = str(self.price).strip().replace("$", "").replace(",", "")
            self.price = Decimal(price_str) if price_str else Decimal("0.0")
        except (InvalidOperation, ValueError):
            self.price = Decimal("0.0")

        self.details = ast.literal_eval(self.details) if self.details else {}
