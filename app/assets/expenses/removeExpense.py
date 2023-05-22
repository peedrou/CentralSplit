from dataclasses import dataclass
from typing import List

from app.support.abstracts.removeExpense import AbstractRemoveExpense
from app.data.db_methods import DataBaseMethods as DBM
from google.cloud import firestore as fs

@dataclass
class RemoveExpense(AbstractRemoveExpense):
    amount_for_each: float
    payer: str
    receivers: List[str] | str
    group: str | None


    def handle_remove_expense_amount(self):
        db = DBM.get_db()
        expense_exists = self.check_if_expense_exists(db)

        if expense_exists == True:
            if isinstance(self.receivers, str):
                expense_will_be_eliminated = self.check_if_expense_is_going_to_be_eliminated(db, self.receivers)
                self.remove_expense_from_payer(db, self.receivers)
                self.remove_expense_from_receiver(db, self.receivers)

                if expense_will_be_eliminated == True:
                    self.eliminate_expense_from_receiver(db, self.receivers)
                    self.eliminate_expense_from_payer(db, self.receivers)
            else:
                for receiver in self.receivers:
                    expense_will_be_eliminated = self.check_if_expense_is_going_to_be_eliminated(db, receiver)
                    self.remove_expense_from_payer(db, receiver)
                    self.remove_expense_from_receiver(db, receiver)

                    if expense_will_be_eliminated == True:
                        self.eliminate_expense_from_receiver(db, receiver)
                        self.eliminate_expense_from_payer(db, receiver)

            if isinstance(self.group, str):
                self.remove_expense_from_group(db)
                
        else:
            raise Exception("You are not owing money to the receiver/s")


    def eliminate_expense_from_payer(self, db: fs.Client, receiver) -> None:
        try:
            user_doc = DBM.check_if_property_exists_in_collection_and_return_doc(db, "Users", "username", self.payer)[0]
            DBM.remove_document_non_array_attribute(user_doc, {f"moneyTO{receiver}": ""})
            DBM.remove_document_array_attribute(user_doc, {"usersToPay": receiver})
        except Exception as e:
            print(f"Error: {e}")

    def eliminate_expense_from_receiver(self, db: fs.Client, receiver) -> None:
        try:
            receiver_doc = DBM.check_if_property_exists_in_collection_and_return_doc(db, "Users", "username", receiver)[0]
            DBM.remove_document_non_array_attribute(receiver_doc, {f"moneyFROM{self.payer}": ""})
            DBM.remove_document_array_attribute(receiver_doc, {"usersToReceive": self.payer})
        except Exception as e:
            print(f"Error: {e}")

    def remove_expense_from_payer(self, db: fs.Client, receiver) -> None:
        try:
            user_doc = DBM.check_if_property_exists_in_collection_and_return_doc(db, "Users", "username", self.payer)[0]
            current_debt = DBM.check_if_property_exists_in_document_with_doc_ref_and_return_value(user_doc, f"moneyTO{receiver}")
            total_debt = DBM.check_if_property_exists_in_document_with_doc_ref_and_return_value(user_doc, "totalToPay")

            DBM.update_document_non_array_attribute(user_doc, {f"moneyTO{receiver}": current_debt - self.amount_for_each})
            DBM.update_document_non_array_attribute(user_doc, {"totalToPay": total_debt - self.amount_for_each})
        except Exception as e:
            print(f"Error: {e}")

    def remove_expense_from_receiver(self, db: fs.Client, receiver) -> None:
        try:
            receiver_doc = DBM.check_if_property_exists_in_collection_and_return_doc(db, "Users", "username", receiver)[0]
            current_debt = DBM.check_if_property_exists_in_document_with_doc_ref_and_return_value(receiver_doc, f"moneyFROM{self.payer}")
            total_debt = DBM.check_if_property_exists_in_document_with_doc_ref_and_return_value(receiver_doc, "totalToReceive")

            DBM.update_document_non_array_attribute(receiver_doc, {f"moneyFROM{self.payer}": current_debt - self.amount_for_each})
            DBM.update_document_non_array_attribute(receiver_doc, {"totalToReceive": total_debt - self.amount_for_each})
        except Exception as e:
            print(f"Error: {e}")

    def remove_expense_from_group(self, db: fs.Client):
        try:
            group_doc = DBM.check_if_property_exists_in_collection_and_return_doc(db, "Groups", "groupName", self.group)[0]
            total_debt = DBM.check_if_property_exists_in_document_with_doc_ref_and_return_value(group_doc, "totalExpenses")

            DBM.update_document_non_array_attribute(group_doc, {f"totalExpenses": total_debt - self.amount_for_each})
        except Exception as e:
            print(f"Error: {e}")

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

    def check_if_expense_is_going_to_be_eliminated(self, db: fs.Client, receiver) -> bool:
        user_doc = DBM.check_if_property_exists_in_collection_and_return_doc(db, "Users", "username", self.payer)[0]
        try:
            if isinstance(receiver, str):
                result = DBM.check_if_property_exists_in_document_with_doc_ref_and_return_value(user_doc, f"moneyTO{receiver}")
                if result == False:
                    return False
                elif result - self.amount_for_each > 0:
                    return False
                elif result - self.amount_for_each < 0:
                    raise Exception("The amount you are trying to pay is higher than the total debt")
                else:
                    return True
            else:
                raise Exception("Error: Something went wrong with eliminating the expense")
        except Exception as e:
            print(f"Error: {e}")