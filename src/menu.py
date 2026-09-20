# CLI management menu

## Standard library
from decimal import Decimal, InvalidOperation
from datetime import date

## Local project import
from src.models import Expense, Category
from src import utility, storage, filters, expense_statistics
from enums.error_codes import ErrorCode


def main_menu() -> None:
    print("\nPersonal Expense Tracker\n")

    while True:
        print("""Choose your operation:
    1. Expense management
    2. Expense statistics
    3. Expense report
    4. Exit
        """)
        choosen_option = input("-> ")
        match(choosen_option):
            case "1": expense_menu()
            case "2": statistics_menu()
            case "3": report_menu()
            case "4": break
            case _: print("Select a number from those shown\n")

    print("\nGoodbye")

def expense_menu() -> None:
    while True:
        print("""\nExpense management:
    1. Create expense
    2. Search expense by ID
    3. Show expenses with/without filters
    4. Update expense
    5. Delete expense
    6. Back
    """)
        choosen_option = input("-> ")
        match(choosen_option):
            case "1": create_expense()
            case "2": handle_search_expense()
            case "3": handle_filter_search()
            case "4": handle_update_expense()
            case "5": handle_delete_expense()
            case "6": break
            case _: print("Select a number from those shown")
    print()

def statistics_menu() -> None:
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
        choosen_option = input("-> ")

        match(choosen_option):
            case "1": reset_filter()
            case "2": print(f"\nTotal amount: {expense_statistics.get_total_amount()}")
            case "3": print(f"\nAverage amount: {expense_statistics.get_average_amount()}")
            case "4": 
                min_amount = expense_statistics.get_min_amount()
                if min_amount is not None:
                    print("\nMinimum amount: ",min_amount)
                else:
                    print("No expense found.")
            case "5": 
                max_amount = expense_statistics.get_max_amount()
                if max_amount is not None:
                    print("\nMaximum amount: ", max_amount)
                else:
                    print("No expense found.")
            case "6": 
                category_dict = expense_statistics.get_amount_by_category()
                if category_dict is not None:
                    for key, value in category_dict.items():
                        print(f"{key}: {value}")
                else: 
                    print("No expense found.")
            case "7": break
            case _: print("Select a number from those shown")

def report_menu() -> None:
    while True:
        print("""\nChoose your operation:
    1. Montly report
    2. Yearly report
    3. Back
        """)
        choosen_option = input("-> ")
        match(choosen_option):
            case "1": handle_monthly_report()
            case "2": handle_yearly_report()
            case "3": break
            case _: print("Select a number from those shown\n")

def create_expense() -> None:
    """Create a new expense"""
    print("Insert expense data")
    name = input("Name: ")
    name = check_input_string("Name", name)

    cost = input("Cost (positive number): ")
    cost = check_input_decimal(cost)

    category = input("Category: ")
    category = check_input_string("Category", category)

    print("Date in day/month/year format (press Enter if it's today): ")
    expense_date = input("-> ")
    expense_date = check_date_format(expense_date)
    expense = Expense(name, cost, Category(category), expense_date)
    
    storage.add_expense(expense)
    storage.save_expenses()

def handle_search_expense() -> None:
    """Search an expense in the list"""
    searched_id = check_input_integer("Insert ID: ")
    expense_found = storage.search_expense(searched_id)
    if expense_found is not None:
        print(expense_found)
    else:
        print("Expense not found!")

def set_filter_by_cost() -> None:
    min_cost = input("Minimum cost [Enter to skip]: ")
    if min_cost != "":
        min_cost = check_input_decimal(min_cost)
    max_cost = input("Maximum cost [Enter to skip]: ")
    if max_cost != "":
        max_cost = check_input_decimal(max_cost)

    if min_cost != "" or max_cost != "":
        check_filter_range_value(min_cost, max_cost, "cost")

def set_filter_by_category() -> None:
    category = input("Category: [Enter to skip]: ")
    if category != "":
        category = check_input_string("Category", category)
        filters.filter_by_category(category)

def set_filter_by_date() -> None:
    date_only = ""
    first_date = input("First date [Enter to skip]: ")
    if first_date != "":
        first_date = check_date_format(first_date)

        date_only = input("Only this date? (y,n): ").lower()
        while date_only != 'y' and date_only != 'n':
            date_only = input("Only this date? (y,n): ").lower()
        if date_only == "y":
            filters.filter_by_date(first_date)
    
    if date_only != "y":
        second_date = input("Second date [Enter to skip]: ")
        if second_date != "":
            second_date = check_date_format(second_date)
            check_filter_range_value(first_date, second_date, "date")

def handle_filter_search() -> None:
    """Search an expense by multiple filters"""
    filters.set_filter_list()

    print()
    set_filter_by_cost()
    set_filter_by_category()
    set_filter_by_date()

    filtered_expenses = filters.get_filtered_expenses()
    if filtered_expenses:
        print()
        for expense in filtered_expenses:
            print(expense)
    else: 
        print("No expense found.")
    input("Press Enter to continue...")

