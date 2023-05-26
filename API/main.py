from fastapi import FastAPI, Query
from app.assets.users.user import User
from app.data.db_methods import DataBaseMethods as DBM
from pydantic import BaseModel
from typing import List

app = FastAPI()

class UserInfo(BaseModel):
    email: str
    username: str
    UID: str
    groups: list[str]
    friends: list[str]
    usersToPay: dict[str, float]
    usersToReceive: dict[str, float]
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

@app.post("/create-group")
def create_group(
    username: str = Query(..., description="The username of the user"),
    groupName: str = Query(..., description="The name of the group"),
    members: List[str] = Query(None, description="A list of member usernames")
):
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
    user.create_group(userIDS=members, groupName=groupName)

    return f"Group {groupName} was created sucessfully"

@app.post("/delete-group")
def delete_group(
    username: str = Query(..., description="The username of the user"),
    groupName: str = Query(..., description="The name of the group"),
    members: None = Query(None, description="A list of member usernames")
):
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
    result = user.delete_group(userIDS=members, groupName=groupName)
    if result == True:
        return f"Group {groupName} was deleted sucessfully"
    else:
        return f"Group {groupName} was not deleted due to an error"

    