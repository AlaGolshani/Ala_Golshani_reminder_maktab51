import json
from user import User
import datetime
from os import system
# import calendar
# import threading
from bson import json_util


class Task:
    def __init__(self, description=None, date=None, time=None, importance=None, urgency=None, link=None, location=None):
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
        self.category = None

    def edit(self):
        """
        Edits task attributes (postpones or so on)
        :return: Returns the modified task
        """
        print('Enter this information about the task: ')

        self.description = input('Title or description: ')

        date = input('Date (in this format month/day/year):').split('/')
        date = [int(x) for x in date]
        time = input('Time (in this format hour:minute:second):').split(':')
        time = [int(x) for x in time]

        self.dt = datetime.datetime(date[2], date[0], date[1], time[0], time[1], time[2])

        important = input('Is it important?  1)yes  2)no  : ')
        self.importance = True if important == 1 else False
        urgent = input('Is it urgent? 1)yes 2)no  : ')
        self.urgency = True if urgent == 1 else False

        self.link = input('Link: ')
        self.location = input('Location: ')

        input("\nDone.\n\nPress Enter to Continue...")

    @classmethod
    def add(cls, user):
        """
            Add a new task and append it to the user tasks list
            :return: new task object
        """

        print('Enter this information about the task:')

        description = input('Title or description: ')

        date = input('Date (in this format month/day/year):').split('/')
        date = [int(x) for x in date]
        time = input('Time (in this format hour:minute:second):').split(':')
        time = [int(x) for x in time]

        task = Task(description, date, time)

        important = input('Is it important? 1)yes 2)no  : ')
        task.importance = True if important == 1 else False
        urgent = input('Is it urgent? 1)yes 2)no  : ')
        task.urgency = True if urgent == 1 else False

        task.link = input('Link: ')
        task.location = input('Location: ')

        user.tasks.append(task)
        input("\nDone.\n\nPress Enter to Continue...")
        return task

    @staticmethod
    def daily_report(user):
        """
            this function Reports task done and task left in the day
        """
        print('your undone task in this day:')
        for task in user.takes:
            if task.dt.date() == datetime.datetime.today().date() and task.done is False:
                task.print()

        print('your done task in this day:')
        for task in user.takes:
            if task.dt.date() == datetime.datetime.today().date() and task.done is True:
                task.print()

    @staticmethod
    def weekly_report(user):
        """
            this function Reports task done and task left in the week
        """
        print('your undone task in this week:')
        now = datetime.datetime.now()
        for task in user.takes:
            if task.dt.strftime("%V") == now.strftime("%V") and task.done is False:
                task.print()
        print('your done task in this week:')
        for task in user.takes:
            if task.dt.strftime("%V") == now.strftime("%V") and task.done is True:
                task.print()

    @staticmethod
    def monthly_report(user):
        """
            this function Reports task done and task left in the month
        """
        now = datetime.datetime.now()
        print('your undone task in this month:')
        for task in user.takes:
            if task.dt.month == now.month and task.done is False:
                task.print()
        print('your undone task in this month:')
        for task in user.takes:
            if task.dt.month == now.month and task.done is True:
                task.print()

    def share(self, uname):
        """
            this function shares task to other users
        """
        for usr in User.users:
            if usr.username == uname:
                usr.shared_with_me.append(self)
        input("\nDone.\n\nPress Enter to Continue...")

    @classmethod
    def task_write(cls):
        with open('tasks.json', 'w') as file:
            result = {user.username: [task.__dict__ for task in user.takes] for user in User.users}
            # for user in User.users:
            #     for task in user.takes:
            #         result[user.username] = []...
            json.dump(result, file, default=json_util.default)
    
    @classmethod
    def task_read(cls):
        with open('tasks.json') as file:
            result = json.load(file, object_hook=json_util.object_hook)
            for user in User.users: 
                for task in result[user.username]:
                    new_task = Task()
                    new_task.dt = task['datetime']
                    new_task.description = task['description']
                    new_task.done = task['done']
                    new_task.category = task['category']
                    new_task.urgency = task['urgency']
                    new_task.importance = task['importance']
                    new_task.link = task['link']
                    new_task.location = task['location']
                    user.takes.append(new_task)
        return result

    @staticmethod
    def reminder(user):
        now = datetime.datetime.now()
        print("it's the time to do : ")
        for task in user.takes:
            if task.dt == now:
                if task.importance is True and task.urgency is True:
                    # threading.Timer(60.0*5, task.print).start()  # called every 5 minute
                    task.print()
                    task.dt += datetime.timedelta(minutes=5)
                if task.importance is False and task.urgency is True:
                    task.print()
                if task.importance is True and task.urgency is False:
                    task.print()
                    task.dt = task.dt.replace(hour=23, minute=59, second=59)
                if task.importance is True and task.urgency is True:
                    task.print()
                    task.dt = task.dt.replace(day=Task.friday())
        else:
            print('\nnothing to do yet...')

        input("\n\nPress Enter to Continue...")
        system('cls')

    def print(self):
        for key, val in self.__dict__:
            print(key, val)

    @staticmethod
    def friday():
        d = datetime.date.today()
        while d.weekday() != 4:
            d += datetime.timedelta(1)
        return d.day
