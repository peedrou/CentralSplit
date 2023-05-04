from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Dict

@dataclass
class AbstractFriend(ABC):
    UID: str
    email: str
    totalToPay: float
    totalToReceive: float

    @abstractmethod
    def add_friend(self, userID: str):
        pass

    @abstractmethod
    def remove_friend(self, userID: str):
        pass

    @abstractmethod
    def check_debt_with_friend(self, userID: str):
        pass