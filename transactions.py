import sqlite3
from database import get_db_connection
from budgets import set_budget, get_budget

def add_transaction(user_id, amount, category_id, type_, date, description=""):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Insert the transaction
    cursor.execute('''
    INSERT INTO transactions (user_id, amount, category_id, type, date, description)
    VALUES(?, ?, ?, ?, ?, ?)
    ''', (user_id, amount, category_id, type_, date, description))

    conn.commit()

    # Check if the budget is exceeded
    year = date.split('-')[0]
    month = date.split('-')[1]
    budget = get_budget(user_id, category_id, year, month)

    if budget:
        cursor.execute('''
        SELECT SUM(amount) as total_expenses FROM transactions
        WHERE user_id = ? AND category_id = ? AND type = 'expense' AND strftime('%Y', date) = ? AND strftime('%m', date) = ?
        ''', (user_id, category_id, year, month))

        # Fetch the total expenses for the category in the given month/year
        result = cursor.fetchone()
        total_expenses = result[0] if result[0] is not None else 0

        # Compare total expenses with the budget
        if total_expenses > budget:
            print(f"Warning: You have exceeded your budget of ${budget:.2f} for this category!")

    conn.close()
    print(f"{type_.capitalize()} of ${amount} added successfully.")

def update_transaction(transaction_id, amount, category_id, type_, date, description=""):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('''
    UPDATE transactions
    SET amount = ?, category_id = ?, type = ?, date = ?, description = ?
    WHERE id = ?
    ''', (amount, category_id, type_, date, description, transaction_id))

    conn.commit()
    conn.close()
    print(f"Transaction ID {transaction_id} updated successfully.")

def delete_transaction(transaction_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('''
    DELETE FROM transactions WHERE id = ?
    ''', (transaction_id,))

    conn.commit()
    conn.close()
    print(f"Transaction ID {transaction_id} deleted successfully.")

def get_transactions_by_category(user_id, category_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('''
    SELECT * FROM transactions
    WHERE user_id = ? AND category_id = ?
    ''', (user_id, category_id))

    transactions = cursor.fetchall()
    conn.close()
    return transactions
