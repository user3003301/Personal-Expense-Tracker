from datetime import date
from decimal import Decimal
from models import Expense, Category

if __name__ == "__main__":
	app = Expense("Laptop", Decimal("299.99"), Category("Tech"))
	print(app)
	app = Expense("Owen", Decimal("349.99"), Category("Kitchen"), date(2026, 1, 1))
	print(app)