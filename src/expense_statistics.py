# Elaborate expense statistics

from decimal import Decimal, ROUND_HALF_UP
from datetime import date
from calendar import month_name
from .models import Expense
from src import filters, storage

current_expenses = []

def get_expenses_list():
    """Get the list of expenses from a filtered list"""
    global current_expenses
    current_expenses = filters.get_filtered_expenses()

def get_total_expenses() -> int:
    """Return the number of expenses in the list"""
    return len(current_expenses)

def get_total_amount(alternative_list: list[Expense] | None = None) -> Decimal:
    """Returns the sum of the expenses"""
    if alternative_list is None:
        category_list = current_expenses
    else:
        category_list = alternative_list

    total = Decimal('0')
    for expense in category_list:
        total = total + expense.amount

    return total

def get_average_amount() -> Decimal:
    """Returns the average cost of a expense"""
    total = Decimal('0')
    n_expenses = len(current_expenses)

    if n_expenses == 0:
        return total
    
    for expense in current_expenses:
            total = total + expense.amount

    average = total/Decimal(n_expenses)
    return average.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

def get_min_amount() -> Decimal | None:
    """Returns the minimum amount or None"""
    if len(current_expenses) < 1:
        return None

    min_amount = current_expenses[0].amount
    for expense in current_expenses[1:]:
        if min_amount > expense.amount:
            min_amount = expense.amount

    return min_amount
     
def get_max_amount() -> Decimal | None:
    """Returns the maximum amount or None"""
    if len(current_expenses) < 1:
        return None

    max_amount = current_expenses[0].amount
    for expense in current_expenses[1:]:
            if max_amount < expense.amount:
                max_amount = expense.amount
    
    return max_amount

def get_amount_by_category(alternative_list: list[Expense] | None = None) -> dict[str, Decimal] | None:
    """Returns a dict containing all expenses category and their total amount or None"""
    if alternative_list is None:
        category_list = current_expenses
    else:
        category_list = alternative_list

    if len(category_list) < 1:
        return None

    category_dict = {}
    for expense in category_list:
        if expense.category.name in category_dict:
            amount_before = category_dict[expense.category.name]
            category_dict[expense.category.name] = amount_before + expense.amount
        else:
            category_dict[expense.category.name] = expense.amount

    return category_dict

def get_expensive_category(category_dict: dict[str, Decimal] | None) -> list[dict[str, Decimal]] | None:
    """Returns a dict containing only expensive category and their total amount or None"""
    if category_dict is None or not category_dict:
        return None
    
    first_key = list(category_dict.keys())[0]
    first_value = list(category_dict.values())[0]
    expensive_category = {"name": first_key, "amount": first_value}

    expensive_list = []
    for key, value in category_dict.items():
        if expensive_category["amount"] < value:
            expensive_category["name"] = key
            expensive_category['amount'] = value
    expensive_list.append(expensive_category)
    
    for key, value in category_dict.items():
            temp_category = {}
            if expensive_category["amount"] == value and expensive_category["name"] != key:
                temp_category["name"] = key
                temp_category['amount'] = value
                expensive_list.append(temp_category)
    return expensive_list

def get_monthly_report(month: int, year: int) -> dict | None:
    """Returns a monthly expense report"""
    all_expenses = storage.get_all_expenses()
    monthy_expenses = []

    temp_year = year
    temp_month = month

    # calculate the date end range
    first_day = date(temp_year, temp_month, 1)
    if temp_month == 12: 
        temp_month = 1 
        temp_year = temp_year + 1
    else:
        temp_month = temp_month + 1
    last_day = date(temp_year, temp_month, 1)

    for expense in all_expenses:
        if first_day <= expense.expense_date < last_day:
            monthy_expenses.append(expense)

    if monthy_expenses == []:
        return None

    categories = get_amount_by_category(monthy_expenses)
    expensive_category = get_expensive_category(categories)

    month_report = {}
    month_report["date"] = f"{month_name[month]} {year}"
    month_report["total_expenses"] = len(monthy_expenses)
    month_report["total_amount"] = get_total_amount(monthy_expenses)
    month_report["expensive_category"] = expensive_category
    return month_report

def get_yearly_report(year: int) -> dict | None:
    """Returns a yearly expense report"""
    all_expenses = storage.get_all_expenses()
    yearly_expenses = []

    # calculate the date end range
    first_day = date(year, 1, 1)
    last_day = date(year+1, 1, 1)

    for expense in all_expenses:
        if first_day <= expense.expense_date < last_day:
            yearly_expenses.append(expense)

    if yearly_expenses == []:
        return None

    categories = get_amount_by_category(yearly_expenses)
    expensive_category = get_expensive_category(categories)

    year_report = {}
    year_report["year"] = year
    year_report["total_expenses"] = len(yearly_expenses)
    year_report["total_amount"] = get_total_amount(yearly_expenses)
    year_report["expensive_category"] = expensive_category
    return year_report