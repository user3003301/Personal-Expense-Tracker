# Data management

import os
import json
from decimal import Decimal
from datetime import datetime
from json import JSONDecodeError
from src.models import Expense, Category
from src import utility
from enums.error_codes import ErrorCode
from exception.exceptions import StorageDataCorruptedError





expense_list: list[Expense] = []
count: int = 1

def load_expenses() -> None:
    """Read the JSON file and save the expenses in a list"""
    global expense_list, count
    try: # Check if file exists
        with open("data/expenses.json", "r", encoding="UTF-8") as file:
            expenses_data = json.load(file)
    except FileNotFoundError:
        expenses_data = ""
    except JSONDecodeError:
        raise StorageDataCorruptedError()

    if expenses_data != "":
        max_id = 0
        for expense_data in expenses_data:
            
            expense_id = expense_data.get("id")
            name = expense_data.get("name")
            amount = Decimal(expense_data.get("amount"))
            category = Category(expense_data.get("category"))
            expense_date = utility.string_to_date(expense_data.get("expense_date"))
            loaded_expense = Expense(name, amount, category, expense_date)
            loaded_expense._id = expense_id
            expense_list.append(loaded_expense)

            if max_id < expense_id: 
                max_id = expense_id
                
        count = max_id + 1

def save_expenses() -> None:
    """Save the expenses in expenses_list in a JSON file"""
    expenses_data = []
    for expense in expense_list:
        expense_id = expense.id
        name = expense.name
        amount = str(expense.amount)
        category = expense.category.name
        expense_date = utility.date_to_string(expense.expense_date)

        expense_data = {}
        expense_data["id"] = expense_id
        expense_data["name"] = name
        expense_data["amount"] = amount
        expense_data["category"] = category
        expense_data["expense_date"] = expense_date

        expenses_data.append(expense_data)

    with open("data/expenses.json", "w", encoding="UTF-8 ") as file:
        json.dump(expenses_data, file)

def get_all_expenses() -> list[Expense]:
    """Return a list of expenses saved in a file"""
    return expense_list.copy()

def add_expense(expense: Expense) -> None:
    """Add a new expense in the expense list"""
    global count
    expense._id = count
    expense_list.append(expense)
    count = count + 1

def search_expense(id: int) -> Expense | None:
    """Return an expense by its id"""
    for e in expense_list:
        if id == e._id:
            return e

def update_expense(id: int, new_expense: Expense) -> bool:
    """Update an expense passing its id and new values by expense obj"""
    for e in expense_list:
        if id == e._id:
            e.name = new_expense.name
            e.amount = new_expense.amount
            e.category = new_expense.category
            e.expense_date = new_expense.expense_date
            return True
    return False

def delete_expense(id: int) -> bool:
    """Delete an expense passing its id"""
    for e in expense_list:
        if id == e._id:
            expense_list.remove(e)
            return True
    return False

def backup_corrupted_file() -> ErrorCode:
    date_and_time = datetime.strftime(datetime.now(), "%Y%m%d_%H%M%S")
    try:
        os.rename("data/expenses.json", f"data/expenses_corrupted_{date_and_time}.json")
        with open("data/expenses.json", "w", encoding="UTF-8") as new_file:
            new_file.write("[]")
        return ErrorCode.SUCCESS
    except FileNotFoundError:
        return ErrorCode.SRC_NOT_FOUND
    except FileExistsError:
        return ErrorCode.DST_EXISTS
    except OSError:
        return ErrorCode.OS_ERROR 

