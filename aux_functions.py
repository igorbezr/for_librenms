'''
Small module that contains auxiliary functions
'''
# Import getpass for getting the password from the user without echo
from getpass import getpass


# Simple auxiliary function for usage with map()
def converter_to_string(value):
    return str(value)


# Printing the greetings to the CLI
def initial_dialog():
    greetings = (
        'Hello, dear customer !' + '\n'
        'This is script for generating the devices downtime report' + '\n'
        'Do you want to generate report ? [Yes/No]')
    processing = 'Program is starting, please wait ...'
    error_message = (
        'Please type "Yes", or "No"' + '\n'
        'Or press Ctrl-C for exit')
    exit_message = 'Program has been successfully terminated !'
    print(greetings)
    while True:
        try:
            answer = input()
            if answer == 'Yes':
                print(processing)
                return
            elif answer == 'No':
                print(exit_message)
                exit()
                return
            else:
                print(error_message)
        except KeyboardInterrupt:
            print(exit_message)
            exit()


# Function for getting DB credentials from config and password from the user
def get_credentials():
    ctrl_c_message = (
        '\n' + 'You pressed Ctrl-C ! Program will be terminated now !')
    try:
        passwd = getpass('Please provide password for your DB > ')
    except KeyboardInterrupt:
                print(ctrl_c_message)
                exit()
    with open('conf.txt', 'r') as config:
        credentials = config.readlines()
    credentials.append(passwd)
    return tuple(credentials)
