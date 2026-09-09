# CLI management menu

from decimal import Decimal, InvalidOperation
from models import Expense, Category
from datetime import date
import utility


def run():
    loop = True
    print("Personal Expense Tracker\n")

    while loop:
        print("""Choose your operation:
    1. Expense management
    2. Expense report
    3. Exit
        """)
        x = input("-> ")
        match(x):
            case "1":
                create_expense()
            case "2":
                print("Report menu\n")
            case "3":
                loop = False
            case _:
                print("Select a number from those shown\n")

    print("\nGoodbye")


def create_expense():
    """Create a new expense"""
    print("Insert expense data")
    name = check_input_string("Name: ")
    cost = check_input_number()
    category = check_input_string("Category: ")
    expense_date = check_date_format()
    expense = Expense(name, cost, Category(category), expense_date)
    print(expense, "\n")

def check_input_string(output: str) -> str:
    """Check that the string is not empty or that it does not consist solely of consecutive spaces"""
    word = input(output)
    while word == "" or word.isspace():
        print("Invalid ", output, "! Try again.")
        word = input(output)
    return word

def check_input_number() -> Decimal:
    """Check whether the input is a positive number—either an integer or a decimal."""
    while True:
        cost = input("Cost (positive number): ")
        try:
            decimal_cost = Decimal(cost)
            if decimal_cost.is_finite() and decimal_cost > 0:
                return decimal_cost
            else:
                print("The cost must be positive and not zero")
        except InvalidOperation:
            print("Invalid cost! Try again.")


def check_date_format() -> date | None:
    while True:
        print("Date in day/month/year format (press Enter if it's today): ")
        in_date = input("-> ")
        try:
            return utility.string_to_date(in_date)
        except ValueError:
            print("Invalid date format! Try again.")