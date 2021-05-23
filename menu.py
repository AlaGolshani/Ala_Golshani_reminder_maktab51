from user import User
from task import Task
from fileModule import write_to_file
import datetime


def sign_in(logger):
    continuation = True
    while continuation is True:
        print(f'\33[97m{"-" * 100}\33[m')
        print('''\33[34m
        1. Register
        2. Login
        3. Quit\33[m''')
        choice = None
        while choice is None:
            try:
                choice = int(input('\33[35m\t\t>> Please select one of the items: \33[m'))
                assert choice in range(1, 4)
            except ValueError:
                print('Invalid input. Please try again.')
            except AssertionError:
                print('Enter a number between one and four.')
                choice = None

        if choice == 3:  # Quit
            continuation = False

        elif choice == 1:  # Register
            user = User.register()
            if user == 'back':
                continue
            try:
                assert user
                logger.info(f'{user.username} logged in')
                menu(user, logger)
                write_to_file(User.user_list)
            except AssertionError:
                print()
                print('\33[35m\t\tUsername available, please login.\33[m')
                input("\t\tPress Enter to Continue...")
                continue

        elif choice == 2:  # Login
            user = User.login(logger)
            try:
                assert user and user != 'back'
                print()
                logger.info(f'{user.username} logged in')
                Task.reminder(user)
                menu(user, logger)
            except AssertionError:
                continue


def menu(user, logger):
    continuation = True
    while continuation is True:
        print(f'\33[97m{"-" * 100}\33[m')
        print('''\33[34m
        1.my tasks
        2.change password
        3.log out\33[m''')

        if user.shared_with_me:
            print('\33[34m\t\t4.shared with me\33[m')

        choice = None
        while choice is None:
            try:
                choice = int(input('\33[35m\n\t\t>> Please select one of the above items: \33[m'))
                assert choice in range(1, 5)
            except ValueError:
                print('Invalid input. Please try again.')
            except AssertionError:
                print('Invalid input. Please try again.')
                choice = None

        if choice == 1:  # my tasks
            task_menu(user, logger)

        elif choice == 2:   # change password
            user.change_password()
            write_to_file(User.user_list)

        elif choice == 3:  # log out
            continuation = False

        elif choice == 4:  # shared with me
            if not user.shared_with_me:  # user.shared_with_me = []
                print('\t\tNothing shared with you...')
                input("\t\tPress Enter to Continue...")
            else:
                save = None
                for task in user.shared_with_me:
                    print(task)
                    while save is None:
                        try:
                            save = int(input('\33[35m\t\tDo you wanna save it?   1)Yes  2)No  : \33[m'))
                            assert save in [1, 2]
                        except ValueError:
                            print('Invalid input. Please try again.')
                        except AssertionError:
                            print('Enter 1 or 2.')
                            save = None
                    if save == 1:
                        user.tasks.append(task)
                user.shared_with_me = []
                write_to_file(User.user_list)


