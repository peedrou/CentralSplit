import random
import pytest

from dotenv import load_dotenv
from app.assets.users.user import User

load_dotenv()


class TestUser():

    def _make_random_email(self) -> str:
        my_string = "abcdefghijklmnopqrstuvwxyz"
        random_string = ''.join(random.choices(my_string, k=10))
        email = random_string + '@gmail.com'
        return email
    
    def _make_random_group_name(self) -> str:
        my_string = "abcdefghijklmnopqrstuvwxyz"
        random_string = ''.join(random.choices(my_string, k=10))
        groupName = "Group" + " " + random_string
        return groupName

    def test_register_user(self):
        user = User(
            email=self._make_random_email(),
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

    def test_if_user_exists(self):
        user = User(
            email='test@gmail.com',
            UID="",
            groups=[],
            friends=[],
            usersToPay={},
            usersToReceive={},
            totalToPay=0,
            totalToReceive=0
        )

        with pytest.raises(Exception) as e:
            user.register_user()
        assert str(e.value) == "User already exists"

    def test_create_group(self):
        user = User(
            email='test@gmail.com',
            UID="",
            groups=[],
            friends=[],
            usersToPay={},
            usersToReceive={},
            totalToPay=0,
            totalToReceive=0
        )
        members = ['user1','user2','user3']
        groupName = self._make_random_group_name()

        response = user.create_group(userIDS=members, groupName=groupName)

        group_info = {
            'members': members, 
            'groupName': groupName
        }

        assert response == group_info

    def test_group_exists(self):
        user = User(
            email='test@gmail.com',
            UID="",
            groups=[],
            friends=[],
            usersToPay={},
            usersToReceive={},
            totalToPay=0,
            totalToReceive=0
        )
        members = ['user1','user2','user3']
        groupName = "Test Group 2"

        with pytest.raises(Exception) as e:
            user.create_group(userIDS=members, groupName=groupName)
        assert str(e.value) == "Group already exists with that name, please insert a different name"

    def test_delete_group(self):
        user = User(
            email='test@gmail.com',
            UID="",
            groups=[],
            friends=[],
            usersToPay={},
            usersToReceive={},
            totalToPay=0,
            totalToReceive=0
        )

        members = ['user1','user2','user3']
        groupName = self._make_random_group_name()
        user.create_group(userIDS=members, groupName=groupName)
        
        response = user.delete_group(userIDS=None, groupName=groupName)

        assert response == True

    def test_add_users_to_group(self):
        user = User(
            email='test@gmail.com',
            UID="",
            groups=[],
            friends=[],
            usersToPay={},
            usersToReceive={},
            totalToPay=0,
            totalToReceive=0
        )

        members = ['user1','user2','user3']
        groupName = self._make_random_group_name()
        user.create_group(userIDS=members, groupName=groupName)

        response = user.add_users_to_group(None, ['user2', 'user4', 'user5'], groupName)

        assert response == ['user4', 'user5']

    def test_remove_users_from_group(self):
        user = User(
            email='test@gmail.com',
            UID="",
            groups=[],
            friends=[],
            usersToPay={},
            usersToReceive={},
            totalToPay=0,
            totalToReceive=0
        )

        members = ['user1','user2','user3']
        groupName = self._make_random_group_name()
        user.create_group(userIDS=members, groupName=groupName)

        response = user.remove_users_from_group(None, ['user4', 'user2', 'user8'], groupName)

        assert response == ['user2']