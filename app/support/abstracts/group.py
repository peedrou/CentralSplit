from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Dict

@dataclass
class Group(ABC):
    groupName: str
    members: List[str]

    @abstractmethod
    def handle_create_group(self, members: List[str], groupName: str):
        pass

    @abstractmethod
    def handle_add_users_to_group(self, members: List[str], groupName: str):
        pass

    @abstractmethod
    def handle_remove_users_from_group(self, members: List[str], groupName: str):
        pass

    @abstractmethod
    def handle_delete_group(self, members: List[str], groupName: str):
        pass