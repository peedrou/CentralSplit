from app.support.abstracts.createExpense import AbstractCreateExpense
from app.data.db_methods import DataBaseMethods as DBM
from google.cloud import firestore as fs

from dataclasses import dataclass
from typing import List, Optional
from enum import Enum

class SplitMethod(Enum):
    EQUAL = "equal"
    CUSTOM = "custom"
    SINGLE = "single"

@dataclass
class CreateExpense(AbstractCreateExpense):
    amount: float
    payer: str
    receivers: List[str] | str
    customAmounts: List[float] | None
    group: str | None
    splitMethod: SplitMethod

    def __post_init__(self):
        if isinstance(self.receivers, list) and isinstance(self.customAmounts, list):
            if len(self.receivers) != len(self.customAmounts):
                raise ValueError("Length of receivers must be the same as length of custom amounts.")

    def handle_make_expense(self):
        db = DBM.get_db()
        payer_doc = DBM.check_if_property_exists_in_collection_and_return_doc(db, "Users", "username", self.payer)[0]
        receiver_docs = self.get_receiver_docs()

        if isinstance(self.group, str):
            group_doc = DBM.check_if_property_exists_in_collection_and_return_doc(db, "Groups", "groupName", self.group)
            self.handle_add_expense_to_group(group_doc)

        if isinstance(self.receivers, str):
            self.handle_add_expense_to_payer(payer_doc, None)
        else:
            for i in range(len(self.receivers)):
                self.handle_add_expense_to_payer(payer_doc, i)
        
        self.sort_split_method_and_handle_request(receiver_docs)

    def handle_add_expense_to_payer(self, doc_ref: fs.DocumentReference, index: int | None):
        if index is None:
            DBM.update_document_array_attribute(doc_ref, {"usersToPay":self.receivers})
            DBM.update_document_non_array_attribute(doc_ref, {f"moneyTO{self.receivers}": self.amount})
            total_to_pay_current_value = DBM.check_if_property_exists_in_document_with_doc_ref_and_return_value(doc_ref, "totalToPay")
            DBM.update_document_non_array_attribute(doc_ref, {"totalToPay": total_to_pay_current_value + self.amount})
        else:
            amount_to_each_receiver = self.amount/len(self.receivers)
            DBM.update_document_array_attribute(doc_ref, {"usersToPay":self.receivers[index]})
            DBM.update_document_non_array_attribute(doc_ref, {f"moneyTO{self.receivers[index]}": amount_to_each_receiver})
            total_to_pay_current_value = DBM.check_if_property_exists_in_document_with_doc_ref_and_return_value(doc_ref, "totalToPay")
            DBM.update_document_non_array_attribute(doc_ref, {"totalToPay": total_to_pay_current_value + amount_to_each_receiver})

    def handle_add_expense_to_receivers_equal(self, doc_ref: fs.DocumentReference):
        amount_to_each_receiver = self.amount/len(self.receivers)

        DBM.update_document_array_attribute(doc_ref, {"usersToReceive":self.payer})
        DBM.update_document_non_array_attribute(doc_ref, {f"moneyFROM{self.payer}": amount_to_each_receiver})
        total_to_receive_current_value = DBM.check_if_property_exists_in_document_with_doc_ref_and_return_value(doc_ref, "totalToReceive")
        DBM.update_document_non_array_attribute(doc_ref, {"totalToReceive": total_to_receive_current_value + amount_to_each_receiver})
    
    def handle_add_expense_to_receivers_single(self, doc_ref: fs.DocumentReference):
        DBM.update_document_array_attribute(doc_ref, {"usersToReceive":self.payer})
        DBM.update_document_non_array_attribute(doc_ref, {f"moneyFROM{self.payer}": self.amount})
        total_to_receive_current_value = DBM.check_if_property_exists_in_document_with_doc_ref_and_return_value(doc_ref, "totalToReceive")
        DBM.update_document_non_array_attribute(doc_ref, {"totalToReceive": total_to_receive_current_value + self.amount})

    def handle_add_expense_to_receivers_custom(self, doc_ref: fs.DocumentReference, custom_amount: float):
        DBM.update_document_array_attribute(doc_ref, {"usersToReceive":self.payer})
        DBM.update_document_non_array_attribute(doc_ref, {f"moneyFROM{self.payer}": custom_amount})
        total_to_receive_current_value = DBM.check_if_property_exists_in_document_with_doc_ref_and_return_value(doc_ref, "totalToReceive")
        DBM.update_document_non_array_attribute(doc_ref, {"totalToReceive": total_to_receive_current_value + custom_amount})

    def handle_add_expense_to_group(self, doc_ref: fs.DocumentReference):
        total_debt = DBM.check_if_property_exists_in_document_with_doc_ref_and_return_value(doc_ref, "totalExpenses")
        DBM.update_document_non_array_attribute(doc_ref, {"totalExpenses": total_debt + self.amount})

    def get_receiver_docs(self):
        db = DBM.get_db()
        if isinstance(self.receivers, str):
            receiver_docs = []
            receiver_doc = DBM.check_if_property_exists_in_collection_and_return_doc(db, "Users", "username", self.receivers)[0]
            receiver_docs.append(receiver_doc)
            return receiver_docs
        else:
            receiver_docs = []
            for receiver in self.receivers:
                receiver_doc = DBM.check_if_property_exists_in_collection_and_return_doc(db, "Users", "username", receiver)[0]
                receiver_docs.append(receiver_doc)
            return receiver_docs
        
    def check_if_only_one_receiver_doc(self, doc_refs: List[fs.DocumentReference]) -> bool:
        if len(doc_refs) == 1:
            return True
        else:
            return False
        
    def sort_split_method_and_handle_request(self, receiver_docs):
        if self.splitMethod == "equal":
            for i in range(len(self.receivers)):
                self.handle_add_expense_to_receivers_equal(receiver_docs[i])
        elif self.splitMethod == "single":
            only_one_receiver = self.check_if_only_one_receiver_doc(receiver_docs)
            if only_one_receiver == True:
                self.handle_add_expense_to_receivers_single(receiver_docs[0])
            else:
                raise Exception("You cannot use single option for multiple receivers")
        else:
            for i in range(len(self.receivers)):
                self.handle_add_expense_to_receivers_custom(receiver_docs[i], self.customAmounts[i])