from user import User
import datetime
import threading
from plyer import notification


class Task:
    def __init__(self, description=None, date=None, time=None,
                 importance=None, urgency=None, link=None, location=None):
        """
        :param description: Description of the task
        :param date, time: date and time of the task
        :param importance: A boolean that indicates the task is important or not
        :param urgency: A boolean that indicates the task is urgent or not
        :param link: link of the task
        :param location: location of the task

            Prioritizing tasks by urgency and importance
            results 4 categories with different warnings
            (Based on the Eisenhower matrix)
                • Immediate and important tasks have repeated warnings every 5 minutes.
                • Display urgent and unimportant tasks only at the specified time
                • Display urgent and important tasks at the end of each day.
                • Display urgent and unimportant tasks at the end of the week (Friday)
        """

        self.description = description
        self.dt = datetime.datetime(date[2], date[0], date[1], time[0], time[1], time[2])
        self.link = link
        self.location = location
        self.importance = importance
        self.urgency = urgency
        self.done = False
        self.category = ''
        self.activation = True

    @classmethod
    def add(cls, user):
        """
        Adds a new task and append it to the user tasks list
        :return: new task object
        """

        print('\33[35m\n\t\tEnter the information about the task: \33[m')

        description = input('\33[35m\t\tTitle or description: \33[m')

        time = date = None
        task = None
        while time is None or date is None:
            date = input('\33[35m\t\tDate (in this format month/day/year): \33[m').split('/')
            time = input('\33[35m\t\tTime (in this format hour:minute:second): \33[m').split(':')
            try:
                date = [int(x) for x in date]  # date = [month, day, year]
                time = [int(x) for x in time]   # time = [hour, minute, second]
                task = Task(description, date, time)
                # assert time and date match with the regex...
            except ValueError as e:
                print('Error: ', e)
                time = date = None
            except TypeError as e:
                print('Error: ', e)
                time = date = None
            # except AssertionError: ...

        important = input('\33[35m\t\tIs it important? 1)yes 2)no  : \33[m')
        task.importance = True if important == '1' else False
        urgent = input('\33[35m\t\tIs it urgent? 1)yes 2)no  : \33[m')
        task.urgency = True if urgent == '1' else False

        task.link = input('\33[35m\t\tLink: \33[m')
        task.location = input('\33[35m\t\tLocation: \33[m')

        user.tasks.append(task)
        input("\n\t\tDone.\n\t\tPress Enter to Continue...")
        return task

    def edit(self, atr, value):
        """
        Edits task attributes (postpones or so on)
        :return: Returns the modified task
        """
        self.__dict__[atr] = value
        return self

    @staticmethod
    def daily_report(user):
        """
        this method Reports task done and task left in the day
        """
        flag = 0
        print('\33[35m\t\tyour undone tasks in this day: \33[m')
        for task in user.tasks:
            if task.dt.date() == datetime.datetime.today().date() \
                    and task.done is False and task.activation is True:
                print(task)
                flag = 1
        if flag == 0:
            print('\33[35m\t\tThere is no task.\33[m')

        flag = 0
        print('\33[35m\t\tyour done tasks in this day: \33[m')
        for task in user.tasks:
            if task.dt.date() == datetime.datetime.today().date() \
                    and task.done is True and task.activation is True:
                print(task)
                flag = 1
        if flag == 0:
            print('\33[35m\t\tThere is no task.\33[m')

    @staticmethod
    def weekly_report(user):
        """
        this method Reports task done and task left in the week

        """
        flag = 0
        print('\33[35m\t\tyour undone tasks in this week: \33[m')
        now = datetime.datetime.now()
        for task in user.tasks:
            if task.dt.strftime("%V") == now.strftime("%V") \
                    and task.done is False and task.activation is True:
                print(task)
                flag = 1
        if flag == 0:
            print('\33[35m\t\tThere is no task.\33[m')

        flag = 0
        print('\33[35m\t\tyour done tasks in this week:\33[m')
        for task in user.tasks:
            if task.dt.strftime("%V") == now.strftime("%V")\
                    and task.done is True and task.activation is True:
                print(task)
                flag = 1
        if flag == 0:
            print('\33[35m\t\tThere is no task.\33[m')

    @staticmethod
    def monthly_report(user):
        """
        this method Reports task done and task left in the month
        """
        flag = 0
        now = datetime.datetime.now()
        print('\33[35m\t\tyour undone tasks in this month: \33[m')
        for task in user.tasks:
            if task.dt.month == now.month\
                    and task.done is False and task.activation is True:
                print(task)
                flag = 1
        if flag == 0:
            print('\33[35m\t\tThere is no task.\33[m')

        flag = 0
        print('\33[35m\t\tyour done tasks in this month: \33[m')
        for task in user.tasks:
            if task.dt.month == now.month \
                    and task.done is True and task.activation is True:
                print(task)
                flag = 1
        if flag == 0:
            print('\33[35m\t\tThere is no task.\33[m')

    def share(self, usernames):
        """
        this method shares a task to some other users
        """
        for usr in User.user_list:
            if usr.username in usernames:
                usr.shared_with_me.append(self)
                usernames.remove(usr.username)

        if not usernames:
            for uname in usernames:
                print(f'\33[35m\t\t{uname} does not exist.\33[m')

    @staticmethod
    def reminder(user):
        now = datetime.datetime.now()
        for index, task in enumerate(user.tasks):
            if task.importance is True and task.urgency is True and task.done is False:
                task.task_alarm(now, index)
            elif task.importance is False and task.urgency is True and task.done is False:
                if task.dt == now:
                    task.notification()
            elif task.importance is True and task.urgency is False and task.done is False:
                if now.time() == datetime.time(23, 59, 59):
                    task.notification()
            elif task.importance is False and task.urgency is False and task.done is False:
                if datetime.date.today().strftime('%A') == 'Friday':
                    task.notification()

    def task_alarm(self, now, index):
        """
        this method sets a timer for every 5 minutes for the important and urgent task
        :param now:
        :param index: index of the task
        """
        if now < self.dt:
            total_seconds = (now - self.dt).total_seconds()
            threading.Timer(total_seconds, self.task_alarm).start()
        else:
            self.task_notification(index)
            threading.Timer(60 * 5, self.task_alarm).start()  # called every 5 minute

    def task_notification(self, index):
        """
        sends a desktop notification for the task
        :param index: index of the task
        """
        notification.notify(
            title=f'TASK {index} ALARM',
            message=self.description,

            # displaying time
            timeout=4)

    def __str__(self):
        return '\n'.join(f'\33[32m{key} : {val}\33[m'.center(100)
                         for key, val in self.__dict__.items()) + \
                         f'\n\33[97m{"-" * 100}\33[m'
