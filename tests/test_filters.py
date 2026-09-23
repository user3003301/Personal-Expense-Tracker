import pytest
from datetime import date
from decimal import Decimal

from src.storage import load_expenses
from src.models import Expense, Category
from src import filters, utility


# Read the expenses in the JSON file
@pytest.fixture
def set_up_list():
    load_expenses("tests/expenses_test.json")
    filters.set_filter_list()
    yield
    # TODO aggiungi un reset globale (Forse)

# Help the tests for assert list serialized with deserialized one
def build_expected_expenses(expected_list: list) -> list:
    serialized_list = []
    for expense_data in expected_list:
        expense_id = expense_data.get("id")
        name = expense_data.get("name")
        amount = Decimal(expense_data.get("amount"))
        category = Category(expense_data.get("category"))
        expense_date = utility.string_to_date(expense_data.get("expense_date"))
        loaded_expense = Expense(name, amount, category, expense_date)
        loaded_expense._id = expense_id
        serialized_list.append(loaded_expense)
    return serialized_list


# Test the category filter applied to expenses produce result
def test_filter_by_category(set_up_list):
    expected_json_value = [
        {"id":1,"name":"Normal Pizza","amount":"6.00","category":"Food","expense_date":"12/08/2026"},
        {"id":2,"name":"Pepperoni Pizza","amount":"7.00","category":"Food","expense_date":"12/08/2026"},
        {"id":3,"name":"Naples Pizza","amount":"7.00","category":"Food","expense_date":"12/08/2026"},
        {"id":4,"name":"Four Cheese Pizza","amount":"8.00","category":"Food","expense_date":"12/08/2026"},
        {"id":5,"name":"Special Pizza","amount":"10.00","category":"Food","expense_date":"12/08/2026"},
        {"id":7,"name":"Mixed Grill","amount":"30.00","category":"Food","expense_date":"01/09/2026"}
    ]
    expected_list = build_expected_expenses(expected_json_value)

    filtered_list = filters.filter_by_category("Food")
    assert len(filtered_list) == 6
    assert filtered_list == expected_list

# Test the category filter applied to expenses prodeuce an empty list
def test_filter_by_category_without_result(set_up_list):
    filtered_list = filters.filter_by_category("")
    assert filtered_list == []

# Test the minimum cost filter applied to expenses
def test_filter_by_minimum_cost(set_up_list):
    expected_json_value = [
        {"id":6,"name":"Champagne 96'","amount":"1500","category":"Drink","expense_date":"01/09/2026"},
        {"id":8,"name":"Smoking","amount":"500","category":"Clothes","expense_date":"25/09/2026"},
        {"id":10,"name":"New Car","amount":"40000","category":"Transport","expense_date":"01/12/2026"}
    ]
    expected_list = build_expected_expenses(expected_json_value)

    filtered_list = filters.filter_by_cost(Decimal("100"), None)
    assert len(filtered_list) == 3
    assert filtered_list == expected_list

# Test the maximum cost filter applied to expenses
def test_filter_by_maximum_cost(set_up_list):
    expected_json_value = [
        {"id":1,"name":"Normal Pizza","amount":"6.00","category":"Food","expense_date":"12/08/2026"},
        {"id":2,"name":"Pepperoni Pizza","amount":"7.00","category":"Food","expense_date":"12/08/2026"},
        {"id":3,"name":"Naples Pizza","amount":"7.00","category":"Food","expense_date":"12/08/2026"},
        {"id":4,"name":"Four Cheese Pizza","amount":"8.00","category":"Food","expense_date":"12/08/2026"},
        {"id":5,"name":"Special Pizza","amount":"10.00","category":"Food","expense_date":"12/08/2026"}
        ]
    expected_list = build_expected_expenses(expected_json_value)

    filtered_list = filters.filter_by_cost(None, Decimal("10"))
    assert len(filtered_list) == 5
    assert filtered_list == expected_list

# Test the range price filter applied to expenses
def test_filter_by_range_cost(set_up_list):
    expected_json_value = [
        {"id":5,"name":"Special Pizza","amount":"10.00","category":"Food","expense_date":"12/08/2026"},
        {"id":7,"name":"Mixed Grill","amount":"30.00","category":"Food","expense_date":"01/09/2026"}
        ]
    expected_list = build_expected_expenses(expected_json_value)

    filtered_list = filters.filter_by_cost(Decimal("10"), Decimal("50"))
    assert len(filtered_list) == 2
    assert filtered_list == expected_list

# Test the range price filter applied to expenses produce no result
def test_filter_by_cost_without_result(set_up_list):
    filtered_list = filters.filter_by_cost(Decimal("100"), Decimal("0"))
    print(filtered_list)
    assert filtered_list == []

# Test the date filter applied to expenses
def test_filter_by_date_only(set_up_list):
    expected_json_value = [
        {"id":6,"name":"Champagne 96'","amount":"1500","category":"Drink","expense_date":"01/09/2026"},
        {"id":7,"name":"Mixed Grill","amount":"30.00","category":"Food","expense_date":"01/09/2026"}
        ]
    expected_list = build_expected_expenses(expected_json_value)
    

    filtered_list = filters.filter_by_date(date(2026,9,1))
    assert len(filtered_list) == 2
    assert filtered_list == expected_list

