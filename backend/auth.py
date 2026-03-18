import getpass
from db import check_lockout, create_user, get_user, verify_user, record_failed_attempt


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
    while True:
        menu_option = input("Please select an option: \n0. Exit \n1. Login\n2. Register\nEnter a number: ").strip()
        if menu_option == "0":
            print("Goodbye!")
            return None
        elif menu_option == "1":
            result = login()
            if result is not None:
                return result
        elif menu_option == "2":
            result = register()
            if result is not None:
                return result
        else:
            print("Invalid option. Please enter a valid option.")
def login():
        while True:
            name = input("Enter your name (or 0 to go back): ").strip()
            if name == "0":
                return None
            # 1. Get username
            # 2. Check if user exists
            # 3. Call check_lockout once, store result in variable
            # 4. If result is truthy, print locked message with timestamp, continue
            # 5. Ask for password
            # 6. Call verify_user
            # 7. If wrong password: call record_failed_attempt, ask again
            # 8. If correct password: return user_id

            does_user_exist = get_user(name)
            if does_user_exist:
                lockout_status = check_lockout(user_id=does_user_exist[0])
                if lockout_status:
                    print(f"Account locked until {lockout_status}")
                    continue
                password = getpass.getpass("Enter password: ")
                user = verify_user(name, password)
                while not user:
                    record_failed_attempt(does_user_exist[0])
                    print("Incorrect password. Please try again.")
                    password = getpass.getpass("Enter password: ")
                    user = verify_user(name, password)
                    if check_lockout(user_id=does_user_exist[0]):
                        print("Too many failed attempts. Account locked for 15 minutes.")
                        return None
                return user[0] 
            else:
                print("User not found. Please register first.")
def register():
    while True:
        name = input("Enter your name (or 0 to go back): ").strip()
        if name == "0":
            return None
        if get_user(name):
            print("User already exists. Please choose another username.")
        else:
            password = get_new_password()
            addiction = input("What can I help you with? (e.g., smoking, binge-eating, pornography, etc.): ").strip()
            user_id = create_user(name, addiction, password)
            print(f"User '{name}' registered successfully! Please log in.")
            return login()
