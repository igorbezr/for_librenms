'''
Small module that contains auxiliary functions
'''
# Import getpass for getting the password from the user without echo
from getpass import getpass
# Import json to fetch data from the configuration file
from json import load


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
    with open('config.json', 'r') as config:
        credentials = load(config)
    credentials['passwd'] = passwd
    return tuple(credentials.values())

# Functions for getting date range from user input to report generation
def get_date_range():
    ctrl_c_message = (
        '\n' + 'You pressed Ctrl-C ! Program will be terminated now !')
    inform_message = (
        'Inputting dates must be compliant with following format :'
        '\n' + 'xxxxyyzz where xxxx - year, yy - month, zz - day.')
    print(inform_message)
    try:
        first_date = input('Provide start date > ')
        second_date = input('Provide finish date > ')
    except KeyboardInterrupt:
                print(ctrl_c_message)
                exit()
    return first_date, second_date
