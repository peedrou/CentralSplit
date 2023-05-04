from dotenv import load_dotenv
from app.assets.users.user import User
from app.data.db_methods import DataBaseMethods as DBM

load_dotenv()

class TestUser():

    def test_register_user(self):
        user = User(
            email="test@gmail.com",
            UID="",
            groups=[],
            friends=[],
            usersToPay={},
            usersToReceive={},
            totalToPay=0,
            totalToReceive=0
        )

        response = user.register_user()

        user_info = {
            "email":f"{user.email}",
            "UID":f'{response["UID"]}',
            "groups":user.groups,
            "friends":user.friends,
            "usersToPay":user.usersToPay,
            "usersToReceive":user.usersToReceive,
            "totalToPay":user.totalToPay,
            "totalToReceive":user.totalToReceive
        }

        assert response == user_info