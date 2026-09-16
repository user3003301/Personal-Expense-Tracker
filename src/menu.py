# CLI management menu

from decimal import Decimal, InvalidOperation
from models import Expense, Category
from datetime import date
import utility, storage, filters, expense_statistics


def main_menu():
    print("Personal Expense Tracker\n")

    while True:
        print("""\nChoose your operation:
    1. Expense management
    2. Expense statistics
    3. Expense report
    4. Exit
        """)
        x = input("-> ")
        match(x):
            case "1": expense_menu()
            case "2": statistics_menu()
            case "3": report_menu()
            case "4": break
            case _: print("Select a number from those shown\n")

    print("\nGoodbye")

def expense_menu():
    while True:
        print("""\nExpense management:
    1. Create expense
    2. Search expense
    3. Update expense
    4. Delete expense
    5. Back
    """)
        x = input("-> ")
        match(x):
            case "1": create_expense()
            case "2": handle_filter_search()
            case "3": handle_update_expense()
            case "4": handle_delete_expense()
            case "5": break
            case _: print("Select a number from those shown")
    print()

def statistics_menu():
    expense_statistics.get_expenses_list()

    while True:
        print(f"""\nExpense report

    Current expenses: {expense_statistics.get_total_expenses()}

    1. Reset Filters
    2. Total amount
    3. Average amount
    4. Minimum expense
    5. Maximum expense
    6. Amount by category
    7. Back""")
        x = input("-> ")

        match(x):
            case "1": reset_filter()
            case "2": print(f"\nTotal amount: {expense_statistics.get_total_amount()}")
            case "3": print(f"\nAverage amount: {expense_statistics.get_average_amount()}")
            case "4": print(f"\nMinimum amount: {expense_statistics.get_min_amount()}")
            case "5": print(f"\nMaximum amount: {expense_statistics.get_max_amount()}")
            case "6": 
                category_dict = expense_statistics.get_amount_by_category()
                for k, v, in category_dict.items():
                    print(f"{k}: {v}")
            case "7": break
            case _: print("Select a number from those shown")

def report_menu():
    while True:
        print("""\nChoose your operation:
    1. Montly report
    2. Yearly report
    3. Back
        """)
        x = input("-> ")
        match(x):
            case "1": handle_monthly_report()
            case "2": handle_yearly_report()
            case "3": break
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
    storage.save_expenses()

def handle_search_expense():
    """Search an expense in the list"""
    searched_id = check_input_integer("Insert ID: ")
    expense_found = storage.search_expense(searched_id)
    if expense_found is not None:
        print(expense_found)
    else:
        print("Expense not found!")

def handle_filter_search():
    """Search an expense by multiple filters"""
    filters.set_filter_list()
    
    # cost filter
    min_cost = input("Minimum cost [Enter to skip]: ")
    if min_cost != "":
        min_cost = check_input_decimal(min_cost)
    max_cost = input("Maximum cost [Enter to skip]: ")
    if max_cost != "":
        max_cost = check_input_decimal(max_cost)

    if min_cost != "" or max_cost != "":
        if min_cost == "": min_cost = None
        if max_cost == "": max_cost = None
        filters.filter_by_cost(min_cost, max_cost)

    # category filter
    category = input("Category: [Enter to skip]: ")
    if category != "":
        category = check_input_string("Category: ", category)
        filters.filter_by_category(category)

    # date filter
    date_only = ""
    first_date = input("First date [Enter to skip]: ")
    if first_date != "":
        first_date = check_date_format(first_date)

        date_only = input("Only this date? (y,n): ")
        while date_only != 'y' and date_only != 'n':
            date_only = input("Only this date? (y,n): ")
        if date_only.lower() == "y":
            filters.filter_by_date(first_date)
    
    if date_only != "y":
        second_date = input("Second date [Enter to skip]: ")
        if second_date != "":
            second_date = check_date_format(second_date)

            if first_date == "": first_date = None
            if second_date == "": second_date = None
            filters.filter_by_date_range(first_date, second_date)

    filtered_expenses = filters.get_filtered_expenses()
    if filtered_expenses:
        for expense in filtered_expenses:
            print(expense)
    else: print("No expense found.")

def handle_update_expense():
    """Update an existing expense"""
    searched_id = check_input_integer("Insert ID: ")
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
            storage.save_expenses()
        else:
            # Only god know why this operation failed after all validation and control :(
            print("Expense not updated")

def handle_delete_expense():
    """Delete an existing expense"""
    searched_id = check_input_integer("Insert ID: ")
    expense_deleted = storage.delete_expense(searched_id)
    if expense_deleted:
        print("Expense deleted successfully")
        storage.save_expenses()
    else:
        print("Expense not found!")

def handle_monthly_report():
    print("\nMontly report\n")
    month = 13
    while month > 12:
        month = check_input_integer("Insert month: ")
    year = check_input_integer("Insert year: ")

    print()
    result = expense_statistics.get_monthly_report(month, year)
    print_report(result)

def handle_yearly_report():
    print("\nYearly report\n")
    year = check_input_integer("Insert year: ")

    print()
    result = expense_statistics.get_yearly_report(year)
    print_report(result)
        
def check_input_string(output: str, word: str) -> str:
    """Check that the string is not empty or that it does not consist solely of consecutive spaces"""
    while word == "" or word.isspace():
        print(f"Invalid {output}! Try again.")
        word = input(output)
    return word.strip().capitalize()

def check_input_integer(output: str) -> int:
    """Check whether the input is a positive integer number"""
    while True:
        try:
            number = int(input(output))
            if number > 0:
                return number
            else:
                print("The number must be positive and not zero")
        except ValueError:
            print(f"Invalid input! Try again")

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

def reset_filter():
    """Reset the list"""
    filters.set_filter_list()
    expense_statistics.get_expenses_list()

def print_report(result: dict):
    if result is None:
        print("No expense found in this period.")
    else:
        for key, value in result.items():
            if key == "expensive_category":
                print("expensive_category: ")
                for i in range(len(value)):
                    for key2, value2 in value[i].items():
                        print(f"\t{key2}: {value2}")
                    print()
            else: print(f"{key}: {value}")