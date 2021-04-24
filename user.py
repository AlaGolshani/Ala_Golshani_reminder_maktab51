from hashlib import sha256
import csv

class User:
    users = []   # List of all users object

    def __init__(self, username, password = None):
        """
            :param username: user name
            :param __hpassword: user hashed password
        """

        self.username = username
        self.__hpassword = sha256(str(password).encode('utf-8')).hexdigest()
        self.tasks = []

    @classmethod
    def register(cls):
        """
            This method takes the new user information and registers her/him
            :return: the new user object
        """
        
        username = input("Please enter a username: ")

        while True:
            password = input("Please enter a password: ")
            repeated_pass = input("Please enter the password again: ")
            if password == repeated_pass:
                break
            else:
                print('passwords are not the same.')

        __Hashed_password = sha256(str(password).encode('utf-8')).hexdigest()

        user = User(username, password)

        User.users.append(user)

    @classmethod
    def login(cls):
        """
        This method takes the user information for login
        if she/he enters a wrong input more than three times,
        the account will be suspended for one day
        :return: a Boolean that indicates whether the login was successful or not
        """
        counter = 0
        while counter < 3:
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
                    return True
            counter += 1
        
        print('Your account has been blocked for one day.')
        # block(username)
        return False 

    @classmethod
    def is_registered(cls, username):
        for user in User.users:
            if user.username == username and user.__hpassword:
                return True
        return False

    @classmethod
    def fwrite(cls, file_name = 'register.csv'):
        with open(file_name, 'w', newline='', encoding='utf-8') as csvfile:
            rows = [{'username' : user.username, 
                        'password' : user.__hpassword}
                        for user in User.users]

            fields = ['username', 'password']

            csv_writer = csv.DictWriter(csvfile, fieldnames=fields)
            csv_writer.writeheader()
            csv_writer.writerows(rows)

    @classmethod
    def fread(cls, file_name = 'register.csv'):
        with open(file_name) as csvfile:
            lines = csvfile.readlines()

            rows = [row.strip().split(',') for row in lines]

            for uname, pswrd in rows[1:]:
                new_user = User(uname, None)
                new_user.__hpassword = pswrd
                User.users.append(new_user)
