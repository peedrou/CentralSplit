from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List

@dataclass
class AbstractRemoveExpense(ABC):
    amount: float
    payer: str
    receivers: List[str] | str
    group: str | None


    @abstractmethod
    def handle_remove_expense_amount(self):
        pass

    @abstractmethod
    def eliminate_expense_from_payer(self):
        pass

    @abstractmethod
    def eliminate_expense_from_receiver(self):
        pass

    @abstractmethod
    def remove_expense_from_payer(self):
        pass

    @abstractmethod
    def remove_expense_from_receiver(self):
        pass

    @abstractmethod
    def remove_expense_from_group(self):
        pass
    
    @abstractmethod
    def check_if_expense_exists(self):
        pass

    @abstractmethod
    def check_if_expense_is_going_to_be_eliminated(self):
        pass