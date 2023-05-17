from dotenv import load_dotenv
from typing import List, Optional

from app.assets.groups.group import Group
from app.assets.friends.friend import Friend
from app.assets.expenses.createExpense import CreateExpense
from app.assets.expenses.createExpense import SplitMethod

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
    
    @staticmethod
    def instantiate_create_expense(
            amount: float,
            payer: str,
            receivers: List[str] | str,
            customAmounts: List[float] | None,
            group: str | None,
            splitMethod: SplitMethod
        ):
        instantiatedNewExpense = CreateExpense(
            amount=amount,
            payer=payer,
            receivers=receivers,
            customAmounts=customAmounts,
            group=group,
            splitMethod=splitMethod
        )
        return instantiatedNewExpense