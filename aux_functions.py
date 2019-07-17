'''
Small module that contains auxiliary functions
'''
# Import getpass for getting the password from the user without echo
from getpass import getpass


# Simple auxiliary function for usage with map()
def converter_to_string(value):
    return str(value)


# Function for getting DB credentials from the user
def get_credentials():
    host = input(['Please input the DB hostname >'])
    user = input(['username >'])
    passwd = getpass()
    db_name = input(['data base name >'])
    credentials = host, user, passwd, db_name
    return credentials
