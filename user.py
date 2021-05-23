from hashlib import sha256
from datetime import datetime, timedelta
from fileModule import write_to_file


class User:
    user_list = []  # List of all users object

    def __init__(self, username, password=None):
        self.username = username
        self.password = password
        self.tasks = []
        self.shared_with_me = []  # list of tasks that shared with the user
        self.block = False  # block datetime, if user was blocked
        self.deleted_tasks = []

    @classmethod
    def register(cls):
        """
            This method takes the new user information and registers her/him
            :return: the new user object
        """
        username = input("\33[35m\t\tPlease enter your username, 0 >> back: \33[m")
        if username == '0':
            return 'back'
        try:
            if User.user_list:
                assert username not in [user.username for user in User.user_list]
        except AssertionError:
            return False

        while True:
            password = input('\33[35m\t\tPlease enter a password: \33[m')
            repeated_pass = input('\33[35m\t\tPlease enter the password again: \33[m')
            if password == repeated_pass:
                break
            else:
                print('\33[35m\t\tpasswords are not the same.\33[m')

        hashed_password = sha256(password.encode('utf-8')).hexdigest()

        user = User(username, hashed_password)

        User.user_list.append(user)
        write_to_file(User.user_list)
        return user

    @classmethod
    def login(cls, logger):
        """
        This method takes the user information for login
        if she/he enters a wrong input more than three times,
        the account will be suspended for one day
        :return: a boolean or string that indicates whether the login was successful or not
        """
        counter = 1
        while counter <= 3:
            username = None
            while username is None:
                username = input("\33[35m\t\tPlease enter your username, 0 >> back: \33[m")
                if username == '0':
                    return 'back'
                try:
                    assert User.user_list and username in [user.username for user in User.user_list]
                except AssertionError:
                    print('\33[35m\n\t\tThe username is invalid.')
                    username = None

            password = input("\33[35m\t\tPlease enter your password: \33[m")
            hash_pass = sha256(str(password).encode('utf-8')).hexdigest()
            user = None
            for user in User.user_list:
                if user.username == username and user.password == hash_pass:
                    if user.block is False:
                        return user
                    elif user.block + timedelta(days=1) < datetime.now():
                        user.block = False
                        return user
                    else:
                        total_seconds = (datetime.now() - user.block).total_seconds()
                        hours = int(24 - total_seconds / (60 * 60))
                        minutes = int(60 - (total_seconds % (60 * 60)) / 60)
                        print(f'\33[35m\n\t\tYour account is block for '
                              f'{hours} hours and {minutes} minutes.\33[m')
                        input("\n\t\tPress Enter to Continue...")
                        return False

            print('\33[35m\n\t\tWrong password.')
            logger.warning(f'{username} entered a wrong password')
            if counter == 3:
                print('\33[35m\n\t\tYour account has been blocked for one day.\33[m')
                logger.warning(f'{username} has been blocked for one day')
                user.block = datetime.now()
                write_to_file(User.user_list)
                input("\n\t\tPress Enter to Continue...")
            counter += 1

    def change_password(self):
        """
        This method is for changing the user password
        """
        while True:
            last_pass = input('\33[35m\t\tEnter current password:\33[m')
            hash_password = sha256(last_pass.encode('utf-8')).hexdigest()

            if hash_password == self.password:
                break
            print('\33[35m\t\tinvalid password. try again.\33[m')

        while True:
            new_pass = input("\33[35m\t\tPlease enter new password: \33[m")
            repeated_pass = input("\33[35m\t\tPlease enter the password again: \33[m")
            if new_pass == repeated_pass:
                break
            else:
                print('\33[35m\t\tpasswords are not the same.\33[m')

        hash_password = sha256(new_pass.encode('utf-8')).hexdigest()
        self.password = hash_password

        input("\n\t\tDone.\n\t\tPress Enter to Continue...")

    def show_tasks(self):
        """
        shows all of the user tasks
        """
        if not self.tasks:   # self.tasks = []
            print('\33[35m\t\tNo task defined yet...\33[m')
            return False

        for index, task in enumerate(self.tasks, 1):
            if task.activation is True:
                print(f'\33[93m task {index}\33[m =>'.center(100))
                print(task)
        return True
