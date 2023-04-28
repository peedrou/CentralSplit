from dataclasses import dataclass
from typing import List, Dict

from app.support.abstracts.user import AbstractUser

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

    def pay_user(self, userID: str, amount: float):
        pass

    def create_group(self, userIDS: List[str], groupName: str):
        pass

    def add_users_to_group(self, userIDS: List[str], groupName: str):
        pass

    def remove_users_from_group(self, userIDS: List[str], groupName: str):
        pass

    def create_expense(self, payers: List[str] | str, receivers: List[str] | str, amount: float):
        pass

    def check_total_balance(self):
        pass

    def add_friend(self, userID: str):
        pass

    def remove_friend(self, userID: str):
        pass

    def get_payment(self, userID: str, amount: float):
        pass