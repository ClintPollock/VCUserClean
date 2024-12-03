import requests
import json
import os
import shutil
import csv
from veracode_api_signing.plugin_requests import RequestsAuthPluginVeracodeHMAC

# Load Veracode credentials
with open('veracode_credentials.json') as f:
    credentials = json.load(f)

api_key_id = credentials['api_key_id']
api_key_secret = credentials['api_key_secret']

auth = RequestsAuthPluginVeracodeHMAC(api_key_id, api_key_secret)

# Function to fetch all users with pagination
def fetch_all_users():
    users = []
    page = 0
    size = 20  # Adjust the size if needed

    while True:
        response = requests.get(f'https://api.veracode.com/api/authn/v2/users?page={page}&size={size}', auth=auth)
        if response.status_code != 200:
            print(f"Failed to fetch users: {response.status_code} - {response.text}")
            exit(1)

        data = response.json()
        users.extend(data['_embedded']['users'])

        if page >= data['page']['total_pages'] - 1:
            break

        page += 1

    return users

# Fetch all users
all_users = fetch_all_users()

# Log total records fetched
print(f"Total records fetched: {len(all_users)}")

# Determine the filename
base_filename = 'CurrentUsers'
extension = '.csv'
filename = base_filename + extension
counter = 1

while os.path.exists(filename):
    filename = f"{base_filename}_{counter}{extension}"
    counter += 1

# Save users to the determined filename
with open(filename, 'w', newline='') as csvfile:
    fieldnames = ['user_id', 'user_legacy_id', 'user_name', 'first_name', 'last_name', 'email_address', 'saml_user', 'login_enabled']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for user in all_users:
        writer.writerow({
            'user_id': user['user_id'],
            'user_legacy_id': user['user_legacy_id'],
            'user_name': user['user_name'],
            'first_name': user['first_name'],
            'last_name': user['last_name'],
            'email_address': user['email_address'],
            'saml_user': user['saml_user'],
            'login_enabled': user['login_enabled']
        })

# Copy to UsersToDelete.csv
shutil.copy(filename, 'UsersToDelete.csv')