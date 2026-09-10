# Data management

from models import Expense

expense_list: list[Expense] = []
count: int = 1

def get_all_expenses():
    return expense_list

def add_expense(expense: Expense) -> None:
    """add a new expense in the expense list"""
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
    for e in expense_list:
        if id == e._id:
            expense_list.remove(e)
            return True
    return False
