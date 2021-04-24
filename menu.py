from user import User
from task import Task

def sign_in():

    choice = int(input('1) Register\t2) Login\n>> Please enter a number: '))

    if choice == 1:
        User.register()
        User.fwrite()

    elif choice == 2:
        User.login()
    

def menu():
    while True:
        item = int(input('''
         1) Add a task
         2) Edit a task
         3) Delete a task
         4) Postpone a task
         5) some tasks were done
         6) Define a categorize
         7) Show the schedule in calendar
         8) Show done/undone tasks on this day/week/month
         9) share a task
        10) Quit
        >> Please select one of the above items: '''))

        if item == 1:
            description = input('Please enter the description:')
            importance = input('is it importance? 1)Yes  2)No  :')
            importance = True if importance == 1 else False

            urgency = input('is it urgency: 1)Yes  2)No  :')
            urgency = True if urgency == 1 else False

            link = input('Enter a link for the task, If you want :')

            location = input('Enter a location for the task, If you want :')

            Task.add(description, importance, urgency, link, location)

        elif item == 2:
            Task.edit()

        elif item == 3:
            Task.delete()
            
        elif item == 4:
            Task.Postpone()
        
        elif item == 5:
            Task.show()
            dones = input('Enter the tasks number which are done(separated by comma)').split(',')
            for i, task in enumerate(Task.tasks):
                if i in dones:
                    task.done = True

        elif item == 6:
            Task.group()

        elif item == 7:
            Task.schedule()

        elif item == 8:
            Task.report()

        elif item == 9:
            Task.share()

        elif item == 10:
            break
    