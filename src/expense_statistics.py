# Elaborate expense statistics

from decimal import Decimal, ROUND_HALF_UP
import filters

current_expenses = []

def get_expenses_list():
    """Get the list of expenses from a filtered list"""
    global current_expenses
    current_expenses = filters.get_filtered_expenses()

def get_total_expenses() -> int:
    """Return the number of expenses in the list"""
    return len(current_expenses)

def get_total_amount() -> Decimal:
    """Returns the sum of the expenses"""
    total = Decimal('0')
    for expense in current_expenses:
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
    """Returns the minimum amount"""
    if len(current_expenses) < 1:
        return None

    min_amount = current_expenses[0].amount
    for expense in current_expenses[1:]:
        if min_amount > expense.amount:
            min_amount = expense.amount

    return min_amount
     
def get_max_amount() -> Decimal | None:
    """Returns the maximum amount"""
    if len(current_expenses) < 1:
        return None

    max_amount = current_expenses[0].amount
    for expense in current_expenses[1:]:
            if max_amount < expense.amount:
                max_amount = expense.amount
    
    return max_amount

def get_amount_by_category() -> dict[str, Decimal] | None:
    if len(current_expenses) < 1:
        return None

    category_dict = {}
    for expense in current_expenses:
        if expense.category.name in category_dict:
            amount_before = category_dict[expense.category.name]
            category_dict[expense.category.name] = amount_before + expense.amount
        else:
            category_dict[expense.category.name] = expense.amount

    return category_dict

     