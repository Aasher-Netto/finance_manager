import shutil
import os
from datetime import datetime

from auth import register_user, login_user
from transactions import add_transaction, update_transaction, delete_transaction, get_transactions_by_category #Import the transactions file
from categories import add_category, update_category, delete_category, get_all_categories  #Import the categories
from reports import get_monthly_report, get_yearly_report  #Import the reports 
from budgets import set_budget, get_budget #Import the budgets
from database import get_db_connection  # Import the database connection function

def backup_database(backup_dir='backups'):
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)

    db_path = 'finance_manager.db'
    backup_file = os.path.join(backup_dir, f"backup_{get_timestamp()}.db")

    shutil.copy(db_path, backup_file)
    print(f"Backup created successfully at {backup_file}")

def restore_database(backup_file, db_path='finance_manager.db'):
    if not os.path.exists(backup_file):
        print(f"Backup file {backup_file} does not exist.")
        return
    
    shutil.copy(backup_file, db_path)
    print(f"Database restored successfully from {backup_file}")

def get_timestamp():
    return datetime.now().strftime("%Y%m%d_%H%M%S")

def main_menu(user_id):
    while True:
        print("\n--- Main Menu ---")
        print("1. Add Transaction")
        print("2. Update Transaction")
        print("3. Delete Transaction")
        print("4. View Transactions by Category")
        print("5. Generate Financial Reports.")
        print("6. Manage Categories")
        print("7. Set Monthly Budget")
        print("8. Backup database")
        print("9. Restore Database")
        print("10. Logout")
        choice = input("Choose an option: ")

        if choice == '1':
            amount = float(input("Enter amount: "))
            categories = get_all_categories()
            print("Available Categories:")
            for cat in categories:
                print(f"{cat['id']}:{cat['name']}")
            category_id = int(input("Choose a category by ID: "))
            type_ = input("Enter type (income/expense): ").lower()  # Updated variable name to type_
            date = input("Enter date (YYYY-MM-DD): ")
            description = input("Enter description (optional): ")
            add_transaction(user_id, amount, category_id, type_, date, description)
        elif choice == '2':
            transaction_id = int(input("Enter transaction ID to update: "))
            amount = float(input("Enter new amount: "))
            categories = get_all_categories()
            print("Available Categories:")
            for cat in categories:
                print(f"{cat['id']}:{cat['name']}")
            category_id = int(input("Choose a new category by ID: "))
            type_ = input("Enter new type (income/expense): ").lower()
            date = input("Enter new date (YYYY-MM-DD): ")
            description = input("Enter new description (optional): ")
            update_transaction(transaction_id, amount, category_id, type_, date, description)
        elif choice == '3':
            transaction_id = int(input("Enter transaction ID to delete: "))
            delete_transaction(transaction_id)
        elif choice == '4':
            categories = get_all_categories()
            print("Available Categories:")
            for cat in categories:
                print(f"{cat['id']}:{cat['name']}")
            category_id = int(input("Choose a category by ID to filter: "))
            transactions = get_transactions_by_category(user_id, category_id)
            for transaction in transactions:
                print(transaction)
        elif choice == '5':
            generate_reports(user_id)
        elif choice == '6':
            manage_categories()
        elif choice == '7':
            set_budget_menu(user_id)
        elif choice == '8':
            backup_database()
        elif choice == '9':
            backup_file = input("Enter the backup file path: ")
            restore_database(backup_file)
        elif choice == '10':
            print("Logged out.")
            break
        else:
            print("Invalid choice. Please try again.")

def generate_reports(user_id):
    print("\n--- Generate Financial Reports ---")
    print("1. Monthly Report")
    print("2. Yearly Report")
    choice = input("Choose an option: ")

    if choice == '1':
        year = input("Enter year (YYYY): ")
        month = input("Enter month (MM): ")
        report = get_monthly_report(user_id, year, month)
    elif choice == '2':
        year = input("Enter year (YYYY): ")
        report = get_yearly_report(user_id, year)
    else:
        print("Invalid choice. Please try again.")
        return

    print("\n--- Financial Report ---")
    print(f"Income: ${report['income']: .2f}")
    print(f"Expenses: ${report['expenses']: .2f}")
    print(f"Savings: ${report['savings']: .2f}")

def manage_categories():
    while True:
        print("\n--- Manage Categories ---")
        print("1. Add Category")
        print("2. Update Category")
        print("3. Delete Category")
        print("4. Back to Main Menu")
        choice = input("Choose an option: ")

        if choice == '1':
            name = input("Enter category name: ")
            add_category(name)
        elif choice == '2':
            categories = get_all_categories()
            print("Available Categories:")
            for cat in categories:
                print(f"{cat['id']}:{cat['name']}")
            category_id = int(input("Choose a category by ID to update: "))
            new_name = input("Enter new category name: ")
            update_category(category_id, new_name)
        elif choice == '3':
            categories = get_all_categories()
            print("Available Categories:")
            for cat in categories:
                print(f"{cat['id']}:{cat['name']}")
            category_id = int(input("Choose a category by ID to delete: "))
            delete_category(category_id)
        elif choice == '4':
            break
        else:
            print("Invalid choice. Please try again.")
            
def set_budget_menu(user_id):
    categories = get_all_categories()
    if not categories:
        print("No categories found. Please add categories first.")
        return

    print("Available Categories:")
    for cat in categories:
        print(f"{cat['id']}:{cat['name']}")

    try:
        category_id = int(input("Choose a category by ID: "))
        selected_category = next((cat for cat in categories if cat['id'] == category_id), None)

        if selected_category is None:
            print("Invalid category ID.")
            return

        year = input("Enter year (YYYY): ")
        month = input("Enter month (MM): ")
        budget_amount = float(input("Enter budget amount: "))

        set_budget(user_id, category_id, year, month, budget_amount)
        print(f"Budget of ${budget_amount} set for {selected_category['name']} in {month}-{year}.")

    except ValueError:
        print("Invalid input. Please enter a valid number for category ID and budget amount.")

def main():
    print("Welcome to Finance Manager!")
    while True:
        print("1. Register")
        print("2. Login")
        print("3. Exit")
        choice = input("Choose an option: ")

        if choice == '1':
            username = input("Enter a username: ")
            password = input("Enter a password: ")
            register_user(username, password)
        elif choice == '2':
            username = input("Enter your username: ")
            password = input("Enter your password: ")
            if login_user(username, password):
                user_id = get_user_id(username)
                if user_id:
                    main_menu(user_id)
                else:
                    print("Error: User ID not found.")
        elif choice == '3':
            break
        else:
            print("Invalid choice. Please try again.")

def get_user_id(username):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('SELECT id FROM users WHERE username = ?', (username,))
    result = cursor.fetchone()
    conn.close()

    if result:
        return result['id']
    return None

if __name__ == "__main__":
    main()