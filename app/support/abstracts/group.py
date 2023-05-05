from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List

@dataclass
class AbstractGroup(ABC):
    groupName: str
    members: List[str]

    @abstractmethod
    def handle_create_group(self):
        pass

    @abstractmethod
    def handle_add_users_to_group(self):
        pass

    @abstractmethod
    def handle_remove_users_from_group(self):
        pass

    @abstractmethod
    def handle_delete_group(self):
        pass