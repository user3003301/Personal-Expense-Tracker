# Filters and Searching

from decimal import Decimal
from datetime import date
from .models import Expense
from src import storage


current_expenses = []

def set_filter_list() -> None:
    """Get a copy of the list containig saved expenses"""
    global current_expenses
    current_expenses = storage.get_all_expenses()

def get_filtered_expenses() -> list[Expense]:
    """Return the filtered expense list"""
    return current_expenses.copy()

def filter_by_category(category: str) -> list[Expense]:
    """Filters the current search results by category and saves it as the new current result."""
    global current_expenses
    filtered_list = []

    for expense in current_expenses:
        if expense.category.name == category:
            filtered_list.append(expense)

    current_expenses = filtered_list
    return filtered_list

def filter_by_cost(min_cost: Decimal| None, max_cost: Decimal | None) -> list[Expense]:
    """Filters the current search results by cost range and saves it as the new current result."""
    global current_expenses
    filtered_list = []

    if min_cost is None:
        for expense in current_expenses:
                if expense.amount <= max_cost:
                    filtered_list.append(expense)
    elif max_cost is None:
        for expense in current_expenses:
                if expense.amount >= min_cost:
                    filtered_list.append(expense)
    else:
        for expense in current_expenses:
            if expense.amount >= min_cost and expense.amount <= max_cost:
                filtered_list.append(expense)

    current_expenses = filtered_list
    return filtered_list

def filter_by_date(day: date) -> list[Expense]:
    """Filters the current search results by a single date and saves it as the new current result."""
    global current_expenses
    filtered_list = []

    for expense in current_expenses:
        if expense.expense_date == day:
            filtered_list.append(expense)

    current_expenses = filtered_list
    return filtered_list

def filter_by_date_range(start_date: date | None, end_date: date | None) -> list[Expense]:
    """Filters the current search results based on date range and saves it as the new current result."""
    global current_expenses
    filtered_list = []

    if end_date is None:
        for expense in current_expenses:
            if expense.expense_date >= start_date: 
                filtered_list.append(expense)
    elif start_date is None:
        for expense in current_expenses:
             if expense.expense_date <= end_date: 
                 filtered_list.append(expense)       
    else:
        for expense in current_expenses:
            if expense.expense_date >= start_date and expense.expense_date <= end_date: 
                filtered_list.append(expense)

    current_expenses = filtered_list
    return filtered_list