def task_menu(user, logger):
    continuation = True
    while continuation is True:
        print(f'\33[97m{"-" * 100}\33[m')
        print('''\33[34m
        1.add a task
        2.show my tasks
        3.edit a task
        4.share a task
        5.back\33[m''')
        choice = None
        while choice is None:
            try:
                choice = int(input('\33[35m\t\t>> Please select one of the above items: \33[m'))
                assert choice in range(1, 6)
            except ValueError:
                print('\33[34m\t\tInvalid input. Please try again.\33[m')
            except AssertionError:
                print('\33[34m\t\tEnter a number between 1 and 5.\33[m')
                choice = None

        if choice == 1:  # add a task
            Task.add(user)
            logger.info('a new task added')
            write_to_file(User.user_list)

        elif choice == 2:  # show my tasks
            print(f'\33[97m{"-" * 100}\33[m')
            print('''\33[34m
        1.show all of the tasks
        2.daily report
        3.weekly report
        4.monthly report
        5.back\33[m''')
            item = None
            while item is None:
                try:
                    item = int(input('\33[35m\t\t>> Please select one of the above items: \33[m'))
                    assert item in range(1, 6)
                except ValueError:
                    print('\33[35m\t\tInvalid input. Please try again.\33[m')
                except AssertionError:
                    print('\33[35m\t\tEnter a number between 1 and 5.\33[m')
                    item = None

            if item == 1:
                user.show_tasks()
            elif item == 2:
                Task.daily_report(user)
            elif item == 3:
                Task.weekly_report(user)
            elif item == 4:
                Task.monthly_report(user)
            elif item == 5:
                continue

        elif choice == 3:  # edit a task
            if not user.tasks:
                print('\33[35m\t\tNo task defined yet...\33[m')
                input("\n\t\tPress Enter to Continue...")
                continue

            user.show_tasks()
            code = None
            while code is None:
                try:
                    code = int(input('\33[35m\t\tPlease enter the task code which you wanna edit: \33[m'))
                    assert code in range(1, len(user.tasks) + 1) and user.tasks[code - 1].activation is True
                except ValueError:
                    print('\33[35m\t\tInvalid input. Please try again.\33[m')
                except AssertionError:
                    print('\33[35m\t\tInvalid number. Please try again.\33[m')
                    code = None

            print('''\33[34m
        1.done              2.postpone
        3.category          4.description
        5.location          6.link
        7.importance        8.urgency
                   9.delete\33[m''')
            item = None
            while item is None:
                try:
                    item = int(input('\33[35m\t\t>> Which item do you wanna edit? \33[m'))
                    assert item in range(1, 10)
                except ValueError:
                    print('\33[35\t\tmInvalid input. Please try again.\33[m')
                except AssertionError:
                    print('\33[35m\t\tEnter a number between 1 and 9.\33[m')
                    item = None
            edit_task(user.tasks[code - 1], user, item, logger)
            write_to_file(User.user_list)

        elif choice == 4:  # share a task
            try:
                assert user.show_tasks()
                code = None
                while code is None:
                    try:
                        code = int(input('\33[35m\t\tPlease enter the task code which you wanna share: \33[m'))
                        assert code in range(1, len(user.tasks) + 1) and user.tasks[code - 1].activation is True
                    except ValueError:
                        print('\33[35m\t\tInvalid input. Please try again.\33[m')
                    except AssertionError:
                        print('\33[35m\t\tInvalid number. Please try again.\33[m')
                        code = None

                usernames = None
                while usernames is None:
                    usernames = input('\33[35m\t\tEnter the usernames of the users you wanna share with.\n\t\t'
                                      ' (separated with comma) : \33[m').split(',')
                    usernames = [username.strip() for username in usernames]
                    for username in usernames:
                        try:
                            assert username in [user.username for user in User.user_list]
                        except AssertionError:
                            print(f'\33[35m\t\t{username} does not exist.\33[m')
                            usernames = None
                            break
                user.tasks[code - 1].share(usernames)
                input("\n\t\tDone.\n\t\tPress Enter to Continue...")
            except AssertionError:
                print('\33[35m\t\tDefine a task first, then try to share it.\33[m')
                input("\t\tPress Enter to Continue...")

        elif choice == 5:  # back
            continuation = False


