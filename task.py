from datetime import datetime


class Task:
    tasks = []   # List of all tasks

    # List of categorized tasks dictionary
    # key of dictionaries is the title of that category
    categories = []

    def __init__(self, description, importance, urgency, link=None, location=None):
        """
        :param description: Description of this task
        :param link: link of this task
        :param location: location of this task
        :param importance: importance of this task
        :param urgency: urgency of this task

            Prioritizing tasks by urgency and importance
            results 4 categories with different warnings
            (Based on the Eisenhower matrix)
                • Immediate and important tasks have repeated warnings every 5 minutes.
                • Display urgent and unimportant tasks only at the specified time
                • Display urgent and important tasks at the end of each day.
                • Display urgent and unimportant tasks at the end of the week (Friday)
        """

        self.description = description
        self.link = link
        self.location = location
        self.importance = importance
        self.urgency = urgency
        self.done = False
        self.current_time = datetime.now()
        self.accept = False

    def postpone(self, date, time):
        return """
            Postpones the task to another date and time
        """

    def edit(self):
        return """
        Edits task attributes (postpones or so on)
        :return: Returns the modified task
        """

    @classmethod
    def add(cls, description, importance, urgency, link=None, location=None):
        return """
            Add a new task and append it to tasks list
            :return: new task object
        """
        # new_task = Task(description, importance, urgency, link=None, location=None)
        # return new_task

    @classmethod
    def group(cls):
        return """
            Defines categories for tasks
            :return: list of the new category
        """

    @staticmethod
    def report():
        return """
            this function Reports work done and work left in the day, week or month
        """

    @classmethod
    def share(cls, task, username):
        return """
            this function shares task to other users
        """

    @classmethod
    def remove(cls):
        return """
            this function removes several tasks
        """

    @classmethod
    def schedule(cls):
        """
            this function shows the schedule in calendar
        """