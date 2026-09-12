# Contains model data

from decimal import Decimal, ROUND_HALF_UP
from datetime import date
import utility
from dataclasses import dataclass, field


@dataclass
class Category:
    """Represents a category"""
    _name: str
    
    def __post_init__(self):
        self.name = self._name

    @property
    def name(self) -> str:
        """the category name"""
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        if not isinstance(value, str):
            raise TypeError("The category name must be a string")
        if len(value) < 1 or value.isspace():
            raise ValueError("the category name cannot be empty or whitespace")
        self._name = value

    def __str__(self) -> str:
        return f"name: {self._name}"


@dataclass
class Expense:
    """Represents a single expense"""
    _id: int | None = field(init=False, compare=False, default=None)
    _name: str
    _amount: Decimal
    _category: Category
    _expense_date: date = field(default=None)

    def __post_init__(self):
        self.name = self._name
        self.amount = self._amount
        self.category = self._category
        if self._expense_date is not None:
            self.expense_date = self._expense_date
        else:
            self.expense_date = date.today()

    @property
    def id(self):
        """the id of the expense"""
        return self._id

    @property
    def name(self) -> str:
        """the name of the expense"""
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        if not isinstance(value, str):
            raise TypeError("The name of the expense must be a string")
        if len(value) < 1 or value.isspace():
                    raise ValueError("the name of the expense cannot be empty or whitespace")
        self._name = value

    @property
    def amount(self) -> Decimal:
        """the cost of the expense"""
        return self._amount

    @amount.setter
    def amount(self, value: Decimal) -> None:
        if not isinstance(value, Decimal):
            raise TypeError("the cost must be a Decimal")
        price = Decimal(value)
        self._amount = price.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

    @property
    def category(self) -> Category:
        """the category of the expense"""
        return self._category
    
    @category.setter
    def category(self, value: Category) -> None:
        if not isinstance(value, Category):
            raise TypeError("the category must be a Category object")
        self._category = value

    @property
    def expense_date(self) -> date:
        """the expense date"""
        return self._expense_date

    @expense_date.setter
    def expense_date(self, value: date) -> None:
        if not isinstance(value, date):
            raise TypeError("The date must be a date(year, month, day)")
        self._expense_date = value

    # print class variable
    def __str__(self) -> str:
        return "id: {}, name: {}, amount: {}, category[{}], date: {}".format(
            self._id, self._name, self._amount, self._category, utility.date_to_string(self._expense_date)
            )
    