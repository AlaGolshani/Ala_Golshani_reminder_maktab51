"""
    This program helps you to schedule your tasks,
    and reminds you to do that

    released on 4/23/2021

    author: Ala Golshani
"""

from user import User
from task import Task
from menu import menu, sign_in

if __name__ == '__main__':
    # user1 = User('ala_gol', 123)
    # user2 = User('ilia_gol', 1234)

    # user1.register()
    # user2.register()

    # print(user1.is_registered())
    # print(user2.is_registered())

    # User.fwrite()
    
    User.fread()
    # print(User.login('ala_gol', 123))
    
    # for user in User.users:
    #     print(user.username)

    sign_in()
    menu()

    