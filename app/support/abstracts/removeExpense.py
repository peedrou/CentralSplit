from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List

@dataclass
class AbstractRemoveExpense(ABC):
    amount: float
    payers: List[str] | str
    receivers: List[str] | str
    expense: any #to change


    @abstractmethod
    def remove_expense_amount(self):
        pass

    @abstractmethod
    def eliminate_expense(self):
        pass

    @abstractmethod
    def remove_expense_from_payers(self):
        pass

    @abstractmethod
    def remove_expense_from_receivers(self):
        pass

    @abstractmethod
    def remove_expense_from_group(self):
        pass