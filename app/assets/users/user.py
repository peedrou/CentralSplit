from dataclasses import dataclass
from typing import List, Dict, Any
from app.data.db_methods import DataBaseMethods as DBM
from app.support.instantiation.instantiation import Instantiation as ITT
from app.assets.expenses.createExpense import SplitMethod
from dotenv import load_dotenv

from app.support.abstracts.user import AbstractUser

load_dotenv()

@dataclass
class User(AbstractUser):
    email: str
    username: str
    UID: str
    groups: List[str]
    friends: List[str]
    usersToPay: Dict[str, float]
    usersToReceive: Dict[str, float]
    totalToPay: float
    totalToReceive: float

    def register_user(self) -> Dict[str, Any]:
        db = DBM.get_db()
        user_collection = DBM.get_collection(db, "Users")
        empty_user = DBM.create_empty_document(user_collection)
        doc_id = DBM.fetch_doc_id(empty_user)

        user_info = {
            "email":f"{self.email}",
            "username": f"{self.username}",
            "UID":f"{doc_id}",
            "groups":self.groups,
            "friends":self.friends,
            "usersToPay":self.usersToPay,
            "usersToReceive":self.usersToReceive,
            "totalToPay":self.totalToPay,
            "totalToReceive":self.totalToReceive
        }
        try:
            user_status = DBM.check_if_property_exists_in_collection(db, "Users", "email", self.email)
            if user_status == True:
                raise Exception("User already exists")
            else:
                DBM.add_new_info_to_document(empty_user, user_info)
                print(f"User was created with UID: {doc_id}")
                new_user = DBM.fetch_doc_info(db, "Users", doc_id)
                return new_user

        except Exception:
            raise Exception("User already exists")

    def create_group(self, userIDS: List[str], groupName: str) -> Dict[str, Any]:
        group = ITT.instantiate_group(userIDS=userIDS, groupName=groupName)
        response = group.handle_create_group()
        return response
    
    def delete_group(self, userIDS: None, groupName: str) -> bool:
        group = ITT.instantiate_group(userIDS=userIDS, groupName=groupName)
        try:
            group.handle_delete_group()
            return True
        except Exception as e:
            print(f"Error: {e}")
            return False

    def add_users_to_group(self, userIDS: None, usersToAdd: List[str], groupName: str) -> list:
        group = ITT.instantiate_group(userIDS=userIDS, groupName=groupName)
        try:
            users_added = group.handle_add_users_to_group(usersToAdd)
            return users_added
        except Exception as e:
            print(f"Error: {e}")

    def remove_users_from_group(self, userIDS: None, usersToRemove: List[str], groupName: str) -> list:
        group = ITT.instantiate_group(userIDS=userIDS, groupName=groupName)
        try:
            users_removed = group.handle_remove_users_from_group(usersToRemove)
            return users_removed
        except Exception as e:
            print(f"Error: {e}")

    def add_friend(self, friendEmail: str, friendUsername: str) -> bool:
        friend = ITT.instantiate_friend(friendEmail, self.email, self.username, friendUsername)
        try:
            friend_added = friend.handle_add_friend()
            return friend_added
        except Exception as e:
            print(f"Error: {e}")

    def remove_friend(self, friendEmail: str, friendUsername: str) -> bool:
        friend = ITT.instantiate_friend(friendEmail, self.email, self.username, friendUsername)
        try:
            friend_removed = friend.handle_remove_friend()
            return friend_removed
        except Exception as e:
            print(f"Error: {e}")

    def check_debt_with_friend(self, friendEmail: str, friendUsername: str) -> str:
        friend = ITT.instantiate_friend(friendEmail, self.email, self.username, friendUsername)
        money_owed, money_to_receive = friend.handle_check_debt_with_friend()

        money_owed_message = f'You must pay {money_owed}'
        money_to_receive_message = f'You must receive {money_to_receive}'
        print(money_owed_message)
        print(money_to_receive_message)

        return money_owed_message, money_to_receive_message

    def create_expense(
            self,
            payer: str | str,
            receivers: List[str] | str,
            amount: float,
            group: str | None,
            split_method: SplitMethod,
            custom_amounts: List[float] | None
        ) -> bool:

        new_expense = ITT.instantiate_create_expense(
            amount=amount,
            payer=payer,
            receivers=receivers,
            group=group,
            customAmounts=custom_amounts,
            splitMethod=split_method
        )
        new_expense.handle_make_expense()
        return True

    def check_total_balance(self):
        db = DBM.get_db()

    def pay_user(self, userID: str, amount: float):
        db = DBM.get_db()

    def get_payment(self, userID: str, amount: float):
        db = DBM.get_db()


    

    