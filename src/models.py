# Contains model data

from decimal import Decimal, ROUND_HALF_UP
from datetime import date
from dataclasses import dataclass, field

# TODO think about Python compatibility
# @dataclass was added in Python 3.7, use @attr for Python 2.7 and later.

@dataclass
class Expense:
    """Represents a single expense"""
    _name: str
    _amount: Decimal = field(compare=True)
    _category: object
    _dateOfRegistration: date = field(default=date.today())


    @property
    def name(self) -> str:
        """the name of the expense"""
        return self._name

    @name.setter
    def name(self, value) -> None:
        if not isinstance(value, str):
            raise TypeError("Description must be a string")
        self._name = value

    @property
    def amount(self) -> Decimal:
        """the cost of the expense"""
        return self._amount

    @amount.setter
    def amount(self, value) -> None:
        if not isinstance(value, float):
            raise TypeError("Amount must be a float")
        price = Decimal(value)
        self._amount = price.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

    @property
    def category(self) -> object:
        """the category of the expense"""
        return self._category
    
    @category.setter
    def category(self, value) -> None:
        if not isinstance(value, Category):
            raise TypeError("Category must be a Category object")
        self._category = value

    @property
    def dateOfRegistration(self) -> date:
        """the expense date"""
        return self._dateOfRegistration

    @dateOfRegistration.setter
    def dateOfRegistration(self, value) -> None:
        if not isinstance(value, date):
            raise TypeError("The date must be a date(year, mounth, day)")
        self._dateOfRegistration = value

    # print class variable
    def __str__(self) -> str:
        return f"name: {self._name}, amount: {self._amount}, category[{self._category}], date: {self._dateOfRegistration}\n"


@dataclass
class Category:
    """Represents a category"""
    _name: str = field(repr=True)
    

    # getter and setter
    @property
    def name(self) -> str:
        """the name of the category"""
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        if (not isinstance(value, str)) or len(value) < 1:
            print("the category name must be a string, setting to: Not Setted")
            self._name = "Not Setted"
        self._name = value

    # print class variable
    def __str__(self) -> str:
        return f"name: {self._name}"