def edit_task(task, user, item, logger):
    if item == 1:
        try:
            assert task.done is not True
        except AssertionError:
            print('\33[35m\t\tThis task has already been done.\33[m')
        else:
            task.edit('done', True)
            print("\n\t\t\33[35mDone.\33[m")
            logger.info('a task was done')
        finally:
            input("\t\tPress Enter to Continue...")

    if item == 2:
        print('\33[35m\t\tPrevious date and time: \33[m', task.dt)

        print('\33[35m\t\tEnter new date and time or 0 for back: \33[m')

        date = input('\33[35m\t\tDate (in this format month/day/year): \33[m')
        if date == 0:
            return
        # elif regex...
        date = date.split('/')
        date = [int(x) for x in date]
        time = input('\33[35m\t\tTime (in this format hour:minute:second): \33[m').split(':')
        time = [int(x) for x in time]
        dt = datetime.datetime(date[2], date[0], date[1],
                               time[0], time[1], time[2])
        task.edit('dt', dt)
        logger.info('a task was postponed')

    if item == 3:
        categories = []
        for tsk in user.tasks:
            if tsk.category and tsk.category not in categories:
                categories.append(tsk.category)

        if categories:
            for index, category in enumerate(categories, 1):
                print(f'\n\33[35m\t\t{index}) {category}\33[m')

            category_name = None
            while category_name is None:
                category_name = input(
                    '\n\33[35m\t\tSelect one of the previous categories or '
                    'enter a new category name (0 for back) : \33[m')
                try:
                    category_name = int(category_name)
                    assert category_name in range(1, len(categories) + 1)
                except ValueError:
                    if category_name:
                        task.edit('category', category_name)
                except AssertionError:
                    if category_name == 0:
                        return
                    print('\33[35m\t\tInvalid number.\33[m')
                    category_name = None
                else:
                    task.edit('category', categories[category_name - 1])

        else:
            category_name = input('\33[35m\t\tPlease enter the category name: \33[m')
            task.edit('category', category_name)

        logger.info(f'{category_name} category added')
        print("\n\t\t\33[35mDone.\33[m")
        input("\t\tPress Enter to Continue...")

    if item == 4:
        description = input("\n\t\t\33[35mPlease enter the description's of the task: \33[m")
        task.edit('description', description)
        print("\n\t\t\33[35mDone.\33[m")
        input("\t\tPress Enter to Continue...")

    if item == 5:
        print('\t\t\33[35mThe previous location: \33[m', task.location)
        loc = input('\t\t\33[35mPlease enter the new location: \33[m')
        task.edit('location', loc)
        input("\n\t\t\33[35mDone.\33[m")
        input("\t\tPress Enter to Continue...")

    if item == 6:
        print('\t\t\33[35mThe previous link: \33[m', task.link)
        link = input('\t\t\33[35mPlease enter the new link: \33[m')
        task.edit('link', link)
        print("\n\t\t\33[35mDone.\33[m")
        input("\t\tPress Enter to Continue...")

    if item == 7:
        if task.importance is True:
            print('\t\t\33[35mThe task was important.\33[m')
        else:
            print('\t\t\33[35mThe task was not important.\33[m')

        status = None
        while status is None:
            print(f'\33[97m{"-" * 100}\33[m')
            print('''\33[34m
        1.Important
        2.Not important\33[m''')
            try:
                status = int(input('''\t\t\33[35mSpecify the current status of the task importance:\33[m'''))
            except ValueError:
                print('\33[35mInvalid input. Please try again.\33[m')
            else:
                if status not in [1, 2]:
                    print('\33[35mInvalid number. Please try again.\33[m')
                    continue
        importance = True if status == 1 else False
        task.edit('importance', importance)
        print("\n\t\t\33[35mDone.\33[m")
        input("\t\tPress Enter to Continue...")

    if item == 8:
        if task.urgency is True:
            print('\t\t\33[35mIt was an urgent task.\33[m')
        else:
            print("\t\t\33[35mIt wasn't an urgent task.\33[m")

        status = None
        while status is None:
            print(f'\33[97m{"-" * 100}\33[m')
            print('''\33[34m
        1.Urgent
        2.Not Urgent\33[m''')
            try:
                status = int(input('''\t\t\33[35mSpecify the current status of the task urgency:\33[m'''))
            except ValueError:
                print('\33[35mInvalid input. Please try again.\33[m')
            else:
                if status not in [1, 2]:
                    print('\33[35mInvalid number. Please try again.\33[m')
                    status = None
                    continue
        urgency = True if status == 1 else False
        task.edit('urgency', urgency)
        print("\n\t\t\33[35mDone.\33[m")
        input("\t\tPress Enter to Continue...")

    if item == 9:
        print(task)
        delete = None
        while delete is None:
            print('\33[35m\t\tAre you sure you want to delete this task?\33[m')
            try:
                delete = int(input('\33[35m\t\t1)Yes\n\t\t2)No\n\t\t\33[m'))
                assert delete in [1, 2]
            except ValueError:
                print('Invalid input. Please try again.')
            except AssertionError:
                print('Invalid input. Enter 1 or 2.')
                delete = None
            else:
                if delete not in [1, 2]:
                    print('Invalid input. Enter 1 or 2.')
                    delete = None
        task.edit('activation', False)
        print("\n\t\t\33[35mDone.\33[m")
        input("\t\tPress Enter to Continue...")
