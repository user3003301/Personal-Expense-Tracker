# Data management

## Standard libray
from os import rename
from json import load as jsonload, dump as jsondump, JSONDecodeError
from logging import getLogger
from decimal import Decimal
from datetime import datetime

## Local project module
from src.models import Expense, Category
from src import utility
from enums.error_codes import ErrorCode
from exception.exceptions import StorageDataCorruptedError

logger = getLogger(__name__)
expenses_list: list[Expense] = []
count: int = 1

def load_expenses(filename: str | None = None) -> None:
    """Read the JSON file and save the expenses in a list"""
    global expenses_list, count
    expenses_list = []
    count = 1

    path = ""
    if filename: path = filename
    else: path = "data/expenses.json"

    try:
        with open(path, "r", encoding="UTF-8") as file:
            expenses_data = jsonload(file)
    except FileNotFoundError:
        expenses_data = ""
    except JSONDecodeError:
        logger.error("The JSON file is corrupted")
        raise StorageDataCorruptedError()

    if expenses_data != "":
        max_id = deserialize_json_data_into_expense(expenses_data)
        count = max_id + 1
    logger.info("Loading complete")

def deserialize_json_data_into_expense(expenses_data: str) -> int:
    """take the data read from the JSON file, deserializes it into an Expense
    object, and adds it to expenses_list.

    Return the next ID to be assigned to the new expense.
    """
    global expenses_list
    max_id = 0
    for expense_item in expenses_data:  
        expense_id = expense_item.get("id")
        name = expense_item.get("name")
        amount = Decimal(expense_item.get("amount"))
        category = Category(expense_item.get("category"))
        expense_date = utility.string_to_date(expense_item.get("expense_date"))

        loaded_expense = Expense(name, amount, category, expense_date)
        loaded_expense._id = expense_id
        expenses_list.append(loaded_expense)
    
        if max_id < expense_id: 
            max_id = expense_id
    
    return max_id
    
def save_expenses() -> None:
    """Save the expenses in expenses_list in a JSON file"""
    expenses_data = serialize_expense_into_json_data()

    with open("data/expenses.json", "w", encoding="UTF-8") as file:
        jsondump(expenses_data, file)
    logger.info("Save completed")

def serialize_expense_into_json_data() -> list:
    """Retrieves data from storage list, serializes all Expense attributes into 
    JSON format, and adds them into another list, which retrun
    """
    expenses_data = []
    for expense in expenses_list:
        expense_id = expense.id
        name = expense.name
        amount = str(expense.amount)
        category = expense.category.name
        expense_date = utility.date_to_string(expense.expense_date)
    
        expense_item = {}
        expense_item["id"] = expense_id
        expense_item["name"] = name
        expense_item["amount"] = amount
        expense_item["category"] = category
        expense_item["expense_date"] = expense_date

        expenses_data.append(expense_item)
    return expenses_data

def get_all_expenses() -> list[Expense]:
    """Return a list of expenses saved in a file"""
    return expenses_list.copy()

def add_expense(expense: Expense) -> None:
    """Add a new expense in the expense list"""
    global count
    expense._id = count
    expenses_list.append(expense)
    count = count + 1

def search_expense(id: int) -> Expense | None:
    """Return an expense by its id"""
    for expense in expenses_list:
        if id == expense.id:
            return expense
    return None

def update_expense(id: int, new_expense: Expense) -> bool:
    """Update an expense passing its id and new values by expense obj"""
    for e in expenses_list:
        if id == e._id:
            e.name = new_expense.name
            e.amount = new_expense.amount
            e.category = new_expense.category
            e.expense_date = new_expense.expense_date
            return True
    return False

def delete_expense(id: int) -> bool:
    """Delete an expense passing its id"""
    for e in expenses_list:
        if id == e._id:
            expenses_list.remove(e)
            return True
    return False

def backup_corrupted_file() -> ErrorCode:
    """Returns an ErrorCode enumerator to indicate the result of the operation 
    to back up the corrupted file and create a new file.
    """
    date_and_time = datetime.strftime(datetime.now(), "%Y%m%d_%H%M%S")
    try:
        rename("data/expenses.json", f"data/expenses_corrupted_{date_and_time}.json")
        with open("data/expenses.json", "w", encoding="UTF-8") as new_file:
            new_file.write("[]")
        logger.info("Backed up the damaged file and created a new file")
        return ErrorCode.SUCCESS
    except FileNotFoundError:
        logger.error("Source file not found")
        return ErrorCode.SRC_NOT_FOUND
    except FileExistsError:
        logger.error("The filename already exists")
        return ErrorCode.DST_EXISTS
    except OSError:
        logger.error("I/O error")
        return ErrorCode.OS_ERROR 
