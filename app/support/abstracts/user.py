from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Dict

@dataclass
class AbstractUser(ABC):
    email: str
    username: str
    UID: str
    groups: List[str]
    friends: List[str]
    usersToPay: Dict[str, float]
    usersToReceive: Dict[str, float]
    totalToPay: float
    totalToReceive: float

    @abstractmethod
    def pay_user(self, userID: str, amount: float):
        pass

    @abstractmethod
    def create_group(self, userIDS: List[str], groupName: str):
        pass

    @abstractmethod
    def add_users_to_group(self, userIDS: List[str], groupName: str):
        pass

    @abstractmethod
    def remove_users_from_group(self, userIDS: List[str], groupName: str):
        pass

    @abstractmethod
    def create_expense(self, payers: List[str] | str, receivers: List[str] | str, amount: float):
        pass

    @abstractmethod
    def check_total_balance(self):
        pass

    @abstractmethod
    def add_friend(self, userID: str):
        pass

    @abstractmethod
    def remove_friend(self, userID: str):
        pass

    @abstractmethod
    def check_debt_with_friend(self, userID: str):
        pass

    @abstractmethod
    def get_payment(self, userID: str, amount: float):
        pass