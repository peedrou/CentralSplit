from app.support.abstracts.createExpense import AbstractCreateExpense

from dataclasses import dataclass
from typing import List
from enum import Enum

class SplitMethod(Enum):
    EQUAL = "equal"
    CUSTOM = "custom"

@dataclass
class CreateExpense(AbstractCreateExpense):
    amount: float
    payer: str
    receivers: List[str] | str
    group: str | None
    splitMethod: SplitMethod


    def handle_make_expense(self):
        pass

    def handle_add_expense_to_payer(self):
        pass

    def handle_add_expense_to_receivers_equal(self):
        pass

    def handle_add_expense_to_receivers_custom(self, custom_amounts: List[float]):
        pass

    def handle_add_expense_to_group(self):
        pass