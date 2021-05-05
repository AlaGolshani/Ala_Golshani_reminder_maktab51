"""
    This program helps you to schedule your tasks,
    and reminds you to do it

    released on 4/23/2021

    author: Ala Golshani
"""

from menu import menu, sign_in
from user import User


if __name__ == '__main__':
    User.reg_read()
    user = sign_in()
    if user is False:
        exit()
    menu(user)
    User.reg_write()
