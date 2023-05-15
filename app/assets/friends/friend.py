from dataclasses import dataclass
from typing import List

from app.data.db_methods import DataBaseMethods as DBM
from dotenv import load_dotenv

from app.support.abstracts.friend import AbstractFriend

@dataclass
class Friend(AbstractFriend):
    userEmail: str
    friendEmail: str
    totalToPay: float
    totalToReceive: float

    def handle_add_friend(self):
        friend_doc, user_doc, check_if_already_friend = self.fetch_friend_and_user_docs_and_check_if_already_friends()
        if check_if_already_friend == True:
            raise Exception("Already Friends")
        else:
            self.add_each_other_as_friend(friend_doc, user_doc)
            self.add_initial_expenses(friend_doc, user_doc)
            return True

    def handle_remove_friend(self):
        friend_doc, user_doc, check_if_already_friend = self.fetch_friend_and_user_docs_and_check_if_already_friends()
        if check_if_already_friend == False:
            raise Exception("Users are not friends")
        else:
            self.remove_each_other_as_friend(friend_doc, user_doc)
            self.remove_expenses_with_each_other(friend_doc, user_doc)
            return True

    def handle_check_debt_with_friend(self):
        friend_doc, user_doc, check_if_already_friend = self.fetch_friend_and_user_docs_and_check_if_already_friends()
        if check_if_already_friend == False:
            raise Exception("Users are not friends")
        else:
            userEmailWithoutHandle, friendEmailWithoutHandle = self.remove_email_handle()
            money_owed = DBM.check_if_property_exists_in_document_with_doc_ref_and_return_value(friend_doc, f'moneyFROM{userEmailWithoutHandle}')
            money_to_receive = DBM.check_if_property_exists_in_document_with_doc_ref_and_return_value(friend_doc, f'moneyTO{userEmailWithoutHandle}')
            return money_owed, money_to_receive


    def fetch_user_and_friend_doc(self, db):
        friend_docs = DBM.check_if_property_exists_in_collection_and_return_doc(db, 'Users', "email", self.friendEmail)
        user_docs = DBM.check_if_property_exists_in_collection_and_return_doc(db, 'Users', "email", self.userEmail)
        return friend_docs[0], user_docs[0]
    
    def add_each_other_as_friend(self, friend_doc, user_doc):
        DBM.update_document_array_attribute(friend_doc, {'friends': self.userEmail})
        DBM.update_document_array_attribute(user_doc, {'friends': self.friendEmail})

    def remove_each_other_as_friend(self, friend_doc, user_doc):
        DBM.remove_document_array_attribute(friend_doc, {'friends': self.userEmail})
        DBM.remove_document_array_attribute(user_doc, {'friends': self.friendEmail})

    def add_initial_expenses(self, friend_doc, user_doc):
        userEmailWithoutHandle, friendEmailWithoutHandle = self.remove_email_handle()

        DBM.update_document_non_array_attribute(friend_doc, {f'moneyFROM{userEmailWithoutHandle}': 0})
        DBM.update_document_non_array_attribute(friend_doc, {f'moneyTO{userEmailWithoutHandle}': 0})
        DBM.update_document_non_array_attribute(user_doc, {f'moneyFROM{friendEmailWithoutHandle}': 0})
        DBM.update_document_non_array_attribute(user_doc, {f'moneyTO{friendEmailWithoutHandle}': 0})

    def remove_expenses_with_each_other(self, friend_doc, user_doc):
        userEmailWithoutHandle, friendEmailWithoutHandle = self.remove_email_handle()

        DBM.remove_document_non_array_attribute(friend_doc, {f'moneyFROM{userEmailWithoutHandle}': 0})
        DBM.remove_document_non_array_attribute(friend_doc, {f'moneyTO{userEmailWithoutHandle}': 0})
        DBM.remove_document_non_array_attribute(user_doc, {f'moneyFROM{friendEmailWithoutHandle}': 0})
        DBM.remove_document_non_array_attribute(user_doc, {f'moneyTO{friendEmailWithoutHandle}': 0})

    def remove_email_handle(self):
        userEmailWithoutHandle = self.userEmail.split("@")[0]
        friendEmailWithoutHandle = self.friendEmail.split("@")[0]

        return userEmailWithoutHandle, friendEmailWithoutHandle

    def fetch_friend_and_user_docs_and_check_if_already_friends(self):
        db = DBM.get_db()
        friend_doc, user_doc = self.fetch_user_and_friend_doc(db)

        user_doc_snapshot = user_doc.get()
        user_doc_dict = user_doc_snapshot.to_dict()
        check_if_already_friend = DBM.check_if_property_exists_in_document_with_doc_ref(user_doc_dict, 'friends', self.friendEmail)
        return friend_doc,user_doc,check_if_already_friend