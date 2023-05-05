from dataclasses import dataclass
from typing import List, Dict
from app.data.db_methods import DataBaseMethods as DBM
from app.support.instantiation.instantiation import Instantiation as ITT
from dotenv import load_dotenv

from app.support.abstracts.user import AbstractUser

load_dotenv()

@dataclass
class User(AbstractUser):
    email: str
    UID: str
    groups: List[str]
    friends: List[str]
    usersToPay: Dict[str, float]
    usersToReceive: Dict[str, float]
    totalToPay: float
    totalToReceive: float

    def register_user(self):
        db = DBM.get_db()
        user_collection = DBM.get_collection(db, "Users")
        empty_user = DBM.create_empty_document(user_collection)
        doc_id = DBM.fetch_doc_id(empty_user)

        user_info = {
            "email":f"{self.email}",
            "UID":f"{doc_id}",
            "groups":self.groups,
            "friends":self.friends,
            "usersToPay":self.usersToPay,
            "usersToReceive":self.usersToReceive,
            "totalToPay":self.totalToPay,
            "totalToReceive":self.totalToReceive
        }
        try:
            user_status = DBM.check_if_property_exists(db, "Users", "email", self.email)
            if user_status == True:
                raise Exception("User already exists")
            else:
                DBM.add_new_info_to_document(empty_user, user_info)
                print(f"User was created with UID: {doc_id}")
                new_user = DBM.fetch_doc(db, "Users", doc_id)
                return new_user

        except Exception:
            raise Exception("User already exists")


    def pay_user(self, userID: str, amount: float):
        db = DBM.get_db()

    def create_group(self, userIDS: List[str], groupName: str):
        group = ITT.instantiate_group(userIDS=userIDS, groupName=groupName)
        response = group.handle_create_group()
        return response

    def add_users_to_group(self, userIDS: List[str], groupName: str):
        db = DBM.get_db()

    def remove_users_from_group(self, userIDS: List[str], groupName: str):
        db = DBM.get_db()

    def create_expense(self, payers: List[str] | str, receivers: List[str] | str, amount: float):
        db = DBM.get_db()

    def check_total_balance(self):
        db = DBM.get_db()

    def add_friend(self, userID: str):
        db = DBM.get_db()

    def remove_friend(self, userID: str):
        db = DBM.get_db()

    def get_payment(self, userID: str, amount: float):
        db = DBM.get_db()

    def check_debt_with_friend(self, userID: str):
        db = DBM.get_db()

    

    