import sqlite3

def get_db_connection(db_path='finance_manager.db'):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

def create_tables():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Create users table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL
    )
    ''')

    # Create categories table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS categories (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE
    )
    ''')

    # Create transactions table with category_id
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        amount REAL NOT NULL,
        category_id INTEGER,
        type TEXT NOT NULL,  -- "income" or "expense"
        date TEXT NOT NULL,
        description TEXT,
        FOREIGN KEY (user_id) REFERENCES users(id),
        FOREIGN KEY (category_id) REFERENCES categories(id)
    )
    ''')

    #create budgets table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS budgets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        category_id INTEGER NOT NULL,
        month TEXT NOT NULL,
        year TEXT NOT NULL,
        budget_amount REAL NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users(id),
        FOREIGN KEY (category_id) REFERENCES categories(id),
        UNIQUE(user_id, category_id, month, year)
    )
    ''')

    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_tables()
