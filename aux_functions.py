'''
Small module that contains auxiliary functions
'''
# Import getpass for getting the password from the user without echo
from getpass import getpass


# Simple auxiliary function for usage with map()
def converter_to_string(value):
    return str(value)


# Function for getting DB credentials from config and password from the user
def get_credentials():
    passwd = getpass(promt='Please provide password for your DB > ')
    with open('conf.txt', 'r') as config:
        credentials = config.readlines()
    credentials.append(passwd)
    return tuple(credentials)
