import argparse
from pyfiglet import Figlet
from dataclasses import dataclass
from typing import List, Dict, Any
from assets.users.user import User, SplitMethod

@dataclass
class UserInterface:
    email: str
    username: str
    UID: str
    groups: List[str]
    friends: List[str]
    usersToPay: Dict[str, float]
    usersToReceive: Dict[str, float]
    totalToPay: float
    totalToReceive: float

    def __init__(self):
        self.user = User(
            email=self.email,
            username=self.username,
            UID=self.UID,
            groups=self.groups,
            friends=self.friends,
            usersToPay=self.usersToPay,
            usersToReceive=self.usersToReceive,
            totalToPay=self.totalToPay,
            totalToReceive=self.totalToReceive
        )

    def register_user(self) -> Dict[str, Any]:
        return self.user.register_user()

    def create_group(self, userIDS: List[str], groupName: str) -> Dict[str, Any]:
        return self.user.create_group(userIDS, groupName)

    def delete_group(self, userIDS: None, groupName: str) -> bool:
        return self.user.delete_group(userIDS, groupName)

    def add_users_to_group(self, userIDS: None, usersToAdd: List[str], groupName: str) -> list:
        return self.user.add_users_to_group(userIDS, usersToAdd, groupName)

    def remove_users_from_group(self, userIDS: None, usersToRemove: List[str], groupName: str) -> list:
        return self.user.remove_users_from_group(userIDS, usersToRemove, groupName)

    def add_friend(self, friendEmail: str, friendUsername: str) -> bool:
        return self.user.add_friend(friendEmail, friendUsername)

    def remove_friend(self, friendEmail: str, friendUsername: str) -> bool:
        return self.user.remove_friend(friendEmail, friendUsername)

    def check_debt_with_friend(self, friendEmail: str, friendUsername: str) -> str:
        return self.user.check_debt_with_friend(friendEmail, friendUsername)

    def create_expense(
            self,
            receivers: List[str] | str,
            amount: float,
            group: str | None,
            split_method: SplitMethod,
            custom_amounts: List[float] | None
        ) -> bool:
        return self.user.create_expense(receivers, amount, group, split_method, custom_amounts)

    def check_total_balance(self) -> float | int:
        return self.user.check_total_balance()

    def pay_user(
            self,
            amount_for_each: float,
            receivers: List[str] | str,
            group: str | None
        ) -> bool:
        return self.user.pay_user(amount_for_each, receivers, group)


def process_command_line_arguments():
    parser = argparse.ArgumentParser(description='Your Application Name')

    # Add command-line arguments here
    parser.add_argument('-e', '--email', type=str, help='User email')
    parser.add_argument('-u', '--username', type=str, help='Username')
    # Add more arguments as needed

    return parser.parse_args()

def print_app_name():
    custom_font = Figlet(font='slant')
    app_name = 'CentralSplit'
    ascii_art = custom_font.renderText(app_name)
    print(ascii_art)

def main():
    print_app_name()
    args = process_command_line_arguments()

    # Get user input for email and username from the command line
    if not args.email:
        email = input("Enter your email: ")
    if not args.username:
        username = input("Enter your username: ")

    user_interface = UserInterface(
        email=email,
        username=username,
        UID='',
        groups=[],
        friends=[],
        usersToPay={},
        usersToReceive={},
        totalToPay=0.0,
        totalToReceive=0.0
    )

    # Register the user
    registered_user = user_interface.register_user()
    print('Registered User:', registered_user)

    # Call other functions as needed using user_interface object
    # user_interface.create_group(...)
    # user_interface.delete_group(...)
    # user_interface.add_users_to_group(...)
    # user_interface.remove_users_from_group(...)
    # user_interface.add_friend(...)
    # user_interface.remove_friend(...)
    # user_interface.check_debt_with_friend(...)
    # user_interface.create_expense(...)
    # user_interface.check_total_balance(...)
    # user_interface.pay_user(...)


if __name__ == '__main__':
    main()

