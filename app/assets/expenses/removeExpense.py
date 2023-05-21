from dataclasses import dataclass
from typing import List

from app.support.abstracts.removeExpense import AbstractRemoveExpense
from app.data.db_methods import DataBaseMethods as DBM
from google.cloud import firestore as fs

@dataclass
class RemoveExpense(AbstractRemoveExpense):
    amount: float
    payer: str
    receivers: List[str] | str
    group: str | None


    def remove_expense_amount(self):
        db = DBM.get_db()
        expense_exists = self.check_if_expense_exists(db)


    def eliminate_expense(self):
        pass

    def remove_expense_from_payers(self):
        pass

    def remove_expense_from_receivers(self):
        pass

    def remove_expense_from_group(self):
        pass

    def check_if_expense_exists(self, db: fs.Client) -> bool:
        user_doc = DBM.check_if_property_exists_in_collection_and_return_doc(db, "Users", "username", self.payer)[0]
        try:
            if isinstance(self.receivers, str):
                result = DBM.check_if_property_exists_in_document_with_doc_ref_and_return_value(user_doc, f"moneyTO{self.receivers}")
                if result != False:
                    return True
                else:
                    return False
            else:
                for receiver in self.receivers:
                    result = DBM.check_if_property_exists_in_document_with_doc_ref_and_return_value(user_doc, f"moneyTO{receiver}")
                    if result == False:
                        return False
                return True
        except Exception as e:
            print(f"Error: {e}")

    def check_if_expense_is_going_to_be_eliminated(self, db: fs.Client) -> bool:
        pass