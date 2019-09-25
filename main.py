'''
Main module for working with LibreNMS
'''
# Import custom modules
from db_class import LibreNMSReport,SQL
from aux_functions import initial_dialog, get_credentials, get_date_range

# Initial dialog with user
initial_dialog()
# Credentials for connection to the DB
credentials = get_credentials()
date_range = get_date_range()
librenms = LibreNMSReport(*credentials)
# Send query about downtime periods
query = (
    'SELECT device_id, state, time_logged FROM librenms.alert_log '
    'WHERE rule_id = 1 AND time_logged BETWEEN {} and {} '
    'ORDER by device_id, time_logged;').format(*date_range)
try:
    librenms.mariadb_send_query(query)
except SQL.errors.ProgrammingError:
    print('Incorrect date range has been provided !',
          'Please restart script and try input dates again.')
    exit()
# Creation of the report
librenms.generate_report()
# Send query about hostnames
query = 'SELECT device_id, hostname FROM librenms.devices order by device_id;'
librenms.mariadb_send_query(query)
librenms.resolve_device_id()
# Export output to .csv file
librenms.export_to_csv('output.csv')
# Send report to customer by e-mail
librenms.send_mail()
