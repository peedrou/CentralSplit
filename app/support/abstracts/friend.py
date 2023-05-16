from abc import ABC, abstractmethod
from dataclasses import dataclass

@dataclass
class AbstractFriend(ABC):
    userEmail: str
    friendEmail: str
    userUsername: str
    friendUsername: str
    totalToPay: float
    totalToReceive: float

    @abstractmethod
    def handle_add_friend(self, userID: str):
        pass

    @abstractmethod
    def handle_remove_friend(self, userID: str):
        pass

    @abstractmethod
    def handle_check_debt_with_friend(self, userID: str):
        pass