def enter_updated_data(expense) -> Expense:
    print(f"Current name: {expense.name}")
    new_name = input("New name [Enter to keep]: ")
    if new_name != "":
        new_name = check_input_string("Name", new_name)
    else:
        new_name = expense.name
        
    print(f"Current cost: {expense.amount}")
    new_cost = input("New cost [Enter to keep]: ")
    if new_cost != "":
        new_cost = check_input_decimal(new_cost)
    else:
        new_cost = expense.amount
        
    print(f"Current category: {expense.category}")
    new_category = input("New category [Enter to keep]: ")
    if new_category != "":
        new_category = check_input_string("Category", new_category)
    else:
        new_category = expense.category.name
        
    print(f"Current date: {expense.expense_date}")
    new_date = input("New date [Enter to keep]: ")
    if new_date != "":
        new_date = check_date_format(new_date)
    else:
        new_date = expense.expense_date

    return Expense(new_name, new_cost, Category(new_category), new_date)    

def handle_update_expense() -> None:
    """Update an existing expense"""
    searched_id = check_input_integer("Insert ID: ")
    expense_found = storage.search_expense(searched_id)
    if expense_found is None:
        print("Expense not found!")
    else:
        updated_expense = enter_updated_data(expense_found)
        update_result = storage.update_expense(searched_id, updated_expense)
        if update_result:
            print("Expense updated successfully")
            storage.save_expenses()
        else:
            #Only God knows why this operation failed after all those validations and checks. :)
            print("Expense not updated")

def handle_delete_expense() -> None:
    """Delete an existing expense"""
    searched_id = check_input_integer("Insert ID: ")
    expense_deleted = storage.delete_expense(searched_id)
    if expense_deleted:
        print("Expense deleted successfully")
        storage.save_expenses()
    else:
        print("Expense not found!")

def handle_monthly_report() -> None:
    print("\nMontly report\n")
    month = 0
    while month < 1 or month > 12:
        month = check_input_integer("Insert month: ")
    year = check_input_integer("Insert year: ")

    print()
    report_result = expense_statistics.get_monthly_report(month, year)
    print_report(report_result)

def handle_yearly_report() -> None:
    print("\nYearly report\n")
    year = check_input_integer("Insert year: ")

    print()
    report_result = expense_statistics.get_yearly_report(year)
    print_report(report_result)

def handle_corrupted_file() -> bool:
    print("EXPENSE FILE IS CORRUPTED!\n")
    answer = ""
    while answer != 'Y' and answer != 'N':
        print("If you want to exit > enter [n]")
        print("If you want to backup the corrupted file and continue > enter [y]")
        answer = input("-> ")
        answer = check_input_string("answer, only [y] or [n]", answer)
    
    if answer == 'Y':
        backup_result = storage.backup_corrupted_file()
        match(backup_result):
            case ErrorCode.SUCCESS: return True
            case ErrorCode.SRC_NOT_FOUND: 
                print("Source file not found.")
                return False
            case ErrorCode.DST_EXISTS:
                print("Destination already exists.")
                return False
            case ErrorCode.OS_ERROR: 
                print("OS error")
                return False
    else:
        print("I'm closing the program.")
        return False

def check_input_string(output: str, word: str) -> str:
    """Checks that the string is not empty or consists solely of consecutive spaces
    \nReturns a string with the first letter of each word capitalized"""
    while word == "" or word.isspace():
        print(f"Invalid {output}! Please try again")
        word = input(f"{output}: ")
    return word.strip().capitalize()

def check_input_integer(output: str) -> int:
    """Check whether the input is a positive integer number
    \nReturns a valid value"""
    while True:
        try:
            number = int(input(output))
            if number > 0:
                return number
            else:
                print("The number must be positive and not zero")
        except ValueError:
            print("Invalid input! Please try again")

def check_input_decimal(number: str) -> Decimal:
    """Check whether the input is a positive number—either an integer or a decimal
    \nReturn a valid value"""
    while True:
        try:
            decimal_cost = Decimal(number)
            if decimal_cost.is_finite() and decimal_cost > 0:
                return decimal_cost
            else:
                print("The cost must be positive and not zero")
        except InvalidOperation:
            print("Invalid cost! Please try again")
        
        # enter the value again
        number = input("Cost (positive number): ")

def check_date_format(input_date) -> date | None:
    while True:
        try:
            return utility.string_to_date(input_date)
        except ValueError:
            print("Invalid date format! Please try again")

        # enter the value again
        print("Date in day/month/year format (press Enter if it's today): ")
        input_date = input("-> ")

def check_filter_range_value(min_value, max_value, filter_name: str):
    if filter_name == "cost":
        if min_value == "": filters.filter_by_cost(None, max_value)
        elif max_value == "": filters.filter_by_cost(min_value, None)
        elif min_value <= max_value: filters.filter_by_cost(min_value, max_value)
        else: print("The lower cost is greater than the higher cost!")
    else:
        if min_value == "": filters.filter_by_date_range(None, max_value)
        elif max_value == "": filters.filter_by_date_range(min_value, None)
        elif min_value <= max_value: filters.filter_by_date_range(min_value, max_value)  
        else: print("The first date is late than the second date!")          

def reset_filter() -> None:
    """Reset the list"""
    filters.set_filter_list()
    expense_statistics.get_expenses_list()

def print_report(report_result: dict) -> None:
    if report_result is None:
        print("No expense found in this period.")
    else:
        for key, value in report_result.items():
            if key == "expensive_category":
                print("expensive_category: ")
                for i in range(len(value)):
                    for key2, value2 in value[i].items():
                        print(f"\t{key2}: {value2}")
                    print()
            else: print(f"{key}: {value}")