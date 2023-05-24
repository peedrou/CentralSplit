from fastapi import FastAPI
from app.assets.users.user import User
from app.data.db_methods import DataBaseMethods as DBM
from pydantic import BaseModel

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

class Username(BaseModel):
    username: str


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