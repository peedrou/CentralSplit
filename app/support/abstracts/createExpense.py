from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List

@dataclass
class AbstractCreateExpense(ABC):
    amount: float
    payers: List[str] | str
    receivers: List[str] | str
    splitMethod: any #to change


    @abstractmethod
    def make_expense(self):
        pass

    @abstractmethod
    def add_expense_to_payers(self):
        pass

    @abstractmethod
    def add_expense_to_receivers(self):
        pass

    @abstractmethod
    def add_expense_to_group(self):
        pass