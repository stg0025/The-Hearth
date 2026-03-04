from sessions import daily_checkin, craving_session
from display import show_dashboard
from db import create_tables, create_user, get_user

def main():
    create_tables()
    # Get or create user
    name = input("Welcome to The Hearth. What should I call you? ").strip()
    user = get_user(name)
    
    if not user:
        addiction_type = input("What can I help you with? (e.g. food, pornography, gambling): ").strip()
        user_id = create_user(name, addiction_type)
    else:
        user_id = user[0]
    
    # Menu
    print()
    print("What would you like to do?")
    print("1. Daily check-in")
    print("2. Craving session")
    print("3. Dashboard")
    print()
    choice = input("Enter 1, 2, or 3: ").strip()
    
    if choice == "1":
        daily_checkin(user_id)
    elif choice == "2":
        craving_session(user_id)
    elif choice == "3":
        show_dashboard(user_id)
    else:
        print("Invalid choice. Run the app again and enter 1, 2, or 3.")

if __name__ == "__main__":
    main()