# Test the date range filter applied to expenses
def test_filter_by_date_range(set_up_list):
    expected_json_value = [
        {"id":6,"name":"Champagne 96'","amount":"1500","category":"Drink","expense_date":"01/09/2026"},
        {"id":7,"name":"Mixed Grill","amount":"30.00","category":"Food","expense_date":"01/09/2026"},
        {"id":8,"name":"Smoking","amount":"500","category":"Clothes","expense_date":"25/09/2026"},
        {"id":9,"name":"Dior Perfume","amount":"79.99","category":"Accessories","expense_date":"26/09/2026"}
        ]
    expected_list = build_expected_expenses(expected_json_value)

    filtered_list = filters.filter_by_date_range(date(2026,9,1), date(2026,10,1))
    assert len(filtered_list) == 4
    assert filtered_list == expected_list

# Test the start date filter applied to expenses
def test_filter_by_start_date(set_up_list):
    expected_json_value = [
        {"id":6,"name":"Champagne 96'","amount":"1500","category":"Drink","expense_date":"01/09/2026"},
        {"id":7,"name":"Mixed Grill","amount":"30.00","category":"Food","expense_date":"01/09/2026"},
        {"id":8,"name":"Smoking","amount":"500","category":"Clothes","expense_date":"25/09/2026"},
        {"id":9,"name":"Dior Perfume","amount":"79.99","category":"Accessories","expense_date":"26/09/2026"},
        {"id":10,"name":"New Car","amount":"40000","category":"Transport","expense_date":"01/12/2026"}
        ]
    expected_list = build_expected_expenses(expected_json_value)    

    filtered_list = filters.filter_by_date_range(date(2026,9,1), None)
    assert len(filtered_list) == 5
    assert filtered_list == expected_list

# Test the end date filter applied to expenses
def test_filter_by_end_date(set_up_list):
    expected_json_value = [
        {"id":1,"name":"Normal Pizza","amount":"6.00","category":"Food","expense_date":"12/08/2026"},
        {"id":2,"name":"Pepperoni Pizza","amount":"7.00","category":"Food","expense_date":"12/08/2026"},
        {"id":3,"name":"Naples Pizza","amount":"7.00","category":"Food","expense_date":"12/08/2026"},
        {"id":4,"name":"Four Cheese Pizza","amount":"8.00","category":"Food","expense_date":"12/08/2026"},
        {"id":5,"name":"Special Pizza","amount":"10.00","category":"Food","expense_date":"12/08/2026"},
        {"id":6,"name":"Champagne 96'","amount":"1500","category":"Drink","expense_date":"01/09/2026"},
        {"id":7,"name":"Mixed Grill","amount":"30.00","category":"Food","expense_date":"01/09/2026"},
        {"id":8,"name":"Smoking","amount":"500","category":"Clothes","expense_date":"25/09/2026"},
        {"id":9,"name":"Dior Perfume","amount":"79.99","category":"Accessories","expense_date":"26/09/2026"}
        ]
    expected_list = build_expected_expenses(expected_json_value)

    filtered_list = filters.filter_by_date_range(None, date(2026,10,1))
    assert len(filtered_list) == 9
    assert filtered_list == expected_list

# Test the date range filter applied to expenses produce no result
def test_filter_by_date_range_without_result(set_up_list):
    filtered_list = filters.filter_by_date_range(date(1900,1,1), date(1900,1,1))
    assert filtered_list == []

# Test the combination of more filter applied to expenses
def test_filter_using_multiple_filter(set_up_list):
    expected_json_value = [
        {"id":1,"name":"Normal Pizza","amount":"6.00","category":"Food","expense_date":"12/08/2026"},
        {"id":2,"name":"Pepperoni Pizza","amount":"7.00","category":"Food","expense_date":"12/08/2026"},
        {"id":3,"name":"Naples Pizza","amount":"7.00","category":"Food","expense_date":"12/08/2026"},
        {"id":4,"name":"Four Cheese Pizza","amount":"8.00","category":"Food","expense_date":"12/08/2026"},
        {"id":5,"name":"Special Pizza","amount":"10.00","category":"Food","expense_date":"12/08/2026"},
        {"id":7,"name":"Mixed Grill","amount":"30.00","category":"Food","expense_date":"01/09/2026"}
        ]
    expected_list = build_expected_expenses(expected_json_value)

    filters.filter_by_category("Food")
    filters.filter_by_cost(Decimal("1"), Decimal("100"))
    filtered_list = filters.filter_by_date_range(date(2026,1,1), date(2026,12,31))
    assert len(filtered_list) == 6
    assert filtered_list == expected_list

# Test reset filter applied to expenses
def test_reset_filter(set_up_list):
    original_list = filters.get_filtered_expenses()

    filtered_list = filters.filter_by_category("Clothes")
    current_list = filters.get_filtered_expenses()
    assert filtered_list == current_list

    filters.set_filter_list()
    current_list = filters.get_filtered_expenses()
    assert current_list == original_list