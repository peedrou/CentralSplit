from dotenv import load_dotenv
from typing import List

from app.assets.groups.group import Group
from app.assets.friends.friend import Friend

load_dotenv()

class Instantiation():

    @staticmethod
    def instantiate_group(userIDS: List[str], groupName: str):
        instantiatedGroup = Group(groupName=groupName, members=userIDS)
        return instantiatedGroup
    
    @staticmethod
    def instantiate_friend(friendEmail: str, userEmail: str, userUsername: str, friendUsername: str):
        instantiatedFriend = Friend(friendEmail=friendEmail, userEmail=userEmail, userUsername=userUsername, friendUsername=friendUsername, totalToPay= 0, totalToReceive= 0)
        return instantiatedFriend