# CLI management menu

from decimal import Decimal, InvalidOperation
from models import Expense, Category
from datetime import date
import utility
import storage


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
            case "1": expense_menu()
            case "2": print("Report menu\n")
            case "3": loop = False
            case _: print("Select a number from those shown\n")

    print("\nGoodbye")

def expense_menu():
    while True:
        print(""""Expense management:
    1. Create expense
    2. Search expense
    3. Update expense
    4. Delete expense
    5. Exit
    """)
        x = input("-> ")
        match(x):
            case "1": create_expense()
            case "2": handle_search_expense()
            case "3": handle_update_expense()
            case "4": handle_delete_expense()
            case "5": break
            case _: print("Select a number from those shown\n")

def create_expense():
    """Create a new expense"""
    print("Insert expense data")
    name = input("Name: ")
    name = check_input_string("Name: ", name)

    cost = input("Cost (positive number): ")
    cost = check_input_decimal(cost)

    category = input("Category: ")
    category = check_input_string("Category: ", category)

    print("Date in day/month/year format (press Enter if it's today): ")
    expense_date = input("-> ")
    expense_date = check_date_format(expense_date)
    expense = Expense(name, cost, Category(category), expense_date)
    
    storage.add_expense(expense)

def handle_search_expense():
    """Search an expense in the list"""
    searched_id = check_input_integer()
    expense_found = storage.search_expense(searched_id)
    if expense_found is not None:
        print(expense_found)
    else:
        print("Expense not found!")

def handle_update_expense():
    """Update an existing expense"""
    searched_id = check_input_integer()
    expense_found = storage.search_expense(searched_id)
    if expense_found is None:
        print("Expense not found!")
    else:
        print(f"Current name: {expense_found.name}")
        new_name = input("New name [Enter to keep]: ")
        if new_name != "":
            new_name = check_input_string("Name: ", new_name)
        else:
            new_name = expense_found.name
        
        print(f"Current cost: {expense_found.amount}")
        new_cost = input("New cost [Enter to keep]: ")
        if new_cost != "":
            new_cost = check_input_decimal(new_cost)
        else:
            new_cost = expense_found.amount
        
        print(f"Current category: {expense_found.category}")
        new_category = input("New category [Enter to keep]: ")
        if new_category != "":
            new_category = check_input_string("Category: ", new_category)
        else:
            new_category = expense_found.category.name
        
        print(f"Current date: {expense_found.expense_date}")
        new_date = input("New date [Enter to keep]: ")
        if new_date != "":
            new_date = check_date_format(new_date)
        else:
            new_date = expense_found.expense_date

        new_expense = Expense(new_name, new_cost, Category(new_category), new_date)
        result = storage.update_expense(searched_id, new_expense)
        if result:
            print("Expense updated successfully")
        else:
            # Only god know why this operation failed after all validation and control :(
            print("Expense not updated")

def handle_delete_expense():
    """Delete an existing expense"""
    searched_id = check_input_integer()
    expense_deleted = storage.delete_expense(searched_id)
    if expense_deleted:
        print("Expense deleted successfully")
    else:
        print("Expense not found!")

def check_input_string(output: str, word: str) -> str:
    """Check that the string is not empty or that it does not consist solely of consecutive spaces"""
    while word == "" or word.isspace():
        print(f"Invalid {output}! Try again.")
        word = input(output)
    return word

def check_input_integer() -> int:
    """Check whether the input is a positive integer number"""
    while True:
        try:
            number = int(input("Insert expense ID: "))
            if number > 0:
                return number
            else:
                print("The number must be positive and not zero")
        except ValueError:
            print("Invalid ID input! Try again")

def check_input_decimal(number: str) -> Decimal:
    """Check whether the input is a positive number—either an integer or a decimal."""
    while True:
        try:
            decimal_cost = Decimal(number)
            if decimal_cost.is_finite() and decimal_cost > 0:
                return decimal_cost
            else:
                print("The cost must be positive and not zero")
        except InvalidOperation:
            print("Invalid cost! Try again.")
        
        number = input("Cost (positive number): ")

def check_date_format(in_date) -> date | None:
    while True:
        try:
            return utility.string_to_date(in_date)
        except ValueError:
            print("Invalid date format! Try again.")
        
        print("Date in day/month/year format (press Enter if it's today): ")
        in_date = input("-> ")