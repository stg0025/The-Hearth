import getpass
from auth import get_new_password
from sessions import daily_checkin, craving_session
from display import show_dashboard
from db import create_tables, create_user, get_user, verify_user

def main():
    create_tables()
    #login() called from auth.py
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

    # Menu
    print()
    print("What would you like to do?")
    print("1. Daily check-in")
    print("2. Craving session")
    print("3. Dashboard")
    print("4. Exit")
    print()
    choice = input("Enter 1, 2, 3, or 4: ").strip()
    
    while choice not in ["1", "2", "3", "4"]:
        print("Invalid choice. Run the app again and enter 1, 2, 3, or 4.")
        choice = input("Enter 1, 2, 3, or 4: ").strip()

    if choice == "1":
        daily_checkin(user_id)
    elif choice == "2":
        craving_session(user_id)
    elif choice == "3":
        show_dashboard(user_id)
    elif choice == "4":
        print("Have a wonderful day!")
        return

if __name__ == "__main__":
    main()