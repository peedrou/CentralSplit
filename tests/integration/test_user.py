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
    
    def _make_random_username(self) -> str:
        my_string = "abcdefghijklmnopqrstuvwxyz"
        username = ''.join(random.choices(my_string, k=10))
        return username
    
    def _make_random_group_name(self) -> str:
        my_string = "abcdefghijklmnopqrstuvwxyz"
        random_string = ''.join(random.choices(my_string, k=10))
        groupName = "Group" + " " + random_string
        return groupName
    
    def _make_two_users_and_register(self):
        user1 = User(
            email=self._make_random_email(),
            username=self._make_random_username(),
            UID="",
            groups=[],
            friends=[],
            usersToPay={},
            usersToReceive={},
            totalToPay=0,
            totalToReceive=0
        )

        user2 = User(
            email=self._make_random_email(),
            username=self._make_random_username(),
            UID="",
            groups=[],
            friends=[],
            usersToPay={},
            usersToReceive={},
            totalToPay=0,
            totalToReceive=0
        )

        user1.register_user()
        user2.register_user()
        return user1,user2
    
    def _make_three_users_and_register(self):
        user1, user2 = self._make_two_users_and_register()

        user3 = User(
            email=self._make_random_email(),
            username=self._make_random_username(),
            UID="",
            groups=[],
            friends=[],
            usersToPay={},
            usersToReceive={},
            totalToPay=0,
            totalToReceive=0
        )

        user3.register_user()
        return user1,user2,user3

    def test_register_user(self):
        user = User(
            email=self._make_random_email(),
            username=self._make_random_username(),
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
            "username":f"{user.username}",
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
            username=self._make_random_username(),
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
            username=self._make_random_username(),
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
            'groupName': groupName,
            'totalExpenses': 0
        }

        assert response == group_info

    def test_group_exists(self):
        user = User(
            email='test@gmail.com',
            username=self._make_random_username(),
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
            username=self._make_random_username(),
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
            username=self._make_random_username(),
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
            username=self._make_random_username(),
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

    def test_add_friend(self):
        user1, user2 = self._make_two_users_and_register()

        response = user1.add_friend(user2.email, user2.username)

        assert response == True

    def test_remove_friend(self):
        user1, user2 = self._make_two_users_and_register()
        user1.add_friend(user2.email, user2.username)

        response = user1.remove_friend(user2.email, user2.username)

        assert response == True

    def test_check_debt_with_friend(self):
        user1, user2 = self._make_two_users_and_register()
        user1.add_friend(user2.email, user2.username)

        money_owed_message, money_to_receive_message = user1.check_debt_with_friend(user2.email, user2.username)

        assert money_owed_message == f'You must pay 0'
        assert money_to_receive_message == f'You must receive 0'

    def test_create_single_split_expense(self):
        user1, user2 = self._make_two_users_and_register()

        result = user1.create_expense(
            receivers=user2.username,
            amount=100,
            group=None,
            custom_amounts=None,
            split_method="single"
        )

        assert result == True
    
    def test_create_equal_split_expense(self):
        user1, user2, user3 = self._make_three_users_and_register()

        result = user1.create_expense(
            receivers=[user2.username, user3.username],
            amount=100,
            group=None,
            custom_amounts=[50,50],
            split_method="equal"
        )

        assert result == True


    def test_check_balance(self):
        user1, user2 = self._make_two_users_and_register()

        user1.create_expense(
            receivers=[user2.username],
            amount=100,
            group=None,
            custom_amounts=None,
            split_method="single"
        )

        balance = user1.check_total_balance()

        assert balance == -100

    def test_remove_expense_partial_one_receiver(self):
        user1, user2 = self._make_two_users_and_register()

        user1.create_expense(
            receivers=[user2.username],
            amount=100,
            group=None,
            custom_amounts=None,
            split_method="single"
        )

        result = user1.pay_user(
            amount_for_each=75,
            receivers=user2.username,
            group=None
        )

        assert result == True

    def test_remove_expense_partial_multiple_receivers(self):
        user1, user2, user3 = self._make_three_users_and_register()

        user1.create_expense(
            receivers=[user2.username, user3.username],
            amount=100,
            group=None,
            custom_amounts=None,
            split_method="equal"
        )

        result = user1.pay_user(
            amount_for_each=30,
            receivers=[user2.username, user3.username],
            group=None
        )

        assert result == True

    def test_remove_expense_total_one_receiver(self):
        user1, user2 = self._make_two_users_and_register()

        user1.create_expense(
            receivers=[user2.username],
            amount=100,
            group=None,
            custom_amounts=None,
            split_method="single"
        )

        balance = user1.check_total_balance()

        assert balance == -100

    def test_remove_expense_total_multiple_receivers(self):
        user1, user2 = self._make_two_users_and_register()

        user1.create_expense(
            receivers=[user2.username],
            amount=100,
            group=None,
            custom_amounts=None,
            split_method="single"
        )

        balance = user1.check_total_balance()

        assert balance == -100

    
  