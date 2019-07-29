'''
Main module for working with LibreNMS
'''
# Import custom modules
from db_class import LibreNMSReport
from aux_functions import initial_dialog, get_credentials

# Initial dialog with user
initial_dialog()
# Credentials for connection to the DB
credentials = get_credentials()
librenms = LibreNMSReport(*credentials)
# Send query about downtime periods
librenms.mariadb_send_query(
    'SELECT device_id, state, time_logged FROM librenms.alert_log '
    'where rule_id = 1 order by device_id, time_logged;')
# Creation of the report
librenms.generate_report()
# Send query about hostnames
librenms.mariadb_send_query(
    'SELECT device_id, hostname FROM librenms.devices order by device_id;')
librenms.resolve_device_id()
# Export output to .csv file
librenms.export_to_csv('output.csv')
# Send report to customer by e-mail
librenms.send_mail()
