"""
    This program helps you to schedule your tasks,
    and reminds you to do it

    released on 4/23/2021

    author: Ala Golshani
"""

from menu import sign_in
from user import User
from fileModule import read_from_file, write_to_file
import logging

if __name__ == '__main__':
    logger = logging.getLogger('logger')
    f_handler = logging.FileHandler(filename='reminder.log')
    f_handler.setLevel(logging.INFO)
    f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                                 datefmt='%m-%d-%y %H:%M:%S')
    f_handler.setFormatter(f_format)
    logger.addHandler(f_handler)

    User.user_list = read_from_file()
    sign_in(logger)
    write_to_file(User.user_list)
