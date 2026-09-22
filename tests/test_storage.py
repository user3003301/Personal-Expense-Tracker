import pytest
from decimal import Decimal

from src import storage
from src.models import Expense, Category


# Function to initialise an expense
@pytest.fixture
def storage_test_configure(request):
    expense = Expense("Sandwich", Decimal("5"), Category("Food"))
    storage.add_expense(expense)
    yield expense

    storage.delete_expense(expense.id)

# Test add of a expense in storage list
def test_add_expense():
    expense = Expense("Sandwich", Decimal("5"), Category("Food"))
    storage.add_expense(expense)
    assert expense.id is not None
    storage.delete_expense(expense.id)

# Test the increment of the id counter after adding an expense
def test_increment_id(storage_test_configure):
    expense = storage_test_configure
    new_id = expense.id+1
    assert storage.count == new_id

# Test the search of an existent expense by its ID
def test_search_existent_expense(storage_test_configure):
    expense = storage_test_configure
    assert storage.search_expense(expense.id) is not None
    assert storage.search_expense(expense.id) == expense

# Test the search of a non-existent expense by its ID
def test_search_nonexistent_expense():
    assert storage.search_expense(15) is None

# Test the update an existent expense
def test_update_existent_expense(storage_test_configure):
    expense = storage_test_configure
    updated_expense = Expense("Hamburger", Decimal("7"), Category("Food"))
    saved_id = expense.id
    update_result = storage.update_expense(expense.id, updated_expense)
    assert update_result == True
    x = storage.search_expense(expense.id)
    assert x.id == saved_id

# Test the update a non-existent expense
def test_update_nonexistent_expense():
    updated_expense = Expense("Hamburger", Decimal("7"), Category("Food"))
    update_result = storage.update_expense(15, updated_expense)
    assert update_result == False

# Test the deletion of an existing expense
def test_delete_existent_expense():
    expense = Expense("Sandwich", Decimal("5"), Category("Food"))
    storage.add_expense(expense)
    result = storage.delete_expense(expense.id)
    assert result == True
    assert storage.search_expense(expense.id) is None

# Test the deletion of an non-existing expense
def test_delete_nonexisting_expense():
    result = storage.delete_expense(15)
    assert result == False

# Test the copy of list expenses
def test_get_all_expenses():
    expense1 = Expense("Sandwich", Decimal("5"), Category("Food"))
    expense2 = Expense("Beer", Decimal("2.5"), Category("Drink"))
    storage.add_expense(expense1)
    storage.add_expense(expense2)

    current_expenses_list = storage.get_all_expenses()

    expense3 = Expense("Fries", Decimal("4"), Category("Food"))
    current_expenses_list.append(expense3)
    
    assert current_expenses_list != storage.get_all_expenses()
    storage.delete_expense(expense1.id)
    storage.delete_expense(expense2.id)