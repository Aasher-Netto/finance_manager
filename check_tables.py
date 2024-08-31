import sqlite3

def check_tables():
    conn = sqlite3.connect('finance_manager.db')
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()

    if tables:
        print("Tables in the database:")
        for table in tables:
            print(table[0])
    else:
        print("No tables found in the database.")

    conn.close()

if __name__ == "__main__":
    check_tables()