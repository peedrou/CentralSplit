from dotenv import load_dotenv
from typing import List

from app.assets.groups.group import Group

load_dotenv()

class Instantiation():

    @staticmethod
    def instantiate_group(userIDS: List[str], groupName: str):
        instantiatedGroup = Group(groupName=groupName, members=userIDS)
        return instantiatedGroup