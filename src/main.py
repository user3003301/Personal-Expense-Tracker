from datetime import date
from models import Expense

if __name__ == "__main__":
	app = Expense("Laptop", 299.99, "Tech")
	print(app)