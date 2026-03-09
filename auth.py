import getpass
from db import create_user, get_user, verify_user


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
        

def login_or_register():
    name = input("Welcome to The Hearth. What should I call you? ").strip()
    while not name:
        print("Please enter a name to continue.")
        name = input("Enter your name: ").strip()
    if get_user(name):
        password = getpass.getpass("Enter password: ")
        user = verify_user(name, password)
        while not user:
            print("Incorrect password. Please try again.")
            password = getpass.getpass("Enter password: ")
            user = verify_user(name, password)
        user_id = user[0] 
    else:
        password = get_new_password()
        addiction_type = input("What can I help you with? (e.g. food, pornography, gambling, etc): ").strip()
        user_id = create_user(name, addiction_type, password)
    return user_id