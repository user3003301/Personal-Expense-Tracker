# Test for models.py

import pytest
from contextlib import nullcontext as do_not_raise
from decimal import Decimal
from datetime import date

from src.models import Expense, Category
from src.storage import add_expense


class TestCategory:
    @pytest.mark.parametrize("example_input, expectation", [
    ("Food", do_not_raise()),
    (10, pytest.raises(TypeError)),
    ("", pytest.raises(ValueError)),
    ("    ", pytest.raises(ValueError)),
    ])

    # Test the creation of Category
    def test_create_category(self, example_input, expectation):
        with expectation:
            Category(example_input)

    # Test the getter
    def test_getter_name(self):
        category = Category("Drink")
        assert category.name == "Drink"

    # Test the setter of a valid Category name
    def test_valid_name(self):
        category = Category("Not setted")
        category.name = "Drink"
        assert category.name == "Drink"

    # Test the setter of an invalid Category name
    @pytest.mark.parametrize("value, expectation", [
        (20, pytest.raises(TypeError)),
        ("", pytest.raises(ValueError)),
        ("    ", pytest.raises(ValueError)),
        ])
    def test_invalid_name(self, value, expectation):
        category = Category("Not setted")
        with expectation:
            category.name = value

    # Test the __str__ of Category class
    def test_str_(self):
        category = Category("Drink")
        category_string = str(category)
        assert category_string == "name: Drink"


class TestExpense:
    # Arrange
    @pytest.fixture
    def default_expense(self):
        return Expense("Water", Decimal("1"), Category("Drink"))

    # Create expense with valid data
    def test_create_expense(self, default_expense):
        expense = Expense("Water", Decimal("1"), Category("Drink"))
        assert expense == default_expense

    # Test for set valid name
    def test_valid_name(self, default_expense):
        expense = default_expense
        expense.name = "Beer"
        assert expense.name == "Beer"

    # Test for set invalid name
    @pytest.mark.parametrize("value, expectation", [
        (10, pytest.raises(TypeError)),
        ("", pytest.raises(ValueError)),
        ("  ", pytest.raises(ValueError)),
    ])
    def test_invalid_name(self, default_expense, value, expectation):
        expense = default_expense
        with expectation:
            expense.name = value

    # Test for set valid amount
    def test_valid_amount(self, default_expense):
        expense = default_expense
        expense.amount = Decimal("10.505")
        assert expense.amount == Decimal("10.51")
        
    # Test for set invalid amount
    @pytest.mark.parametrize("value, expectation", [
        (100, pytest.raises(TypeError)),
        (Decimal("0"), pytest.raises(ValueError)),
        (Decimal("-20"), pytest.raises(ValueError)),
    ])
    def test_invalid_amount(self, default_expense, value, expectation):
        expense = default_expense
        with expectation:
            expense.amount = value

    # Test for set valid category
    def test_valid_category(self, default_expense):
        expense = default_expense
        expense.category = Category("Food")
        assert expense.category == Category("Food")

    # Test for set invalid category
    @pytest.mark.parametrize("value, expectation", [
        (20, pytest.raises(TypeError)),
        ("Food", pytest.raises(TypeError)), 
    ])
    def test_invalid_category(self, default_expense, value, expectation):
        expense = default_expense
        with expectation:
            expense.category = value

    # Test for set valid expense_date
    def test_valid_date(self, default_expense):
        expense = default_expense
        expense.expense_date = date(2000, 1, 1)
        assert expense.expense_date == date(2000, 1, 1)

    # Test for set invalid date
    @pytest.mark.parametrize("value, expectation", [
        (None, pytest.raises(TypeError)),
        ("2000/01/01",  pytest.raises(TypeError)),
        (2000,  pytest.raises(TypeError)),
    ])
    def test_invalid_date(self, default_expense, value, expectation):
        expense = default_expense
        with expectation:
            expense.expense_date = value

    # Test if two expense are equal even if they have different ID 
    def test_equal_expenses(self):
        expense1 = Expense("Pizza", Decimal(7), Category("Food"))
        expense2 = Expense("Pizza", Decimal(7), Category("Food"))

        # assign id
        add_expense(expense1)
        add_expense(expense2)

        assert expense1.id != expense2.id
        assert expense1 == expense2

    # Test if two expense are not equal by comaparing their date
    def test_notequal_expenses(self):
        expense1 = Expense("Pizza", Decimal(7), Category("Food"), date(2026,1,1))
        expense2 = Expense("Pizza", Decimal(7), Category("Food"), date(2026,1,30))
        
        assert expense1.expense_date != expense2.expense_date
        assert expense1 != expense2

    # Test if the id = None by default
    def test_id_is_none(self, default_expense):
        expense = default_expense
        assert expense._id is None