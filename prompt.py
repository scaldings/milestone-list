import os
import stdiomask
import database as db
from time import sleep


def prompt_auth():
    print('\n' + '*' * 25)
    print('1. Create account')
    print('2. Log in')
    print('3. Quit')
    print('*' * 25)
    func = input(': ')

    if func == '1':
        cls()
        create_account()
    elif func == '2':
        cls()
        login()
    elif func == '3':
        cls()
        exit()
    else:
        cls()
        print('Invalid function.')
        prompt_auth()


def create_account():
    name_input = input('\nEnter your name: ')

    names = db.get_account_names()
    if names is not None:
        if name_input in names:
            print('This username is already used.')
            create_account()

    password_input1 = stdiomask.getpass('Enter your password: ')
    password_input2 = stdiomask.getpass('Repeat your password: ')

    if password_input1 == password_input2:
        db.create_account(name_input, password_input1)
        cls()
        print('\nSuccessfully created an account.')
        prompt(name_input)
    else:
        cls()
        print('\nThe passwords are not matching.')
        prompt_auth()


def login():
    name_input = input('\nEnter your name: ')

    names = db.get_account_names()
    if names is not None:
        if name_input not in names:
            print('This username does not exist.')
            login()

    password_input = stdiomask.getpass('Enter your password: ')
    password = db.get_account_password(name_input)

    if password_input == password:
        cls()
        print('\nLogged in.')
        prompt(name_input)
    else:
        cls()
        print('\nIncorrect password.')
        prompt_auth()


def prompt(name):
    print('\n' + '*' * 25)
    print('1. Add milestone')
    print('2. Remove milestone')
    print('3. Show all milestones')
    print('4. Log out')
    print('5. Quit')
    print('*' * 25)
    func = input(': ')

    if func == '1':
        cls()
        add_milestone(name)
    elif func == '2':
        cls()
        remove_milestone(name)
    elif func == '3':
        cls()
        show_milestones(name)
    elif func == '4':
        cls()
        print('\nLogged out.')
        prompt_auth()
    elif func == '5':
        cls()
        exit()
    else:
        cls()
        print('Invalid function.')
        prompt(name)


def add_milestone(name: str):
    milestone = input('\nWhat is your milestone?: ')
    date = input('Enter the date of the milestone: ')
    db.add_milestone(name, date, milestone)
    cls()
    print('\nMilestone added!')
    prompt(name)


def remove_milestone(name: str):
    print('\n' + '*' * 25)
    for x in db.list_milestones(name):
        print(x)
    if len(db.list_milestones(name)) == 0:
        print('None')
    print('*' * 25)
    identifier = input('Enter the ID of the milestone you want to remove: ')

    db.remove_milestone(name, identifier)
    cls()
    print('\nMilestone removed successfully.')
    prompt(name)


def show_milestones(name):
    print('\n' + '*' * 25)
    for x in db.list_milestones(name):
        print(x)
    if len(db.list_milestones(name)) == 0:
        print('None')
    print('*' * 25)
    back = input('Back to menu? (Y/N) ')

    if back == 'Y':
        cls()
        prompt(name)
    elif back == 'N':
        sleep(15)
        cls()
        prompt(name)
    else:
        cls()
        prompt(name)


def cls():
    os.system('cls' if os.name == 'nt' else 'clear')


if __name__ == '__main__':
    db.init()
    cls()
    prompt_auth()
