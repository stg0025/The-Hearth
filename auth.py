import getpass
import sqlite3
from db import get_connection

def get_new_password():
    '''
    1. Prompt the user to enter a new password using getpass.getpass() to hide input.
    2. Ensure it meets criteria (at least 10 characters).
    3. Prompt the user to confirm the new password.
    4. If the passwords match, return the new password.
    5. If they don't match, print an error message and repeat the process until they do.
    '''
    while True:
        password = getpass.getpass("Enter a new password (at least 10 characters): ")
        if len(password) < 10:
            print("Password must be at least 10 characters long. Please try again.")
            continue
        confirm_password = getpass.getpass("Confirm your new password: ")
        if password != confirm_password:
            print("Passwords do not match. Please try again.")
            continue
        return password
        

