import sqlite3
from database import get_db_connection

def get_monthly_report(user_id, year, month):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Summing income
    cursor.execute('''
        SELECT SUM(amount) FROM transactions 
        WHERE user_id = ? AND type = 'income' AND strftime('%Y-%m', date) = ?
    ''', (user_id, f'{year}-{month}'))
    income = cursor.fetchone()[0] or 0.0

    # Summing expenses
    cursor.execute('''
        SELECT SUM(amount) FROM transactions 
        WHERE user_id = ? AND type = 'expense' AND strftime('%Y-%m', date) = ?
    ''', (user_id, f'{year}-{month}'))
    expenses = cursor.fetchone()[0] or 0.0

    # Returning the report
    return {'income': income, 'expenses': expenses, 'savings': income - expenses}



def get_yearly_report(user_id, year):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Summing income for the year
    cursor.execute('''
        SELECT SUM(amount) FROM transactions 
        WHERE user_id = ? AND type = 'income' AND strftime('%Y', date) = ?
    ''', (user_id, str(year)))
    income = cursor.fetchone()[0] or 0.0
    print(f"Yearly income for {year}: {income}")

    # Summing expenses for the year
    cursor.execute('''
        SELECT SUM(amount) FROM transactions 
        WHERE user_id = ? AND type = 'expense' AND strftime('%Y', date) = ?
    ''', (user_id, str(year)))
    expenses = cursor.fetchone()[0] or 0.0
    print(f"Yearly expenses for {year}: {expenses}")

    # Returning the report
    return {'income': income, 'expenses': expenses, 'savings': income - expenses}
