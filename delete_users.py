import requests
import csv
import json
import logging
from veracode_api_signing.plugin_requests import RequestsAuthPluginVeracodeHMAC

# Setup logging
logging.basicConfig(filename='log.txt', level=logging.INFO, format='%(asctime)s - %(message)s')

# Load Veracode credentials
with open('veracode_credentials.json') as f:
    credentials = json.load(f)

api_key_id = credentials['api_key_id']
api_key_secret = credentials['api_key_secret']

auth = RequestsAuthPluginVeracodeHMAC(api_key_id, api_key_secret)

# Delete users listed in UsersToDelete.csv
with open('UsersToDelete.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    users_to_delete = [row for row in reader]

# Log total records to be deleted
total_users = len(users_to_delete)
log_message = f"Total records to be deleted: {total_users}"
logging.info(log_message)
print(log_message)

for index, user in enumerate(users_to_delete, start=1):
    user_id = user['user_id']
    first_name = user['first_name']
    last_name = user['last_name']
    email_address = user['email_address']
    
    log_message = f"Deleting user {index} of {total_users}: {user_id} ({first_name} {last_name}, {email_address})"
    logging.info(log_message)
    print(log_message)
    
    delete_response = requests.delete(f'https://api.veracode.com/api/authn/v2/users/{user_id}', auth=auth)
    if delete_response.status_code == 200:
        log_message = f'Successfully deleted user {user_id} ({first_name} {last_name}, {email_address})'
        logging.info(log_message)
        print(log_message)
    else:
        log_message = f'Failed to delete user {user_id} ({first_name} {last_name}, {email_address}): {delete_response.status_code} - {delete_response.text}'
        logging.error(log_message)
        print(log_message)