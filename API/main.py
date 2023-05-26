from fastapi import FastAPI, Query, Body
from app.assets.users.user import User
from app.assets.users.user import SplitMethod
from app.data.db_methods import DataBaseMethods as DBM
from pydantic import BaseModel
from typing import List, Optional, Dict

app = FastAPI()

class UserInfo(BaseModel):
    email: str
    username: str
    UID: str
    groups: List[str]
    friends: List[str]
    usersToPay: List[str] | str
    usersToReceive: Dict[str, str] | str
    totalToPay: float
    totalToReceive: float


@app.post("/user-info")
def _return_user_info_from_username(username: str) -> UserInfo:
    db = DBM.get_db()
    user_doc = DBM.check_if_property_exists_in_collection_and_return_doc(db, "Users", "username", username)[0]

    email = DBM.check_if_property_exists_in_document_with_doc_ref_and_return_value(user_doc, "email")
    UID = DBM.check_if_property_exists_in_document_with_doc_ref_and_return_value(user_doc, "UID")
    friends = totalToPay = DBM.check_if_property_exists_in_document_with_doc_ref_and_return_value(user_doc, "friends")
    groups = DBM.check_if_property_exists_in_document_with_doc_ref_and_return_value(user_doc, "groups")
    totalToPay = DBM.check_if_property_exists_in_document_with_doc_ref_and_return_value(user_doc, "totalToPay")
    totalToReceive = DBM.check_if_property_exists_in_document_with_doc_ref_and_return_value(user_doc, "totalToReceive")
    usersToPay = DBM.check_if_property_exists_in_document_with_doc_ref_and_return_value(user_doc, "usersToPay")
    usersToReceive = DBM.check_if_property_exists_in_document_with_doc_ref_and_return_value(user_doc, "usersToReceive")

    user_info = UserInfo(
        email=email,
        username=username,
        UID=UID,
        friends=friends,
        groups=groups,
        totalToPay=totalToPay,
        totalToReceive=totalToReceive,
        usersToPay=usersToPay,
        usersToReceive=usersToReceive
    )

    return user_info

def get_user(username):
    user_info = _return_user_info_from_username(username)
    user = User(
        email=user_info.email,
        username=user_info.username,
        UID=user_info.UID,
        groups=user_info.groups,
        friends=user_info.friends,
        usersToPay=user_info.usersToPay,
        usersToReceive=user_info.usersToReceive,
        totalToPay=user_info.totalToPay,
        totalToReceive=user_info.totalToReceive
    )
    
    return user

@app.post("/create-group")
def create_group(
    username: str = Query(..., description="The username of the user"),
    groupName: str = Query(..., description="The name of the group"),
    members: List[str] = Query(None, description="A list of member usernames")
):
    user = get_user(username)
    user.create_group(userIDS=members, groupName=groupName)

    return f"Group {groupName} was created sucessfully"


@app.post("/delete-group")
def delete_group(
    username: str = Query(..., description="The username of the user"),
    groupName: str = Query(..., description="The name of the group"),
    members: None = Query(None, description="None")
):
    user = get_user(username)
    result = user.delete_group(userIDS=members, groupName=groupName)
    if result == True:
        return f"Group {groupName} was deleted sucessfully"
    else:
        return f"Group {groupName} was not deleted due to an error"
    

@app.post("/add-users-group")
def add_users_to_group(
    username: str = Query(..., description="The username of the user"),
    groupName: str = Query(..., description="The name of the group"),
    members: None = Query(None, description="None"),
    usersToAdd: List[str] = Query(..., description="A list of member usernames")
):
    user = get_user(username)
    result = user.add_users_to_group(userIDS=members, groupName=groupName, usersToAdd=usersToAdd)
    return f"Users {result} were added to group {groupName}"

@app.post("/remove-users-group")
def add_users_to_group(
    username: str = Query(..., description="The username of the user"),
    groupName: str = Query(..., description="The name of the group"),
    members: None = Query(None, description="None"),
    usersToRemove: List[str] = Query(..., description="A list of member usernames")
):
    user = get_user(username)
    result = user.remove_users_from_group(userIDS=members, groupName=groupName, usersToRemove=usersToRemove)
    return f"Users {result} were removed from group {groupName}"

@app.post("/add-friend")
def add_friend(
    username: str = Query(..., description="The username of the user"),
    friendEmail: str = Query(..., description="Email of the Friend"),
    friendUsername: str = Query(..., description="Username of the Friend"),
):
    user = get_user(username)
    user.add_friend(friendEmail=friendEmail, friendUsername=friendUsername)
    return f"User {friendUsername} was added as friend"

@app.post("/remove-friend")
def remove_friend(
    username: str = Query(..., description="The username of the user"),
    friendEmail: str = Query(..., description="Email of the Friend"),
    friendUsername: str = Query(..., description="Username of the Friend"),
):
    user = get_user(username)
    user.remove_friend(friendEmail=friendEmail, friendUsername=friendUsername)
    return f"User {friendUsername} was removed as friend"

@app.post("/check-debt-friend")
def check_debt_with_friend(
    username: str = Query(..., description="The username of the user"),
    friendEmail: str = Query(..., description="Email of the Friend"),
    friendUsername: str = Query(..., description="Username of the Friend"),
):
    user = get_user(username)
    money_owed_message, money_to_receive_message = user.check_debt_with_friend(friendEmail=friendEmail, friendUsername=friendUsername)
    return f"{money_owed_message} / {money_to_receive_message}"

@app.post("/create-expense")
def create_expense(
            username: str = Body(..., description="The payer of the expense"),
            receivers: List[str] | str = Body(..., description="The receivers of the expense"),
            amount: float = Body(..., description="The expense amount"),
            group: Optional[str] = Body(None, description="The group in which the expense was made, if any"),
            split_method: SplitMethod = Body(..., description="The way in which the expense will be divided"),
            custom_amounts: Optional[List[float]] = Body(None, description="The username of the user")
        ):
    user = get_user(username)
    result = user.create_expense(
            amount=amount,
            receivers=receivers,
            group=group,
            custom_amounts=custom_amounts,
            split_method=split_method
        )
    
    if result == True:
        return f"Expense was created"
    else:
        return f"Expense was not created due to an error"

    
@app.post("/check-balance")
def create_group(
    username: str = Query(..., description="The username of the user"),
):
    user = get_user(username)
    balance = user.check_total_balance()

    return f"Your balance is {balance}$"

@app.post("/pay-user")
def pay_user(
    username: str = Body(..., description="The username of the user"),
    amount_for_each: float = Body(..., description="The amount to pay the user"),
    receivers: List[str] | str = Body(..., description="The username/s of the receiver/s"),
    group: Optional[str] = Body(None, description="The group in which the expense was made, if any")
):
    user = get_user(username)
    result = user.pay_user(
        amount_for_each=amount_for_each,
        receivers=receivers,
        group=group
    )

    if result == True:
        return f"Expense was paid"
    else:
        return f"Expense was not paid due to an error"