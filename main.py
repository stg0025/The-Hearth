import getpass
from auth import login_or_register
from display import show_dashboard
from db import create_tables
from sessions import daily_checkin, craving_session

def main():
    create_tables()
    user_id = login_or_register()
    if user_id is None:
        return

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
        print("Invalid choice. Please enter 1, 2, 3, or 4.")
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