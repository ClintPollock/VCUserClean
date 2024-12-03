# Veracode User Clean Up Scripts

This repository contains Python script to fetch users, and then delete users.

## Scripts

1. **fetch_users.py**: Fetches users from the Veracode API and saves them to a CSV file(s) - one oringal `CurrentUsers.csv` and one you can remove users that you do not want deleted.
2. **delete_users.py**: Deletes users listed in the `UsersToDelete.CSV` file and logs the deletion process.

## Configuration

1. **Install Dependencies**:
    Python is requied, also install veracode-api-signing with command - `pip install veracode-api-signing`
    

2. **Update veracode_credentials.json**:
    Update your API key and secret (must have administrator role).

## Usage

1. **Fetch Users**:
run `python fetch_users.py` script to fetch users from the Veracode API and saves them to CSV files.  One is called `CurrentUsers.csv` as an original, and the other is a copy for you to edit and remove users you do not want to delete in `UsersToDelete.csv`.


2. **Delete Users**:
    Run `python delete_users.py` to delete the users still remaining in `UsersToDelete.csv` after you have removed the users that you do not want to delete.
    Details are stored in log.txt for your archive.
## Sample Output

### Sample [UsersToDelete.csv](http://_vscodecontentref_/3)

The CSV will include the following:
user_id,user_legacy_id,user_name,first_name,last_name,email_address,saml_user,login_enabled
