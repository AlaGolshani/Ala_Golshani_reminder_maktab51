from user import User
from task import Task
from os import system


def sign_in():
    while True:
        choice = int(input('1) Register\n2) Login\n3) Quit\n>> Please enter a number: '))
        system('cls')
        if choice == 3:  # Quit
            return False

        elif choice == 1:  # Register
            user = User.register()
            if user is False:
                print('Username available, please login.')
                input("\n\nPress Enter to Continue...")
                system('cls')
                continue
            else:
                menu(user)

        elif choice == 2:  # Login
            user = User.login()
            if user is False:
                system('cls')
                continue
            else:
                Task.reminder(user)
                menu(user)

        system('cls')


def menu(user):
    while True:
        system('cls')
        item = int(input('''
            1) Add a task
            2) edit/show/were done/share a task
            3) shared with me
            4) change password
            5) log out

            >> Please select one of the above items: '''))
        system('cls')
        
        if item == 5:   # log out
            break

        elif item == 1:   # Add a task
            Task.add(user)
            
        elif item == 2:   # edit/show/share tasks
            submenu(user)

        elif item == 3:   # shared with me

            for task in user.shared_with_me:
                task.print()
                save = input('Do you wanna save it?   1)Yes  2)No  :')
                if save == 1:
                    user.tasks.append(task)
                else:
                    continue

        elif item == 4:   # change password
            user.change_pass()

        system('cls')


# edit show share a task menu
def submenu(user):
    while True:
        system('cls')
        item = int(input('''
            1) Edit a task
            2) Were done a task
            3) Show all the tasks on the calendar
            4) Show done/undone tasks on this day/week/month
            5) Define a category
            6) Share a task
            7) Back

            >> Please select one of the above items: '''))
        system('cls')

        if item == 7:
            break

        elif item == 1:
            user.show_tasks()
            code = int(input('Please enter the task code which you wanna edit: '))
            user.tasks[code].edit()

        elif item == 2:
            user.show_tasks()
            code = int(input('Please enter the task code which you were done: '))
            user.tasks[code].done = True

        elif item == 4:
            subitem = int(input('''
                1) daily report
                2) weekly report
                3) monthly report
                4) back

                >> Please select one of the above items: '''))
            system('cls')

            if subitem == 4:
                continue
            elif subitem == 1:
                Task.daily_report(user)
            elif subitem == 2:
                Task.weekly_report(user)
            elif subitem == 3:
                Task.monthly_report(user)

        elif item == 5:
            user.show_tasks()
            code = int(input('Please enter the task code which you wanna define a category for that: '))
            user.tasks[code].category = input('enter the category name:')
            input("\nDone.\n\nPress Enter to Continue...")

        elif item == 6:
            code = int(input('Please enter the task code which you wanna share: '))
            uname = input('enter the username who you share with:')
            user.tasks[code].share(uname)
