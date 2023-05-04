from dataclasses import dataclass
from typing import List, Dict
from app.data.db_methods import DataBaseMethods as DBM
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

    def pay_user(self, userID: str, amount: float):
        db = DBM.get_db()

    def create_group(self, userIDS: List[str], groupName: str):
        db = DBM.get_db()

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

    