import sqlite3
from database import get_db_connection

def set_budget(user_id, category_id, year, month, budget_amount):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('''
    INSERT INTO budgets (user_id, category_id, year, month, budget_amount)
    VALUES (?, ?, ?, ?, ?)
    ON CONFLICT(user_id, category_id, month, year) DO UPDATE SET budget_amount = excluded.budget_amount
    ''', (user_id, category_id, year, month, budget_amount))

    conn.commit()
    conn.close()

def get_remaining_budgets(user_id, category_id, year, month):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('''
    SELECT budget_amount FROM budgets
    WHERE user_id = ? AND category_id = ? AND year = ? AND month =?
    ''', (user_id, category_id, year, month))
    result = cursor.fetchone()

    if not result:
        print("No budget set for this category and time period.")
        conn.close()
        return None

    total_budget = result['budget_amount']

    cursor.execute('''
    SELECT SUM(amount) as total_expenses FROM transactions
    WHERE user_id = ? AND category_id = ? AND type = 'expense'
    AND strftime('%Y', date) = ? AND strftime('%m', date) = ?
    ''', (user_id, category_id, year, month))
    result = cursor.fetchone()
    total_expenses = result['total_expenses'] if result['total_expenses'] else 0

    conn.close()
    return total_budget - total_expenses

def check_budget_exceeded(user_id, category_id, year, month):
    remaining_budget = get_remaining_budgets(user_id, category_id, year, month)
    if remaining_budget is not None and remaining_budget < 0:
        print("Budget exceeded for this category!")
        return True
    return False

def get_budget(user_id, category_id, year, month):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('''
    SELECT budget_amount 
    FROM budgets 
    WHERE user_id = ? AND category_id = ? AND year = ? AND month = ?
    ''', (user_id, category_id, year, month))
    
    result = cursor.fetchone()
    conn.close()

    # Check if result is not None and return the budget amount correctly
    if result:
        return result[0]  # Access the first item in the tuple
    return None