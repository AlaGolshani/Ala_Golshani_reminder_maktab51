from hashlib import sha256
from datetime import datetime, timedelta
import csv


class User:
    users = []  # List of all users object

    def __init__(self, username, password=None):
        """
        :param username:
        :param password:
        """
        self.id = None
        self.username = username
        self.__hpassword = sha256(str(password).encode('utf-8')).hexdigest()
        self.tasks = []
        self.categories = []  # User-defined categories name
        self.shared_with_me = []  # List of task that shared with me
        self.block = False  # block datetime, if user is blocked

    @classmethod
    def register(cls):
        """
            This method takes the new user information and registers her/him
            :return: the new user object
        """

        username = input("Please enter a username: ")
        if User.is_registered(username):
            return False

        while True:
            password = input("Please enter a password: ")
            repeated_pass = input("Please enter the password again: ")
            if password == repeated_pass:
                break
            else:
                print('passwords are not the same.')

        __Hashed_password = sha256(password.encode('utf-8')).hexdigest()

        user = User(username, __Hashed_password)

        User.users.append(user)
        return user

    @classmethod
    def login(cls):
        """
        This method takes the user information for login
        if she/he enters a wrong input more than three times,
        the account will be suspended for one day
        :return: a Boolean that indicates whether the login was successful or not
        """
        counter = 1
        while True:

            while True:
                username = input("Please enter your username: ")
                if User.is_registered(username):
                    break
                else:
                    print('The username is invalid.')

            password = input("Please enter your password: ")
            hash_pass = sha256(str(password).encode('utf-8')).hexdigest()

            for user in User.users:
                if user.username == username and user.__hpassword == hash_pass:
                    if user.block is False or \
                            user.action + timedelta(days=1) > datetime.now():
                        user.block = False
                        return user
                    else:
                        print(f'Your account is blocked for {user.block.hour} hours.')
                        return False
                else:
                    print('Wrong password.')
                    if counter == 3:
                        print('Your account has been blocked for one day.')
                        user.block = datetime.now()
            counter += 1

    @classmethod
    def is_registered(cls, username):
        for user in User.users:
            if user.username == username and user.__hpassword:
                return True
        return False

    @classmethod
    def reg_write(cls, file_name='register.csv'):
        with open(file_name, 'w', newline='', encoding='utf-8') as csvfile:
            rows = [{'username': user.username,
                     'password': user.__hpassword}
                    for user in User.users]

            fields = ['username', 'password']

            csv_writer = csv.DictWriter(csvfile, fieldnames=fields)
            csv_writer.writeheader()
            csv_writer.writerows(rows)

    @classmethod
    def reg_read(cls):
        with open('register.csv') as csvfile:
            lines = csvfile.readlines()

            rows = [row.strip().split(',') for row in lines]

            for uname, pswrd in rows[1:]:
                new_user = User(uname, None)
                new_user.__hpassword = pswrd
                User.users.append(new_user)

    def change_pass(self):
        while True:
            last_pass = input('enter current password:')
            hash_password = sha256(last_pass.encode('utf-8')).hexdigest()

            if hash_password == self.__hpassword:
                break
            print('invalid password. try again.')

        while True:
            new_pass = input("Please enter new password: ")
            repeated_pass = input("Please enter the password again: ")
            if new_pass == repeated_pass:
                break
            else:
                print('passwords are not the same.')

        hash_password = sha256(new_pass.encode('utf-8')).hexdigest()
        self.__hpassword = hash_password

        input("\nDone.\n\nPress Enter to Continue...")

    def show_tasks(self):
        for index in range(len(self.tasks)):
            print(f'task {index} :\n', self.tasks[index].print())
