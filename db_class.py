'''
Module contains class for working with MySQL LibreNMS DB
'''
# Importing module that need to sent query to MySQL
import mysql.connector as SQL
# Import custom module contains auxiliary functions
from aux_functions import converter_to_string
# Import subprocess for send report by e-mail
from subprocess import Popen, PIPE


# Class section
class LibreNMSReport():
    '''
    Class for working with Librenms MySQL DB and generating reports
    '''
    def __init__(self, host, user, db_name, e_mail, passwd):
        '''
        The __init__ method takes values needing to connect to the DB
        '''
        self.host = host
        self.user = user
        self.db_name = db_name
        self.e_mail = e_mail
        self.passwd = passwd

    def mariadb_send_query(self, query):
        '''
        Method for send query to Maria DB and gets back the list of tuples
        '''
        # Connection to the database
        db = SQL.connect(
            host=self.host,
            user=self.user,
            passwd=self.passwd,
            database=self.db_name)
        # Creation the cursor object
        cursor = db.cursor()
        # Send query to the DB
        cursor.execute(query)
        # Get result of the query
        self.query_output = cursor.fetchall()
        # Closing connection to the DB
        db.close()

    def generate_report(self):
        '''
        Method to generate report about downtime periods
        '''
        temp = dict()
        self.report = dict()
        # Populating temporary dictionary
        for device, state, time in self.query_output:
            if device not in temp:
                temp[device] = [(state, time)]
            else:
                temp[device].append((state, time))
        # Finding outage periods in temporary dictionary and adding it
        # to the report
        for device in temp:
            self.report[device] = []
            for index in range(0, len(temp[device]) - 1):
                # State of the device (up/down)
                current_state = temp[device][index][0]
                new_state = temp[device][index + 1][0]
                # Device's timestamps for corresponding state
                current_time = temp[device][index][1]
                new_time = temp[device][index + 1][1]
                if current_state == 1 and new_state == 0:
                    self.report[device].append((
                        current_time,
                        new_time,
                        new_time - current_time))

    def resolve_device_id(self):
        '''
        Method to resolve numeric device_id to device's hostname.
        It replaces all numeric keys to string hostnames
        '''
        device_list = list()
        for index in range(0, len(self.query_output) - 1):
            # List of hostnames
            device_list.append(self.query_output[index][1])
        # Replacing keys
        self.report = dict(zip(device_list, list(self.report.values())))

    def export_to_csv(self, filename):
        '''
        Method to export collected data to .csv format for future usage
        '''
        with open(filename, "w") as csv_file:
            # Explicit declaration about using separators for Excel
            csv_file.write('sep=,' + '\n')
            # Write columns names
            csv_file.write(
                'Hostname, Start date, End date,'
                ' Duration in days (if more than 1 day),'
                ' Duration in hours' + '\n')
            # For each device and each downtime
            for device, timedata in self.report.items():
                # Convert each tuple value to list of strings and add to row
                for tuple_value in timedata:
                    csv_row = (
                        [device] +
                        list(map(converter_to_string, list(tuple_value))))
                    csv_file.write(", ".join(csv_row) + "\n")

    def send_mail(self):
        '''
        Send e-mail by invoking postfix (with Unix 'mail' utility)
        '''
        subject_text = 'Hello, dear customer ! There is a report for you !'
        attach_name = 'output.csv'
        mail_body = Popen(["echo"], stdout=PIPE)
        mail_sending = Popen([
            'mail',
            '-s',
            subject_text,
            self.e_mail,
            '-A',
            attach_name],
            stdin=mail_body.stdout,
            stdout=PIPE)
        mail_body.stdout.close()
        output = mail_sending.communicate()
        print(output)
        return output
